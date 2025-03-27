import json
from datetime import datetime

# Dosya adı
JSON_PATH = "news1.json"

# Şu anki zaman (ISO 8601 formatında)
now_iso = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

# Dosyayı aç ve yükle
with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

# Her article için kontrol et
for article in data["articles"]:
    if not article.get("published"):
        article["published"] = True
        if not article.get("publication_date"):
            article["publication_date"] = now_iso

# Güncellenmiş veriyi tekrar yaz
with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("✅ JSON dosyası güncellendi.")
