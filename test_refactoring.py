"""Logic test for refactored ollama_translator package files."""
import os, sys, json, re, threading, tempfile

# ── 1. utils.py ──
print("=== utils.py ===")
from ollama_translator.utils import (
    _PREFIX_TO_LANG, PLATFORM_PATTERNS,
    _glossary_dir, load_stopwords, stem_en,
    tokenize_en, tokenize_tgt, tokenize_game_en,
    tokenize_tgt_pure, parse_yml,
    OllamaTranslator  # for _LANG_CODE
)

# _PREFIX_TO_LANG
assert "l_korean" in _PREFIX_TO_LANG, "Missing l_korean"
assert _PREFIX_TO_LANG["l_korean"] == "Korean"
assert _PREFIX_TO_LANG["l_english"] == "English"
assert len(_PREFIX_TO_LANG) == len(OllamaTranslator._LANG_CODE)
print("  _PREFIX_TO_LANG: %d mappings OK" % len(_PREFIX_TO_LANG))

# PLATFORM_PATTERNS
assert len(PLATFORM_PATTERNS) == 3
print("  PLATFORM_PATTERNS: 3 patterns OK")

# _glossary_dir
gdir = _glossary_dir()
assert isinstance(gdir, str)
print("  _glossary_dir():", repr(gdir))

# load_stopwords
sw_en = load_stopwords("l_english")
assert isinstance(sw_en, set)
print("  load_stopwords(l_english): %d stopwords" % len(sw_en))

# stem_en
print("  stem_en examples: running->%s, happiness->%s, dogs->%s" % (stem_en("running"), stem_en("happiness"), stem_en("dogs")))
assert isinstance(stem_en("running"), str)
assert len(stem_en("running")) >= 2
print("  stem_en: OK")

# tokenize_en
assert tokenize_en("Hello World") == ["hello", "world"]
print("  tokenize_en: OK")

# tokenize_tgt
tokens = tokenize_tgt("\uc548\ub155\ud558\uc138\uc694 \uc138\uacc4")
assert isinstance(tokens, list)
print("  tokenize_tgt: OK")

# parse_yml (takes string content, not file path)
result = parse_yml('NDef0:0 "Test"\nNTest1:1 "Value"\n')
assert result == {"ndef0": "Test", "ntest1": "Value"}, "Got %r" % result
print("  parse_yml: OK")

# tokenize_game_en
gt = tokenize_game_en("hello_world test-value")
assert "hello" in gt and "world" in gt
print("  tokenize_game_en: OK (%d tokens)" % len(gt))

# tokenize_tgt_pure
pure = tokenize_tgt_pure("\uc548\ub155\ud558\uc138\uc694")
assert isinstance(pure, list)
print("  tokenize_tgt_pure: OK")

print("\u2713 utils.py all tests passed\n")


# ── 2. engine.py ──
print("=== engine.py ===")
from ollama_translator.engine import OllamaTranslator as Engine

# _LANG_CODE
assert len(Engine._LANG_CODE) == 10
assert Engine._LANG_CODE["Korean"] == "korean"
assert Engine._LANG_CODE["English"] == "english"
print("  _LANG_CODE: %d language codes OK" % len(Engine._LANG_CODE))

# _glossary_dir (static)
gdir2 = Engine._glossary_dir()
assert isinstance(gdir2, str)
print("  _glossary_dir static: OK")

# _strip_codes (static)
assert Engine._strip_codes("hello [brackets] $var$ world") == "hello   world"
print("  _strip_codes: OK")

# _find_duplicate_keys (static)
from io import StringIO
with tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False, encoding="utf-8") as f:
    f.write("key1: val1\nkey2: val2\nkey1: val3\n")
    dup_path = f.name
dupes = Engine._find_duplicate_keys(dup_path)
assert "key1" in dupes
os.unlink(dup_path)
print("  _find_duplicate_keys: OK (%d dupes)" % len(dupes))

# check_quality (instance method, no Ollama needed)
engine_inst = Engine(
    log_callback=lambda m: None,
    progress_callback=lambda c, t: None,
    status_callback=lambda s: None,
    live_callback=None
)
engine_inst.stop_event.clear()
with tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False, encoding="utf-8") as f:
    f.write('key1: "hello"\n')
    src = f.name
with tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False, encoding="utf-8") as f:
    f.write('key1: "hola"\n')
    tgt = f.name
issues = engine_inst.check_quality(src, tgt)
assert isinstance(issues, list)
os.unlink(src); os.unlink(tgt)
print("  check_quality: OK (%d issues)" % len(issues))

# _has_foreign_chars (instance)
assert not engine_inst._has_foreign_chars("hello world", "English")
print("  _has_foreign_chars: OK")

# _translate_batch - skipping (requires LLM connection)
# Instead test simpler filtering logic by checking _get_glossary_text
glossary_text = engine_inst._get_glossary_text("English", "Korean", "None")
assert isinstance(glossary_text, str)
print("  _get_glossary_text: OK (got %d chars)" % len(glossary_text))

print("\u2713 engine.py all tests passed\n")


# ── 3. Import chain ──
print("=== Import chain ===")
from ollama_translator_app import OllamaTranslatorGUI
assert issubclass(OllamaTranslatorGUI, object)
print("  ollama_translator_app -> OllamaTranslatorGUI imported OK")
print("  MRO length:", len(OllamaTranslatorGUI.__mro__))

# Verify key mixin methods are reachable
mixin_methods = [
    "_g_browse", "_game_extract", "_game_validate",
    "_mod_extract", "_mod_translate", "_mod_save",
    "_m_prev_page", "_m_next_page"
]
for m in mixin_methods:
    assert hasattr(OllamaTranslatorGUI, m), "Missing %s" % m
print("  Mixin methods (%d): all reachable" % len(mixin_methods))

print("\u2713 Import chain OK\n")


print("=" * 40)
print("ALL TESTS PASSED")
print("=" * 40)
