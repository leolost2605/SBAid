"""
This module contains methods for the internationalization
(translation between languages) of the SBAid Program.
"""
import gettext
from typing import Callable


class Internationalization:
    """This class keeps track of the active language"""
    _: Callable[[str], str]

    def __init__(self, default_lang: str):
        super().__init__()
        self._ = gettext.translation(default_lang,
                                     localedir="../translations",
                                     languages=[default_lang, "de"],
                                     fallback=True).gettext

    def set_active_language(self, language: str) -> None:
        """Sets the active language"""
        self._ = gettext.translation(language,
                                     localedir="../translations",
                                     languages=["en", "de"],
                                     fallback=True).gettext


# global singleton
i18n = Internationalization("en")

# def get_available_languages() -> Gio.ListModel:
#    """Returns a list of available languages by reading what is present in the translation files.
#    Returns ListModel containing the LanguageWrapper class."""
#    available_languages = Gio.ListStore.new(LanguageWrapper)
#    available_languages.append(LanguageWrapper("en"))  # add default language code

# add languages that have translation files
#    for directory in os.listdir("../translations"):
#        if "." not in directory:
#            available_languages.append(LanguageWrapper(directory))
#    return available_languages
