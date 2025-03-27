import subprocess
from cosmos_to_json import fetch_articles_from_cosmos

def git_push():
    """Commit and push changes to Git."""
    try:
        # Git'e ekle
        subprocess.run(["git", "add", "news1.json"], check=True)

        # Değişiklik varsa commit et
        result = subprocess.run(["git", "diff", "--cached", "--quiet"])
        if result.returncode != 0:  # Değişiklik varsa
            subprocess.run(["git", "commit", "-m", "📰 Auto update from Cosmos DB"], check=True)
            subprocess.run(["git", "push"], check=True)
            print("✅ Changes pushed to Git successfully.")
        else:
            print("ℹ️ No changes to commit.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Git push failed: {e}")

# Cosmos DB'den verileri al ve news1.json dosyasını güncelle
if fetch_articles_from_cosmos():
    git_push()
else:
    print("❌ Failed to fetch articles from Cosmos DB.")
