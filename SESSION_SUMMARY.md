# Session Summary — v0.2.1

## Last Commit
`9673f01` — `Fix: input browse localisation detection + auto output path`

## Current State
- Git remote: `https://github.com/greenlight5916/OllamaTranslator`
- EXE: `OllamaTranslator.exe` (root)
- Config: `ollama_translator_config.json` (gitignored)
- Logs: `rog/` (gitignored)

## Tab Structure

### Translate Tab
- Source/Target language selection, Input/Output folder browse
- **Input Browse**: auto-detects `localisation/` (or `localization/`) subfolder, then `english/` language folder
- **Output auto-set**: if input folder name matches source language code (e.g. `english`), output auto-set to target language folder (e.g. `korean/`), created if missing
- Output path color: gray (`#888888`) when auto-filled, white when manually set via Browse Output
- config.json saved immediately on input browse (persists across restarts)
- Start Ollama, Connect, Start Translation, Stop, Reset, Live, Debug Log
- Checkpoint save/resume, Edit Prompt support
- Batch size, Temperature, Max Tokens, Max Retries settings

### Validate Tab (redesigned)
- **Load Files**: scans input_dir for `l_{src}` files, matches with output files (same name, different lang code)
- **Dropdown**: file list with severity icons (`⚠` warn, `✗` error), sorted by issue priority
- **Line table**: KEY / Source / Target(editable) / Status / Ln / Checkbox — fixed-width columns
- **Show headers** checkbox: toggles H/`-` line visibility (default off)
- **Lines/page**: user-configurable page size
- **Page navigation**: ◀ Prev / Next ▶ buttons + page info + stats
- **Retry Selected**: LLM re-translates checked lines with placeholder protection
- **Save Changes**: persists edited/retried lines to output file
- **Double-click popup**: Source(50%) / Target(50%, editable) side by side, Prev/Next, Retry with LLM
- **Exit warning**: unsaved changes prompt (Save & Exit / Exit / Cancel)
- **Depth-limited os.walk**: 1 level only for file scanning

### Glossary Tab (GAME / MOD)
- GAME: Dice coefficient extraction, pagination, search, save/load
- MOD: English term frequency, LLM batch translation, checkbox select, retry

## Key Architecture Changes (this session)
- **Value-only translation**: game codes replaced with `{PHn}` placeholders before LLM, restored after
- **Line markers** `⟨N⟩`: added to values for robust batch count matching
- **YAML structure preserved**: original copy in memory, only translated values swapped in
- **`codecs.open` → `open`**: Python 3.14 deprecation fix
- **BOM fix**: output written with `utf-8-sig` for game recognition
- **`\\n` preservation**: escaped newlines re-escaped post-translation
- **Subfolder output**: input subdirectory structure mirrored in output (`english/` → `english/`)

## Known Config Keys
Translate: `ollama_url`, `ollama_model`, `input_dir`, `output_dir`, `source_lang`, `target_lang`, `selected_game`, `temperature`, `max_tokens`, `batch_size`, `max_retries`, `prompt_template`, `show_prompt`
Glossary: `glossary_game`, `glossary_src`, `glossary_tgt`, `glossary_min`, `glossary_folder`, `glossary_mod_game`, `glossary_mod_tgt`, `glossary_mod_min`, `glossary_mod_folder`, `glossary_mod_name`

## Expected Workflows
1. Browse Input → mod root → auto-detects `localisation/english/` → Output = `localisation/korean/`
2. Translate → files go to `korean/` folder
3. Validate tab → Load Files → review, edit, retry → Save Changes
4. Double-click any cell → popup editor for full text view/edit/retry
