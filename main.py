#!/usr/bin/python3
# pyright:reportMissingImports=false
import os, sys, logging, random
from slack_bolt import App, Complete, Fail
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
from logs import log
from traceback import format_exc
from funcs import toBool, blacklist

random.seed()
load_dotenv()

for requiredVar in ["SLACK_BOT_TOKEN", "SLACK_SIGNING_SECRET", "PORT"]:
    if not os.environ.get(requiredVar):
        raise ValueError(
            f'Missing required environment variable "{requiredVar}". Please create a .env file in the same directory as this script and define the missing variable.'
        )

debug = toBool(os.environ.get("DEBUG", False))
if debug:
    logging.basicConfig(level=logging.DEBUG)

log("Establishing a connection to slack...")
app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
    signing_secret=os.environ["SLACK_SIGNING_SECRET"],
)
client = app.client
log("Connected to slack")


@app.function("template")
def template(inputs: dict, fail: Fail, complete: Complete, logger: logging.Logger):
    try:
        raise NotImplementedError()
    except:
        log(format_exc(), "ERROR")
        fail(
            "An error occured app-side trying to process the `template` workflow step. Please contact <@U06JLP2R8JV> about this issue."
        )


@app.function("convert_user_to_channel")
def useridToChannel(
    inputs: dict, fail: Fail, complete: Complete, logger: logging.Logger
):
    try:
        ids = [inputs["user_id"], inputs["workflow_id"]]
        channel_id = client.conversations_open(users=ids)["channel"]["id"]
        if debug:
            log(f"{ids} -> {channel_id}", "DEBUG")
        complete({"channel_id": channel_id})
    except:
        log(format_exc(), "ERROR")
        fail(
            "An error occured app-side trying to process the `convert_user_to_channel` workflow step. Please contact <@U06JLP2R8JV> about this issue."
        )


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
        if debug:
            log(f"{inputs['channel_id']} + {inputs['message_ts']} ->\n" + message)
        complete({"message_content": message})
    except:
        log(format_exc(), "ERROR")
        fail(
            "An error occured app-side trying to process the `get_message_content` workflow step. Please contact <@U06JLP2R8JV> about this issue."
        )


@app.function("get_users_from_group")
def getUsersFromGroup(
    inputs: dict, fail: Fail, complete: Complete, logger: logging.Logger
):
    try:
        result = client.usergroups_users_list(
            usergroup=inputs["ping_group"][0]["elements"][0]["elements"][0][
                "usergroup_id"
            ]
        )
        message = ""
        if inputs.get("exclude_blacklisted", False):
            result["users"] = list(filter(blacklist, result["users"]))
        if inputs.get("include_names", False):
            for user in result["users"]:
                userData = client.users_info(user=user)["user"]
                name = (
                    userData["profile"]["display_name_normalized"]
                    if userData["profile"]["display_name_normalized"]
                    else (
                        userData["profile"]["real_name_normalized"]
                        if userData["profile"]["real_name_normalized"]
                        else userData["real_name"]
                    )
                )
                message = f"{message}\n{user}: {name}"
            message = message.strip()
        else:
            message = "\n".join(result["users"])
        complete({"user_list": message})
    except:
        log(format_exc(), "ERROR")
        fail(
            "An error occured app-side trying to process the `get_users_from_group` workflow step. Please contact <@U06JLP2R8JV> about this issue."
        )


@app.function("get_random_user_from_list")
def getRandomUserFromList(
    inputs: dict, fail: Fail, complete: Complete, logger: logging.Logger
):
    try:
        users = []
        for item in inputs["users"][0]["elements"][0]["elements"]:
            if item["type"] == "user":
                users.append(item["user_id"])
        if inputs.get("exclude_blacklisted", False):
            users = list(filter(blacklist, users))
        if debug:
            log(str(users), "DEBUG")
        random.seed()
        complete({"user": random.choice(users)})
    except:
        log(format_exc(), "ERROR")
        fail(
            "An error occured app-side trying to process the `get_random_user_from_list` workflow step. Please contact <@U06JLP2R8JV> about this issue."
        )


@app.function("get_random_user_from_group")
def getRandomUserFromGroup(
    inputs: dict, fail: Fail, complete: Complete, logger: logging.Logger
):
    try:
        users = client.usergroups_users_list(usergroup=inputs["user_group"])["users"]
        if inputs.get("exclude_blacklisted", False):
            users = list(filter(blacklist, users))
        if debug:
            log(str(users), "DEBUG")
        random.seed()
        complete({"user": random.choice(users)})
    except:
        log(format_exc(), "ERROR")
        fail(
            "An error occured app-side trying to process the `get_random_user_from_group` workflow step. Please contact <@U06JLP2R8JV> about this issue."
        )


@app.function("get_random_user_from_channel")
def getRandomUserFromChannel(
    inputs: dict, fail: Fail, complete: Complete, logger: logging.Logger
):
    try:
        users = []
        data = client.conversations_members(channel=inputs["channel"], limit=200)
        users.extend(data["members"])
        while data["response_metadata"]["next_cursor"]:
            data = client.conversations_members(
                channel=inputs["channel"],
                limit=200,
                cursor=data["response_metadata"]["next_cursor"],
            )
            users.extend(data["members"])
        if inputs.get("exclude_blacklisted", False):
            users = list(filter(blacklist, users))
        if debug:
            log(str(users), "DEBUG")
        random.seed()
        complete({"user": random.choice(users)})
    except:
        log(format_exc(), "ERROR")
        fail(
            "An error occured app-side trying to process the `get_random_user_from_channel` workflow step. Please contact <@U06JLP2R8JV> about this issue."
        )


@app.function("get_random_channel")
def getRandomChannel(
    inputs: dict, fail: Fail, complete: Complete, logger: logging.Logger
):
    try:
        channels = []
        for item in inputs["channels"][0]["elements"][0]["elements"]:
            if item["type"] == "channel":
                channels.append(item["channel_id"])
        if debug:
            log(str(channels), "DEBUG")
        random.seed()
        complete({"channel": random.choice(channels)})
    except:
        log(format_exc(), "ERROR")
        fail(
            "An error occured app-side trying to process the `get_random_channel` workflow step. Please contact <@U06JLP2R8JV> about this issue."
        )


if __name__ == "__main__":
    log(f"Starting bot on port {os.environ.get('PORT')}")
    app.start(port=int(os.environ["PORT"]))
