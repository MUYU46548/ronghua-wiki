---
publish: true
---

# Agent Context Index

This vault uses Agent Context Indexing.

Before exploring this vault directly, read:

`.agent_context/latest/agent_context_manifest.json`

Recommended workflow:

1. Read `.agent_context/latest/agent_context_manifest.json`.
2. Read `.agent_context/latest/directory_context.md`.
3. Read `.agent_context/latest/large_index_notice.md`.
4. Read `.agent_context/latest/folder_tree_summary.md`.
5. Read `.agent_context/latest/file_inventory_summary.md`.
6. Read `.agent_context/latest/inventory_group_counts.csv`.
7. Use the category-specific inventory files only as needed.
8. Use `.agent_context/latest/note_index.csv`, `.agent_context/latest/markdown_outline.csv`, `.agent_context/latest/note_link_graph.csv`, `.agent_context/latest/backlink_summary.md`, and `.agent_context/latest/frontmatter_index.csv` for note navigation.
9. Use `.agent_context/latest/attachment_reference_graph.csv` to understand references from notes to PDFs, images, data files, and other non-Markdown files.
10. Prefer rows where target_exists is true before trying to read original files.
11. Read original source files only after selecting a small number of relevant candidates.

Important notes:

- The index is breadth-first and metadata-first.
- The index is intentionally capped to avoid large single files.
- Non-Markdown files are indexed by metadata only.
- If this file was generated as AGENTS.agent-context-indexer.md, an existing AGENTS.md was not overwritten. Merge manually if desired.
- If the index looks stale, ask the user to rerun the appropriate agent context command in Obsidian.