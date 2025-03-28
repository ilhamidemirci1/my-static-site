import subprocess
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

def git_push():
    """Git komutlarını çalıştırarak değişiklikleri push eder."""
    try:
        print("🚀 Git işlemleri başlatılıyor...")
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "msnewsbot"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("✅ Değişiklikler başarıyla GitHub'a push edildi.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Git işlemleri sırasında bir hata oluştu: {e}")
        exit(1)

if __name__ == "__main__":
    # update_json.py dosyasını çalıştır
    run_update_json()

    # Git işlemlerini gerçekleştir
    git_push()