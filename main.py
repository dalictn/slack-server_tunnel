import os
import subprocess
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import re
import shlex


# Initialize the app with your Bot Token (xoxb-)
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# run a command
@app.message(re.compile(r"^run\s+(.+)$"))

def parse_command(message, say, context):
    # This executes locally on your Linux server
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


if __name__ == "__main__":
    # Start the daemon using your App-Level Token (xapp-)
    handler = SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN"))
    handler.start()
