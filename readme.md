<div align="center">
  <img src="https://img.shields.io/badge/AURA-AGI-red?style=for-the-badge&logo=huggingface" alt="AURA AGI Badge">

  <p>
    <a href="https://github.com/ShreyasP10/AURA-AGI/stargazers">
      <img alt="GitHub stars" src="https://img.shields.io/github/stars/ShreyasP10/AURA-AGI?style=social">
    </a>
    <a href="https://github.com/ShreyasP10/AURA-AGI/network/members">
      <img alt="GitHub forks" src="https://img.shields.io/github/forks/ShreyasP10/AURA-AGI?style=social">
    </a>
    <a href="https://github.com/ShreyasP10/AURA-AGI/issues">
      <img alt="GitHub issues" src="https://img.shields.io/github/issues/ShreyasP10/AURA-AGI?style=social">
    </a>
  </p>
</div>

<div align="center">
  <a href="https://youtube.com/@AURA-Team"><img alt="YouTube" src="https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white"></a>
  <a href="https://t.me/AURA-Team"><img alt="Telegram" src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white"></a>
  <a href="https://www.instagram.com/Shreyas.shades_/"><img alt="Instagram" src="https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white"></a>
  <a href="https://www.linkedin.com/in/developer-Shreyas/"><img alt="LinkedIn" src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a>
  <a href="https://patreon.com/AURA-Team"><img alt="Support on Patreon" src="https://img.shields.io/badge/Patreon-FF424D?style=for-the-badge&logo=patreon&logoColor=white"></a>
  <a href="https://buymeacoffee.com/AURA-Team"><img alt="Buy Me A Coffee" src="https://img.shields.io/badge/Buy%20Me%20A%20Coffee-FFDD00?style=for-the-badge&logo=buymeacoffee&logoColor=black"></a>
</div>

<div align="center">
  <h1>🛑 Follow This Series Live: <a href="https://www.youtube.com/playlist?list=PLcb7hDy97wSJ0MRX_cKufrKDUuET1K-5d">AURA 2.0 Series</a></h1>
</div>

---

# AURA-AGI

## Project Overview

AURA-AGI is an advanced AI project designed to integrate multiple AI capabilities, including speech recognition, text processing, and image analysis, into a cohesive system. Named after the iconic AI assistant from popular culture, AURA is built with cutting-edge natural language processing capabilities, allowing users to interact with it through voice commands. Whether it's checking the weather, setting reminders, managing calendars, or searching the web, AURA is equipped to handle a wide range of tasks efficiently and effectively. With its intuitive interface and robust functionality, AURA aims to revolutionize the way users engage with technology, making everyday tasks simpler and more convenient.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Directory Structure](#directory-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Connect with Us](#connect-with-us)

## Features

- **Speech Recognition**: Convert spoken language into text using various models.
- **Text Processing**: Analyze and generate text with multiple AI tools.
- **Image Analysis**: Perform image recognition and processing tasks.
- **Audio Tools**: Detect hotwords and manage audio playback interruptions.
- **Interactive Prompts**: Predefined prompts to guide AI interactions.

## Directory Structure

The project is organized into several key directories:

```
AURA-AGI/
├── .env
├── .env.example
├── .gitattributes
├── .gitignore
├── ASSETS/
│   ├── CLAP_DETECTS/
│   │   └── MODELS/
│   │       └── Model.txt
│   ├── SOUNDS/
│   │   ├── activation_sound.wav
│   │   ├── audio_file.mp3
│   │   └── deactivation_sound.wav
│   ├── STREAM_AUDIOS/
│   │   ├── output_audio_6.mp3
│   │   ├── output_audio_7.mp3
│   │   ├── output_audio_8.mp3
│   │   ├── output_audio_9.mp3
│   │   ├── output_audio_10.mp3
│   │   ├── output_audio_11.mp3
│   │   ├── output_audio_12.mp3
│   │   ├── output_audio_13.mp3
│   │   ├── output_audio_14.mp3
│   │   ├── output_audio_15.mp3
│   │   ├── output_audio_16.mp3
│   │   ├── output_audio_17.mp3
│   │   ├── output_audio_18.mp3
│   │   ├── output_audio_19.mp3
│   │   └── output_audio_20.mp3
│   ├── USERDATA/
│   │   └── LE CHAT/
│   │       └── How_To_Store_UserData.txt
│   ├── Vosk/
│   ├── available_working_proxies.txt
│   ├── conversation_history.json
│   └── openGPT_IDs.txt
├── BRAIN/
│   ├── AI/
│   │   ├── IMAGE/
│   │   │   ├── decohere_ai.py
│   │   │   └── deepInfra_IMG.py
│   │   ├── TEXT/
│   │   │   ├── API/
│   │   │   │   ├── Blackbox_ai.py
│   │   │   │   ├── Bnn_GPT.py
│   │   │   │   ├── FarFalle.py
│   │   │   │   ├── Hugging_Face_TEXT.py
│   │   │   │   ├── Le_Chat.py
│   │   │   │   ├── Phind.py
│   │   │   │   ├── Pi_Ai.py
│   │   │   │   ├── Uncensored.py
│   │   │   │   ├── basedGPT.py
│   │   │   │   ├── deepInfra_TEXT.py
│   │   │   │   ├── deepseek_ai.py
│   │   │   │   ├── hugging_chat.py
│   │   │   │   ├── liaobots.py
│   │   │   │   ├── openGPT.py
│   │   │   │   └── openrouter.py
│   │   │   ├── LOCAL/
│   │   │   │   └── llama_CPP.py
│   │   │   └── STREAM/
│   │   │       ├── basedGPT.py
│   │   │       └── deepInfra_TEXT.py
│   │   └── VISION/
│   │       └── deepInfra_VISION.py
│   └── TOOLS/
│       └── groq_web_access.py
├── ENGINE/
│   ├── STT/
│   │   ├── AURA-Team.py
│   │   ├── NetHyTech.py
│   │   ├── src/
│   │   │   └── index.html
│   │   └── vosk_recog.py
│   └── TTS/
│       ├── STREAMING/
│       │   ├── DeepGram.py
│       │   └── speechify.py
│       ├── DeepGram.py
│       ├── ElevenLabs.py
│       ├── ai_voice.py
│       ├── deepAI.py
│       ├── edge_tts.py
│       ├── hearling.py
│       ├── speechify.py
│       └── stream_elements_api.py
├── PLAYGROUND/
│   ├── ADB_CALL/
│   │   ├── ADB COMMANDS.txt
│   │   ├── Details.txt
│   │   ├── IMP Commands.txt
│   │   ├── Information.txt
│   │   ├── android_device_connection_setup.py
│   │   └── make_call.py
│   ├── CAMERA/
│   │   └── camera_vision.py
│   ├── CLAP_NN/
│   │   ├── DATASETS/
│   │   │   └── Informtation.txt
│   │   ├── ClapDetector.py
│   │   ├── Model_Trainer.py
│   │   ├── audio_inference.py
│   │   ├── cnn_sound_model.py
│   │   └── load_dataset.py
│   └── WEBSITE_ASSISTANT/
│       ├── chrome_latest_url.py
│       └── jenna_reader.py
├── PROMPTS/
│   ├── BISECTORS.py
│   ├── INSTRUCTIONS.py
│   ├── PROMPTS.py
│   └── SYSTEM.py
├── TOOLS/
│   ├── AUDIO/
│   │   ├── Hotword_Detection.py
│   │   └── Interrupted_Playsound.py
│   ├── LE_CHAT_COOKIES/
│   │   └── Cookie_Extractor.py
│   ├── SYSTEM_SETTINGS/
│   │   ├── SETTING.py
│   │   ├── system_theme.py
│   │   └── taskbar.py
│   ├── Alpaca_DS_Converser.py
│   ├── ProxyAPI.py
│   ├── RawDog.py
│   ├── TXT_DS_Converser.py
│   ├── Web_Results.py
│   └── stream_audio_cleanup.py
├── CODE_OF_CONDUCT.md
├── IMPORTS.py
├── LICENCE
├── Le_Chat_Tester.py
├── Memory ConvoTxt.py
├── SpeedTester.py
├── StreamSpeak.py
├── WebTester.py
├── main.py
├── readme.md
└── requirements.txt
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ShreyasP10/AURA-AGI.git
   cd AURA-AGI
   ```

2. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

3. **(Optional) Install Vosk Speech Recognition Models**:

   Vosk provides pre-trained models for various languages. To install the models for your desired language, follow these steps:

   - Go to the Vosk GitHub repository releases page: [Vosk GitHub Releases](https://github.com/alphacep/vosk-api/releases)
   - Download the model folder for your language. For example, if you want English models, download the folder named `vosk-model-en-us-aspire-0.2`.
   - Extract the contents of the folder into a directory named `ASSETS` in your project directory.
   - Ensure that the extracted model folder is directly under the `ASSETS` directory, without any additional nesting.
   - Now, you should have a structure like this: `<your-main-project-directory>/ASSETS/vosk-model-en-us-aspire-0.2`.
   - Modify the `main.py` or any relevant script to point to the model directory. For example:
     ```python
     from ENGINE.STT.vosk_recog import speech_to_text

     for speech in speech_to_text(model_path="ASSETS/Vosk/vosk-model-small-en-us-0.15"):
         if speech != "":
             print("Human >>", speech)
     ```  

## Usage

1. **Run the main script**:
   ```bash
   python main.py
   ```

2. **Configuration**: Modify API configuration

 in the `.env` directory to suit your needs.

## Contributing

We welcome contributions to improve AURA-AGI. To contribute, follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/ShreyasP10/AURA-AGI/blob/main/LICENCE) file for details.

## Connect with Us

Made With 💓 By - Shreyas Pawar (AURA-AGI)

For any questions or concerns, reach out to us via our social media handles. Our top choice for contact is Telegram: [AURA Team Telegram](https://t.me/AURA-Team)

- YouTube Channel: [AURA Team](https://www.youtube.com/@AURA-Team)
- Telegram Group: [AURA Team Telegram](https://t.me/AURA-Team)
- Discord Server: [AURA Team Discord](https://discord.gg/ehwfVtsAts)
- Instagram:
  - Personal: [Shreyas](https://www.instagram.com/Shreyas.shades_/)
  - Channel: [AURA Team](https://www.instagram.com/AURA-Team_/)

---

## AURA Team

Dive into the world of coding with AURA Team - where passion meets programming! Make sure to hit that Subscribe button to stay tuned for exciting content!

Pro Tip: For optimal performance and a seamless experience, we recommend using the default library versions demonstrated in this demo. Your coding journey just got even better! Happy coding!

---

Now you're all set to explore the AURA Team's project! Enjoy coding!

<div align="center">
  <a href="https://youtube.com/@AURA-Team"><img alt="YouTube" src="https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white"></a>
  <a href="https://t.me/AURA-Team"><img alt="Telegram" src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white"></a>
  <a href="https://www.instagram.com/Shreyas.shades_/"><img alt="Instagram" src="https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white"></a>
  <a href="https://www.linkedin.com/in/developer-Shreyas/"><img alt="LinkedIn" src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a>
  <a href="https://patreon.com/AURA-Team"><img alt="Support on Patreon" src="https://img.shields.io/badge/Patreon-FF424D?style=for-the-badge&logo=patreon&logoColor=white"></a>
  <a href="https://buymeacoffee.com/AURA-Team"><img alt="Buy Me A Coffee" src="https://img.shields.io/badge/Buy%20Me%20A%20Coffee-FFDD00?style=for-the-badge&logo=buymeacoffee&logoColor=black"></a>
</div>


