"""Graph Stream Utils."""

from typing import Any, AsyncGenerator, AsyncIterator, Iterator, Literal, TypeVar

from langchain_core.messages import (
    AIMessage,
    AIMessageChunk,
    ToolMessage,
    ToolMessageChunk,
)
from langchain_core.runnables import RunnableConfig
from langchain_core.runnables.schema import EventData, StreamEvent

T = TypeVar("T")


def print_invoke(response: dict[str, Any] | T, stream_mode: str = "updates") -> None:
    """Print the invoke response."""
    if stream_mode == "updates":
        for nodes in response:
            for node, value in nodes.items():
                print("=" * 30 + f"{node}" + "=" * 30)
                print(f"{value}")
    else:
        for key, value in response.items():
            print(f"{key} : {value}")


def print_stream(
    response: Iterator[dict[str, Any] | T], stream_mode: str = "updates"
) -> None:
    """Print the stream response."""
    if stream_mode == "updates":
        for chunk in response:
            for node, value in chunk.items():
                print("=" * 30 + f"{node}" + "=" * 30)
                print(f"{value}")
    elif stream_mode == "values":
        for chunk in response:
            for key, value in chunk.items():
                print("=" * 30 + "=" * 30)
                print(f"{key} : {value}")
    elif stream_mode == "messages":
        for chunk_msg, metadata in response:
            if not isinstance(
                chunk_msg, AIMessageChunk | ToolMessageChunk | ToolMessage
            ):
                print(f"chunk_msg type ::: {type(chunk_msg)}")

            if isinstance(chunk_msg, AIMessageChunk):
                print(chunk_msg.content, end="", flush=True)
            elif isinstance(chunk_msg, ToolMessageChunk):
                # tool message chunk
                print(chunk_msg.content, end="", flush=True)
            elif isinstance(chunk_msg, ToolMessage):
                print("=========================ToolMessage=========================")
                print(f"Tool Type ::: {chunk_msg.type}")
                print(f"Tool Name ::: {chunk_msg.name}")

                if isinstance(chunk_msg.content, str):
                    # print(chunk_msg.content, end="\n", flush=True)
                    print(">>> ToolMessage generated")
                    # chunk_msg.
                elif isinstance(chunk_msg.content, list[str]):
                    for content in chunk_msg.content:
                        # print(content, end="\n", flush=True)
                        print(">>> ToolMessages generated")
    else:
        ...


async def print_astream(
    response: AsyncIterator[dict[str, Any] | T], stream_mode: str = "updates"
) -> None:
    """Print the async stream response."""
    if stream_mode == "updates":
        async for chunk in response:
            for node, value in chunk.items():
                print("=" * 30 + f"{node}" + "=" * 30)
                print(f"{node} : {value}")
    elif stream_mode == "values":
        async for chunk in response:
            for key, value in chunk.items():
                print(f"{key} : {value}")
    elif stream_mode == "messages":
        async for chunk_msg, metadata in response:
            if not isinstance(
                chunk_msg, AIMessageChunk | ToolMessageChunk | ToolMessage
            ):
                ...

            if isinstance(chunk_msg, AIMessageChunk):
                if chunk_msg.content:
                    if isinstance(chunk_msg.content, str):
                        print(chunk_msg.content, end="", flush=True)
                    elif isinstance(chunk_msg.content, list):
                        for content in chunk_msg.content:
                            if isinstance(content, dict):
                                if content.get("type") == "text":
                                    print(content["text"], end="", flush=True)
                            else:
                                print(content, end="", flush=True)

            elif isinstance(chunk_msg, ToolMessageChunk):
                print(chunk_msg.content, end="", flush=True)
            elif isinstance(chunk_msg, ToolMessage):
                print("=========================ToolMessage=========================")
                print(f"Tool Type ::: {chunk_msg.type}")
                print(f"Tool Name ::: {chunk_msg.name}")
                print(f"Tool status ::: {chunk_msg.status}")

    else:
        ...


async def print_astream_event(
    response: AsyncIterator[StreamEvent], config: RunnableConfig | None
) -> None:
    """Print the async stream event."""
    async for event in response:
        kind: str = event.get("event")
        data: EventData = event.get("data")
        name: str = event.get("name")
        # metadata: dict[str, Any] = event.get("metadata")
        # tags: list[str] = event.get("tags")

        input = data.get("input")
        output = data.get("output")

        if kind == "on_chat_model_start":
            print("\n========= on_chat_model_start =========")
            print(f"name ::: {name} started")
            messages = input.get("messages")
            if isinstance(messages, list):
                for message in messages:
                    if isinstance(message, list):
                        for i, msg in enumerate(message):
                            print(f"message {i} ::: {type(msg)}")
                    else:
                        print(f"message ::: {type(message)}")

        elif kind == "on_chat_model_stream":
            chunk: AIMessageChunk = data["chunk"]
            if chunk.content:
                print(chunk.content, end="", flush=True)
        elif kind == "on_chat_model_end":
            print("\n========= on_chat_model_end =========")
            print(f"name ::: {name} finished")
            if isinstance(output, AIMessage):
                if output.tool_calls:
                    print(f"Tool will be called ::: {output.tool_calls}")

        elif kind == "on_tool_start":
            print("\n========= tool_start =========")
            print(f"{name} started")

        elif kind == "on_tool_end":
            print("\n========= tool_end =========")
            print(f"{name} finished")
            if isinstance(output, ToolMessage):
                print(f"{name} result ::: {output.content}")


async def sse_astream(
    response: AsyncIterator[StreamEvent], stream_mode: str
) -> AsyncGenerator[str, None]:
    """SSE stream the async stream event."""
    async for chunk_msg, metadata in response:
        # print(f"chunk_msg ::: {type(chunk_msg)}, type ::: {chunk_msg.type}")
        message_type: Literal["ai_message", "tool_calls", "tool_message"] | None = None

        # yield ai_message in tuple (type, key, chunk, index)
        if isinstance(chunk_msg, AIMessageChunk):
            ai_message_chunk: AIMessageChunk = chunk_msg

            if ai_message_chunk.content:
                message_type = "ai_message"
                if isinstance(ai_message_chunk.content, str):
                    yield (message_type, None, ai_message_chunk.content, None)
                elif isinstance(ai_message_chunk.content, list):
                    for content in ai_message_chunk.content:
                        if isinstance(content, dict):
                            if content.get("type") == "text":
                                yield (message_type, None, content["text"], None)
                        else:
                            yield (message_type, None, content, None)

            if ai_message_chunk.tool_call_chunks:
                message_type = "tool_calls"
                for tool_call_chunk in ai_message_chunk.tool_call_chunks:
                    if tool_call_chunk["id"]:
                        yield (
                            message_type,
                            "tool_call_id",
                            tool_call_chunk["id"],
                            tool_call_chunk["index"],
                        )
                    if tool_call_chunk["name"]:
                        yield (
                            message_type,
                            "name",
                            tool_call_chunk["name"],
                            tool_call_chunk["index"],
                        )
                    if tool_call_chunk["args"]:
                        yield (
                            message_type,
                            "args",
                            tool_call_chunk["args"],
                            tool_call_chunk["index"],
                        )

        elif isinstance(chunk_msg, ToolMessageChunk):
            # tool_message_chunk: ToolMessageChunk = chunk_msg
            # yield (tool_message_chunk.type, tool_message_chunk.content)
            ...
        elif isinstance(chunk_msg, ToolMessage):
            message_type = "tool_message"
            tool_message: ToolMessage = chunk_msg
            yield (message_type, "tool_call_id", tool_message.tool_call_id, None)
            yield (message_type, "status", tool_message.status, None)
            yield (message_type, "result", tool_message.content, None)
