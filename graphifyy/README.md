# graphifyy

> Knowledge graph builder for local Obsidian vaults.

## Install

```bash
cd graphifyy
pip install -e .
```

## Usage

```python
from graphifyy.main import VaultGraph

graph = VaultGraph("/path/to/vault").index()
print(graph.stats())

# Search notes
results = graph.search("architecture")

# Find by tag
nodes = graph.get_by_tag("sprint")

# Find orphaned notes (no links in or out)
orphans = graph.get_orphaned()
```

## CLI

```bash
graphifyy /path/to/vault
```

## Test

```bash
pytest
```
