import requests
import pandas as pd
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib

BASE_URL = "http://127.0.0.1:8000"
START_DATE = "2020-01-01"
END_DATE = "2022-02-01"

def get_epidemiologie(date_str, session):
    try:
        r = session.get(f"{BASE_URL}/epidemiologie/date/{date_str}", timeout=5)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"Erreur épidémiologie pour {date_str} : {e}")
        return None

def get_all_regions(session):
    try:
        r = session.get(f"{BASE_URL}/regions", timeout=10)
        r.raise_for_status()
        regions = r.json()
        return {region["location_key"].strip(): region for region in regions}
    except Exception as e:
        print(f"Erreur lors de la récupération des régions : {e}")
        return {}

def fetch_dataset(start_date, end_date, session):
    data = []
    region_lookup = get_all_regions(session)

    if not region_lookup:
        print("Aucune région disponible, vérifie l'API.")
        return pd.DataFrame()

    current_date = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    while current_date <= end:
        date_str = current_date.strftime("%Y-%m-%d")
        entries = get_epidemiologie(date_str, session)

        if entries and isinstance(entries, list):
            for entry in entries:
                loc_key = entry.get("location_key", "").strip()
                region_data = region_lookup.get(loc_key)
                if region_data:
                    data.append({
                        "date": entry["date_jour"],
                        "day": current_date.day,
                        "month": current_date.month,
                        "year": current_date.year,
                        "week": current_date.isocalendar()[1],
                        "location_key": loc_key,
                        "region": region_data.get("subregion1_name", "").strip(),
                        "population": region_data.get("population", 0),
                        "nbr_hospitalises": entry.get("nbr_hospitalises", 0)
                    })

        current_date += timedelta(days=1)

    print(f"{len(data)} enregistrements collectés.")
    return pd.DataFrame(data)

def train_model(df):
    if df.empty:
        print("❌ Le DataFrame est vide, arrêt de l'entraînement.")
        return

    df = df.dropna()
    df = df[df["nbr_hospitalises"] >= 0]  # Élimine les valeurs invalides
    df = df[df["nbr_hospitalises"] < df["nbr_hospitalises"].quantile(0.99)]  # Élimine les extrêmes

    if "region" in df.columns:
        df = pd.get_dummies(df, columns=["region"], drop_first=False)
        
    else:
        print("❌ Colonne 'region' manquante. Impossible de créer les variables indicatrices.")
        return

    features = ["day", "month", "year", "week", "population"] + [col for col in df.columns if col.startswith("region_")]
    X = df[features]
    y = df["nbr_hospitalises"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=50, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)

    print("Colonnes utilisées dans le modèle :", model.feature_names_in_)


    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    print(f"📉 MAE: {mae:.2f}")

    joblib.dump(model, "hospitalisation_model.pkl")
    print("✅ Modèle sauvegardé dans hospitalisation_model.pkl")

def main():
    print("🔄 Création de la session HTTP...")
    session = requests.Session()

    print("⬇️  Chargement des données depuis l’API...")
    df = fetch_dataset(START_DATE, END_DATE, session)
    df.to_csv("dataset_hospitalisations.csv", index=False)
    print("💾 Dataset sauvegardé dans dataset_hospitalisations.csv")

    print("🏋️ Entraînement du modèle...")
    train_model(df)

if __name__ == "__main__":
    main()