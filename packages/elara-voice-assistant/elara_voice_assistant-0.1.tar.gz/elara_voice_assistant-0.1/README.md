# 🎙️ ELARA – Voice Assistant - GUI - Python

ELARA is a modern Python-based voice assistant with a sleek graphical interface. It supports voice commands such as playing music, telling time, searching Wikipedia, and cracking jokes — all with spoken responses and intuitive GUI interactions.

![alt text](image.png)
---


## ✨ Features

- 🎧 Voice command recognition via microphone  
- 🗣️ Speech responses using text-to-speech  
- ⏰ Tells you the current time  
- 🎵 Plays YouTube videos by voice command  
- 📚 Answers factual questions using Wikipedia  
- 😂 Tells jokes with `pyjokes`  
- 🖥️ Stylish and responsive tkinter-based GUI  
- 👥 User role selector (Admin / User / Guest)

---

## 🛠️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/iamafridi/Elara-virtual-assistant-GUI.git
cd Elara-virtual-assistant-GUI
```


### 2. Install dependencies
```bash
pip install -r requirements.txt
```

> 💡 If you encounter issues with `pyaudio`, try:
> - Windows: `pip install pipwin` then `pipwin install pyaudio`
> - macOS/Linux: Ensure PortAudio is installed via `brew` or `apt`

---

## 🚀 Usage

### Option 1: Run with GUI (Recommended)
```bash
python gui_main.py
```

### Option 2: Run in terminal (headless mode)
```bash
python main.py
```

---

## 🎤 How to Use

1. Say **"Elara"** followed by a command.
2. Try things like:
   - `Elara play Shape of You`
   - `Elara what time is it?`
   - `Elara tell me about Python`
   - `Elara tell me a joke`
3. Use the GUI to:
   - View conversations
   - Select user roles
   - Start or stop listening
   - Clear the chat history

---

## 📁 File Structure

```
elara-voice-assistant/
├── gui_main.py       # Modern GUI version of Elara
├── main.py           # Command-line based Elara
├── requirements.txt  # List of Python packages
└── README.md         # Project documentation
```

---

## 📦 Requirements

- Python 3.8 or higher
- Dependencies in `requirements.txt`:
  - `pyttsx3`
  - `SpeechRecognition`
  - `pywhatkit`
  - `wikipedia`
  - `pyjokes`
  - `pyaudio` (requires PortAudio)

Install them with:
```bash
pip install -r requirements.txt
```

---

## 🧠 Inspiration

This project was built to mimic essential features of commercial voice assistants like Alexa or Siri, but entirely using open-source Python libraries, offering both flexibility and educational value.

---

## 🪪 License

This project is licensed under the **MIT License**. You are free to use, modify, and distribute it with proper attribution.

---

## 🙌 Acknowledgments

Thanks to the open-source community and the developers behind the libraries used:
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
- [pyttsx3](https://pypi.org/project/pyttsx3/)
- [pywhatkit](https://pypi.org/project/pywhatkit/)
- [wikipedia](https://pypi.org/project/wikipedia/)
- [pyjokes](https://pypi.org/project/pyjokes/)