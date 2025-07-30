# inprompt

A tiny CLI that outputs files as Markdown-formatted code blocks.
Handy for pasting source into prompts for large-language models.

## Usage

Pass files or glob patterns to `inprompt` and pipe the result to your clipboard:

```bash
inprompt pyproject.toml '**/*.py' | pbcopy
```

Need a different fence delimiter? Use `--fence` (or `-f`):

```bash
inprompt -f "~~~" script.py | pbcopy
```

**Note:** Always quote glob patterns such as `'**/*.py'` so the shell doesn't expand
them before `inprompt` sees them.

The `| pbcopy` (or equivalent) copies the formatted blocks directly to your clipboard:

- **macOS:** `pbcopy` is built-in.
- **Linux:** install `xclip` and define aliases for convenience:

  ```bash
  alias pbcopy='xclip -selection clipboard'
  alias pbpaste='xclip -selection clipboard -o'
  ```

Output format:

`````markdown
<filename>
````         ← configurable with --fence / -f
<file contents>
````
`````

## Installation

```bash
pip install inprompt
```

## License

[MIT License](LICENSE)
