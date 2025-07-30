#
#   IMPORTS
#

# IMPORTS -> COMMON
import os


#
#   SETTINGS
#

SET = {
    "width": 64,
    "separator": "=",
    "indentation": 4,
    "palette": {
        "APP": "\x1b[36m",
        "DATA": "\x1b[33m",
        "INPUT": "\x1b[32m",
        "PROMPT": "\x1b[37m",
        "RESET": "\x1b[0m"
    }
}


#
#   HELPERS
#

# HELPERS -> SEPARATOR
def separator():
    return SET["separator"] * SET["width"]

# HELPERS -> INDENT
def indent():
    return " " * SET["indentation"]

# HELPERS -> RENDER
def render(content, style, end="\n"):
    print(SET["palette"][style] + content + SET["palette"][style] + SET["palette"]["RESET"], end=end)

# HELPERS -> ASK
def ask(content):
    input(SET["palette"]["PROMPT"] + content + SET["palette"]["INPUT"])
    print(SET["palette"]["RESET"])

# HELPERS -> HEADER
def header(title):
    render(separator(), "APP")
    render(indent() + title, "APP")
    render(separator(), "APP", end="\n\n")

# HELPERS -> BODY
def body(metalist):
    for item in metalist:
        if item[1] != "INPUT" and item[1] != "PROMPT":
            render(indent() + item[0], item[1], end="\n\n")
        else:
            ask(indent() + item[0])

# HELPERS -> CLEAR
def clear():
    os.system("cls")


#
#   MAIN
#

# MAIN -> FUNCTION
def main(title, metalist):
    clear()
    header(title)
    body(metalist)