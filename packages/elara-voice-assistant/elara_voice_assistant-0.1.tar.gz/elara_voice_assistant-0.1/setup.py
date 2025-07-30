from setuptools import setup, find_packages

setup(
    name="elara-voice-assistant",
    version="0.1",
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
    url="https://github.com/iamafridi/elara",
)
