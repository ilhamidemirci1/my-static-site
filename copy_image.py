import shutil
import os

# Kaynaktaki dosyanın tam yolu
source_path = r'C:\Users\Enqura\Downloads\teknohaber.jpg'

# Hedef klasör (images içinde olması gerekiyor)
destination_path = r'C:\Users\Enqura\Desktop\my-static-site\images\teknohaber.jpg'

# Hedef klasörü oluştur (varsa geç)
os.makedirs(os.path.dirname(destination_path), exist_ok=True)

# Kopyalama işlemi
shutil.copy(source_path, destination_path)

print(f"Image copied to: {destination_path}")


