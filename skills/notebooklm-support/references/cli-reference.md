# notebooklm-py CLI Reference

## Notebooks
- `notebooklm notebooks list`: List all notebooks.
- `notebooklm notebooks create "<title>"`: Create a new notebook.
- `notebooklm notebooks delete <id>`: Delete a notebook.

## Sources
- `notebooklm sources list --notebook-id <id>`: List sources in a notebook.
- `notebooklm sources add <url|path> --notebook-id <id>`: Add a source (PDF, TXT, YouTube, URL).
- `notebooklm sources delete <source-id> --notebook-id <id>`: Remove a source.

## Queries
- `notebooklm ask "<prompt>" --notebook-id <id>`: Ask a question against the notebook's corpus.

## Artifacts
- `notebooklm artifacts generate audio --notebook-id <id>`: Generate a "Deep Dive" audio overview.
- `notebooklm artifacts download audio --notebook-id <id> --output <path>`: Download the generated audio (MP3).
- `notebooklm artifacts download slides --notebook-id <id> --output <path>`: Download the notebook slide deck (PPTX).
- `notebooklm artifacts download quiz --notebook-id <id> --output <path>`: Export study guide/quiz as Markdown/JSON/HTML.

## Profiles
- `notebooklm login`: Authenticate a new Google account.
- `notebooklm logout`: Clear credentials.
