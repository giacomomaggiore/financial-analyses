---
name: check-markdown-latex
description: "Edit one Markdown file for grammar, spelling, Markdown syntax, typo, character, and LaTeX rendering errors while preserving all content. Use for conservative proofreading of .md or .mdx files."
argument-hint: "Path to one .md or .mdx file"
---

# Markdown Grammar and LaTeX Editor

## Purpose

Edit one `.md` or `.mdx` file as a conservative proofreading pass. Correct grammar, spelling, punctuation, Markdown syntax, malformed characters, and LaTeX notation that prevents the intended formula from rendering. Preserve the author's content, meaning, structure, and voice.

## Strict Boundaries

- Work only on the requested `.md` or `.mdx` file.
- Do not add explanations, examples, sentences, headings, citations, references, or factual claims.
- Do not remove paragraphs, sentences, list items, formulas, or other substantive content.
- Do not summarize, rewrite, reorder, expand, or stylistically modernize the text.
- Preserve paragraph boundaries, list structure, heading hierarchy, and formula meaning.
- Preserve frontmatter, fenced code blocks, inline code, HTML, JSX, imports, and exports unless a clearly malformed delimiter prevents parsing.
- If a correction would require guessing the author's meaning, leave it unchanged and report it for review.

## Procedure

1. Identify exactly one target path. Require a `.md` or `.mdx` extension; ask for clarification if the path is missing or ambiguous.
2. Read the complete current file before editing. Treat the current contents as authoritative, including user edits made since an earlier pass.
3. Inspect the surrounding paragraph and neighboring Markdown or LaTeX before changing any fragment.
4. Make only these corrections:
   - grammar, spelling, punctuation, capitalization, and obvious typographical errors;
   - malformed Markdown delimiters, escapes, list markers, links, or emphasis that clearly cause parsing or rendering errors;
   - wrong or non-standard characters that clearly cause compilation or rendering errors;
   - LaTeX delimiters, commands, braces, subscripts, superscripts, operators, and symbols when the intended expression is unambiguous.
5. For an incomplete LaTeX formula, infer the missing notation only from the formula's immediate paragraph and an explicitly available source article. Restore notation that is clearly implied by that context; never derive or introduce a new result.
6. If the source article is unavailable or the formula has multiple plausible interpretations, do not complete it. Preserve the original and flag the location instead.
7. Apply the smallest possible edit with no unrelated formatting changes.
8. Review the diff and verify that every change is a local grammar, typo, Markdown, character, or LaTeX representation fix. Confirm that no paragraph or substantive sentence was added, removed, or rewritten.
9. Run a whitespace check on the changed file, for example:

   ```bash
   git diff --check -- <path>
   ```

10. Report the file edited, the categories of corrections made, and any ambiguous fragments deliberately left unchanged.

## Completion Criteria

The task is complete only when the file remains semantically and structurally the same, all unambiguous targeted errors are corrected, Markdown and LaTeX delimiters are balanced where applicable, and no uncertain mathematical content has been invented.