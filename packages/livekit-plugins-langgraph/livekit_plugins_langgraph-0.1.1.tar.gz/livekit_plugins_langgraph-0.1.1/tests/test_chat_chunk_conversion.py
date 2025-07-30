"""Tests for _to_chat_chunk function."""

import pytest
from unittest.mock import Mock
from livekit.plugins.langgraph.langgraph import _to_chat_chunk
from livekit.agents import llm
from langchain_core.messages import AIMessageChunk, HumanMessageChunk, SystemMessageChunk


class TestToChatChunk:
    """Test the _to_chat_chunk function."""
    
    def test_string_input(self):
        """Test conversion of string input."""
        result = _to_chat_chunk("Hello world")
        
        assert isinstance(result, llm.ChatChunk)
        assert result.choices[0].delta.content == "Hello world"
        assert result.choices[0].delta.role == "assistant"
    
    def test_ai_message_chunk(self):
        """Test conversion of AIMessageChunk."""
        msg = AIMessageChunk(content="AI response")
        result = _to_chat_chunk(msg)
        
        assert isinstance(result, llm.ChatChunk)
        assert result.choices[0].delta.content == "AI response"
        assert result.choices[0].delta.role == "assistant"
    
    def test_human_message_chunk(self):
        """Test conversion of HumanMessageChunk."""
        msg = HumanMessageChunk(content="Human message")
        result = _to_chat_chunk(msg)
        
        assert isinstance(result, llm.ChatChunk)
        assert result.choices[0].delta.content == "Human message"
        assert result.choices[0].delta.role == "user"
    
    def test_system_message_chunk(self):
        """Test conversion of SystemMessageChunk."""
        msg = SystemMessageChunk(content="System message")
        result = _to_chat_chunk(msg)
        
        assert isinstance(result, llm.ChatChunk)
        assert result.choices[0].delta.content == "System message"
        assert result.choices[0].delta.role == "system"
    
    def test_dict_with_normal_content(self):
        """Test conversion of dict with normal content."""
        chunk = {
            "type": "AIMessageChunk",
            "content": "Normal response",
            "tool_calls": []
        }
        result = _to_chat_chunk(chunk)
        
        assert isinstance(result, llm.ChatChunk)
        assert result.choices[0].delta.content == "Normal response"
    
    def test_dict_with_tool_calls_filtered(self):
        """Test that dict with tool calls is filtered out."""
        chunk = {
            "type": "AIMessageChunk",
            "content": "Response with tools",
            "tool_calls": [{"name": "search", "args": {}}]
        }
        result = _to_chat_chunk(chunk)
        
        assert result is None
    
    def test_dict_with_node_filtering_allowed(self):
        """Test dict with node filtering - allowed node."""
        chunk = {
            "type": "AIMessageChunk",
            "content": "Node response"
        }
        run_id = {"langgraph_node": "allowed_node"}
        
        result = _to_chat_chunk(chunk, langgraph_node="allowed_node", run_id=run_id)
        
        assert isinstance(result, llm.ChatChunk)
        assert result.choices[0].delta.content == "Node response"
    
    def test_dict_with_node_filtering_blocked(self):
        """Test dict with node filtering - blocked node."""
        chunk = {
            "type": "AIMessageChunk",
            "content": "Node response"
        }
        run_id = {"langgraph_node": "other_node"}
        
        result = _to_chat_chunk(chunk, langgraph_node="allowed_node", run_id=run_id)
        
        assert result is None
    
    def test_empty_content(self):
        """Test handling of empty content."""
        result = _to_chat_chunk("")
        
        assert isinstance(result, llm.ChatChunk)
        assert result.choices[0].delta.content == ""
    
    def test_none_input(self):
        """Test handling of None input."""
        result = _to_chat_chunk(None)
        
        assert isinstance(result, llm.ChatChunk)
        assert result.choices[0].delta.content == ""
    
    def test_unsupported_dict_type(self):
        """Test handling of unsupported dict types."""
        chunk = {
            "type": "UnsupportedType",
            "content": "Some content"
        }
        result = _to_chat_chunk(chunk)
        
        # Should return None for unsupported types
        assert result is None
    
    def test_dict_without_type(self):
        """Test handling of dict without type field."""
        chunk = {
            "content": "Content without type"
        }
        result = _to_chat_chunk(chunk)
        
        # Should return None for dicts without proper type
        assert result is None
    
    def test_multiple_node_filtering(self):
        """Test node filtering with multiple allowed nodes."""
        chunk = {
            "type": "AIMessageChunk",
            "content": "Multi-node response"
        }
        run_id = {"langgraph_node": "node_b"}
        
        result = _to_chat_chunk(chunk, langgraph_node=["node_a", "node_b"], run_id=run_id)
        
        assert isinstance(result, llm.ChatChunk)
        assert result.choices[0].delta.content == "Multi-node response"
    
    def test_node_filtering_with_no_run_id(self):
        """Test node filtering when run_id is None."""
        chunk = {
            "type": "AIMessageChunk",
            "content": "Response without run_id",
            "langgraph_node": "test_node"
        }
        
        result = _to_chat_chunk(chunk, langgraph_node="test_node", run_id=None)
        
        assert isinstance(result, llm.ChatChunk)
        assert result.choices[0].delta.content == "Response without run_id"