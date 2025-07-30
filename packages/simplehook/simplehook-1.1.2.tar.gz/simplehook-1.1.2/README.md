# SimpleHook

**SimpleHook** is a minimalistic Python wrapper for Discord webhooks. It allows you to easily send messages, files, and embedded images to a Discord channel using just a few lines of code.

![PyPI](https://img.shields.io/pypi/v/simplehook) ![Python](https://img.shields.io/pypi/pyversions/simplehook) ![License](https://img.shields.io/github/license/jstiin/simplehook)

## 🔧 Features

- Send plain text messages
- Customize username and avatar
- Mention users or everyone/here
- Use Text-to-speech
- Upload files and images
- Embed multiple images (up to 10)
- Create and send polls

## 🚀 Usage

```python
from simplehook import SimpleHook

# Initialize with your webhook URL
hook = SimpleHook("https://discord.com/api/webhooks/your_webhook_url")

# Send a simple message
hook.send_message("Hello, world!")

# Send a message with a custom username,avatar and Text-to-speech
hook.send_customized_message(
    message="I'm a bot!",
    username="CoolBot",
    avatar_url="https://i.imgur.com/your_avatar.png",
    tts=True
)

# Mention a user by ID or everyone/here
hook.send_customized_message("Look here!", mention="123456789012345678")  # user mention
hook.send_customized_message("Attention!", mention="everyone")  # @everyone

# Send a file
hook.send_file("example.txt")

# Send embedded images (max 10)
hook.send_embedded_images(["img1.png", "img2.jpg"], message="Check these out!")

# Create and send a poll
hook.create_poll(
    question="What's your favorite color?",
    answers=["Blue", "Red", "Green"],
    emojis=["🔵", "🔴", "🟢"],
    duration=48,
    allow_multiselect=True
)
```

## 📦 Installation

```bash
pip install simplehook
```

