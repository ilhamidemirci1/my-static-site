import os
import json

def load_git_credentials():
    """GitHub kullanıcı adı ve token'ı .env gibi yükler."""
    credentials_file = "git_token.json"

    if os.path.exists(credentials_file):
        with open(credentials_file, "r", encoding="utf-8") as f:
            creds = json.load(f)
            os.environ["GITHUB_USERNAME"] = creds["github_username"]
            os.environ["GITHUB_TOKEN"] = creds["github_token"]
    else:
        raise FileNotFoundError("git_token.json bulunamadı. Token gerekiyor.")
