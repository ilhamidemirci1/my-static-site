import subprocess
import json

def run_update_json():
    """update_json.py dosyasını çalıştırır."""
    try:
        print("🚀 update_json.py çalıştırılıyor...")
        subprocess.run(["python", "update_json.py"], check=True)
        print("✅ update_json.py başarıyla çalıştırıldı.")
    except subprocess.CalledProcessError as e:
        print(f"❌ update_json.py çalıştırılırken bir hata oluştu: {e}")
        exit(1)

def git_push():
    """Git komutlarını çalıştırarak değişiklikleri push eder."""
    try:
        print("🚀 Git işlemleri başlatılıyor...")

        # TOKEN'I YÜKLE
        with open("git_token.json", "r") as f:
            token_data = json.load(f)

        username = token_data["github_username"]
        token = token_data["github_token"]

        # Uzak bağlantıyı ayarla (geçici olarak)
        remote_url = f"https://{username}:{token}@github.com/{username}/my-static-site.git"
        subprocess.run(["git", "remote", "set-url", "origin", remote_url], check=True)

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
