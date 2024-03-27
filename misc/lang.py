from PyQt5.QtCore import QCoreApplication

_translate = QCoreApplication.translate

# Languages
LANG = {}

def retranslate_lang():
    """
    Initialize language dictionary
    """
    LANG.clear()
    LANG["en"] = _translate("Language", "English")
    LANG["fr"] = _translate("Language", "French")
    LANG["ko"] = _translate("Language", "Korean")