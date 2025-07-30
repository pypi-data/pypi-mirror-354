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
def separator() -> str:
    return SET["separator"] * SET["width"]

# HELPERS -> INDENT
def indent() -> str:
    return " " * SET["indentation"]

# HELPERS -> RENDER
def render(content: str, style: str, end: str = "\n") -> None:
    print(SET["palette"][style] + content + SET["palette"][style] + SET["palette"]["RESET"], end=end)

# HELPERS -> ASK
def ask(content: str) -> str:
    answer = input(SET["palette"]["PROMPT"] + content + SET["palette"]["INPUT"])
    print(SET["palette"]["RESET"])
    return answer

# HELPERS -> HEADER
def header(title: str) -> None:
    render(separator(), "APP")
    render(indent() + title, "APP")
    render(separator(), "APP", end="\n\n")

# HELPERS -> BODY
def body(metalist: list) -> list:
    answers = []
    for item in metalist:
        if item[1] != "INPUT" and item[1] != "PROMPT":
            render(indent() + item[0], item[1], end="\n\n")
        else:
            answers.append(ask(indent() + item[0]))
    return answers

# HELPERS -> CLEAR
def clear() -> None:
    os.system("cls")


#
#   MAIN
#

# MAIN -> FUNCTION
def main(title: str, metalist: list) -> list:
    clear()
    header(title)
    return body(metalist)