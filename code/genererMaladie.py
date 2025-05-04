import csv

# Définir les données à écrire
data = [
    {"id_maladie": 1, "nom_maladie": "Covid-19", "nom_specifique": "SRAS-CoV-2", "type": "Respiratoire"}
]

# Nom du fichier
fichier_csv = "maladie.csv"

# Écriture du CSV
with open(fichier_csv, mode="w", newline="", encoding="utf-8") as fichier:
    writer = csv.DictWriter(fichier, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)

print(f"✅ Fichier '{fichier_csv}' créé avec succès.")
 