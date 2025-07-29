import json
import requests
import os
from typing import Optional


class SimpleHook:

    """
    A minimalistic class to send messages, files, and images using Discord Webhooks.
    """

    webhook_url: str

    def __init__(self, webhook_url: str) -> None:
        """
        Initialize the webhook client.

        Args:
            webhook_url (str): The Discord webhook URL to send messages to.
        """

        self.webhook_url = webhook_url

    def __post(self, **kwargs) -> None:
        r = requests.post(url=self.webhook_url, **kwargs)
        r.raise_for_status()

    def send_message(self, message: str) -> None:
        """
        Send a basic text message to the Discord webhook.

        Args:
            message (str): The plain text message to send.
        """

        body = {
            "content": message
        }

        self.__post(json=body)

    def send_customized_message(
        self,
        message: str,
        username: Optional[str] = None,
        avatar_url: Optional[str] = None,
        mention: Optional[str] = None
    ) -> None:
        """
        Send a customized message with optional username, avatar, and a user mention.

        Args:
            message (str): The message content.
            username (Optional[str]): A custom username to display instead of the webhook default.
            avatar_url (Optional[str]): A URL to a custom avatar image.
            user_mention (Optional[str]): The ID of the user to mention in the message.
        """

        body: dict = {
            "content": message,
        }

        if username:
            body['username'] = username

        if avatar_url:
            body['avatar_url'] = avatar_url

        if mention:
            body['content'] = f"<@{mention}> {message}"

            if mention == "everyone" or mention == "here":
                body['content'] = f"@{mention} {message}"

        self.__post(json=body)

    def send_file(self, image_path: str) -> None:
        """
        Send a single file to the Discord webhook.

        Args:
            image_path (str): The local path to the file.
        """

        with open(image_path, "rb") as f:
            file = f.read()
            filename = os.path.basename(image_path)

        file_body: dict = {
            filename: file
        }

        self.__post(files=file_body)

    def send_embedded_images(self, paths: list[str], message: Optional[str] = None) -> None:
        """
        Send multiple files as embedded content in a Discord message.

        Args:
            paths (list[str]): A list of local file paths to files (10 max.).
            message (Optional[str]): Optional text content to include alongside the embeds.
        """
        
        if len(paths) > 10:
            raise ValueError("Cannot send more than 10 images")

        embeds: list = []
        files: list = []

        for index, path in enumerate(paths):
            with open(path, "rb") as f:
                file = f.read()
                filename = os.path.basename(path)
                files.append((f"files[{index}]", (filename, file)))
                embeds.append({
                    "image": {"url": f"attachment://"+filename}
                })

        payload = {
            "content": message or "",
            "embeds": embeds
        }

        self.__post(data={"payload_json": json.dumps(payload)}, files=files)
