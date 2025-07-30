# Copyright 2025 LiveKit, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
LiveKit LangGraph Plugin

This plugin provides seamless integration between LiveKit voice agents and LangGraph workflows.
It includes universal filtering capabilities to ensure only user-facing responses are spoken
by voice agents, while filtering out tool calls and intermediate workflow outputs.

Key Features:
- Universal tool call filtering
- Node-based message filtering (optional)
- Real-time streaming preservation
- Support for both RemoteGraph and CompiledStateGraph
"""

from __future__ import annotations

from typing import Any

from langchain_core.messages import (
    AIMessage,
    BaseMessageChunk,
    HumanMessage,
    SystemMessage,
    AIMessageChunk,
)
from langchain_core.runnables import RunnableConfig
from langgraph.pregel.protocol import PregelProtocol

from livekit.agents import llm, utils
from livekit.agents.llm import ToolChoice
from livekit.agents.llm.chat_context import ChatContext, ChatMessage
from livekit.agents.llm.tool_context import FunctionTool, RawFunctionTool
from livekit.agents.types import (
    DEFAULT_API_CONNECT_OPTIONS,
    NOT_GIVEN,
    APIConnectOptions,
    NotGivenOr,
)


class LLMAdapter(llm.LLM):
    """LiveKit LLM adapter for LangGraph with universal filtering.
    
    This adapter provides seamless integration between LiveKit agents and LangGraph
    workflows, with advanced filtering capabilities to ensure only user-facing
    responses are spoken by the voice agent.
    
    Args:
        graph: LangGraph PregelProtocol instance (RemoteGraph or CompiledStateGraph)
        config: Optional RunnableConfig for the graph execution
        langgraph_node: Optional node name(s) to filter by. Can be a string or list of strings.
                       Only messages from these nodes will be spoken.
    
    Example:
        ```python
        # Only allow specific node messages
        adapter = LLMAdapter(graph, config=config, langgraph_node="node_name")
        
        # Allow multiple specific nodes
        adapter = LLMAdapter(graph, config=config, langgraph_node=["node1", "node2"])
        
        # No node filtering (allow all non-tool content)
        adapter = LLMAdapter(graph, config=config)
        ```
    """
    
    def __init__(
        self,
        graph: PregelProtocol,
        *,
        config: RunnableConfig | None = None,
        langgraph_node: str | list[str] | None = None,
    ) -> None:
        super().__init__()
        self._graph = graph
        self._config = config
        self._langgraph_node = langgraph_node

    def chat(
        self,
        *,
        chat_ctx: ChatContext,
        tools: list[FunctionTool | RawFunctionTool] | None = None,
        conn_options: APIConnectOptions = DEFAULT_API_CONNECT_OPTIONS,
        # these are unused, since tool execution takes place in langgraph
        parallel_tool_calls: NotGivenOr[bool] = NOT_GIVEN,
        tool_choice: NotGivenOr[ToolChoice] = NOT_GIVEN,
        extra_kwargs: NotGivenOr[dict[str, Any]] = NOT_GIVEN,
    ) -> "LangGraphStream":
        return LangGraphStream(
            self,
            chat_ctx=chat_ctx,
            tools=tools or [],
            graph=self._graph,
            config=self._config,
            conn_options=conn_options,
            langgraph_node=self._langgraph_node,
        )


class LangGraphStream(llm.LLMStream):
    """LiveKit LangGraph stream with universal filtering.
    
    This stream processes LangGraph message chunks and applies comprehensive filtering
    to ensure only appropriate content is spoken by the voice agent.
    """
    
    def __init__(
        self,
        llm_adapter: LLMAdapter,
        chat_ctx: ChatContext,
        tools: list[FunctionTool | RawFunctionTool],
        graph: PregelProtocol,
        config: RunnableConfig | None = None,
        conn_options: APIConnectOptions = DEFAULT_API_CONNECT_OPTIONS,
        langgraph_node: str | list[str] | None = None,
    ) -> None:
        super().__init__(
            llm=llm_adapter, chat_ctx=chat_ctx, tools=tools, conn_options=conn_options
        )
        self._chat_ctx = chat_ctx
        self._tools = tools
        self._graph = graph
        self._config = config
        self._conn_options = conn_options
        self._langgraph_node = langgraph_node

    def _run(self, *args: Any, **kwargs: Any) -> Any:
        """This stream is primarily designed for async iteration via __aiter__.
        
        Synchronous execution is not the primary use case for this stream.
        """
        raise NotImplementedError("LangGraphStream is designed for async iteration")

    async def __aiter__(self) -> "LangGraphStream":
        """Async iterator that processes LangGraph messages and applies filtering.
        
        Converts chat context to LangGraph format, streams responses, and filters
        chunks to ensure only appropriate content is yielded for speech synthesis.
        """
        messages = []
        for item in self._chat_ctx.items:
            if isinstance(item, ChatMessage):
                content = item.text_content
                if content:
                    if item.role == "assistant":
                        messages.append(AIMessage(content=content))
                    elif item.role == "user":
                        messages.append(HumanMessage(content=content))
                    elif item.role in ["system", "developer"]:
                        messages.append(SystemMessage(content=content))

        state = {"messages": messages}
        async for message_chunk, run_id in self._graph.astream(
            state,
            self._config,
            stream_mode="messages",
        ):
            chat_chunk = _to_chat_chunk(message_chunk, self._langgraph_node, run_id)
            if chat_chunk:
                yield chat_chunk


def _to_chat_chunk(msg: str | Any, langgraph_node: str | list[str] | None = None, run_id: dict | None = None) -> llm.ChatChunk | None:
    """Convert LangGraph message chunk to LiveKit ChatChunk with filtering.
    
    Args:
        msg: Message chunk from LangGraph (string, BaseMessageChunk, or dict)
        langgraph_node: Optional node filter for workflows
        run_id: Optional run metadata containing node information
    
    Returns:
        ChatChunk if the message should be processed, None if filtered out
    """
    message_id = utils.shortuuid("LC_")
    content: str | None = None
    role: str = "assistant"

    if isinstance(msg, str):
        content = msg
    elif isinstance(msg, BaseMessageChunk):
        content = msg.content
        if msg.id:
            message_id = msg.id
        if hasattr(msg, "role") and msg.role:
            role = msg.role
    elif isinstance(msg, dict):
        # Handle dictionary-based message chunks from RemoteGraph
        if msg.get("type") in [
            "AIMessageChunk",
            "HumanMessageChunk",
            "SystemMessageChunk",
            "ChatMessageChunk",
        ]:
            # Universal filtering for workflows
            # Skip tool calls and intermediate workflow outputs
            if not _should_process_chunk(msg, langgraph_node, run_id):
                return None

            raw_content = msg.get("content")
            if isinstance(raw_content, str):
                content = raw_content
            if msg.get("id"):
                message_id = msg.get("id")
            if msg.get("type") == "HumanMessageChunk":
                role = "user"
            elif msg.get("type") == "SystemMessageChunk":
                role = "system"

    if content is None or content.strip() == "":
        return None

    return llm.ChatChunk(
        id=message_id,
        delta=llm.ChoiceDelta(
            content=content,
            role=role,
        ),
    )


def _should_process_chunk(chunk: dict, allowed_langgraph_nodes: str | list[str] | None = None, run_id: dict | None = None) -> bool:
    """
    Universal filtering function to determine if a chunk should be processed for speech synthesis.
    
    This function provides comprehensive filtering to ensure only user-facing conversational
    content is spoken by the voice agent, while blocking all tool-related content and
    intermediate workflow outputs.
    
    Args:
        chunk: The message chunk from LangGraph streaming
        allowed_langgraph_nodes: Optional node name(s) to filter by. Only chunks from these
                               nodes will be processed. Can be a string or list of strings.
        run_id: Optional run metadata containing langgraph_node information
        
    Returns:
        bool: True if the chunk should be processed for speech, False if it should be filtered out
        
    Filtering Rules:
        - Blocks all tool calls and tool-related metadata
        - Blocks chunks from non-allowed nodes (if node filtering is enabled)
        - Allows streaming tokens and final conversational responses
        - Allows empty content chunks (for real-time streaming)
    """
    
    # Node-based filtering (optional)
    if allowed_langgraph_nodes is not None:
        if isinstance(allowed_langgraph_nodes, str):
            allowed_langgraph_nodes = [allowed_langgraph_nodes]
        
        # Extract langgraph_node from run_id metadata (preferred) or chunk
        langgraph_node = None
        if run_id and isinstance(run_id, dict):
            langgraph_node = run_id.get('langgraph_node')
        
        if not langgraph_node:
            langgraph_node = chunk.get('response_metadata', {}).get('langgraph_node') or chunk.get('langgraph_node')
        
        if langgraph_node and langgraph_node not in allowed_langgraph_nodes:
            return False

    # Skip any chunk that contains tool calls
    tool_calls = chunk.get("tool_calls", [])
    if tool_calls:
        return False

    # Skip tool call chunks (partial tool calls being built)
    tool_call_chunks = chunk.get("tool_call_chunks", [])
    if tool_call_chunks:
        return False

    # Skip invalid tool calls
    invalid_tool_calls = chunk.get("invalid_tool_calls", [])
    if invalid_tool_calls:
        return False

    # Check if this is a tool message type
    chunk_type = chunk.get("type", "")
    if "Tool" in chunk_type or "tool" in chunk_type.lower():
        return False

    # Check additional_kwargs for tool-related content
    additional_kwargs = chunk.get("additional_kwargs", {})
    if additional_kwargs:
        # Skip if additional_kwargs contains tool_calls
        if "tool_calls" in additional_kwargs:
            return False
        # Skip if it looks like function calling metadata
        if any(key in additional_kwargs for key in ["function_call", "tool_call_id"]):
            return False

    # Allow all other content (including empty content for streaming)
    return True