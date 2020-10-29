from typing import Dict, List
from logging import Logger
from datetime import datetime, timedelta
from django.conf import settings
from slack_sdk.web import WebClient
from slack_bolt import App, Say, Ack

from .models import User

CLIENT = WebClient(token=settings.SLACK_TOKEN)


def post_message(channel: str, link_names=True, **kwargs: Dict):
    # blocks: List[Dict] = kwargs.get("blocks", [])
    # if markdown:
    #     blocks.append(
    #         {
    #             "type": "section",
    #             "text": {
    #                 "type": "mrkdwn",
    #                 "text": markdown,
    #             },
    #         }
    #     )

    return CLIENT.chat_postMessage(channel=channel, link_names=link_names, **kwargs)


ROBOT = App(
    token=settings.SLACK_TOKEN,
    signing_secret=settings.SLACK_SECRET,
)


@ROBOT.event("app_mention")
def handle_robot_mention(payload: Dict, say: Say, ack: Ack, logger: Logger):
    ack()

    text = payload.get("text")
    user = payload.get("user")
    logger.info("Got a message from %s: %s", user, text)

    reply = handle_robot_text(text)
    if reply:
        say(reply)


def handle_robot_text(text: str) -> str:
    if not text:
        return "Hmm?"
    if ("signups" in text) or ("sign ups" in text) or ("signed up" in text):
        signups = get_recent_signups()
        if signups:
            return f"We've had some recent signups! They include:\n{signups}"
        else:
            return "Nobody has signed up in the last 24 hours."


def get_recent_signups() -> List[User]:
    since = datetime.today() - timedelta(days=1)
    users = User.objects.filter(date_joined__gt=since.date())
    infos = [f"   • *{user.name()}* ({user.email})" for user in users]
    return "\n".join(infos)
