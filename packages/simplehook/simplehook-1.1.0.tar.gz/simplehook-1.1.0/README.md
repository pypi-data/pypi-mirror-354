# SimpleHook

**SimpleHook** is a minimalistic Python wrapper for Discord webhooks. It allows you to easily send messages, files, and embedded images to a Discord channel using just a few lines of code.

![PyPI](https://img.shields.io/pypi/v/simplehook) ![Python](https://img.shields.io/pypi/pyversions/simplehook) ![License](https://img.shields.io/github/license/jstiin/simplehook)

## 🔧 Features

- Send plain text messages
- Customize username and avatar
- Mention users or everyone/here
- Upload files and images
- Embed multiple images (up to 10)

## 🚀 Usage

```python
from simplehook import SimpleHook

# Initialize with your webhook URL
hook = SimpleHook("https://discord.com/api/webhooks/your_webhook_url")

# Send a simple message
hook.send_message("Hello, world!")

# Send a message with a custom username and avatar
hook.send_customized_message(
    message="I'm a bot!",
    username="CoolBot",
    avatar_url="https://i.imgur.com/your_avatar.png"
)

# Mention a user by ID or everyone/here
hook.send_customized_message("Look here!", mention="123456789012345678")  # user mention
hook.send_customized_message("Attention!", mention="everyone")  # @everyone

# Send a file
hook.send_file("example.txt")

# Send embedded images (max 10)
hook.send_embedded_images(["img1.png", "img2.jpg"], message="Check these out!")
```
## 📦 Installation

```bash
pip install simplehook
```

