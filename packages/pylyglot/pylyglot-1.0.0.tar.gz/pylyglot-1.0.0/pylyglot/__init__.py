import json
import locale
from pathlib import Path
from typing import Dict, Any, Optional, Set, List, Callable
import warnings
import threading

class PyLyglot:
    _instance = None
    _translations_cache: Dict[str, Dict[str, str]] = {}
    _supported_languages: Set[str] = set()
    _lock = threading.Lock()

    def __new__(cls, lang: Optional[str] = None, missing_key_handler: Optional[Callable[[str], str]] = None, lang_dir: Optional[Path] = None):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, lang: Optional[str] = None, missing_key_handler: Optional[Callable[[str], str]] = None, lang_dir: Optional[Path] = None):
        """
        Initialize the PyLyglot instance.

        Args:
            lang (Optional[str]): The language code to set initially.
            missing_key_handler (Optional[Callable[[str], str]]): A function to handle missing translation keys.
        """
        if not hasattr(self, '_initialized'):
            self._lang_dir = lang_dir or Path.cwd() / "lang"
            self._check_default_language_file()
            self._default_language = "en"
            self._current_language: Optional[str] = None
            self._missing_key_handler = missing_key_handler
            self._fallback_chain: List[str] = []
            self._initialized = True
            self._metadata_cache: Dict[str, Any] = {}
            self.set_language(lang or self.detect_language())

    def _check_default_language_file(self):
        """
        Check if the default language file exists.

        Raises:
            FileNotFoundError: If the default language file is missing.
        """
        en_path = self._lang_dir / "en.json"
        if not en_path.exists():
            raise FileNotFoundError(f"The default language file '{en_path}' is missing.")

    @classmethod
    def get_instance(cls):
        """
        Return the singleton instance of PyLyglot.

        Returns:
            PyLyglot: The singleton instance.
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def detect_language(self) -> str:
        """
        Detect the system language.

        Returns:
            str: The detected language code.
        """
        try:
            system_lang = locale.getlocale()[0]
            if system_lang:
                lang_code = system_lang.split('_')[0].lower()
                if self._is_language_supported(lang_code):
                    return lang_code

            import os
            for env_var in ['LANG', 'LANGUAGE', 'LC_ALL', 'LC_MESSAGES']:
                if env_var in os.environ:
                    lang_code = os.environ[env_var].split(':')[0].split('_')[0].lower()
                    if self._is_language_supported(lang_code):
                        return lang_code
        except Exception as e:
            warnings.warn(f"Language detection failed: {str(e)}", RuntimeWarning)

        return self._default_language

    def _is_language_supported(self, lang_code: str) -> bool:
        """
        Check if a language is supported.

        Args:
            lang_code (str): The language code to check.

        Returns:
            bool: True if the language is supported, False otherwise.
        """
        if not self._supported_languages:
            self._discover_supported_languages()
        return lang_code in self._supported_languages

    def _discover_supported_languages(self):
        """
        Discover available languages in the lang/ directory.

        Raises:
            FileNotFoundError: If the language directory is not found.
        """
        self._supported_languages = set()
        if not self._lang_dir.exists():
            raise FileNotFoundError(f"Language directory '{self._lang_dir}' not found")

        for file in self._lang_dir.glob("*.json"):
            lang_code = file.stem.lower()
            self._supported_languages.add(lang_code)

    def set_language(self, lang: str):
        """
        Set the current language with fallback handling.

        Args:
            lang (str): The language code to set.
        """
        lang = lang.lower()
        if lang == self._current_language:
            return

        if not self._is_language_supported(lang):
            if '-' in lang:
                main_lang = lang.split('-')[0]
                if self._is_language_supported(main_lang):
                    lang = main_lang
                else:
                    warnings.warn(
                        f"Language '{lang}' not supported. Falling back to '{self._default_language}'",
                        RuntimeWarning
                    )
                    lang = self._default_language
            else:
                warnings.warn(
                    f"Language '{lang}' not supported. Falling back to '{self._default_language}'",
                    RuntimeWarning
                )
                lang = self._default_language

        self._current_language = lang
        self._build_fallback_chain(lang)

        self._load_language(lang)
        for fallback_lang in self._fallback_chain:
            if fallback_lang != lang:
                self._load_language(fallback_lang)

    def _build_fallback_chain(self, lang: str):
        """
        Build the fallback chain for a given language.

        Args:
            lang (str): The language code to build the fallback chain for.
        """
        self._fallback_chain = [lang]

        parts = lang.split('-')
        if len(parts) > 1:
            main_lang = parts[0]
            if main_lang != lang:
                self._fallback_chain.append(main_lang)

        if self._default_language not in self._fallback_chain:
            self._fallback_chain.append(self._default_language)

    def _load_language(self, lang: str) -> bool:
        """
        Load a language into the cache if it is not already there.

        Args:
            lang (str): The language code to load.

        Returns:
            bool: True if the language was loaded successfully, False otherwise.
        """
        if lang in self._translations_cache:
            return True

        lang_file = self._lang_dir / f"{lang}.json"
        try:
            with open(lang_file, 'r', encoding='utf-8') as f:
                translations = json.load(f)
                self._validate_translations(translations, lang)
                metadata = translations.pop("_meta", {})
                self._translations_cache[lang] = translations
                self._metadata_cache[lang] = metadata
                return True
        except Exception as e:
            warnings.warn(f"Failed to load language '{lang}': {str(e)}", RuntimeWarning)
            return False

    def _validate_translations(self, data: dict, lang: str):
        """
        Validate the structure of the translation data.

        Args:
            data (dict): The translation data to validate.
            lang (str): The language code associated with the data.

        Raises:
            ValueError: If the translation data is not valid.
        """
        if not isinstance(data, dict):
            raise ValueError(f"Translation file for '{lang}' must be a dictionary")

        def _check_dict(d):
            if not isinstance(d, dict):
                raise ValueError(f"Invalid structure in translation file '{lang}': expected dict, got {type(d)}")

            for key, value in d.items():
                if not isinstance(key, str):
                    raise ValueError(f"Invalid key '{key}' in '{lang}': keys must be strings")

                if isinstance(value, dict):
                    _check_dict(value)
                elif not isinstance(value, str):
                    raise ValueError(f"Invalid value for key '{key}' in '{lang}': expected str, got {type(value)}")

        _check_dict(data)

    def _get_nested_key(self, data: Dict[str, Any], dotted_key: str) -> Optional[str]:
        """
        Get a nested key from a dictionary using a dotted key notation.

        Args:
            data (Dict[str, Any]): The dictionary to search in.
            dotted_key (str): The dotted key notation to search for.

        Returns:
            Optional[str]: The value associated with the key, or None if the key is not found.
        """
        keys = dotted_key.split(".")
        current = data
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return None
        return current if isinstance(current, str) else None

    def __call__(self, key: str, **kwargs: Any) -> str:
        """
        Translate a key with optional formatting, including hierarchical keys.

        Args:
            key (str): The key to translate.
            **kwargs (Any): Optional formatting arguments.

        Returns:
            str: The translated string.
        """
        if not key:
            return ""

        for lang in self._fallback_chain:
            if lang in self._translations_cache:
                raw = self._get_nested_key(self._translations_cache[lang], key)
                if raw is not None:
                    try:
                        return raw.format(**kwargs)
                    except (KeyError, ValueError) as e:
                        warnings.warn(
                            f"Format error in key '{key}' for language '{lang}': {str(e)}",
                            RuntimeWarning
                        )
                        return raw

        if self._missing_key_handler:
            return self._missing_key_handler(key)
        return f"[Missing translation: {key}]"

    def get_available_languages(self) -> Set[str]:
        """
        Return the set of supported languages.

        Returns:
            Set[str]: A set of supported language codes.
        """
        if not self._supported_languages:
            self._discover_supported_languages()
        return self._supported_languages.copy()

    @property
    def current_language(self) -> str:
        """
        Return the current language.

        Returns:
            str: The current language code.
        """
        return self._current_language or self._default_language

    def clear_cache(self):
        """
        Clear the translations cache.
        """
        self._translations_cache.clear()
        self._metadata_cache.clear()

    def get_metadata(self, lang: str) -> dict:
        """
        Return metadata for a specific language.

        Args:
            lang (str): The language code to get metadata for.

        Returns:
            dict: The metadata associated with the language.
        """
        return self._metadata_cache.get(lang, {})

if __name__ == "__main__":
    def my_missing_key_handler(key):
        return f"<<{key}>>"

    pl = PyLyglot(missing_key_handler=my_missing_key_handler)

    print(pl("menu.start"))  # "Start"
    print(pl("menu.quit"))  # "Quit"
    print(pl("welcome", username="Bob"))  # "Welcome, Bob!"

    print("Available languages:", pl.get_available_languages())

    print(pl.get_metadata("en"))
