import subprocess
import json
import os

def run_update_json():
    """update_json.py dosyasını çalıştırır."""
    try:
        print("🚀 update_json.py çalıştırılıyor...")
        subprocess.run(["python", "update_json.py"], check=True)
        print("✅ update_json.py başarıyla çalıştırıldı.")
    except subprocess.CalledProcessError as e:
        print(f"❌ update_json.py çalıştırılırken bir hata oluştu: {e}")
        exit(1)

def load_git_credentials():
    """git_token.json içinden kullanıcı adı ve token bilgilerini yükler."""
    try:
        with open("git_token.json", "r", encoding="utf-8") as f:
            creds = json.load(f)
            return creds["github_username"], creds["github_token"]
    except FileNotFoundError:
        print("❌ git_token.json bulunamadı.")
        exit(1)
    except KeyError:
        print("❌ git_token.json içinde gerekli alanlar eksik.")
        exit(1)

def git_push():
    """GitHub'a token ile otomatik push işlemi yapar."""
    try:
        print("🚀 Git işlemleri başlatılıyor...")

        # Kimlik bilgilerini al
        username, token = load_git_credentials()

        # Geçici remote bağlantısını ayarla
        remote_url = f"https://{username}:{token}@github.com/{username}/my-static-site.git"
        subprocess.run(["git", "remote", "set-url", "origin", remote_url], check=True)

        # Git işlemleri
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "msnewsbot"], check=True)
        subprocess.run(["git", "push"], check=True)

        print("✅ Değişiklikler başarıyla GitHub'a push edildi.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Git işlemleri sırasında bir hata oluştu: {e}")
        exit(1)

if __name__ == "__main__":
    run_update_json()
    git_push()
