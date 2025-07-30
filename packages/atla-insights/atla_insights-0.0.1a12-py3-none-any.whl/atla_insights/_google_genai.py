"""Google GenAI instrumentation."""

import json
from typing import Any, Iterable, Iterator, Mapping, Tuple

from openai.types.chat import ChatCompletionToolParam
from openai.types.shared_params.function_definition import FunctionDefinition
from openinference.semconv.trace import (
    MessageAttributes,
    SpanAttributes,
    ToolAttributes,
    ToolCallAttributes,
)
from opentelemetry.util.types import AttributeValue

try:
    from openinference.instrumentation.google_genai import GoogleGenAIInstrumentor
    from openinference.instrumentation.google_genai._request_attributes_extractor import (
        _RequestAttributesExtractor,
    )
    from openinference.instrumentation.google_genai._response_attributes_extractor import (  # noqa: E501
        _ResponseAttributesExtractor,
    )
except ImportError as e:
    raise ImportError(
        "Google GenAI instrumentation needs to be installed. "
        "Please install it via `pip install atla-insights[google-genai]`."
    ) from e


def _get_tool_calls_from_content_parts(
    content_parts: Iterable[object],
) -> Iterator[Tuple[str, AttributeValue]]:
    """Custom response extractor method for structured tool call information.

    TODO(mathias): Add support for built-in, Google-native tools (e.g. search).

    :param content_parts (Iterable[object]): Content parts to extract from.
    """
    function_call_idx = 0
    for part in content_parts:
        if function_call := getattr(part, "function_call", None):
            function_call_prefix = (
                f"{MessageAttributes.MESSAGE_TOOL_CALLS}.{function_call_idx}"
            )
            if function_name := getattr(function_call, "name", None):
                yield (
                    ".".join(
                        [function_call_prefix, ToolCallAttributes.TOOL_CALL_FUNCTION_NAME]
                    ),
                    function_name,
                )
            if function_id := getattr(function_call, "id", None):
                yield (
                    ".".join([function_call_prefix, ToolCallAttributes.TOOL_CALL_ID]),
                    function_id,
                )
            if function_args := getattr(function_call, "args", None):
                function_args_json = json.dumps(function_args)
            else:
                function_args_json = ""
            yield (
                ".".join(
                    [
                        function_call_prefix,
                        ToolCallAttributes.TOOL_CALL_FUNCTION_ARGUMENTS_JSON,
                    ]
                ),
                function_args_json,
            )

            function_call_idx += 1


def get_tools_from_request(  # noqa: C901
    request_parameters: Mapping[str, Any],
) -> Iterator[Tuple[str, AttributeValue]]:
    """Custom request extractor method for structured information about available tools.

    TODO(mathias): Add support for built-in, Google-native tools (e.g. search).

    :param request_parameters (Mapping[str, Any]): Request params to extract tools from.
    """
    if not isinstance(request_parameters, Mapping):
        return

    input_messages_index = 0

    # If there is a system instruction, this will get counted as a system message.
    if config := request_parameters.get("config"):
        if getattr(config, "system_instruction", None):
            input_messages_index += 1

    if input_contents := request_parameters.get("contents"):
        if isinstance(input_contents, list):
            for input_content in input_contents:
                if not (
                    hasattr(input_content, "parts")
                    and isinstance(input_content.parts, list)
                ):
                    input_messages_index += 1
                    continue

                part_idx = 0
                has_function_response = False
                for input_part in input_content.parts:
                    if function_call := getattr(input_part, "function_call", None):
                        yield (
                            f"{SpanAttributes.LLM_INPUT_MESSAGES}.{input_messages_index}.{MessageAttributes.MESSAGE_ROLE}",
                            "model",
                        )
                        function_call_prefix = f"{SpanAttributes.LLM_INPUT_MESSAGES}.{input_messages_index}.{MessageAttributes.MESSAGE_TOOL_CALLS}.{part_idx}"  # noqa: E501
                        if function_name := getattr(function_call, "name", None):
                            yield (
                                ".".join(
                                    [
                                        function_call_prefix,
                                        ToolCallAttributes.TOOL_CALL_FUNCTION_NAME,
                                    ]
                                ),
                                function_name,
                            )
                        if function_id := getattr(function_call, "id", None):
                            yield (
                                ".".join(
                                    [
                                        function_call_prefix,
                                        ToolCallAttributes.TOOL_CALL_ID,
                                    ]
                                ),
                                function_id,
                            )
                        if function_args := getattr(function_call, "args", None):
                            function_args_json = json.dumps(function_args)
                        else:
                            function_args_json = ""
                        yield (
                            ".".join(
                                [
                                    function_call_prefix,
                                    ToolCallAttributes.TOOL_CALL_FUNCTION_ARGUMENTS_JSON,
                                ]
                            ),
                            function_args_json,
                        )
                        part_idx += 1

                    if function_response := getattr(
                        input_part, "function_response", None
                    ):
                        if hasattr(function_response, "response") and isinstance(
                            function_response.response, Mapping
                        ):
                            yield (
                                f"{SpanAttributes.LLM_INPUT_MESSAGES}.{input_messages_index}.{MessageAttributes.MESSAGE_ROLE}",
                                "tool",
                            )
                            yield (
                                ".".join(
                                    [
                                        SpanAttributes.LLM_INPUT_MESSAGES,
                                        str(input_messages_index),
                                        MessageAttributes.MESSAGE_CONTENT,
                                    ]
                                ),
                                function_response.response.get(
                                    "result", function_response.response
                                ),
                            )

                            # function response parts should be counted as
                            # separate input messages instead
                            input_messages_index += 1
                            has_function_response = True

                if not has_function_response:
                    input_messages_index += 1

    if config := request_parameters.get("config"):
        if tools := getattr(config, "tools", None):
            if not isinstance(tools, Iterable):
                return

            tool_idx = 0
            for tool in tools:
                if not getattr(tool, "function_declarations", None):
                    continue

                function_declarations = tool.function_declarations

                if not isinstance(function_declarations, Iterable):
                    continue

                for function_declaration in function_declarations:
                    tool_attr_name = ".".join(
                        [
                            SpanAttributes.LLM_TOOLS,
                            str(tool_idx),
                            ToolAttributes.TOOL_JSON_SCHEMA,
                        ]
                    )
                    name = getattr(function_declaration, "name", "")
                    description = getattr(function_declaration, "description", "")

                    if (
                        hasattr(function_declaration, "parameters")
                        and hasattr(function_declaration.parameters, "json_schema")
                        and hasattr(
                            function_declaration.parameters.json_schema, "model_dump"
                        )
                        and callable(
                            function_declaration.parameters.json_schema.model_dump
                        )
                    ):
                        parameters = (
                            function_declaration.parameters.json_schema.model_dump(
                                mode="json", exclude_none=True
                            )
                        )
                    else:
                        parameters = {}

                    tool_schema = ChatCompletionToolParam(
                        type="function",
                        function=FunctionDefinition(
                            name=name,
                            description=description,
                            parameters=parameters,
                            strict=None,
                        ),
                    )
                    tool_schema_json = json.dumps(tool_schema)

                    yield tool_attr_name, tool_schema_json

                    tool_idx += 1


class AtlaGoogleGenAIInstrumentor(GoogleGenAIInstrumentor):
    """Atla Google GenAI instrumentor class."""

    def _instrument(self, **kwargs) -> None:
        original_get_extra_attributes_from_request = (
            _RequestAttributesExtractor.get_extra_attributes_from_request
        )

        def get_extra_attributes_from_request(
            self: _RequestAttributesExtractor, request_parameters: Mapping[str, Any]
        ) -> Iterator[Tuple[str, AttributeValue]]:
            yield from original_get_extra_attributes_from_request(
                self, request_parameters
            )
            yield from get_tools_from_request(request_parameters)

        _RequestAttributesExtractor.get_extra_attributes_from_request = (  # type: ignore[method-assign]
            get_extra_attributes_from_request
        )

        original_get_attributes_from_content_parts = (
            _ResponseAttributesExtractor._get_attributes_from_content_parts
        )

        def _get_attributes_from_content_parts(
            self: _ResponseAttributesExtractor,
            content_parts: Iterable[object],
        ) -> Iterator[Tuple[str, AttributeValue]]:
            yield from original_get_attributes_from_content_parts(self, content_parts)
            yield from _get_tool_calls_from_content_parts(content_parts)

        _ResponseAttributesExtractor._get_attributes_from_content_parts = (  # type: ignore[method-assign]
            _get_attributes_from_content_parts
        )

        super()._instrument(**kwargs)
