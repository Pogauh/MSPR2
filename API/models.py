from sqlalchemy import Column, String, Integer, Date, BigInteger, CHAR, ForeignKey
from database import Base

class Maladie(Base):
    __tablename__ = "maladie"
    id_maladie = Column(Integer, primary_key=True, index=True)
    nom_maladie = Column(CHAR(50))
    nom_specifique = Column(CHAR(50))
    type = Column(CHAR(20))

class Pays(Base):
    __tablename__ = "pays"
    country_code = Column(CHAR(2), primary_key=True, index=True)
    country_name = Column(CHAR(60), nullable=False)

class Traitement(Base):
    __tablename__ = "traitement"
    id_traitement = Column(Integer, primary_key=True, index=True)
    nom_traitement = Column(CHAR(30))

class Region(Base):
    __tablename__ = "region"
    location_key = Column(CHAR(7), primary_key=True, index=True)
    population = Column(BigInteger)
    baby = Column(BigInteger)
    junior = Column(BigInteger)
    senior = Column(BigInteger)
    subregion1_name = Column(CHAR(30))
    country_code = Column(CHAR(2), ForeignKey("pays.country_code"))

class DateControle(Base):
    __tablename__ = "date_controle"
    date_jour = Column(Date, primary_key=True, index=True)

class Epidemiologie(Base):
    __tablename__ = "epidemiologie"
    id_maladie = Column(Integer, ForeignKey("maladie.id_maladie"), primary_key=True)
    date_jour = Column(Date, ForeignKey("date_controle.date_jour"), primary_key=True)
    location_key = Column(CHAR(7), ForeignKey("region.location_key"), primary_key=True)
    nbr_cas = Column(Integer)
    nbr_hospitalises = Column(Integer)
    nbr_morts = Column(Integer)
    morts_cumule = Column(Integer)
    contamination_cumule = Column(Integer)

class Traite(Base):
    __tablename__ = "traite"
    id_maladie = Column(Integer, ForeignKey("maladie.id_maladie"), primary_key=True)
    id_traitement = Column(Integer, ForeignKey("traitement.id_traitement"), primary_key=True)
