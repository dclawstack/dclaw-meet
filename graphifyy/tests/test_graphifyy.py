"""Tests for graphifyy VaultGraph."""

import tempfile
from pathlib import Path

import pytest

from graphifyy.main import VaultGraph


@pytest.fixture
def sample_vault():
    with tempfile.TemporaryDirectory() as tmpdir:
        vault = Path(tmpdir)
        (vault / "Notes").mkdir()
        (vault / "Notes" / "hello.md").write_text("# Hello\n\nThis is a note with #greeting tag.")
        (vault / "Notes" / "world.md").write_text("# World\n\nLinks to [[hello]] and #world tag.")
        (vault / "Orphan.md").write_text("# Orphan\n\nNo links here.")
        yield str(vault)


def test_index_builds_nodes(sample_vault):
    graph = VaultGraph(sample_vault).index()
    assert len(graph.nodes) == 3
    assert "Notes/hello.md" in graph.nodes
    assert "Notes/world.md" in graph.nodes


def test_extract_tags(sample_vault):
    graph = VaultGraph(sample_vault).index()
    hello = graph.nodes["Notes/hello.md"]
    assert "greeting" in hello.tags


def test_extract_wikilinks(sample_vault):
    graph = VaultGraph(sample_vault).index()
    world = graph.nodes["Notes/world.md"]
    assert "Notes/hello.md" in world.links


def test_backlinks(sample_vault):
    graph = VaultGraph(sample_vault).index()
    hello = graph.nodes["Notes/hello.md"]
    assert "Notes/world.md" in hello.backlinks


def test_tag_index(sample_vault):
    graph = VaultGraph(sample_vault).index()
    greeting_nodes = graph.get_by_tag("greeting")
    assert len(greeting_nodes) == 1
    assert greeting_nodes[0].id == "Notes/hello.md"


def test_search(sample_vault):
    graph = VaultGraph(sample_vault).index()
    results = graph.search("hello")
    assert any(r.id == "Notes/hello.md" for r in results)


def test_orphaned(sample_vault):
    graph = VaultGraph(sample_vault).index()
    orphaned = graph.get_orphaned()
    assert len(orphaned) == 1
    assert orphaned[0].id == "Orphan.md"


def test_stats(sample_vault):
    graph = VaultGraph(sample_vault).index()
    stats = graph.stats()
    assert stats["total_nodes"] == 3
    assert stats["total_links"] == 1
    assert stats["unique_tags"] == 2  # greeting, world
    assert stats["orphaned_nodes"] == 1
