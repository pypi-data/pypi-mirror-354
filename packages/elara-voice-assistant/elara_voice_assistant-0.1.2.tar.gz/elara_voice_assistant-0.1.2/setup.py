from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="elara-voice-assistant",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "pyttsx3", "speechrecognition", "pywhatkit", "wikipedia", "pyjokes"
    ],
    entry_points={
        "console_scripts": [
            "elara=main:run_elara"
        ]
    },
    author="Afridi Akbar Ifty",
    description="A Python voice assistant with GUI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iamafridi/elara",
)
