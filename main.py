import os
import subprocess
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import re
import shlex
from dotenv import load_dotenv
import sys


load_dotenv()
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))


Admin_IDs = ("UT32PA8UB", "U7KLHB8K1")


# run a command
@app.message(re.compile(r"^send\s+(.+)$"))
def send_command_string(message, say, context):
    # This executes locally on your Linux server

    if context["user_id"] in Admin_IDs:
        
        command = shlex.split(context["matches"][0])

        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )

            output = result.stdout or result.stderr or "(no output)"

        # Slack has a 3000 char message limit
            if len(output) > 3000:
                output = output[:3000] + "\n... (truncated)"

            say(f"```{output}```")

        except subprocess.TimeoutExpired:
            say("Command timed out after 30 seconds.")
        except Exception as e:
            say(f"Error: `{str(e)}`")

    else:
        say("User not authorised to use this command.")

@app.message(re.compile(r"^cmd\s+(.+)$"))
def parse_and_send(message, say, context):
        print(context)
        command = shlex.split(context["matches"][0])
        try:
            result = subprocess.run(
                command,
                shell=False,
                capture_output=True,
                text=True,
                timeout=30
            )

            output = result.stdout or result.stderr or "(no output)"

        # Slack has a 3000 char message limit
            if len(output) > 3000:
                output = output[:3000] + "\n... (truncated)"

            say(f"```{output}```")

        except subprocess.TimeoutExpired:
            say("Command timed out after 30 seconds.")
        except Exception as e:
            say(f"Error: `{str(e)}`")


@app.message("stop server")
def stop_bot(message, say):
    sys.exit()



if __name__ == "__main__":
    # Start the daemon using your App-Level Token (xapp-)
    handler = SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN"))
    handler.start()
