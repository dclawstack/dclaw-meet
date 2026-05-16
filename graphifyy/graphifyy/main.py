"""Main module for graphifyy — Obsidian vault knowledge graph builder."""

import os
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class Node:
    """A node in the knowledge graph representing an Obsidian note."""
    id: str
    title: str
    path: str
    tags: list[str] = field(default_factory=list)
    links: list[str] = field(default_factory=list)
    backlinks: list[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)


class VaultGraph:
    """Builds and queries a knowledge graph from an Obsidian vault."""

    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path).resolve()
        self.nodes: dict[str, Node] = {}
        self.tag_index: dict[str, list[str]] = {}

    def index(self) -> "VaultGraph":
        """Scan the vault and build the graph index."""
        for md_file in self.vault_path.rglob("*.md"):
            rel_path = str(md_file.relative_to(self.vault_path))
            note_id = rel_path.replace(os.sep, "/")
            content = md_file.read_text(encoding="utf-8")

            tags = self._extract_tags(content)
            raw_links = self._extract_wikilinks(content)

            node = Node(
                id=note_id,
                title=md_file.stem,
                path=rel_path,
                tags=tags,
                links=raw_links,
                metadata=self._extract_frontmatter(content),
            )
            self.nodes[note_id] = node

        # Resolve wikilinks (Obsidian links by title, not by path)
        title_to_id: dict[str, str] = {}
        for note_id, node in self.nodes.items():
            title_to_id[node.title] = note_id

        for node in self.nodes.values():
            resolved: list[str] = []
            for link in node.links:
                if link in self.nodes:
                    resolved.append(link)
                elif link in title_to_id:
                    resolved.append(title_to_id[link])
                else:
                    resolved.append(link)  # unresolved, keep as-is
            node.links = resolved

        # Build backlink index
        for node in self.nodes.values():
            for target_id in node.links:
                if target_id in self.nodes:
                    self.nodes[target_id].backlinks.append(node.id)

        # Build tag index
        for node in self.nodes.values():
            for tag in node.tags:
                self.tag_index.setdefault(tag, []).append(node.id)

        return self

    def _extract_tags(self, content: str) -> list[str]:
        """Extract #tags from markdown content."""
        import re
        return list(set(re.findall(r"#([a-zA-Z0-9_/-]+)", content)))

    def _extract_wikilinks(self, content: str) -> list[str]:
        """Extract [[WikiLinks]] from markdown content."""
        import re
        matches = re.findall(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", content)
        return [m.strip().replace(" ", "_") for m in matches]

    def _extract_frontmatter(self, content: str) -> dict:
        """Extract YAML frontmatter from markdown."""
        import yaml
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                try:
                    return yaml.safe_load(parts[1]) or {}
                except yaml.YAMLError:
                    pass
        return {}

    def search(self, query: str) -> list[Node]:
        """Search nodes by title or tag."""
        query_lower = query.lower()
        results = []
        for node in self.nodes.values():
            if query_lower in node.title.lower() or any(query_lower in t.lower() for t in node.tags):
                results.append(node)
        return results

    def get_by_tag(self, tag: str) -> list[Node]:
        """Return all nodes with a given tag."""
        return [self.nodes[nid] for nid in self.tag_index.get(tag, []) if nid in self.nodes]

    def get_orphaned(self) -> list[Node]:
        """Return nodes with no incoming or outgoing links."""
        return [n for n in self.nodes.values() if not n.links and not n.backlinks]

    def stats(self) -> dict:
        """Return graph statistics."""
        return {
            "total_nodes": len(self.nodes),
            "total_links": sum(len(n.links) for n in self.nodes.values()),
            "total_backlinks": sum(len(n.backlinks) for n in self.nodes.values()),
            "unique_tags": len(self.tag_index),
            "orphaned_nodes": len(self.get_orphaned()),
        }


def main() -> None:
    """CLI entry point for graphifyy."""
    import sys
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <vault_path>")
        sys.exit(1)

    vault_path = sys.argv[1]
    graph = VaultGraph(vault_path).index()
    stats = graph.stats()
    print(f"Indexed {stats['total_nodes']} notes from {vault_path}")
    print(f"  Links: {stats['total_links']}, Backlinks: {stats['total_backlinks']}")
    print(f"  Tags: {stats['unique_tags']}, Orphaned: {stats['orphaned_nodes']}")


if __name__ == "__main__":
    main()
