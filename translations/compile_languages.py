"""This module is used to compile the .po file into the .mo file that is needed for the internationalization"""
import polib

po = polib.pofile("translations/de/LC_MESSAGES/de.po")
po.save_as_mofile("translations/de/LC_MESSAGES/de.mo")

print("Compiled SBAid.po -> SBAid.mo")