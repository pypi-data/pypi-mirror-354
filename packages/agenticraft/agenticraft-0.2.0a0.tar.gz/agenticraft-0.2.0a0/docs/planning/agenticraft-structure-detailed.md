# AgentiCraft - Detailed Project Structure & Implementation Guide

## 📊 Competitive Analysis

### AgentiCraft vs Agentic Framework

| Aspect | AgentiCraft | Agentic Framework | 
|--------|-------------|-------------------|
| **Core Size** | <2000 LOC | ~10,000 LOC |
| **Documentation** | 100% coverage | ~30% coverage |
| **Memory System** | 2 types (simple) | 5 tiers (complex) |
| **Reasoning** | Transparent by default | Hidden/Optional |
| **Examples** | 15+ working examples | Few examples |
| **Quickstart Time** | 5 minutes | 30+ minutes |
| **MCP Support** | First-class | Good implementation |
| **Production Templates** | 4 templates included | None |
| **Plugin System** | Built-in | Not available |
| **Test Coverage** | >95% required | Unknown |

### Implementation Reference Guide

When implementing each component, reference Agentic Framework for:

1. **MCP Protocol** (`agentic/protocols/mcp/`)
   - Study their WebSocket implementation
   - Learn from their type definitions
   - Simplify their connection handling

2. **Tool Structure** (`agentic/tools/`)
   - See their tool organization
   - Adopt their async patterns
   - Avoid their complexity

3. **Testing Approach** (`tests/`)
   - Check their test structure
   - Improve with better coverage
   - Add missing integration tests

## 📁 Project Structure with Implementation Details

```
agenticraft/
├── __init__.py             # Package initialization, version info
├── __version__.py          # Single source of version truth
├── config.py               # Global configuration using Pydantic
│
├── core/                   # Core framework (<2000 LOC total)
│   ├── __init__.py        # Core exports
│   ├── agent.py           # Base Agent class (~300 LOC)
│   ├── reasoning.py       # Reasoning patterns and traces (~200 LOC)
│   ├── tool.py            # Tool abstraction (~200 LOC)
│   ├── workflow.py        # Workflow engine (~400 LOC)
│   ├── memory.py          # Memory interfaces (~150 LOC)
│   ├── provider.py        # LLM provider interface (~150 LOC)
│   ├── plugin.py          # Plugin architecture (~200 LOC)
│   ├── telemetry.py       # OpenTelemetry integration (~200 LOC)
│   └── exceptions.py      # Custom exceptions (~100 LOC)
│
├── protocols/              # Protocol implementations
│   ├── __init__.py
│   └── mcp/               # Model Context Protocol
│       ├── __init__.py
│       ├── types.py       # MCP type definitions
│       ├── client.py      # MCP client implementation
│       ├── server.py      # MCP server implementation
│       ├── registry.py    # Tool registry
│       ├── transport.py   # WebSocket/HTTP transport
│       └── adapters.py    # Tool adapters for MCP
│
├── agents/                 # Pre-built agents
│   ├── __init__.py
│   ├── base.py           # Shared agent functionality
│   ├── simple.py         # Basic conversational agent
│   ├── reasoning.py      # Agent with exposed reasoning
│   ├── react.py          # ReAct pattern implementation
│   ├── workflow.py       # Workflow-aware agent
│   └── team.py           # Multi-agent coordinator
│
├── tools/                  # Built-in tools
│   ├── __init__.py
│   ├── base.py           # Base tool class
│   ├── decorators.py     # @tool and @mcp_tool decorators
│   ├── core/             # Essential tools
│   │   ├── __init__.py
│   │   ├── search.py     # Web search tool
│   │   ├── calculator.py # Math operations
│   │   ├── text.py       # Text processing
│   │   ├── files.py      # File operations
│   │   └── http.py       # HTTP requests
│   └── registry.py       # Tool registry
│
├── memory/                 # Memory implementations
│   ├── __init__.py
│   ├── base.py           # Memory interface
│   ├── conversation.py   # Short-term chat memory
│   └── knowledge.py      # Vector-based long-term memory
│
├── providers/              # LLM integrations
│   ├── __init__.py
│   ├── base.py           # Provider interface
│   ├── openai.py         # OpenAI integration
│   ├── anthropic.py      # Anthropic integration
│   ├── ollama.py         # Local models via Ollama
│   └── litellm.py        # Universal adapter
│
├── plugins/                # Plugin system
│   ├── __init__.py
│   ├── base.py           # Plugin base class
│   ├── loader.py         # Dynamic plugin loading
│   ├── registry.py       # Plugin registry
│   └── manager.py        # Plugin lifecycle management
│
├── workflows/              # Workflow components
│   ├── __init__.py
│   ├── engine.py         # Core workflow executor
│   ├── step.py           # Step definitions
│   ├── conditions.py     # Conditional logic
│   ├── patterns/         # Common workflow patterns
│   │   ├── __init__.py
│   │   ├── parallel.py   # Parallel execution
│   │   ├── sequential.py # Sequential execution
│   │   └── conditional.py # Conditional branching
│   └── builder.py        # Workflow builder API
│
├── telemetry/             # Observability
│   ├── __init__.py
│   ├── config.py         # Telemetry configuration
│   ├── tracer.py         # OpenTelemetry tracer
│   ├── metrics.py        # Metrics collection
│   ├── exporters.py      # Export to various backends
│   └── decorators.py     # @track_metrics decorator
│
├── cli/                   # CLI implementation
│   ├── __init__.py
│   ├── main.py           # CLI entry point
│   ├── commands/         # CLI commands
│   │   ├── __init__.py
│   │   ├── new.py        # agenticraft new
│   │   ├── run.py        # agenticraft run
│   │   └── plugin.py     # agenticraft plugin
│   └── templates.py      # Template management
│
├── utils/                 # Utility functions
│   ├── __init__.py
│   ├── async_utils.py    # Async helpers
│   ├── json_utils.py     # JSON handling
│   ├── validation.py     # Input validation
│   └── logging.py        # Structured logging setup
│
├── templates/             # Production templates
│   └── (see detailed breakdown below)
│
└── examples/              # Comprehensive examples
    └── (see detailed breakdown below)
```

## 📋 Detailed Component Specifications

### Core Components

#### `core/agent.py`
```python
# Base Agent class with reasoning traces
class Agent:
    """Base agent with built-in reasoning transparency"""
    
    def __init__(self, name: str, provider: Provider, **kwargs):
        self.reasoning_trace = ReasoningTrace()
        self.telemetry = Telemetry()
        
    async def think(self, prompt: str) -> ThoughtProcess:
        """Expose agent's thinking process"""
        
    async def act(self, thought: ThoughtProcess) -> Action:
        """Execute based on thinking"""
        
    async def run(self, prompt: str) -> AgentResult:
        """Think and act in one call"""
```

#### `core/reasoning.py`
```python
# Reasoning patterns and transparency
class ReasoningTrace:
    """Captures and exposes agent reasoning"""
    
    def add_step(self, step: ReasoningStep):
        """Add reasoning step with confidence"""
        
    def get_explanation(self) -> str:
        """Human-readable reasoning explanation"""

class ReasoningPatterns:
    """Common reasoning patterns"""
    - ChainOfThought
    - StepByStep
    - ProblemDecomposition
    - SelfReflection
```

#### `core/tool.py`
```python
# Tool abstraction with MCP compatibility
class Tool:
    """Base tool class supporting both interfaces"""
    
    @abstractmethod
    async def execute(self, **kwargs) -> ToolResult:
        """Execute tool with parameters"""
    
    def to_mcp_tool(self) -> MCPTool:
        """Convert to MCP-compatible tool"""
        
    def get_schema(self) -> dict:
        """Return JSON schema for tool"""
```

#### `core/workflow.py`
```python
# Workflow orchestration engine
class Workflow:
    """Multi-step workflow executor"""
    
    def add_step(self, name: str, agent: Agent, **config):
        """Add workflow step with dependencies"""
        
    async def execute(self, input: Any) -> WorkflowResult:
        """Execute workflow with progress tracking"""
        
    async def visualize(self) -> str:
        """Generate workflow visualization"""
```

### Protocol Components

#### `protocols/mcp/types.py`
```python
# MCP protocol type definitions
@dataclass
class MCPRequest:
    method: str
    params: dict
    id: str

@dataclass
class MCPTool:
    name: str
    description: str
    parameters: JSONSchema
    
@dataclass
class MCPResource:
    uri: str
    type: ResourceType
    metadata: dict
```

### Templates Structure

```
templates/
├── fastapi/               # Production API template
│   ├── app/
│   │   ├── main.py       # FastAPI app with middleware
│   │   ├── agents/       # Agent endpoints
│   │   ├── middleware/   # Auth, rate limiting, CORS
│   │   └── monitoring/   # Health, metrics endpoints
│   ├── docker/
│   │   ├── Dockerfile
│   │   └── docker-compose.yml
│   ├── k8s/              # Kubernetes manifests
│   ├── tests/
│   └── README.md
│
├── cli/                   # CLI application template
│   ├── src/
│   │   ├── main.py
│   │   ├── commands/
│   │   └── config/
│   ├── tests/
│   └── README.md
│
├── mcp-server/           # Standalone MCP server
│   ├── server.py
│   ├── tools/
│   ├── config.yaml
│   └── README.md
│
└── bot/                  # Bot template
    ├── discord/
    ├── slack/
    └── README.md
```

### Examples Structure

```
examples/
├── quickstart/           # 5-minute examples
│   ├── 01_first_agent.py
│   ├── 02_using_tools.py
│   ├── 03_memory.py
│   ├── 04_reasoning.py
│   └── 05_workflow.py
│
├── reasoning/            # Reasoning transparency
│   ├── exposed_thinking.py
│   ├── confidence_levels.py
│   ├── decision_paths.py
│   └── self_reflection.py
│
├── workflows/            # Workflow examples
│   ├── content_pipeline.py
│   ├── research_workflow.py
│   ├── data_processing.py
│   └── multi_agent_flow.py
│
├── mcp/                  # MCP examples
│   ├── mcp_client.py
│   ├── mcp_server.py
│   ├── tool_discovery.py
│   └── bidirectional.py
│
├── plugins/              # Plugin examples
│   ├── weather_plugin/
│   ├── database_plugin/
│   └── custom_memory/
│
└── production/           # Real-world examples
    ├── customer_service/
    ├── content_generation/
    ├── data_analysis/
    └── monitoring_setup/
```

## 🔧 Implementation Guidelines

### Code Organization Rules

1. **Single Responsibility**: Each file should have one clear purpose
2. **Import Structure**: 
   ```python
   # Standard library
   import asyncio
   from typing import Any, Dict
   
   # Third party
   import httpx
   from pydantic import BaseModel
   
   # Local imports
   from agenticraft.core import Agent
   from agenticraft.tools import Tool
   ```

3. **Docstring Standards**:
   ```python
   def process(self, input: str) -> str:
       """Process input and return result.
       
       Args:
           input: The input string to process
           
       Returns:
           Processed result string
           
       Example:
           >>> agent.process("Hello")
           "Processed: Hello"
       """
   ```

4. **Type Hints**: Required for all public APIs
5. **Async First**: All I/O operations should be async

### Testing Structure

```
tests/
├── unit/              # Unit tests mirroring source structure
│   ├── core/
│   ├── agents/
│   └── tools/
├── integration/       # Integration tests
│   ├── test_mcp_integration.py
│   ├── test_provider_switching.py
│   └── test_workflow_execution.py
├── examples/          # Test all examples
│   └── test_examples.py
└── performance/       # Performance benchmarks
    ├── test_response_time.py
    └── test_memory_usage.py
```

### Configuration Management

```python
# config.py
from pydantic import BaseSettings

class AgentiCraftConfig(BaseSettings):
    # Core settings
    default_provider: str = "openai"
    default_model: str = "gpt-4"
    
    # Telemetry settings
    enable_telemetry: bool = True
    otlp_endpoint: str = "http://localhost:4317"
    
    # Memory settings
    max_conversation_length: int = 100
    vector_store_provider: str = "chromadb"
    
    # Plugin settings
    plugin_directory: str = "~/.agenticraft/plugins"
    auto_load_plugins: bool = True
    
    class Config:
        env_prefix = "AGENTICRAFT_"
```

## 📝 File Size Guidelines

To maintain the <2000 LOC limit for core:

- **agent.py**: ~300 lines (base functionality)
- **reasoning.py**: ~200 lines (reasoning patterns)
- **tool.py**: ~200 lines (tool abstraction)
- **workflow.py**: ~400 lines (orchestration)
- **memory.py**: ~150 lines (interfaces only)
- **provider.py**: ~150 lines (interfaces only)
- **plugin.py**: ~200 lines (plugin system)
- **telemetry.py**: ~200 lines (observability)
- **exceptions.py**: ~100 lines (error types)
- **config.py**: ~100 lines (configuration)

**Total Core**: ~2000 lines

## 🚀 Implementation Priority

### Week 1 Focus
1. Core abstractions (agent.py, tool.py)
2. MCP protocol basics
3. Simple agent implementation
4. Basic examples
5. FastAPI template

### Week 2 Focus
1. Reasoning transparency
2. Workflow engine
3. Memory implementations
4. More examples
5. Documentation site

This structure ensures:
- Clear separation of concerns
- Easy navigation for developers
- Modular design for extensibility
- Testable components
- Production-ready organization