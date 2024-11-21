# MooJam Bot 🎵

MooJam is a Telegram bot that helps you search for songs on YouTube, download them, and send the audio files directly to your Telegram chat. It's the perfect tool to create your own music library right within Telegram.

## Features
- 🌐 **Search on YouTube**: Look for any song available on YouTube.
- 🎵 **Download Songs**: Fetch the audio file from YouTube.
- 📩 **Direct Delivery**: Receive the downloaded audio in your Telegram chat for offline listening.

---

## Telegram Bot Link
Start using MooJam by clicking here: [MooJam Bot](https://t.me/MooJamBot)  

---

## How to Run the Bot

### Prerequisites
- Python 3.8 or higher
- A valid Telegram bot token (from [BotFather](https://t.me/botfather))
- A valid Youtube Data api bot token (from [Google Cloud Console](https://console.cloud.google.com/))

### Steps to Run
1. **Clone the Repository**  
   ```bash
   git clone https://github.com/your-username/moojam-bot.git
   cd moojam-bot
   ```

2. **Set Up a Virtual Environment** (optional but recommended)
    ```bash
    python -m venv venv
    ```

3. **Create the .env file in the root like this**
    ```bash
    TOKEN=<BotToken>
    Yt_API=<Youtube API Token>
    ```

4. **Install Dependencies and run**
    ```bash
    pip install -r requirements.txt
    python main.py
    ```

Happy Listening! 🎧