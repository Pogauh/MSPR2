import csv
from datetime import datetime, timedelta

# Début et fin
start_date = datetime(2019, 1, 1)
end_date = datetime(2025, 3, 31)

# Génération des dates
dates = []
current_date = start_date
while current_date <= end_date:
    dates.append(current_date.strftime('%Y-%m-%d'))
    current_date += timedelta(days=1)

# Écriture dans un fichier CSV
with open('dates_2019_2025.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['date_jour'])  # En-tête
    for date in dates:
        writer.writerow([date])

print("✅ Fichier 'dates_2019_2025.csv' généré avec succès.")
