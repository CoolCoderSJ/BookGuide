from cx_Freeze import setup, Executable
import sys


executables = [Executable("main.py", base="Win32GUI", icon="static/images/logo.ico")]

packages = [
"idna",
"flask",
"os",
"sqlite3",
"werkzeug.utils",
"threading",
"PyQt5.QtCore",
"PyQt5.QtWebEngineWidgets",
"PyQt5.QtWidgets",
"sys",
"flask_mail",
"jinja2"
]

options = {
    'build_exe': {
        'packages': packages,
    },
}

setup(
    name = "BookGuide",
    options = options,
    version = "1.0.0",
    description = 'None',
    executables = executables
)
