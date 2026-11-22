---
name: clean-markdown
description: "Preview and conservatively clean grammar, OCR artifacts, Markdown syntax, and non-content noise in one private Obsidian note."
argument-hint: "Exact note title or a unique filename fragment"
---

# Clean Markdown

Use this skill only for one note in `wiki/private/`. Make conservative repairs only: clear OCR and grammar errors, Markdown and LaTeX syntax, and extraction noise. Never summarize, rewrite meaning, or change frontmatter.

## Procedure

1. Require an exact title or a filename fragment that identifies one private note. If it is ambiguous, ask the user to choose the note.
2. Read the complete note and prepare a precise preview of the proposed edits. Do not modify the file during this step.
3. Summarize the proposed cleanup and ask for explicit approval.
4. After approval, apply only the previewed edits.
5. Review the diff to verify that frontmatter, meaning, technical content, formulas, tables, citations, and existing valid wikilinks are unchanged.
6. Suggest `pnpm index` only when the changed note should be searchable through `/ask` locally. Do not run it unless requested.
7. Do not commit, push, or deploy unless explicitly requested.
