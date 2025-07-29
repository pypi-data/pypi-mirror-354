---
description: This rule helps to avoid markdown linting errors
globs: *.md
alwaysApply: false
---
# Markdown Linting Rules

This document outlines the rules for writing consistent, maintainable Markdown files that pass linting checks.

## Spacing Rules

### MD012: No Multiple Consecutive Blank Lines

Do not use more than one consecutive blank line anywhere in the document.

❌ Incorrect:

```
Line 1


Line 2
```

✅ Correct:

```
Line 1

Line 2
```

### MD031: Fenced Code Blocks

Fenced code blocks should be surrounded by blank lines.

❌ Incorrect:
```shell
**Usage:**
```bash
# Code example
```
```

✅ Correct:
```shell
**Usage:**

```bash
# Code example
```

```

### MD032: Lists

Lists should be surrounded by blank lines.

❌ Incorrect:
```shell
This script cleans up:
- Item 1
- Item 2
```

✅ Correct:
```shell
This script cleans up:

- Item 1
- Item 2

```

### MD047: Files Must End With Single Newline

Files should end with a single empty line.

❌ Incorrect:
```shell
# Header
Content
No newline at end```

✅ Correct:
```shell
# Header
Content

```

### MD009: No Trailing Spaces

Lines should not have trailing spaces.

❌ Incorrect:
```shell
This line ends with spaces   
Next line
```

✅ Correct:
```shell
This line has no trailing spaces
Next line
```

## Formatting Rules

### MD050: Strong Style

Use asterisks (`**`) for strong emphasis, not underscores (`__`).

❌ Incorrect: `__bold text__`

✅ Correct: `**bold text**`

### MD040: Fenced Code Language

Fenced code blocks must have a language specified.

❌ Incorrect:
```
# Some code without language
```

✅ Correct:
```bash
# Bash script
```

✅ Correct:
```python
# Python code
```

✅ Correct:
```shell
# Directory structure
project/
├── src/
│   └── main.py
└── README.md
```

Common language specifiers:
- `shell` - For directory structures, shell commands
- `bash` - For bash scripts and commands
- `python` - For Python code
- `javascript` - For JavaScript code
- `json` - For JSON data
- `yaml` - For YAML files
- `mermaid` - For Mermaid diagrams
- `markdown` - For markdown examples

### Code Formatting for Special Syntax

For directory/file names with underscores or special characters, use backticks instead of emphasis.

❌ Incorrect: `**__pycache__**` or `__pycache__`

✅ Corr`__pycache__` ``

## Header Rules

### MD001: Header Increment

Headers should increment by one level at a time.

❌ Incorrect:
```shell
# Header 1
### Header 3
```

✅ Correct:
```shell
# Header 1
## Header 2
### Header 3
```

### MD022: Headers Should Be Surrounded By Blank Lines

❌ Incorrect:
```shell
# Header 1
Content starts here
```

✅ Correct:
```shell
# Header 1

Content starts here
```

### MD025: Single H1 Header

Only one top-level header (H1) is allowed per document.

\
## List Rules

### MD004: List Style

Use consistent list markers. Prefer dashes (`-`) for unordered lists.

❌ Incorrect (mixed):
```markdown
- Item 1
* Item 2
+ Item 3
```

✅ Correct:
```markdown
- Item 1
- Item 2
- Item 3
```

### MD007: Unordered List Indentation

Nested unordered list items should be indented consistently, typically by 2 spaces.

❌ Incorrect (4 spaces):
```markdown
- Item 1
    - Sub-item A
```

✅ Correct (2 spaces):
```markdown
- Item 1
  - Sub-item A
```

### MD030: Spaces After List Markers

Use exactly one space after the list marker (e.g., `-`, `*`, `+`, `1.`).

❌ Incorrect (multiple spaces):
```markdown
-  Item 1
1.   Item 2
```

✅ Correct (one space):
```markdown
- Item 1
1. Item 2
```

### MD029: Ordered List Item Prefix

Use incrementing numbers for ordered lists.

❌ Incorrect:
```shell
1. Item 1
1. Item 2
1. Item 3
```

✅ Correct:
```shell
1. Item 1
2. Item 2
3. Item 3
```

## Link Rules

### MD034: Bare URLs

Enclose bare URLs in angle brackets or format them as links.

❌ Incorrect: `https://example.com`

✅ Correct: `<https://example.com>` or `@Example`

## Code Rules

### MD038: Spaces Inside Code Spans

Don't use spaces immediately inside code spans.

❌ Incorrect: `` ` code ` ``

✅ Correct: `` `code` ``

## General Best Practices

1. Use consistent indentation (usually 2 or 4 spaces)
2. Keep line length under 120 characters
3. Use reference-style links for better readability
4. Use a trailing slash for directory paths
5. Ensure proper escaping of special characters
6. Always specify a language for code fences
7. End files with a single newline
8. Remove trailing spaces from all lines

## IDE Integration

To enable these rules in your editor:

- VS Code: Install the "markdownlint" extension
- JetBrains IDEs: Use the bundled Markdown support or install "Markdown Navigator Enhanced"
- Vim/Neovim: Use "ale" with markdownlint rules

These rules ensure consistency and improve readability across all Markdown documents in the codebase.