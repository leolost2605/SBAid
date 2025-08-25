"""
This module contains methods for the internationalization
(translation between languages) of the SBAid Program.
"""
import gettext
import os
from typing import Callable
from gi.repository import Gio, GObject

def get_translator(language_code: str) -> Callable[[str], str]:

    return gettext.translation(language_code,
                            localedir="../translations",
                            languages=["en", "de"],
                            fallback=True).gettext

class LanguageWrapper(GObject.GObject):
    """This class is a wrapper class for the languages"""
    language_code: str = GObject.Property(  # type: ignore
        type=str,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT)

    translator: Callable[[str], str]

    def __init__(self, language: str):
        super().__init__(language_code=language)
        self.translator = gettext.translation(language,
                                         localedir="../translations",
                                         languages=["en", "de"],
                                         fallback=True).gettext


def get_available_languages() -> Gio.ListModel:
    """Returns a list of available languages by reading what is present in the translation files.
    Returns ListModel containing the LanguageWrapper class."""
    available_languages = Gio.ListStore.new(LanguageWrapper)
    available_languages.append(LanguageWrapper("en"))  # add default language code

    # add languages that have translation files
    for directory in os.listdir("../translations"):
        if "." not in directory:
            available_languages.append(LanguageWrapper(directory))
    return available_languages
