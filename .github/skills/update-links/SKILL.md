---
name: update-links
description: "Review and curate Obsidian wikilinks across requested private notes. Use when asked to review vault links, curate Related notes, validate wikilinks, or reconnect private notes."
argument-hint: "Optional note title or filename fragment; omit to review the entire private vault"
---

# Update Links

Use this skill only for notes in `wiki/private/`. Never read from or link to `wiki/public/` blog posts or notes.

## Procedure

1. Confirm the requested scope. If a title or filename fragment is ambiguous, ask the user to choose one exact note. For vault-wide work, state the number of notes that will be reviewed.
2. Read the requested private notes and identify only meaningful relationships: shared thesis, author, method and application, theory and empirical test, or clear companion material. Do not add links for weak topical overlap.
3. Prepare a preview of every proposed change. Use existing note titles verbatim as wikilink targets, never link a note to itself, and do not alter frontmatter, formulas, tables, citations, or substantive text.
4. Ask for explicit approval before modifying any private note.
5. After approval, apply only the previewed links and, when useful, a concise `## Related notes` section (or `## Note correlate` for Italian notes).
6. Validate every wikilink target against the requested private-note set. Replace an invalid or ambiguous target with plain text instead of guessing.
7. Review the diff and report the changes. Suggest `pnpm index` only when the changed notes should be searchable through `/ask` locally; do not run it unless requested.
8. Do not commit, push, or deploy unless explicitly requested.
