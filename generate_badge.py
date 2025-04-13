import json

# Lire la version depuis version.txt
with open("version.txt", "r", encoding="utf-8") as file:
    version = file.read().strip()

# Contenu du badge JSON
badge_data = {
    "schemaVersion": 1,
    "label": "AegisBOT",
    "message": f"v{version}",
    "color": "blue"
}

# Crée le dossier .github si nécessaire
import os
os.makedirs(".github", exist_ok=True)

# Écrit le fichier JSON
with open(".github/version-badge.json", "w", encoding="utf-8") as outfile:
    json.dump(badge_data, outfile, indent=4)

print(f"✅ Badge généré pour la version {version}")
