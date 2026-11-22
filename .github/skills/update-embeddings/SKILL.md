---
name: update-embeddings
description: "Rebuild the wiki retrieval index and OpenAI embeddings. Use when asked to recreate embeddings, refresh semantic search, rebuild the wiki index, or make new notes searchable in /ask."
argument-hint: "Optional reason, such as a newly added note or blog post"
---

# Update Embeddings

Use the existing wiki indexer. It indexes public notes, blog posts, and private notes. When `OPENAI_API_KEY` is configured, it recreates all note embeddings with `text-embedding-3-small`; otherwise it deliberately produces a BM25-only index.

## Procedure

1. From the repository root, run:

   ```bash
   pnpm index
   ```
2. Report the indexer output, including the note count and whether embeddings were created or skipped because `OPENAI_API_KEY` is unavailable.
3. Do not reveal environment-variable values or API keys.
4. Check `git status` and report generated-file changes. Do not commit or push unless explicitly asked.

`pnpm build` also rebuilds the index automatically through the `prebuild` hook. Use this skill when the index must be refreshed without doing a full production build.