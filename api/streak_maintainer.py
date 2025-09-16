import os
from github import Github
import pytz
from datetime import datetime
import random
import urllib.request

# Aapke GitHub repo details
REPO_NAME = "saeedx302/github-streak-maintainer"
FILE_PATH = "README.md"
COMMIT_MESSAGES_URL = "https://raw.githubusercontent.com/SaeedX302/Github-Streak-Maintainer/refs/heads/main/commit_messages.txt"

# Pakistan Standard Time (PKT) timezone
PKT = pytz.timezone('Asia/Karachi')

def fetch_content_from_url(url):
    """
    Fetches content from a raw URL.
    """
    try:
        with urllib.request.urlopen(url) as response:
            return response.read().decode('utf-8').splitlines()
    except Exception as e:
        print(f"Error fetching content from URL: {e}")
        return []

def update_github_readme():
    """
    Updates the README.md file in the specified GitHub repository.
    """
    # Get GitHub Token from environment variable
    GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
    if not GITHUB_TOKEN:
        print("Error: GITHUB_TOKEN environment variable not set.")
        return {"statusCode": 500, "body": "GITHUB_TOKEN not set"}

    try:
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)
        
        # Fetch content of README from the repository
        readme_content = repo.get_contents(FILE_PATH).decoded_content.decode()
        
        # Fetch commit messages from the specified URL
        commit_messages = fetch_content_from_url(COMMIT_MESSAGES_URL)
        if not commit_messages:
            print("Could not fetch commit messages. Exiting.")
            return {"statusCode": 500, "body": "Could not fetch commit messages"}

        # Logic for selecting random message and quote
        commit_msg = random.choice(commit_messages)
        quotes = ["💀 Darkness never sleeps", "🔥 Keep the flame alive", "👻 Shadows whisper in silence", "⚡ Power never dies", "🕯️ Light in the darkness"]
        random_quote = random.choice(quotes)

        # Get current time in PKT
        now = datetime.now(PKT)
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

        # Update README content
        # Purani history ko preserve karo, sirf nayi row add karo
        new_line = f"| # | Date & Time (PKT) | Message | Quote |\n"
        if new_line not in readme_content:
            updated_content = readme_content.split('## 📅 Commit History')[0] + f"## 📅 Commit History\n| # | Date & Time (PKT) | Message | Quote |\n|---|--------------------|---------|-------|\n"
        else:
            updated_content = readme_content
        
        # Count existing rows
        count = updated_content.count('|')
        new_count = (count // 4) - 2 # -2 for header and separator lines
        
        # Append the new entry
        new_entry = f"| {new_count} | {timestamp} | {commit_msg} | {random_quote} |\n"
        updated_content += new_entry

        # Commit and push the changes
        contents = repo.get_contents(FILE_PATH)
        repo.update_file(contents.path, commit_msg, updated_content, contents.sha)
        
        print("Successfully updated GitHub streak!")
        return {"statusCode": 200, "body": "Successfully updated GitHub streak"}

    except Exception as e:
        print(f"Error updating file on GitHub: {e}")
        return {"statusCode": 500, "body": str(e)}

def handler(event, context):
    """
    Vercel serverless function entry point.
    """
    return update_github_readme()
