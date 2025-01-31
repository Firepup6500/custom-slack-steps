import os, sys, logging
from slack_bolt import App, Complete, Fail
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
from logs import log
from traceback import format_exc

load_dotenv()
logging.basicConfig(level=logging.DEBUG)

for requiredVar in ["SLACK_BOT_TOKEN", "SLACK_SIGNING_SECRET", "PORT"]:
    if not os.environ.get(requiredVar):
        raise ValueError(
            f'Missing required environment variable "{requiredVar}". Please create a .env file in the same directory as this script and define the missing variable.'
        )

print("[INFO] Establishing a connection to slack...", flush=True)
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
)
client = app.client


@app.function("convert_user_to_channel")
def useridToChannel(
    inputs: dict, fail: Fail, complete: Complete, logger: logging.Logger
):
    user_id = inputs["user_id"]
    try:
        complete({"channel_id": user_id})
    except:
        log(format_exc(), "ERROR")
        # fail("Am fail.")
        # We can't run fail() here, unsure why.


@app.function("get_message_content")
def getMessageContent(
    inputs: dict, fail: Fail, complete: Complete, logger: logging.Logger
):
    try:
        result = client.conversations_history(
            channel=inputs["channel_id"],
            inclusive=True,
            oldest=inputs["message_ts"],
            limit=1,
        )

        message = result["messages"][0]["text"]
        log(message, "DEBUG")
        complete({"message_content": message})
    except:
        log(format_exc(), "ERROR")
        fail(
            "An error occured app-side trying to process this workflow step. Please contact <@U06JLP2R8JV> (Firepup650) about this issue."
        )


if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT")))
