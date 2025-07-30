"""Tests for LangGraph filtering functionality."""

import pytest
from livekit.plugins.langgraph.langgraph import _should_process_chunk


class TestUniversalFiltering:
    """Test universal filtering logic for LangGraph chunks."""
    
    def test_allows_normal_content(self):
        """Test that normal conversational content is allowed."""
        chunk = {
            "type": "AIMessageChunk",
            "content": "Hello, how can I help you today?",
            "tool_calls": [],
            "tool_call_chunks": [],
            "invalid_tool_calls": [],
        }
        assert _should_process_chunk(chunk) is True
    
    def test_blocks_tool_calls(self):
        """Test that chunks with tool calls are blocked."""
        chunk = {
            "type": "AIMessageChunk",
            "content": "",
            "tool_calls": [{"name": "search", "args": {}, "id": "123"}],
        }
        assert _should_process_chunk(chunk) is False
    
    def test_blocks_tool_call_chunks(self):
        """Test that tool call chunks are blocked."""
        chunk = {
            "type": "AIMessageChunk",
            "content": "",
            "tool_call_chunks": [{"name": "search", "args": "query"}],
        }
        assert _should_process_chunk(chunk) is False
    
    def test_allows_empty_content(self):
        """Test that empty content chunks are allowed (for streaming)."""
        chunk = {
            "type": "AIMessageChunk",
            "content": "",
            "tool_calls": [],
            "tool_call_chunks": [],
        }
        assert _should_process_chunk(chunk) is True
    
    def test_blocks_tool_messages(self):
        """Test that tool message types are blocked."""
        chunk = {
            "type": "ToolMessage",
            "content": "Tool execution result",
        }
        assert _should_process_chunk(chunk) is False
    
    def test_blocks_additional_kwargs_tool_calls(self):
        """Test that tool calls in additional_kwargs are blocked."""
        chunk = {
            "type": "AIMessageChunk",
            "content": "Processing...",
            "additional_kwargs": {"tool_calls": [{"name": "function"}]}
        }
        assert _should_process_chunk(chunk) is False


class TestNodeFiltering:
    """Test node-based filtering functionality."""
    
    def test_allows_matching_node(self):
        """Test that chunks from allowed nodes are processed."""
        chunk = {"type": "AIMessageChunk", "content": "Hello"}
        run_id = {"langgraph_node": "my_node"}
        
        assert _should_process_chunk(chunk, "my_node", run_id) is True
    
    def test_blocks_non_matching_node(self):
        """Test that chunks from non-allowed nodes are blocked."""
        chunk = {"type": "AIMessageChunk", "content": "Hello"}
        run_id = {"langgraph_node": "other_node"}
        
        assert _should_process_chunk(chunk, "my_node", run_id) is False
    
    def test_allows_multiple_nodes(self):
        """Test filtering with multiple allowed nodes."""
        chunk = {"type": "AIMessageChunk", "content": "Hello"}
        run_id = {"langgraph_node": "node_b"}
        
        allowed_nodes = ["node_a", "node_b"]
        assert _should_process_chunk(chunk, allowed_nodes, run_id) is True
    
    def test_no_node_filtering_when_none(self):
        """Test that no node filtering occurs when langgraph_node is None."""
        chunk = {"type": "AIMessageChunk", "content": "Hello"}
        run_id = {"langgraph_node": "any_node"}
        
        assert _should_process_chunk(chunk, None, run_id) is True


class TestIntegrationFiltering:
    """Test combined filtering scenarios."""
    
    def test_node_filter_with_tool_calls(self):
        """Test that tool calls are blocked even from allowed nodes."""
        chunk = {
            "type": "AIMessageChunk",
            "content": "",
            "tool_calls": [{"name": "search"}],
        }
        run_id = {"langgraph_node": "my_node"}
        
        assert _should_process_chunk(chunk, "my_node", run_id) is False
    
    def test_normal_content_from_allowed_node(self):
        """Test that normal content from allowed nodes is processed."""
        chunk = {
            "type": "AIMessageChunk", 
            "content": "Here is the answer to your question."
        }
        run_id = {"langgraph_node": "my_node"}
        
        assert _should_process_chunk(chunk, "my_node", run_id) is True