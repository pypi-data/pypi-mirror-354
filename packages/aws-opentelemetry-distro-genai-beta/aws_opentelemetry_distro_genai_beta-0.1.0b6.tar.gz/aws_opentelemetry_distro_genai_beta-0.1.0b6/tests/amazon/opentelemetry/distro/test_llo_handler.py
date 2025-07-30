from unittest import TestCase
from unittest.mock import MagicMock, call, patch

from amazon.opentelemetry.distro.llo_handler import LLOHandler
from opentelemetry._events import Event
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk.trace import ReadableSpan, SpanContext
from opentelemetry.trace import SpanKind, TraceFlags, TraceState


class TestLLOHandler(TestCase):
    def setUp(self):
        self.logger_provider_mock = MagicMock(spec=LoggerProvider)
        self.event_logger_mock = MagicMock()
        self.event_logger_provider_mock = MagicMock()
        self.event_logger_provider_mock.get_event_logger.return_value = self.event_logger_mock

        with patch(
            "amazon.opentelemetry.distro.llo_handler.EventLoggerProvider", return_value=self.event_logger_provider_mock
        ):
            self.llo_handler = LLOHandler(self.logger_provider_mock)

    def _create_mock_span(self, attributes=None, kind=SpanKind.INTERNAL):
        """
        Helper method to create a mock span with given attributes
        """
        if attributes is None:
            attributes = {}

        span_context = SpanContext(
            trace_id=0x123456789ABCDEF0123456789ABCDEF0,
            span_id=0x123456789ABCDEF0,
            is_remote=False,
            trace_flags=TraceFlags.SAMPLED,
            trace_state=TraceState.get_default(),
        )

        mock_span = MagicMock(spec=ReadableSpan)
        mock_span.context = span_context
        mock_span.attributes = attributes
        mock_span.kind = kind
        mock_span.start_time = 1234567890

        # Add instrumentation scope
        mock_scope = MagicMock()
        mock_scope.name = "test.instrumentation.scope"
        mock_span.instrumentation_scope = mock_scope

        return mock_span

    def test_init(self):
        """
        Test initialization of LLOHandler
        """
        self.assertEqual(self.llo_handler._logger_provider, self.logger_provider_mock)
        self.assertEqual(self.llo_handler._event_logger_provider, self.event_logger_provider_mock)
        # Event logger is no longer created during init
        self.event_logger_provider_mock.get_event_logger.assert_not_called()

    def test_is_llo_attribute_match(self):
        """
        Test _is_llo_attribute method with matching patterns
        """
        self.assertTrue(self.llo_handler._is_llo_attribute("gen_ai.prompt.0.content"))
        self.assertTrue(self.llo_handler._is_llo_attribute("gen_ai.prompt.123.content"))

    def test_is_llo_attribute_no_match(self):
        """
        Test _is_llo_attribute method with non-matching patterns
        """
        self.assertFalse(self.llo_handler._is_llo_attribute("gen_ai.prompt.content"))
        self.assertFalse(self.llo_handler._is_llo_attribute("gen_ai.prompt.abc.content"))
        self.assertFalse(self.llo_handler._is_llo_attribute("some.other.attribute"))

    def test_is_llo_attribute_traceloop_match(self):
        """
        Test _is_llo_attribute method with Traceloop patterns
        """
        # Test exact matches for Traceloop attributes
        self.assertTrue(self.llo_handler._is_llo_attribute("traceloop.entity.input"))
        self.assertTrue(self.llo_handler._is_llo_attribute("traceloop.entity.output"))

    def test_is_llo_attribute_openlit_match(self):
        """
        Test _is_llo_attribute method with OpenLit patterns
        """
        # Test exact matches for direct OpenLit attributes
        self.assertTrue(self.llo_handler._is_llo_attribute("gen_ai.prompt"))
        self.assertTrue(self.llo_handler._is_llo_attribute("gen_ai.completion"))
        self.assertTrue(self.llo_handler._is_llo_attribute("gen_ai.content.revised_prompt"))

    def test_is_llo_attribute_openinference_match(self):
        """
        Test _is_llo_attribute method with OpenInference patterns
        """
        # Test exact matches
        self.assertTrue(self.llo_handler._is_llo_attribute("input.value"))
        self.assertTrue(self.llo_handler._is_llo_attribute("output.value"))

        # Test regex matches
        self.assertTrue(self.llo_handler._is_llo_attribute("llm.input_messages.0.message.content"))
        self.assertTrue(self.llo_handler._is_llo_attribute("llm.output_messages.123.message.content"))

    def test_is_llo_attribute_crewai_match(self):
        """
        Test _is_llo_attribute method with CrewAI patterns
        """
        # Test exact match for CrewAI attributes (handled by Traceloop and OpenLit)
        self.assertTrue(self.llo_handler._is_llo_attribute("gen_ai.agent.actual_output"))
        self.assertTrue(self.llo_handler._is_llo_attribute("gen_ai.agent.human_input"))
        self.assertTrue(self.llo_handler._is_llo_attribute("crewai.crew.tasks_output"))
        self.assertTrue(self.llo_handler._is_llo_attribute("crewai.crew.result"))

    def test_filter_attributes(self):
        """
        Test _filter_attributes method
        """
        attributes = {
            "gen_ai.prompt.0.content": "test content",
            "gen_ai.prompt.0.role": "user",
            "normal.attribute": "value",
            "another.normal.attribute": 123,
        }

        filtered = self.llo_handler._filter_attributes(attributes)

        self.assertNotIn("gen_ai.prompt.0.content", filtered)
        self.assertIn("gen_ai.prompt.0.role", filtered)
        self.assertIn("normal.attribute", filtered)
        self.assertIn("another.normal.attribute", filtered)

    def test_extract_gen_ai_prompt_messages_system_role(self):
        """
        Test _extract_gen_ai_prompt_messages with system role
        """
        attributes = {
            "gen_ai.prompt.0.content": "system instruction",
            "gen_ai.prompt.0.role": "system",
            "gen_ai.system": "openai",
        }

        span = self._create_mock_span(attributes)

        messages = self.llo_handler._extract_gen_ai_prompt_messages(span, attributes)

        self.assertEqual(len(messages), 1)
        message = messages[0]
        self.assertEqual(message["content"], "system instruction")
        self.assertEqual(message["role"], "system")
        self.assertEqual(message["_source"], "gen_ai.prompt.0.content")

    def test_extract_gen_ai_prompt_messages_user_role(self):
        """
        Test _extract_gen_ai_prompt_messages with user role
        """
        attributes = {
            "gen_ai.prompt.0.content": "user question",
            "gen_ai.prompt.0.role": "user",
            "gen_ai.system": "anthropic",
        }

        span = self._create_mock_span(attributes)

        messages = self.llo_handler._extract_gen_ai_prompt_messages(span, attributes)

        self.assertEqual(len(messages), 1)
        message = messages[0]
        self.assertEqual(message["content"], "user question")
        self.assertEqual(message["role"], "user")
        self.assertEqual(message["_source"], "gen_ai.prompt.0.content")

    def test_extract_gen_ai_prompt_messages_assistant_role(self):
        """
        Test _extract_gen_ai_prompt_messages with assistant role
        """
        attributes = {
            "gen_ai.prompt.1.content": "assistant response",
            "gen_ai.prompt.1.role": "assistant",
            "gen_ai.system": "anthropic",
        }

        span = self._create_mock_span(attributes)

        messages = self.llo_handler._extract_gen_ai_prompt_messages(span, attributes)

        self.assertEqual(len(messages), 1)
        message = messages[0]
        self.assertEqual(message["content"], "assistant response")
        self.assertEqual(message["role"], "assistant")
        self.assertEqual(message["_source"], "gen_ai.prompt.1.content")

    def test_extract_gen_ai_prompt_messages_function_role(self):
        """
        Test _extract_gen_ai_prompt_messages with function role
        """
        attributes = {
            "gen_ai.prompt.2.content": "function data",
            "gen_ai.prompt.2.role": "function",
            "gen_ai.system": "openai",
        }

        span = self._create_mock_span(attributes)
        messages = self.llo_handler._extract_gen_ai_prompt_messages(span, attributes)

        self.assertEqual(len(messages), 1)
        message = messages[0]
        self.assertEqual(message["content"], "function data")
        self.assertEqual(message["role"], "function")
        self.assertEqual(message["_source"], "gen_ai.prompt.2.content")

    def test_extract_gen_ai_prompt_messages_unknown_role(self):
        """
        Test _extract_gen_ai_prompt_messages with unknown role
        """
        attributes = {
            "gen_ai.prompt.3.content": "unknown type content",
            "gen_ai.prompt.3.role": "unknown",
            "gen_ai.system": "bedrock",
        }

        span = self._create_mock_span(attributes)
        messages = self.llo_handler._extract_gen_ai_prompt_messages(span, attributes)

        self.assertEqual(len(messages), 1)
        message = messages[0]
        self.assertEqual(message["content"], "unknown type content")
        self.assertEqual(message["role"], "unknown")
        self.assertEqual(message["_source"], "gen_ai.prompt.3.content")

    def test_extract_gen_ai_completion_messages_assistant_role(self):
        """
        Test _extract_gen_ai_completion_messages with assistant role
        """
        attributes = {
            "gen_ai.completion.0.content": "assistant completion",
            "gen_ai.completion.0.role": "assistant",
            "gen_ai.system": "openai",
        }

        span = self._create_mock_span(attributes)
        span.end_time = 1234567899  # end time for completion events

        messages = self.llo_handler._extract_gen_ai_completion_messages(span, attributes)

        self.assertEqual(len(messages), 1)
        message = messages[0]
        self.assertEqual(message["content"], "assistant completion")
        self.assertEqual(message["role"], "assistant")
        self.assertEqual(message["_source"], "gen_ai.completion.0.content")

    def test_extract_gen_ai_completion_messages_other_role(self):
        """
        Test _extract_gen_ai_completion_messages with non-assistant role
        """
        attributes = {
            "gen_ai.completion.1.content": "other completion",
            "gen_ai.completion.1.role": "other",
            "gen_ai.system": "anthropic",
        }

        span = self._create_mock_span(attributes)
        span.end_time = 1234567899

        messages = self.llo_handler._extract_gen_ai_completion_messages(span, attributes)

        self.assertEqual(len(messages), 1)
        message = messages[0]
        self.assertEqual(message["content"], "other completion")
        self.assertEqual(message["role"], "other")
        self.assertEqual(message["_source"], "gen_ai.completion.1.content")

    def test_extract_traceloop_messages(self):
        """
        Test _extract_traceloop_messages with standard Traceloop attributes
        """
        attributes = {
            "traceloop.entity.input": "input data",
            "traceloop.entity.output": "output data",
            "traceloop.entity.name": "my_entity",
        }

        span = self._create_mock_span(attributes)
        span.end_time = 1234567899

        messages = self.llo_handler._extract_traceloop_messages(span, attributes)

        self.assertEqual(len(messages), 2)

        input_message = messages[0]
        self.assertEqual(input_message["content"], "input data")
        self.assertEqual(input_message["role"], "user")
        self.assertEqual(input_message["_source"], "traceloop.entity.input")

        output_event = events[1]
        self.assertEqual(output_event.name, "gen_ai.my_entity.message")
        self.assertEqual(output_event.body["content"], "output data")
        self.assertEqual(output_event.attributes["gen_ai.system"], "my_entity")
        self.assertEqual(output_event.attributes["original_attribute"], "traceloop.entity.output")
        self.assertEqual(output_event.timestamp, 1234567899)  # end_time

    def test_extract_traceloop_all_attributes(self):
        """
        Test _extract_traceloop_messages with all Traceloop attributes including CrewAI outputs
        """
        attributes = {
            "traceloop.entity.input": "input data",
            "traceloop.entity.output": "output data",
            "crewai.crew.tasks_output": "[TaskOutput(description='Task 1', output='Result 1')]",
            "crewai.crew.result": "Final crew result",
            "traceloop.entity.name": "crewai_agent",
        }

        span = self._create_mock_span(attributes)
        span.end_time = 1234567899

        messages = self.llo_handler._extract_traceloop_messages(span, attributes)

        self.assertEqual(len(messages), 4)

        # Check message contents
        contents_and_roles = [(msg["content"], msg["role"]) for msg in messages]
        self.assertIn(("input data", "user"), contents_and_roles)
        self.assertIn(("output data", "assistant"), contents_and_roles)
        self.assertIn(("[TaskOutput(description='Task 1', output='Result 1')]", "assistant"), contents_and_roles)
        self.assertIn(("Final crew result", "assistant"), contents_and_roles)

        output_message = messages[1]
        self.assertEqual(output_message["content"], "output data")
        self.assertEqual(output_message["role"], "assistant")
        self.assertEqual(output_message["_source"], "traceloop.entity.output")

    def test_extract_openlit_direct_prompt(self):
        """
        Test _extract_openlit_messages with direct prompt attribute
        """
        attributes = {"gen_ai.prompt": "user direct prompt", "gen_ai.system": "openlit"}

        span = self._create_mock_span(attributes)

        messages = self.llo_handler._extract_openlit_messages(span, attributes)

        self.assertEqual(len(messages), 1)
        message = messages[0]
        self.assertEqual(message["content"], "user direct prompt")
        self.assertEqual(message["role"], "user")
        self.assertEqual(message["_source"], "gen_ai.prompt")

    def test_extract_openlit_direct_completion(self):
        """
        Test _extract_openlit_messages with direct completion attribute
        """
        attributes = {"gen_ai.completion": "assistant direct completion", "gen_ai.system": "openlit"}

        span = self._create_mock_span(attributes)
        span.end_time = 1234567899

        messages = self.llo_handler._extract_openlit_messages(span, attributes)

        self.assertEqual(len(messages), 1)
        message = messages[0]
        self.assertEqual(message["content"], "assistant direct completion")
        self.assertEqual(message["role"], "assistant")
        self.assertEqual(message["_source"], "gen_ai.completion")

    def test_extract_openlit_all_attributes(self):
        """
        Test _extract_openlit_messages with all OpenLit attributes
        """
        attributes = {
            "gen_ai.prompt": "user prompt",
            "gen_ai.completion": "assistant response",
            "gen_ai.content.revised_prompt": "revised prompt",
            "gen_ai.agent.actual_output": "agent output",
            "gen_ai.agent.human_input": "human input to agent",
            "gen_ai.system": "langchain",
        }

        span = self._create_mock_span(attributes)
        span.end_time = 1234567899

        messages = self.llo_handler._extract_openlit_messages(span, attributes)

        self.assertEqual(len(messages), 5)

        # Check we have the expected roles
        roles = {msg["role"] for msg in messages}
        self.assertIn("user", roles)
        self.assertIn("assistant", roles)
        self.assertIn("system", roles)

        # Verify counts of user messages (should be 2 - prompt and human input)
        user_messages = [m for m in messages if m["role"] == "user"]
        self.assertEqual(len(user_messages), 2)

        # Check original attributes
        sources = {msg["_source"] for msg in messages}
        self.assertIn("gen_ai.prompt", sources)
        self.assertIn("gen_ai.completion", sources)
        self.assertIn("gen_ai.content.revised_prompt", sources)
        self.assertIn("gen_ai.agent.actual_output", sources)
        self.assertIn("gen_ai.agent.human_input", sources)

    def test_extract_openlit_revised_prompt(self):
        """
        Test _extract_openlit_messages with revised prompt attribute
        """
        attributes = {"gen_ai.content.revised_prompt": "revised system prompt", "gen_ai.system": "openlit"}

        span = self._create_mock_span(attributes)

        messages = self.llo_handler._extract_openlit_messages(span, attributes)

        self.assertEqual(len(messages), 1)
        message = messages[0]
        self.assertEqual(message["content"], "revised system prompt")
        self.assertEqual(message["role"], "system")
        self.assertEqual(message["_source"], "gen_ai.content.revised_prompt")

    def test_extract_openinference_direct_attributes(self):
        """
        Test _extract_openinference_messages with direct input/output values
        """
        attributes = {
            "input.value": "user prompt",
            "output.value": "assistant response",
            "llm.model_name": "gpt-4",
        }

        span = self._create_mock_span(attributes)
        span.end_time = 1234567899

        messages = self.llo_handler._extract_openinference_messages(span, attributes)

        self.assertEqual(len(messages), 2)

        input_message = messages[0]
        self.assertEqual(input_message["content"], "user prompt")
        self.assertEqual(input_message["role"], "user")
        self.assertEqual(input_message["_source"], "input.value")

        output_message = messages[1]
        self.assertEqual(output_message["content"], "assistant response")
        self.assertEqual(output_message["role"], "assistant")
        self.assertEqual(output_message["_source"], "output.value")

    def test_extract_openinference_structured_input_messages(self):
        """
        Test _extract_openinference_messages with structured input messages
        """
        attributes = {
            "llm.input_messages.0.message.content": "system prompt",
            "llm.input_messages.0.message.role": "system",
            "llm.input_messages.1.message.content": "user message",
            "llm.input_messages.1.message.role": "user",
            "llm.model_name": "claude-3",
        }

        span = self._create_mock_span(attributes)

        messages = self.llo_handler._extract_openinference_messages(span, attributes)

        self.assertEqual(len(messages), 2)

        # Messages should be in index order
        system_message = messages[0]
        self.assertEqual(system_message["content"], "system prompt")
        self.assertEqual(system_message["role"], "system")
        self.assertEqual(system_message["_source"], "llm.input_messages.0.message.content")

        user_message = messages[1]
        self.assertEqual(user_event.name, "gen_ai.user.message")
        self.assertEqual(user_event.body["content"], "user message")
        self.assertEqual(user_event.body["role"], "user")
        self.assertEqual(user_event.attributes["gen_ai.system"], "claude-3")
        self.assertEqual(user_event.attributes["original_attribute"], "llm.input_messages.1.message.content")

    def test_extract_openinference_structured_output_messages(self):
        """
        Test _extract_openinference_messages with structured output messages
        """
        attributes = {
            "llm.output_messages.0.message.content": "assistant response",
            "llm.output_messages.0.message.role": "assistant",
            "llm.model_name": "llama-3",
        }

        span = self._create_mock_span(attributes)
        span.end_time = 1234567899

        messages = self.llo_handler._extract_openinference_messages(span, attributes)

        self.assertEqual(len(messages), 1)

        output_message = messages[0]
        self.assertEqual(output_message["content"], "assistant response")
        self.assertEqual(output_message["role"], "assistant")
        self.assertEqual(output_message["_source"], "llm.output_messages.0.message.content")

    def test_extract_openinference_mixed_attributes(self):
        """
        Test _extract_openinference_messages with a mix of all attribute types
        """
        attributes = {
            "input.value": "direct input",
            "output.value": "direct output",
            "llm.input_messages.0.message.content": "message input",
            "llm.input_messages.0.message.role": "user",
            "llm.output_messages.0.message.content": "message output",
            "llm.output_messages.0.message.role": "assistant",
            "llm.model_name": "bedrock.claude-3",
        }

        span = self._create_mock_span(attributes)
        span.end_time = 1234567899

        messages = self.llo_handler._extract_openinference_messages(span, attributes)

        self.assertEqual(len(messages), 4)

        # Check roles
        roles = {msg["role"] for msg in messages}
        self.assertIn("user", roles)
        self.assertIn("assistant", roles)

        # Verify original attributes were correctly captured
        sources = {msg["_source"] for msg in messages}
        self.assertIn("input.value", sources)
        self.assertIn("output.value", sources)
        self.assertIn("llm.input_messages.0.message.content", sources)
        self.assertIn("llm.output_messages.0.message.content", sources)

    def test_extract_openlit_agent_actual_output(self):
        """
        Test _extract_openlit_messages with agent actual output attribute
        """
        attributes = {"gen_ai.agent.actual_output": "Agent task output result", "gen_ai.system": "crewai"}

        span = self._create_mock_span(attributes)
        span.end_time = 1234567899

        messages = self.llo_handler._extract_openlit_messages(span, attributes)

        self.assertEqual(len(messages), 1)

        message = messages[0]
        self.assertEqual(message["content"], "Agent task output result")
        self.assertEqual(message["role"], "assistant")
        self.assertEqual(message["_source"], "gen_ai.agent.actual_output")

    def test_extract_openlit_agent_human_input(self):
        """
        Test _extract_openlit_messages with agent human input attribute
        """
        attributes = {"gen_ai.agent.human_input": "Human input to the agent", "gen_ai.system": "crewai"}

        span = self._create_mock_span(attributes)

        messages = self.llo_handler._extract_openlit_messages(span, attributes)

        self.assertEqual(len(messages), 1)
        message = messages[0]
        self.assertEqual(message["content"], "Human input to the agent")
        self.assertEqual(message["role"], "user")
        self.assertEqual(message["_source"], "gen_ai.agent.human_input")

    def test_extract_traceloop_crew_outputs(self):
        """
        Test _extract_traceloop_messages with CrewAI specific attributes
        """
        attributes = {
            "crewai.crew.tasks_output": "[TaskOutput(description='Task description', output='Task result')]",
            "crewai.crew.result": "Final crew execution result",
            "traceloop.entity.name": "crewai",
        }

        span = self._create_mock_span(attributes)
        span.end_time = 1234567899

        messages = self.llo_handler._extract_traceloop_messages(span, attributes)

        self.assertEqual(len(messages), 2)

        # Check message contents
        contents = {msg["content"] for msg in messages}
        self.assertIn("[TaskOutput(description='Task description', output='Task result')]", contents)
        self.assertIn("Final crew execution result", contents)

        # Both should be assistant messages
        for msg in messages:
            self.assertEqual(msg["role"], "assistant")

    def test_extract_traceloop_crew_outputs_with_gen_ai_system(self):
        """
        Test _extract_traceloop_messages with CrewAI specific attributes when gen_ai.system is available
        """
        attributes = {
            "crewai.crew.tasks_output": "[TaskOutput(description='Task description', output='Task result')]",
            "crewai.crew.result": "Final crew execution result",
            "traceloop.entity.name": "oldvalue",
            "gen_ai.system": "crewai-agent",
        }

        span = self._create_mock_span(attributes)
        span.end_time = 1234567899

        messages = self.llo_handler._extract_traceloop_messages(span, attributes)

        self.assertEqual(len(messages), 2)

        # Check that both messages are assistant messages
        for msg in messages:
            self.assertEqual(msg["role"], "assistant")

    def test_extract_traceloop_entity_with_gen_ai_system(self):
        """
        Test that traceloop.entity.input and traceloop.entity.output still use traceloop.entity.name
        even when gen_ai.system is available
        """
        attributes = {
            "traceloop.entity.input": "input data",
            "traceloop.entity.output": "output data",
            "traceloop.entity.name": "my_entity",
            "gen_ai.system": "should-not-be-used",
        }

        span = self._create_mock_span(attributes)
        span.end_time = 1234567899

        messages = self.llo_handler._extract_traceloop_messages(span, attributes)

        self.assertEqual(len(messages), 2)

        # Check roles and content
        input_msg = next(msg for msg in messages if msg["_source"] == "traceloop.entity.input")
        self.assertEqual(input_msg["role"], "user")
        self.assertEqual(input_msg["content"], "input data")

        output_msg = next(msg for msg in messages if msg["_source"] == "traceloop.entity.output")
        self.assertEqual(output_msg["role"], "assistant")
        self.assertEqual(output_msg["content"], "output data")

    def test_emit_llo_attributes(self):
        """
        Test _emit_llo_attributes with new grouped event format
        """
        attributes = {
            "gen_ai.prompt.0.content": "prompt content",
            "gen_ai.prompt.0.role": "user",
            "gen_ai.completion.0.content": "completion content",
            "gen_ai.completion.0.role": "assistant",
            "traceloop.entity.input": "traceloop input",
            "traceloop.entity.name": "entity_name",
            "gen_ai.system": "openai",
            "gen_ai.agent.actual_output": "agent output",
            "crewai.crew.tasks_output": "tasks output",
            "crewai.crew.result": "crew result",
        }

        span = self._create_mock_span(attributes)
        span.end_time = 1234567899

        with patch.object(self.llo_handler, "_extract_gen_ai_prompt_messages") as mock_extract_prompt, patch.object(
            self.llo_handler, "_extract_gen_ai_completion_messages"
        ) as mock_extract_completion, patch.object(
            self.llo_handler, "_extract_traceloop_messages"
        ) as mock_extract_traceloop, patch.object(
            self.llo_handler, "_extract_openlit_messages"
        ) as mock_extract_openlit, patch.object(
            self.llo_handler, "_extract_openinference_messages"
        ) as mock_extract_openinference:

            # Create message dictionaries instead of events
            prompt_message = {"content": "prompt content", "role": "user", "_source": "gen_ai.prompt.0.content"}
            completion_message = {
                "content": "completion content",
                "role": "assistant",
                "_source": "gen_ai.completion.0.content",
            }
            traceloop_message = {"content": "traceloop input", "role": "user", "_source": "traceloop.entity.input"}
            openlit_message = {"content": "agent output", "role": "assistant", "_source": "gen_ai.agent.actual_output"}
            crewai_message1 = {"content": "tasks output", "role": "assistant", "_source": "crewai.crew.tasks_output"}
            crewai_message2 = {"content": "crew result", "role": "assistant", "_source": "crewai.crew.result"}

            mock_extract_prompt.return_value = [prompt_message]
            mock_extract_completion.return_value = [completion_message]
            mock_extract_traceloop.return_value = [traceloop_message, crewai_message1, crewai_message2]
            mock_extract_openlit.return_value = [openlit_message]
            mock_extract_openinference.return_value = []

            self.llo_handler._emit_llo_attributes(span, attributes)

            mock_extract_prompt.assert_called_once_with(span, attributes, None)
            mock_extract_completion.assert_called_once_with(span, attributes, None)
            mock_extract_traceloop.assert_called_once_with(span, attributes, None)
            mock_extract_openlit.assert_called_once_with(span, attributes, None)
            mock_extract_openinference.assert_called_once_with(span, attributes, None)

            # Should get event logger for the span's instrumentation scope
            self.event_logger_provider_mock.get_event_logger.assert_called_once_with("test.instrumentation.scope")

            # Should emit only one grouped event
            self.event_logger_mock.emit.assert_called_once()

            # Verify the grouped event structure
            emitted_event = self.event_logger_mock.emit.call_args[0][0]
            self.assertEqual(emitted_event.name, "test.instrumentation.scope")
            self.assertEqual(emitted_event.timestamp, 1234567899)

            # Check the grouped body structure
            # The order of messages depends on the order of extraction methods called
            actual_body = emitted_event.body

            # Verify input messages
            self.assertIn("input", actual_body)
            self.assertIn("messages", actual_body["input"])
            input_messages = actual_body["input"]["messages"]
            self.assertEqual(len(input_messages), 2)

            # Check input message contents (order-independent)
            input_contents = {msg["content"] for msg in input_messages}
            self.assertEqual(input_contents, {"prompt content", "traceloop input"})

            # Verify output messages
            self.assertIn("output", actual_body)
            self.assertIn("messages", actual_body["output"])
            output_messages = actual_body["output"]["messages"]
            self.assertEqual(len(output_messages), 4)

            # Check output message contents (order-independent)
            output_contents = {msg["content"] for msg in output_messages}
            self.assertEqual(output_contents, {"completion content", "agent output", "tasks output", "crew result"})

    def test_emit_llo_attributes_with_system_messages(self):
        """
        Test _emit_llo_attributes with system messages included in input
        """
        attributes = {
            "gen_ai.prompt.0.content": "You are a helpful assistant...",
            "gen_ai.prompt.0.role": "system",
            "gen_ai.prompt.1.content": "Hi there, can you book me a flight to New York next week",
            "gen_ai.prompt.1.role": "user",
            "gen_ai.completion.0.content": "Sure, I can help you search for flights to New York for next week...",
            "gen_ai.completion.0.role": "assistant",
            "gen_ai.system": "openai",
        }

        span = self._create_mock_span(attributes)
        span.end_time = 1234567899

        self.llo_handler._emit_llo_attributes(span, attributes)

        # Should get event logger for the span's instrumentation scope
        self.event_logger_provider_mock.get_event_logger.assert_called_once_with("test.instrumentation.scope")

        # Should emit only one grouped event
        self.event_logger_mock.emit.assert_called_once()

        # Verify the grouped event structure
        emitted_event = self.event_logger_mock.emit.call_args[0][0]
        self.assertEqual(emitted_event.name, "test.instrumentation.scope")

        actual_body = emitted_event.body

        # Verify input messages (system + user)
        self.assertIn("input", actual_body)
        input_messages = actual_body["input"]["messages"]
        self.assertEqual(len(input_messages), 2)

        # Check that system message comes first, then user
        self.assertEqual(input_messages[0]["role"], "system")
        self.assertEqual(input_messages[0]["content"], "You are a helpful assistant...")
        self.assertEqual(input_messages[1]["role"], "user")
        self.assertEqual(input_messages[1]["content"], "Hi there, can you book me a flight to New York next week")

        # Verify output messages
        self.assertIn("output", actual_body)
        output_messages = actual_body["output"]["messages"]
        self.assertEqual(len(output_messages), 1)
        self.assertEqual(output_messages[0]["role"], "assistant")
        self.assertEqual(
            output_messages[0]["content"], "Sure, I can help you search for flights to New York for next week..."
        )

    def test_process_spans(self):
        """
        Test process_spans
        """
        attributes = {"gen_ai.prompt.0.content": "prompt content", "normal.attribute": "normal value"}

        span = self._create_mock_span(attributes)

        with patch.object(self.llo_handler, "_emit_llo_attributes") as mock_emit, patch.object(
            self.llo_handler, "_filter_attributes"
        ) as mock_filter:

            filtered_attributes = {"normal.attribute": "normal value"}
            mock_filter.return_value = filtered_attributes

            result = self.llo_handler.process_spans([span])

            mock_emit.assert_called_once_with(span, attributes)
            mock_filter.assert_called_once_with(attributes)

            self.assertEqual(len(result), 1)
            self.assertEqual(result[0], span)
            # Access the _attributes property that was set by the process_spans method
            self.assertEqual(result[0]._attributes, filtered_attributes)

    def test_process_spans_with_bounded_attributes(self):
        """
        Test process_spans with BoundedAttributes
        """
        from opentelemetry.attributes import BoundedAttributes

        bounded_attrs = BoundedAttributes(
            maxlen=10,
            attributes={"gen_ai.prompt.0.content": "prompt content", "normal.attribute": "normal value"},
            immutable=False,
            max_value_len=1000,
        )

        span = self._create_mock_span(bounded_attrs)

        with patch.object(self.llo_handler, "_emit_llo_attributes") as mock_emit, patch.object(
            self.llo_handler, "_filter_attributes"
        ) as mock_filter:

            filtered_attributes = {"normal.attribute": "normal value"}
            mock_filter.return_value = filtered_attributes

            result = self.llo_handler.process_spans([span])

            mock_emit.assert_called_once_with(span, bounded_attrs)
            mock_filter.assert_called_once_with(bounded_attrs)

            self.assertEqual(len(result), 1)
            self.assertEqual(result[0], span)
            # Check that we got a BoundedAttributes instance
            self.assertIsInstance(result[0]._attributes, BoundedAttributes)
            # Check the underlying dictionary content
            self.assertEqual(dict(result[0]._attributes), filtered_attributes)
