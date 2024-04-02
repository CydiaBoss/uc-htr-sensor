import subprocess

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
    LANG["zh_CN"] = _translate("Language", "Mandarin (Simplified)")
    LANG["zh_TW"] = _translate("Language", "Mandarin (Traditional)")

# Files with translations
FILES = [
    "misc/lang.py",
    "main_gui.py",
    "main.py"
]

def generate_ts():
    """
    Generates the TS files
    """
    retranslate_lang()

    # Command creation
    cmd = "pylupdate5 "
    cmd += " ".join(FILES)

    # TS generation
    cmd += " -ts"

    for code in LANG.keys():
        cmd += f" lang/{code}.ts"

    subprocess.run(cmd.split(" "))

if __name__ == "__main__":
    generate_ts()