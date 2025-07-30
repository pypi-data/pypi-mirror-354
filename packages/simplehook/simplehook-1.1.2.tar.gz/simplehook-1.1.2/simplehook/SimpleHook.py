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
        mention: Optional[str] = None,
        tts: Optional[bool] = None
    ) -> None:
        """
        Send a customized message with optional username, avatar, and a user mention.

        Args:
            message (str): The message content.
            username (Optional[str]): A custom username to display instead of the webhook default.
            avatar_url (Optional[str]): A URL to a custom avatar image.
            user_mention (Optional[str]): The ID of the user to mention in the message.
            tts (Optional[bool]): If True, the message will be read aloud using text-to-speech.
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
        
        if tts:
            body["tts"] = tts

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
            paths (list[str]): List of local file paths to send (maximum 10 files).
            message (Optional[str]): Optional text content to include with the embeds.

        Raises:
            ValueError: If more than 10 files are provided.
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

    def create_poll(
        self,
        question: str,
        answers: list,
        emojis: Optional[list] = None,
        duration: Optional[int] = None,
        allow_multiselect: Optional[bool] = None
    ) -> None:
        """
        Create and send a poll message.

        Args:
            question (str): The poll question, maximum 300 characters.
            answers (list[str]): List of answer options, each up to 55 characters.
            emojis (Optional[list]): Optional list of emojis corresponding to each answer.
                For custom emojis, provide the emoji ID as an integer.
            duration (Optional[int]): Optional poll duration in hours, from 1 up to 768.
            allow_multiselect (Optional[bool]): If True, allows selecting multiple answers.

        Raises:
            ValueError: If question exceeds 300 characters.
            ValueError: If any answer exceeds 55 characters.
            ValueError: If duration is outside the range 1 to 768.
            ValueError: If length of emojis list does not match length of answers.
        """

        if len(question) > 300:
            raise ValueError("Question length cannot exceed 300 characters")

        if duration is not None and (duration > 768 or duration < 1):
            raise ValueError("Duration must be between 1 and 768")

        body = {
            "poll": {
                "question": {
                    "text": question
                },
                "answers": [
                ]
            }
        }

        for answer in answers:
            if len(answer) > 55:
                raise ValueError("Answer length cannot exceed 55 characters")

            body["poll"]["answers"].append({"poll_media": {"text": answer}})

        if allow_multiselect:
            body["poll"]["allow_multiselect"] = allow_multiselect

        if duration:
            body["poll"]["duration"] = duration

        if emojis:
            if len(answers) == len(emojis):
                for i, emoji in enumerate(emojis):
                    if isinstance(emoji, str):
                        body["poll"]["answers"][i]["poll_media"]["emoji"] = {
                            "name": emoji}
                    else:
                        body["poll"]["answers"][i]["poll_media"]["emoji"] = {
                            "id": str(emoji)}
            else:
                raise ValueError(
                    "Length of emojis must match length of answers")

        self.__post(json=body)