from app import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    description = db.Column(db.String(500), nullable=True)
    prix = db.Column(db.Float)
    stock = db.Column(db.Integer)
    categorie = db.Column(db.String(100), nullable=True)
    photo = db.Column(db.String(300), nullable=True)
    id_vendeur = db.Column(db.Integer)