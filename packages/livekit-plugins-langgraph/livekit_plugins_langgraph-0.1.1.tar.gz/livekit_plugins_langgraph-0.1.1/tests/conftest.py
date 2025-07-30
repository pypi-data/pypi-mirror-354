"""Pytest configuration and fixtures for LiveKit LangGraph plugin tests."""

import pytest
import sys
from pathlib import Path

# Add the project root to the Python path for testing
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture
def sample_ai_message_chunk():
    """Fixture providing a sample AI message chunk."""
    return {
        "type": "AIMessageChunk",
        "content": "Hello, how can I help you?",
        "tool_calls": [],
        "tool_call_chunks": [],
        "invalid_tool_calls": [],
        "additional_kwargs": {}
    }


@pytest.fixture
def sample_tool_chunk():
    """Fixture providing a sample tool call chunk."""
    return {
        "type": "AIMessageChunk",
        "content": "",
        "tool_calls": [{"name": "search", "args": {"query": "test"}, "id": "123"}],
        "tool_call_chunks": [],
        "invalid_tool_calls": [],
        "additional_kwargs": {}
    }


@pytest.fixture
def sample_run_id():
    """Fixture providing sample run_id metadata."""
    return {
        "langgraph_node": "test_node",
        "run_id": "test_run_123",
        "thread_id": "test_thread_456"
    }