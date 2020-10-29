from typing import Dict
from django.conf import settings
from slack_sdk.web import WebClient

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
