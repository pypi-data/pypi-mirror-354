"""Tests for LLMAdapter and LangGraphStream classes."""

import pytest
from unittest.mock import Mock, AsyncMock
from livekit.plugins.langgraph import LLMAdapter, LangGraphStream
from livekit.agents import llm


class TestLLMAdapter:
    """Test the LLMAdapter class."""
    
    def test_init_with_graph_only(self):
        """Test initialization with just a graph."""
        mock_graph = Mock()
        adapter = LLMAdapter(mock_graph)
        
        assert adapter._graph == mock_graph
        assert adapter._config is None
        assert adapter._langgraph_node is None
    
    def test_init_with_config(self):
        """Test initialization with graph and config."""
        mock_graph = Mock()
        config = {"configurable": {"thread_id": "test"}}
        adapter = LLMAdapter(mock_graph, config=config)
        
        assert adapter._graph == mock_graph
        assert adapter._config == config
        assert adapter._langgraph_node is None
    
    def test_init_with_single_node(self):
        """Test initialization with single node filtering."""
        mock_graph = Mock()
        adapter = LLMAdapter(mock_graph, langgraph_node="test_node")
        
        assert adapter._graph == mock_graph
        assert adapter._langgraph_node == "test_node"
    
    def test_init_with_multiple_nodes(self):
        """Test initialization with multiple node filtering."""
        mock_graph = Mock()
        nodes = ["node1", "node2"]
        adapter = LLMAdapter(mock_graph, langgraph_node=nodes)
        
        assert adapter._graph == mock_graph
        assert adapter._langgraph_node == nodes
    
    def test_chat_returns_langgraph_stream(self):
        """Test that chat method returns LangGraphStream."""
        mock_graph = Mock()
        adapter = LLMAdapter(mock_graph)
        
        mock_chat_ctx = Mock()
        result = adapter.chat(chat_ctx=mock_chat_ctx)
        
        assert isinstance(result, LangGraphStream)
        assert result._graph == mock_graph
        assert result._chat_ctx == mock_chat_ctx


class TestLangGraphStream:
    """Test the LangGraphStream class."""
    
    def test_init(self):
        """Test LangGraphStream initialization."""
        mock_graph = Mock()
        mock_chat_ctx = Mock()
        config = {"test": "config"}
        
        stream = LangGraphStream(
            graph=mock_graph,
            chat_ctx=mock_chat_ctx,
            config=config,
            langgraph_node="test_node"
        )
        
        assert stream._graph == mock_graph
        assert stream._chat_ctx == mock_chat_ctx
        assert stream._config == config
        assert stream._langgraph_node == "test_node"
    
    def test_init_defaults(self):
        """Test LangGraphStream initialization with defaults."""
        mock_graph = Mock()
        mock_chat_ctx = Mock()
        
        stream = LangGraphStream(graph=mock_graph, chat_ctx=mock_chat_ctx)
        
        assert stream._graph == mock_graph
        assert stream._chat_ctx == mock_chat_ctx
        assert stream._config is None
        assert stream._langgraph_node is None
    
    @pytest.mark.asyncio
    async def test_aiter_with_empty_context(self):
        """Test async iteration with empty chat context."""
        mock_graph = Mock()
        mock_chat_ctx = Mock()
        mock_chat_ctx.items = []
        
        # Mock the graph.astream to return empty
        mock_graph.astream = AsyncMock(return_value=iter([]))
        
        stream = LangGraphStream(graph=mock_graph, chat_ctx=mock_chat_ctx)
        
        chunks = []
        async for chunk in stream:
            chunks.append(chunk)
        
        assert len(chunks) == 0
        mock_graph.astream.assert_called_once()
    
    def test_run_not_implemented(self):
        """Test that _run method raises NotImplementedError."""
        mock_graph = Mock()
        mock_chat_ctx = Mock()
        
        stream = LangGraphStream(graph=mock_graph, chat_ctx=mock_chat_ctx)
        
        with pytest.raises(NotImplementedError):
            stream._run()


class TestIntegration:
    """Test integration between LLMAdapter and LangGraphStream."""
    
    def test_adapter_creates_stream_with_correct_params(self):
        """Test that LLMAdapter creates LangGraphStream with correct parameters."""
        mock_graph = Mock()
        config = {"configurable": {"thread_id": "test"}}
        node = "test_node"
        
        adapter = LLMAdapter(mock_graph, config=config, langgraph_node=node)
        mock_chat_ctx = Mock()
        
        stream = adapter.chat(chat_ctx=mock_chat_ctx)
        
        assert isinstance(stream, LangGraphStream)
        assert stream._graph == mock_graph
        assert stream._chat_ctx == mock_chat_ctx
        assert stream._config == config
        assert stream._langgraph_node == node