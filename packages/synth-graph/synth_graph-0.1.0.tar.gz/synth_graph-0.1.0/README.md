# synth-graph

Modern graph orchestration library for building stateful, multi-actor applications with LLMs.

Part of the Synth AI ecosystem.

## Features

- 🔄 Stateful graph orchestration
- 🎭 Multi-actor coordination  
- 🧠 LLM-native workflows
- 📊 Built-in observability
- ⚡ Async-first design
- 🔗 Seamless integration with Synth AI tools

## Installation

```bash
pip install synth-graph
```

## Quick Start

```python
from synth_graph import Graph, Node

# Create a graph
g = Graph()

# Add nodes
g.add_node("start", Node(fn=lambda x: x))
g.add_node("process", Node(fn=lambda x: x * 2))
g.add_node("end", Node(fn=lambda x: x))

# Connect nodes
g.add_edge("start", "process")
g.add_edge("process", "end")

# Execute
result = g.run(input_data=5)
print(result)  # 10
```

## Related Packages

- `finetuning` - Fine-tuning library for LLMs
- `synth-ai` - Main Synth AI SDK

## License

MIT