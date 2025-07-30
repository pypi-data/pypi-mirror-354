import os
import pkg_resources

# Get bot token from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set")

VERSION = pkg_resources.require("python_llm_assistant")[0].version