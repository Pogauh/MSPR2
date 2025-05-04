
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Maladie, Pays, Traitement, Region, DateControle, Epidemiologie, Traite

from datetime import date as DateType
from typing import List

import joblib
from pathlib import Path

import pandas as pd
from fastapi import FastAPI

import unidecode

from pydantic import BaseModel

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()





class PredictionInput(BaseModel):
    day: int
    month: int
    population: int
    region: str  



@app.post("/predict")
def predict(input_data: PredictionInput):
    # Créer une ligne vide avec les colonnes d'entraînement
    data = {col: 0 for col in model.feature_names_in_}
    print([col for col in model.feature_names_in_ if col.startswith("region_")])
    data["day"] = input_data.day
    data["month"] = input_data.month
    data["population"] = input_data.population

    # Normaliser la région entrée (sans accents, minuscules)
    input_region_clean = unidecode.unidecode(input_data.region.strip()).lower()

    matched = False
    for col in data:
        if col.startswith("region_"):
            col_clean = unidecode.unidecode(col.replace("region_", "")).lower()
            if col_clean == input_region_clean:
                data[col] = 1
                matched = True
                break

    if not matched:
        return {"error": f"Région inconnue : {input_data.region}"}

    df = pd.DataFrame([data])
    prediction = model.predict(df)[0]
    return {"prediction": prediction}

# ======= MALADIE =======
@app.post("/maladies/")
def create_maladie(data: dict, db: Session = Depends(get_db)):
    obj = Maladie(**data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@app.get("/maladies/")
def read_all_maladies(db: Session = Depends(get_db)):
    return db.query(Maladie).all()

@app.get("/maladies/{id}")
def read_maladie(id: int, db: Session = Depends(get_db)):
    obj = db.query(Maladie).get(id)
    if not obj:
        raise HTTPException(status_code=404, detail="Maladie non trouvée")
    return obj

@app.delete("/maladies/{id}")
def delete_maladie(id: int, db: Session = Depends(get_db)):
    obj = db.query(Maladie).get(id)
    if not obj:
        raise HTTPException(status_code=404, detail="Maladie non trouvée")
    db.delete(obj)
    db.commit()
    return {"message": "Maladie supprimée"}

# ======= PAYS =======
@app.post("/pays/")
def create_pays(data: dict, db: Session = Depends(get_db)):
    obj = Pays(**data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@app.get("/pays/")
def read_all_pays(db: Session = Depends(get_db)):
    return db.query(Pays).all()

@app.get("/pays/{code}")
def read_pays(code: str, db: Session = Depends(get_db)):
    obj = db.query(Pays).get(code)
    if not obj:
        raise HTTPException(status_code=404, detail="Pays non trouvé")
    return obj

@app.delete("/pays/{code}")
def delete_pays(code: str, db: Session = Depends(get_db)):
    obj = db.query(Pays).get(code)
    if not obj:
        raise HTTPException(status_code=404, detail="Pays non trouvé")
    db.delete(obj)
    db.commit()
    return {"message": "Pays supprimé"}

# ======= TRAITEMENT =======
@app.post("/traitements/")
def create_traitement(data: dict, db: Session = Depends(get_db)):
    obj = Traitement(**data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@app.get("/traitements/")
def read_all_traitements(db: Session = Depends(get_db)):
    return db.query(Traitement).all()

@app.get("/traitements/{id}")
def read_traitement(id: int, db: Session = Depends(get_db)):
    obj = db.query(Traitement).get(id)
    if not obj:
        raise HTTPException(status_code=404, detail="Traitement non trouvé")
    return obj

@app.delete("/traitements/{id}")
def delete_traitement(id: int, db: Session = Depends(get_db)):
    obj = db.query(Traitement).get(id)
    if not obj:
        raise HTTPException(status_code=404, detail="Traitement non trouvé")
    db.delete(obj)
    db.commit()
    return {"message": "Traitement supprimé"}

# ======= REGION =======
@app.post("/regions/")
def create_region(data: dict, db: Session = Depends(get_db)):
    obj = Region(**data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@app.get("/regions/")
def read_all_regions(db: Session = Depends(get_db)):
    return db.query(Region).all()

@app.get("/regions/{key}")
def read_region(key: str, db: Session = Depends(get_db)):
    obj = db.query(Region).get(key)
    if not obj:
        raise HTTPException(status_code=404, detail="Région non trouvée")
    return obj

@app.delete("/regions/{key}")
def delete_region(key: str, db: Session = Depends(get_db)):
    obj = db.query(Region).get(key)
    if not obj:
        raise HTTPException(status_code=404, detail="Région non trouvée")
    db.delete(obj)
    db.commit()
    return {"message": "Région supprimée"}

# ======= DATE CONTROLE =======
@app.post("/dates/")
def create_date(data: dict, db: Session = Depends(get_db)):
    obj = DateControle(**data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@app.get("/dates/")
def read_all_dates(db: Session = Depends(get_db)):
    return db.query(DateControle).all()

@app.get("/dates/{date_jour}")
def read_date(date_jour: str, db: Session = Depends(get_db)):
    obj = db.query(DateControle).get(date_jour)
    if not obj:
        raise HTTPException(status_code=404, detail="Date non trouvée")
    return obj

@app.delete("/dates/{date_jour}")
def delete_date(date_jour: str, db: Session = Depends(get_db)):
    obj = db.query(DateControle).get(date_jour)
    if not obj:
        raise HTTPException(status_code=404, detail="Date non trouvée")
    db.delete(obj)
    db.commit()
    return {"message": "Date supprimée"}

# ======= EPIDEMIOLOGIE =======
@app.post("/epidemiologie/")
def create_epidemiologie(data: dict, db: Session = Depends(get_db)):
    obj = Epidemiologie(**data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@app.get("/epidemiologie/")
def read_all_epidemiologie(db: Session = Depends(get_db)):
    return db.query(Epidemiologie).all()

@app.get("/epidemiologie/date/{date_controle}")
def read_epidemiologie_by_date(date_controle: DateType, db: Session = Depends(get_db)):
    results = db.query(Epidemiologie).filter(Epidemiologie.date_jour == date_controle).all()
    if not results:
        raise HTTPException(status_code=404, detail="Aucune donnée pour cette date")
    return results

@app.get("/epidemiologie/date-range/")
def read_epidemiologie_between_dates(
    start: DateType,
    end: DateType,
    db: Session = Depends(get_db)
):
    results = db.query(Epidemiologie).filter(
        Epidemiologie.date_jour >= start,
        Epidemiologie.date_jour <= end
    ).all()

    if not results:
        raise HTTPException(status_code=404, detail="Aucune donnée trouvée entre ces dates")
    return results


# ======= TRAITE (association maladie/traitement) =======
@app.post("/traite/")
def create_traite(data: dict, db: Session = Depends(get_db)):
    obj = Traite(**data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@app.get("/traite/")
def read_all_traite(db: Session = Depends(get_db)):
    return db.query(Traite).all()


from fastapi.middleware.cors import CORSMiddleware


# Autoriser React à accéder à l'API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Autorise React en développement
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)