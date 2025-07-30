import logging
import re
from typing import Any, Dict, List, Optional, Sequence

from opentelemetry._events import Event
from opentelemetry.attributes import BoundedAttributes
from opentelemetry.sdk._events import EventLoggerProvider
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk.trace import Event as SpanEvent
from opentelemetry.sdk.trace import ReadableSpan

# Framework-specific attribute keys
TRACELOOP_ENTITY_INPUT = "traceloop.entity.input"
TRACELOOP_ENTITY_OUTPUT = "traceloop.entity.output"
TRACELOOP_CREW_TASKS_OUTPUT = "crewai.crew.tasks_output"
TRACELOOP_CREW_RESULT = "crewai.crew.result"
OPENINFERENCE_INPUT_VALUE = "input.value"
OPENINFERENCE_OUTPUT_VALUE = "output.value"
OPENLIT_PROMPT = "gen_ai.prompt"
OPENLIT_COMPLETION = "gen_ai.completion"
OPENLIT_REVISED_PROMPT = "gen_ai.content.revised_prompt"
OPENLIT_AGENT_ACTUAL_OUTPUT = "gen_ai.agent.actual_output"
OPENLIT_AGENT_HUMAN_INPUT = "gen_ai.agent.human_input"

# Roles
ROLE_SYSTEM = "system"
ROLE_USER = "user"
ROLE_ASSISTANT = "assistant"

_logger = logging.getLogger(__name__)


class LLOHandler:
    """
    Utility class for handling Large Language Objects (LLO) in OpenTelemetry spans.

    LLOHandler performs three primary functions:
    1. Identifies Large Language Objects (LLO) content in spans
    2. Extracts and transforms these attributes into OpenTelemetry Gen AI Events
    3. Filters LLO from spans to maintain privacy and reduce span size

    Supported frameworks and their attribute patterns:
    - Standard Gen AI:
      - gen_ai.prompt.{n}.content: Structured prompt content
      - gen_ai.prompt.{n}.role: Role for prompt content (system, user, assistant, etc.)
      - gen_ai.completion.{n}.content: Structured completion content
      - gen_ai.completion.{n}.role: Role for completion content (usually assistant)

    - Traceloop:
      - traceloop.entity.input: Input text for LLM operations
      - traceloop.entity.output: Output text from LLM operations
      - traceloop.entity.name: Name of the entity processing the LLO
      - crewai.crew.tasks_output: Tasks output data from CrewAI (uses gen_ai.system if available)
      - crewai.crew.result: Final result from CrewAI crew (uses gen_ai.system if available)

    - OpenLit:
      - gen_ai.prompt: Direct prompt text (treated as user message)
      - gen_ai.completion: Direct completion text (treated as assistant message)
      - gen_ai.content.revised_prompt: Revised prompt text (treated as system message)
      - gen_ai.agent.actual_output: Output from CrewAI agent (treated as assistant message)

    - OpenInference:
      - input.value: Direct input prompt
      - output.value: Direct output response
      - llm.input_messages.{n}.message.content: Individual structured input messages
      - llm.input_messages.{n}.message.role: Role for input messages
      - llm.output_messages.{n}.message.content: Individual structured output messages
      - llm.output_messages.{n}.message.role: Role for output messages
      - llm.model_name: Model name used for the LLM operation
    """

    def __init__(self, logger_provider: LoggerProvider):
        """
        Initialize an LLOHandler with the specified logger provider.

        This constructor sets up the event logger provider, configures the event logger,
        and initializes the patterns used to identify LLO attributes.

        Args:
            logger_provider: The OpenTelemetry LoggerProvider used for emitting events.
                           Global LoggerProvider instance injected from our AwsOpenTelemetryConfigurator
        """
        self._logger_provider = logger_provider
        self._event_logger_provider = EventLoggerProvider(logger_provider=self._logger_provider)

        # Patterns for attribute filtering - using a set for O(1) lookups
        self._exact_match_patterns = {
            TRACELOOP_ENTITY_INPUT,
            TRACELOOP_ENTITY_OUTPUT,
            TRACELOOP_CREW_TASKS_OUTPUT,
            TRACELOOP_CREW_RESULT,
            OPENLIT_PROMPT,
            OPENLIT_COMPLETION,
            OPENLIT_REVISED_PROMPT,
            OPENLIT_AGENT_ACTUAL_OUTPUT,
            OPENLIT_AGENT_HUMAN_INPUT,
            OPENINFERENCE_INPUT_VALUE,
            OPENINFERENCE_OUTPUT_VALUE,
        }

        # Pre-compile regex patterns for better performance
        self._regex_patterns = [
            re.compile(r"^gen_ai\.prompt\.\d+\.content$"),
            re.compile(r"^gen_ai\.completion\.\d+\.content$"),
            re.compile(r"^llm\.input_messages\.\d+\.message\.content$"),
            re.compile(r"^llm\.output_messages\.\d+\.message\.content$"),
        ]

        # Additional pre-compiled patterns used in extraction methods
        self._prompt_content_pattern = re.compile(r"^gen_ai\.prompt\.(\d+)\.content$")
        self._completion_content_pattern = re.compile(r"^gen_ai\.completion\.(\d+)\.content$")
        self._openinference_input_msg_pattern = re.compile(r"^llm\.input_messages\.(\d+)\.message\.content$")
        self._openinference_output_msg_pattern = re.compile(r"^llm\.output_messages\.(\d+)\.message\.content$")

    def process_spans(self, spans: Sequence[ReadableSpan]) -> List[ReadableSpan]:
        """
        Processes a sequence of spans to extract and filter LLO attributes.

        For each span, this method:
        1. Extracts LLO attributes and emits them as Gen AI Events
        2. Filters out LLO attributes from the span to maintain privacy
        3. Processes any LLO attributes in span events
        4. Preserves non-LLO attributes in the span

        Handles LLO attributes from multiple frameworks:
        - Standard Gen AI (structured prompt/completion pattern)
        - Traceloop (entity input/output pattern)
        - OpenLit (direct prompt/completion pattern)
        - OpenInference (input/output value and structured messages pattern)

        Args:
            spans: A sequence of OpenTelemetry ReadableSpan objects to process

        Returns:
            List[ReadableSpan]: Modified spans with LLO attributes removed
        """
        modified_spans = []

        for span in spans:
            self._emit_llo_attributes(span, span.attributes)
            updated_attributes = self._filter_attributes(span.attributes)

            if isinstance(span.attributes, BoundedAttributes):
                span._attributes = BoundedAttributes(
                    maxlen=span.attributes.maxlen,
                    attributes=updated_attributes,
                    immutable=span.attributes._immutable,
                    max_value_len=span.attributes.max_value_len,
                )
            else:
                span._attributes = updated_attributes

            self.process_span_events(span)

            modified_spans.append(span)

        return modified_spans

    def process_span_events(self, span: ReadableSpan) -> None:
        """
        Process events within a span to extract and filter LLO attributes.

        For each event in the span, this method:
        1. Emits LLO attributes found in event attributes as Gen AI Events
        2. Filters out LLO attributes from event attributes
        3. Creates updated events with filtered attributes
        4. Replaces the original span events with updated events

        This ensures that LLO attributes are properly handled even when they appear
        in span events rather than directly in the span's attributes.

        Args:
            span: The ReadableSpan to process events for

        Returns:
            None: The span is modified in-place
        """
        if not span.events:
            return

        updated_events = []

        for event in span.events:
            if not event.attributes:
                updated_events.append(event)
                continue

            self._emit_llo_attributes(span, event.attributes, event_timestamp=event.timestamp)

            updated_event_attributes = self._filter_attributes(event.attributes)

            if len(updated_event_attributes) != len(event.attributes):
                limit = None
                if isinstance(event.attributes, BoundedAttributes):
                    limit = event.attributes.maxlen

                updated_event = SpanEvent(
                    name=event.name, attributes=updated_event_attributes, timestamp=event.timestamp, limit=limit
                )

                updated_events.append(updated_event)
            else:
                updated_events.append(event)

        span._events = updated_events

    def _emit_llo_attributes(
        self, span: ReadableSpan, attributes: Dict[str, Any], event_timestamp: Optional[int] = None
    ) -> None:
        """
        Extract Gen AI Events from LLO attributes and emit them via the event logger.

        This method:
        1. Collects LLO attributes from multiple frameworks using specialized extractors
        2. Groups messages into input and output categories
        3. Emits a single grouped event containing all messages

        Supported frameworks:
        - Standard Gen AI: Structured prompt/completion with roles
        - Traceloop: Entity input/output and CrewAI outputs
        - OpenLit: Direct prompt/completion/revised prompt and agent outputs
        - OpenInference: Direct values and structured messages

        Args:
            span: The source ReadableSpan containing the attributes
            attributes: Dictionary of attributes to process
            event_timestamp: Optional timestamp to override span timestamps

        Returns:
            None: Events are emitted via the event logger
        """
        # Quick check if we have any LLO attributes before running extractors
        has_llo_attrs = False
        for key in attributes:
            if self._is_llo_attribute(key):
                has_llo_attrs = True
                break

        if not has_llo_attrs:
            return

        # Collect all messages from various frameworks
        all_messages = []
        all_messages.extend(self._extract_gen_ai_prompt_messages(span, attributes, event_timestamp))
        all_messages.extend(self._extract_gen_ai_completion_messages(span, attributes, event_timestamp))
        all_messages.extend(self._extract_traceloop_messages(span, attributes, event_timestamp))
        all_messages.extend(self._extract_openlit_messages(span, attributes, event_timestamp))
        all_messages.extend(self._extract_openinference_messages(span, attributes, event_timestamp))

        if not all_messages:
            return

        # Group messages into input and output
        input_messages = []
        output_messages = []

        for message in all_messages:
            role = message.get("role", "unknown")

            # Determine if this is input or output based on role and source
            if role in [ROLE_SYSTEM, ROLE_USER]:
                input_messages.append(message)
            elif role == ROLE_ASSISTANT:
                output_messages.append(message)
            else:
                # For unknown roles, check the source attribute
                source = message.get("_source", "")
                if "completion" in source or "output" in source:
                    output_messages.append(message)
                else:
                    input_messages.append(message)

        # Remove internal _source field from messages
        for msg in input_messages:
            msg.pop("_source", None)
        for msg in output_messages:
            msg.pop("_source", None)

        # Create the grouped event body
        grouped_body = {}
        if input_messages:
            grouped_body["input"] = {"messages": input_messages}
        if output_messages:
            grouped_body["output"] = {"messages": output_messages}

        # Use span context for the grouped event
        span_ctx = span.context

        # Create and emit the single grouped event
        grouped_event = Event(
            name=span.instrumentation_scope.name,
            timestamp=event_timestamp or span.end_time,
            body=grouped_body,
            trace_id=span_ctx.trace_id,
            span_id=span_ctx.span_id,
            trace_flags=span_ctx.trace_flags,
        )

        # Get event logger for this span's instrumentation scope
        event_logger = self._event_logger_provider.get_event_logger(span.instrumentation_scope.name)
        event_logger.emit(grouped_event)
        _logger.debug(
            f"Emitted grouped Gen AI Event with {len(input_messages)} input messages and {len(output_messages)} output messages"
        )

    def _filter_attributes(self, attributes: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new attributes dictionary with LLO attributes removed.

        This method creates a new dictionary containing only non-LLO attributes,
        preserving the original values while filtering out sensitive LLO content.
        This helps maintain privacy and reduces the size of spans.

        Args:
            attributes: Original dictionary of span or event attributes

        Returns:
            Dict[str, Any]: New dictionary with LLO attributes removed
        """
        # First check if we need to filter anything
        has_llo_attrs = False
        for key in attributes:
            if self._is_llo_attribute(key):
                has_llo_attrs = True
                break

        # If no LLO attributes found, return the original attributes (no need to copy)
        if not has_llo_attrs:
            return attributes

        # Otherwise, create filtered copy
        filtered_attributes = {}
        for key, value in attributes.items():
            if not self._is_llo_attribute(key):
                filtered_attributes[key] = value

        return filtered_attributes

    def _is_llo_attribute(self, key: str) -> bool:
        """
        Determine if an attribute key contains LLO content based on pattern matching.

        Checks attribute keys against two types of patterns:
        1. Exact match patterns (complete string equality):
           - Traceloop: "traceloop.entity.input", "traceloop.entity.output"
           - OpenLit: "gen_ai.prompt", "gen_ai.completion", "gen_ai.content.revised_prompt"
           - OpenInference: "input.value", "output.value"

        2. Regex match patterns (regular expression matching):
           - Standard Gen AI: "gen_ai.prompt.{n}.content", "gen_ai.completion.{n}.content"
           - OpenInference: "llm.input_messages.{n}.message.content",
                           "llm.output_messages.{n}.message.content"

        Args:
            key: The attribute key to check

        Returns:
            bool: True if the key matches any LLO pattern, False otherwise
        """
        # Check exact matches first (O(1) lookup in a set)
        if key in self._exact_match_patterns:
            return True

        # Then check regex patterns
        for pattern in self._regex_patterns:
            if pattern.match(key):
                return True

        return False

    def _extract_gen_ai_prompt_messages(
        self, span: ReadableSpan, attributes: Dict[str, Any], event_timestamp: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Extract message dictionaries from structured prompt attributes.

        Processes attributes matching the pattern `gen_ai.prompt.{n}.content` and their
        associated `gen_ai.prompt.{n}.role` attributes to create appropriate events.

        Event types are determined by the role:
        1. `system` → `gen_ai.system.message` Event
        2. `user` → `gen_ai.user.message` Event
        3. `assistant` → `gen_ai.assistant.message` Event
        4. `function` → `gen_ai.{gen_ai.system}.message` custom Event
        5. `unknown` → `gen_ai.{gen_ai.system}.message` custom Event

        Args:
            span: The source ReadableSpan containing the attributes
            attributes: Dictionary of attributes to process
            event_timestamp: Optional timestamp to override span.start_time

        Returns:
            List[Dict[str, Any]]: Message dictionaries created from prompt attributes
        """
        # Quick check if any prompt content attributes exist
        if not any(self._prompt_content_pattern.match(key) for key in attributes):
            return []

        messages = []

        # Find all prompt content attributes and their roles
        prompt_content_matches = {}
        for key, value in attributes.items():
            match = self._prompt_content_pattern.match(key)
            if match:
                index = match.group(1)
                role_key = f"gen_ai.prompt.{index}.role"
                role = attributes.get(role_key, "unknown")
                prompt_content_matches[index] = (key, value, role)

        # Create message dictionaries for each content+role pair
        for index, (key, value, role) in prompt_content_matches.items():
            message = {"role": role, "content": value, "_source": key}  # Internal field to help with categorization
            messages.append(message)

        return messages

    def _extract_gen_ai_completion_messages(
        self, span: ReadableSpan, attributes: Dict[str, Any], event_timestamp: Optional[int] = None
    ) -> List[Event]:
        """
        Extract Gen AI Events from structured completion attributes.

        Processes attributes matching the pattern `gen_ai.completion.{n}.content` and their
        associated `gen_ai.completion.{n}.role` attributes to create appropriate events.

        Event types are determined by the role:
        1. `assistant` → `gen_ai.assistant.message` Event (most common)
        2. Other roles → `gen_ai.{gen_ai.system}.message` custom Event

        Args:
            span: The source ReadableSpan containing the attributes
            attributes: Dictionary of attributes to process
            event_timestamp: Optional timestamp to override span.end_time

        Returns:
            List[Dict[str, Any]]: Message dictionaries created from completion attributes
        """
        # Quick check if any completion content attributes exist
        if not any(self._completion_content_pattern.match(key) for key in attributes):
            return []

        messages = []

        # Find all completion content attributes and their roles
        completion_content_matches = {}
        for key, value in attributes.items():
            match = self._completion_content_pattern.match(key)
            if match:
                index = match.group(1)
                role_key = f"gen_ai.completion.{index}.role"
                role = attributes.get(role_key, "unknown")
                completion_content_matches[index] = (key, value, role)

        # Create message dictionaries for each content+role pair
        for index, (key, value, role) in completion_content_matches.items():
            message = {"role": role, "content": value, "_source": key}  # Internal field to help with categorization
            messages.append(message)

        return messages

    def _extract_traceloop_messages(
        self, span: ReadableSpan, attributes: Dict[str, Any], event_timestamp: Optional[int] = None
    ) -> List[Event]:
        """
        Extract Gen AI Events from Traceloop attributes.

        Processes Traceloop-specific attributes:
        - `traceloop.entity.input`: Input data (uses span.start_time)
        - `traceloop.entity.output`: Output data (uses span.end_time)
        - `traceloop.entity.name`: Used as the gen_ai.system value when gen_ai.system isn't available
        - `crewai.crew.tasks_output`: Tasks output data from CrewAI (uses span.end_time)
        - `crewai.crew.result`: Final result from CrewAI crew (uses span.end_time)

        Creates generic `gen_ai.{entity_name}.message` events for both input and output,
        and assistant message events for CrewAI outputs.

        For CrewAI-specific attributes (crewai.crew.tasks_output and crewai.crew.result),
        uses span's gen_ai.system attribute if available, otherwise falls back to traceloop.entity.name.

        Args:
            span: The source ReadableSpan containing the attributes
            attributes: Dictionary of attributes to process
            event_timestamp: Optional timestamp to override span timestamps

        Returns:
            List[Dict[str, Any]]: Message dictionaries created from Traceloop attributes
        """
        # Define the Traceloop attributes we're looking for
        traceloop_keys = {
            TRACELOOP_ENTITY_INPUT,
            TRACELOOP_ENTITY_OUTPUT,
            TRACELOOP_CREW_TASKS_OUTPUT,
            TRACELOOP_CREW_RESULT,
        }

        # Quick check if any Traceloop attributes exist
        if not any(key in attributes for key in traceloop_keys):
            return []

        messages = []

        # Standard Traceloop entity attributes
        traceloop_attrs = [
            (TRACELOOP_ENTITY_INPUT, ROLE_USER),  # Treat input as user role
            (TRACELOOP_ENTITY_OUTPUT, ROLE_ASSISTANT),  # Treat output as assistant role
        ]

        for attr_key, role in traceloop_attrs:
            if attr_key in attributes:
                message = {
                    "role": role,
                    "content": attributes[attr_key],
                    "_source": attr_key,  # Internal field to help with categorization
                }
                messages.append(message)

        # CrewAI-specific Traceloop attributes
        crewai_attrs = [
            (TRACELOOP_CREW_TASKS_OUTPUT, ROLE_ASSISTANT),
            (TRACELOOP_CREW_RESULT, ROLE_ASSISTANT),
        ]

        for attr_key, role in crewai_attrs:
            if attr_key in attributes:
                message = {
                    "role": role,
                    "content": attributes[attr_key],
                    "_source": attr_key,  # Internal field to help with categorization
                }
                messages.append(message)

        return messages

    def _extract_openlit_messages(
        self, span: ReadableSpan, attributes: Dict[str, Any], event_timestamp: Optional[int] = None
    ) -> List[Event]:
        """
        Extract Gen AI Events from OpenLit direct attributes.

        OpenLit uses direct key-value pairs for LLO attributes:
        - `gen_ai.prompt`: Direct prompt text (treated as user message)
        - `gen_ai.completion`: Direct completion text (treated as assistant message)
        - `gen_ai.content.revised_prompt`: Revised prompt text (treated as system message)
        - `gen_ai.agent.actual_output`: Output from CrewAI agent (treated as assistant message)

        The event timestamps are set based on attribute type:
        - Prompt and revised prompt: span.start_time
        - Completion and agent output: span.end_time

        Args:
            span: The source ReadableSpan containing the attributes
            attributes: Dictionary of attributes to process
            event_timestamp: Optional timestamp to override span timestamps

        Returns:
            List[Dict[str, Any]]: Message dictionaries created from OpenLit attributes
        """
        # Define the OpenLit attributes we're looking for
        openlit_keys = {
            OPENLIT_PROMPT,
            OPENLIT_COMPLETION,
            OPENLIT_REVISED_PROMPT,
            OPENLIT_AGENT_ACTUAL_OUTPUT,
            OPENLIT_AGENT_HUMAN_INPUT,
        }

        # Quick check if any OpenLit attributes exist
        if not any(key in attributes for key in openlit_keys):
            return []

        messages = []

        openlit_attrs = [
            (OPENLIT_PROMPT, ROLE_USER),  # Assume user role for direct prompts
            (OPENLIT_COMPLETION, ROLE_ASSISTANT),  # Assume assistant role for completions
            (OPENLIT_REVISED_PROMPT, ROLE_SYSTEM),  # Assume system role for revised prompts
            (OPENLIT_AGENT_ACTUAL_OUTPUT, ROLE_ASSISTANT),  # Assume assistant role for agent output
            (OPENLIT_AGENT_HUMAN_INPUT, ROLE_USER),  # Assume user role for agent human input
        ]

        for attr_key, role in openlit_attrs:
            if attr_key in attributes:
                message = {
                    "role": role,
                    "content": attributes[attr_key],
                    "_source": attr_key,  # Internal field to help with categorization
                }
                messages.append(message)

        return messages

    def _extract_openinference_messages(
        self, span: ReadableSpan, attributes: Dict[str, Any], event_timestamp: Optional[int] = None
    ) -> List[Event]:
        """
        Extract Gen AI Events from OpenInference attributes.

        OpenInference uses two patterns for LLO attributes:
        1. Direct values:
           - `input.value`: Direct input prompt (treated as user message)
           - `output.value`: Direct output response (treated as assistant message)

        2. Structured messages:
           - `llm.input_messages.{n}.message.content`: Individual input messages
           - `llm.input_messages.{n}.message.role`: Role for input message
           - `llm.output_messages.{n}.message.content`: Individual output messages
           - `llm.output_messages.{n}.message.role`: Role for output message

        The LLM model name is extracted from the `llm.model_name` attribute
        instead of `gen_ai.system` which other frameworks use.

        Event timestamps are set based on message type:
        - Input messages: span.start_time
        - Output messages: span.end_time

        Args:
            span: The source ReadableSpan containing the attributes
            attributes: Dictionary of attributes to process
            event_timestamp: Optional timestamp to override span timestamps

        Returns:
            List[Dict[str, Any]]: Message dictionaries created from OpenInference attributes
        """
        # Define the OpenInference keys/patterns we're looking for
        openinference_direct_keys = {OPENINFERENCE_INPUT_VALUE, OPENINFERENCE_OUTPUT_VALUE}

        # Quick check if any OpenInference attributes exist
        has_direct_attrs = any(key in attributes for key in openinference_direct_keys)
        has_input_msgs = any(self._openinference_input_msg_pattern.match(key) for key in attributes)
        has_output_msgs = any(self._openinference_output_msg_pattern.match(key) for key in attributes)

        if not (has_direct_attrs or has_input_msgs or has_output_msgs):
            return []

        messages = []

        # Process direct value attributes
        openinference_direct_attrs = [
            (OPENINFERENCE_INPUT_VALUE, ROLE_USER),
            (OPENINFERENCE_OUTPUT_VALUE, ROLE_ASSISTANT),
        ]

        for attr_key, role in openinference_direct_attrs:
            if attr_key in attributes:
                message = {
                    "role": role,
                    "content": attributes[attr_key],
                    "_source": attr_key,  # Internal field to help with categorization
                }
                messages.append(message)

        # Process input messages
        input_messages = {}
        for key, value in attributes.items():
            match = self._openinference_input_msg_pattern.match(key)
            if match:
                index = match.group(1)
                role_key = f"llm.input_messages.{index}.message.role"
                role = attributes.get(role_key, ROLE_USER)  # Default to user if role not specified
                input_messages[index] = (key, value, role)

        # Create message dictionaries for input messages
        for index, (key, value, role) in input_messages.items():
            message = {"role": role, "content": value, "_source": key}  # Internal field to help with categorization
            messages.append(message)

        # Process output messages
        output_messages = {}
        for key, value in attributes.items():
            match = self._openinference_output_msg_pattern.match(key)
            if match:
                index = match.group(1)
                role_key = f"llm.output_messages.{index}.message.role"
                role = attributes.get(role_key, ROLE_ASSISTANT)  # Default to assistant if role not specified
                output_messages[index] = (key, value, role)

        # Create message dictionaries for output messages
        for index, (key, value, role) in output_messages.items():
            message = {"role": role, "content": value, "_source": key}  # Internal field to help with categorization
            messages.append(message)

        return messages
