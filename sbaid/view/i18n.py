"""
This module contains methods for the internationalization
(translation between languages) of the SBAid Program.
"""
import gettext
import os
from typing import Callable
from gi.repository import Gio, GObject

class LanguageWrapper(GObject.GObject):
    language: str = GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT)

    def __init__(self, language: str):
        super().__init__(language=language)

def get_available_languages() -> Gio.ListModel:
    """todo"""
    available_languages = Gio.ListStore.new(LanguageWrapper)
    available_languages.append(LanguageWrapper("en")) # add default language code

    # add languages that have translation files
    for directory in os.listdir("../translations"):
        if not directory.__contains__("."):
            available_languages.append(LanguageWrapper(directory))

    return available_languages

def get_language_translator(language_code: str) -> Callable[[str], str]:
    lang = gettext.translation(language_code,
                               localedir="../translations",
                               languages=["en", "de"],
                               fallback=True)
    return lang.gettext


