import json
from datetime import datetime

import os
JSON_PATH = os.path.join(os.path.dirname(__file__), "news1.json")


# Şu anki zaman (ISO 8601 formatında)
now_iso = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

# Dosyayı aç ve oku
with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

# Her makale için kontrol et
for article in data["articles"]:
    if not article.get("published"):
        article["published"] = True
        # Eğer publication_date yoksa veya null ise o anki tarihi yaz
        if "publication_date" not in article or article["publication_date"] in [None, ""]:
            article["publication_date"] = now_iso

# Güncellenmiş veriyi dosyaya yaz
with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("✅ JSON dosyası güncellendi. Yayınlanmamış makaleler işaretlendi ve tarihleri atandı.")
