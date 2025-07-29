# Week 3 Quick Reference - v0.2.0 Implementation

## 🎯 Core Features to Implement

### 1. Streaming Responses (`core/streaming.py`)
```python
class StreamingResponse:
    """Base class for streaming responses"""
    
class StreamChunk:
    """Individual chunk in stream"""
    token: str
    metadata: dict
    
async def stream(prompt: str) -> AsyncIterator[StreamChunk]:
    """Stream responses token by token"""
```

### 2. Advanced Reasoning (`reasoning/patterns/`)
```python
# Chain of Thought
class ChainOfThoughtReasoning:
    - Step-by-step thinking
    - Confidence scores
    - Explanation generation

# Tree of Thoughts  
class TreeOfThoughtsReasoning:
    - Multiple reasoning paths
    - Branch evaluation
    - Best path selection

# ReAct Pattern
class ReActReasoning:
    - Thought → Action → Observation
    - Tool integration
    - Self-correction
```

### 3. MCP Protocol (`protocols/mcp/`)
```python
# Server
class MCPServer:
    - WebSocket server
    - Tool registration
    - Request handling

# Client
class MCPClient:
    - Tool discovery
    - Remote execution
    - Response handling
```

### 4. Enhanced Workflows (`workflows/`)
```python
# Visual
class WorkflowVisualizer:
    - Mermaid diagrams
    - ASCII art
    - Progress overlay

# Patterns
- Parallel execution
- Conditional branching
- Loop/retry
- Map-reduce
```

### 5. Telemetry (`telemetry/`)
```python
# OpenTelemetry
- Trace all operations
- Collect metrics
- Export to backends
- <1% overhead

# Key Metrics
- Token usage
- Response latency
- Tool execution time
- Error rates
```

### 6. Better Memory (`memory/`)
```python
# Vector Memory
class VectorMemory:
    - ChromaDB backend
    - Similarity search
    - Cross-agent sharing

# Knowledge Graph
class KnowledgeGraphMemory:
    - Entity extraction
    - Relationship mapping
```

### 7. Tool Marketplace (`marketplace/`)
```python
# Foundation
- Plugin manifest schema
- Registry client
- Version management
- Dependency resolution
```

---

## 📁 New Files to Create

```
agenticraft/
├── core/
│   └── streaming.py              # NEW
├── reasoning/
│   └── patterns/                 # NEW
│       ├── chain_of_thought.py
│       ├── tree_of_thoughts.py
│       └── react.py
├── protocols/
│   └── mcp/                      # NEW
│       ├── types.py
│       ├── server.py
│       ├── client.py
│       └── adapters.py
├── workflows/
│   ├── visual/                   # NEW
│   │   └── visualizer.py
│   ├── patterns/                 # NEW
│   └── templates/                # NEW
├── telemetry/                    # NEW
│   ├── tracer.py
│   ├── metrics.py
│   └── exporters/
├── memory/
│   ├── vector/                   # NEW
│   │   └── chromadb_memory.py
│   └── graph/                    # NEW
│       └── knowledge_graph.py
└── marketplace/                  # NEW
    ├── registry.py
    └── manifest.py
```

---

## 🔧 Files to Update

1. **`core/agent.py`**
   - Add `stream()` method
   - Integrate telemetry
   - Support new reasoning patterns

2. **`providers/*.py`** (all 3)
   - Add streaming support
   - Telemetry instrumentation

3. **`agents/reasoning.py`**
   - Use new reasoning patterns
   - Pattern selection logic

4. **`pyproject.toml`**
   - Add new dependencies:
     - `opentelemetry-api>=1.20.0`
     - `opentelemetry-sdk>=1.20.0`
     - `chromadb>=0.4` (optional)
     - `websockets>=12.0`

---

## 📦 New Dependencies

```toml
# Required
websockets = ">=12.0"           # MCP WebSocket
opentelemetry-api = ">=1.20.0"  # Telemetry
opentelemetry-sdk = ">=1.20.0"  # Telemetry

# Optional
chromadb = ">=0.4"              # Vector memory
mermaid-py = ">=0.3"            # Workflow viz
```

---

## 🧪 Test Requirements

Each feature needs:
1. Unit tests (feature logic)
2. Integration tests (with providers)
3. Examples (2+ per feature)
4. Documentation (guide + API docs)
5. Performance benchmarks

---

## 📊 Daily Goals

| Day | Feature | Target | Success Metric |
|-----|---------|--------|----------------|
| Mon | Streaming | All providers | <100ms latency |
| Tue | Reasoning | 3 patterns | Working examples |
| Wed | MCP | Server + Client | Tool discovery |
| Thu | Workflows | Visualization | Valid Mermaid |
| Fri | Telemetry | Integration | <1% overhead |
| Sat | Memory | Vector + Graph | <50ms retrieval |
| Sun | Polish | Tests + Docs | >95% coverage |

---

## 🚀 Git Workflow

```bash
# Start each day
git checkout main
git pull
git checkout -b feature/v0.2.0-{feature}

# Commit frequently
git add .
git commit -m "{component}: {what you did}"

# End of day
git push origin feature/v0.2.0-{feature}
# Create PR for review
```

---

## ⚡ Quick Commands

```bash
# Run tests
pytest tests/ -v

# Check coverage
pytest --cov=agenticraft --cov-report=html

# Format code
black agenticraft/
ruff check agenticraft/

# Build docs
mkdocs serve

# Run examples
python examples/{feature}/{example}.py
```

---

## 📝 PR Template

```markdown
## Feature: {Feature Name}

### What's New
- Brief description of feature
- Key capabilities added

### Implementation
- Files added: 
- Files modified:
- Dependencies added:

### Testing
- [ ] Unit tests added
- [ ] Integration tests added
- [ ] Examples created
- [ ] Coverage >95%

### Documentation
- [ ] API docs updated
- [ ] Feature guide written
- [ ] Examples documented

### Performance
- Benchmark results:
- Overhead: <X%
```

---

## 🎯 Remember

1. **Simplicity First** - Don't over-engineer
2. **Test Everything** - TDD when possible
3. **Document Now** - Not later
4. **Benchmark Often** - Catch regressions
5. **Ship Daily** - Working > Perfect

**Goal**: v0.2.0-alpha ready by Sunday night! 🚀
