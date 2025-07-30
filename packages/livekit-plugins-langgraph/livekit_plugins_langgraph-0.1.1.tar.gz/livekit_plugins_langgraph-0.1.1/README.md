# LiveKit LangGraph Plugin

[![PyPI version](https://badge.fury.io/py/livekit-plugins-langgraph.svg)](https://badge.fury.io/py/livekit-plugins-langgraph)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An enhanced LiveKit plugin for seamless integration with LangGraph workflows. This plugin provides universal filtering capabilities to ensure only user-facing responses are spoken by voice agents, while filtering out tool calls and intermediate workflow outputs.

## 🌟 Key Features

- **Universal Tool Filtering**: Automatically filters out tool calls, tool messages, and tool-related metadata
- **Node-Based Filtering**: Selectively allow messages from specific LangGraph nodes (optional)
- **Real-Time Streaming**: Preserves streaming tokens for smooth, real-time voice synthesis
- **Workflow Support**: Works seamlessly with any LangGraph workflow
- **RemoteGraph & CompiledStateGraph**: Supports both local and remote LangGraph execution

## 🚀 Quick Start

### Installation

```bash
pip install livekit-plugins-langgraph
```

For development with examples:
```bash
pip install livekit-plugins-langgraph[examples]
```

### Basic Usage

```python
from livekit.agents import Agent, AgentSession
from livekit.plugins.langgraph import LLMAdapter
from langgraph.pregel.remote import RemoteGraph

# Connect to your LangGraph workflow
graph = RemoteGraph("your_workflow", url="http://localhost:2024")

# Create adapter with filtering
llm_adapter = LLMAdapter(
    graph,
    config={"configurable": {"thread_id": "unique_session_id"}},
    langgraph_node="final_node"  # Only allow specific node responses (optional)
)

# Use in LiveKit agent
agent = Agent(
    instructions="You are a helpful AI assistant.",
    llm=llm_adapter
)
```

## 📖 Detailed Usage

### Node-Based Filtering

Control which nodes in your LangGraph workflow can speak:

```python
# Only specific node responses
LLMAdapter(graph, langgraph_node="my_node")

# Multiple specific nodes
LLMAdapter(graph, langgraph_node=["node_a", "node_b"])

# No node filtering (only tool filtering)
LLMAdapter(graph, langgraph_node=None)
```

**Note**: Node names like "supervisor", "my_node", etc. are just examples. Use the actual node names from your specific LangGraph workflow.

### Complete Voice Agent Example

```python
import asyncio
from livekit.agents import Agent, AgentSession, JobContext
from livekit.plugins import deepgram, silero
from livekit.plugins.langgraph import LLMAdapter
from livekit.plugins.turn_detector.multilingual import MultilingualModel
from langgraph.pregel.remote import RemoteGraph

async def voice_agent_example(ctx: JobContext):
    # Connect to LangGraph
    graph = RemoteGraph("my_workflow", url="http://localhost:2024")
    
    # Configure with filtering
    llm_adapter = LLMAdapter(
        graph,
        config={"configurable": {"thread_id": "session_123"}},
        langgraph_node="final_node"  # Replace with your actual node name
    )
    
    # Create voice agent
    agent = Agent(
        instructions="You are a helpful AI assistant.",
        llm=llm_adapter
    )
    
    # Set up voice session
    session = AgentSession(
        vad=silero.VAD.load(),
        stt=deepgram.STT(model="nova-2", language="en"),
        tts=deepgram.TTS(model="aura-asteria-en"),
        turn_detection=MultilingualModel(),
    )
    
    # Start voice interaction
    await session.start(agent=agent, room=ctx.room)
```

## 🔧 Configuration Options

### LLMAdapter Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `graph` | `PregelProtocol` | LangGraph instance (RemoteGraph or CompiledStateGraph) |
| `config` | `RunnableConfig` | Optional configuration for graph execution |
| `langgraph_node` | `str \| list[str] \| None` | Node name(s) to filter by. Only messages from these nodes will be spoken |

### Filtering Behavior

The plugin automatically filters out:

- ✅ **Tool Calls**: Function calls between workflow nodes
- ✅ **Tool Messages**: Responses from tools and external services  
- ✅ **Tool Metadata**: Tool-related metadata and chunks
- ✅ **Intermediate Outputs**: Internal workflow communications

While preserving:

- ✅ **Streaming Tokens**: Real-time response building
- ✅ **User-Facing Content**: Final conversational responses
- ✅ **Allowed Nodes**: Messages from specified nodes only (if configured)

## 📁 Examples

### Voice Assistant with LangGraph

See [`examples/multi_agent_voice.py`](examples/multi_agent_voice.py) for a complete example of:

- Setting up a voice-enabled LangGraph workflow
- Configuring node-based filtering
- Handling real-time voice interaction
- Integration with LangGraph RemoteGraph

**Note**: The example uses "supervisor" as a node name, but this should be replaced with the actual node names from your specific workflow.

### Running the Example

1. **Set up LangGraph server** with your workflow
2. **Configure environment**:
   ```bash
   # .env file
   OPENAI_API_KEY=your_openai_key
   LANGGRAPH_SERVER_URL=http://localhost:2024
   ```
3. **Run the voice agent**:
   ```bash
   python examples/multi_agent_voice.py dev
   ```

## 🏗️ Architecture

### How It Works

1. **Message Processing**: Converts LiveKit chat context to LangGraph format
2. **Streaming**: Processes real-time message chunks from LangGraph
3. **Universal Filtering**: Applies comprehensive filtering rules
4. **Node Filtering**: Optionally filters by LangGraph node metadata
5. **Speech Synthesis**: Passes clean content to LiveKit TTS

### Filtering Pipeline

```
LangGraph Stream → Universal Filter → Node Filter → LiveKit TTS
                      ↓                 ↓
                 Blocks tools,     Allows only
                 metadata         specified nodes
```

## 🧪 Testing

The package includes comprehensive filtering tests:

```bash
# Run filtering verification
python -m pytest tests/

# Manual testing with your workflow
python examples/multi_agent_voice.py dev
```

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

### Development Setup

```bash
git clone https://github.com/tim-yung/livekit-plugins-langgraph
cd livekit-plugins-langgraph
pip install -e .[dev]
```

## 📋 Requirements

- **Python**: 3.9+
- **LiveKit Agents**: 0.8.0+
- **LangChain Core**: 0.3.0+
- **LangGraph**: 0.2.0+
- **LangGraph SDK**: 0.1.0+

## 🐛 Troubleshooting

### Common Issues

**Agent is silent / no speech output**
- Check that your LangGraph workflow is running
- Verify node names match your workflow (use `langgraph_node=None` to test)
- Ensure OpenAI API key is configured

**Tool calls being spoken**
- This should not happen with the plugin - please file an issue

### Debug Mode

Enable detailed logging:

```python
import logging
logging.getLogger("livekit.plugins.langgraph").setLevel(logging.DEBUG)
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [LiveKit](https://livekit.io/) for the excellent real-time communication platform
- [LangGraph](https://langchain-ai.github.io/langgraph/) for powerful multi-agent workflows
- The open-source community for inspiration and feedback

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/tim-yung/livekit-plugins-langgraph/issues)
- **Discussions**: [GitHub Discussions](https://github.com/tim-yung/livekit-plugins-langgraph/discussions)
- **Documentation**: [README](https://github.com/tim-yung/livekit-plugins-langgraph#readme)

---

**Made with ❤️ for the voice AI community**