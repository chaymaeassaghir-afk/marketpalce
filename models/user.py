from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    mot_de_passe = db.Column(db.String(200))
    role = db.Column(db.String(20))  # "acheteur" ou "vendeur"
    is_admin = db.Column(db.Boolean, default=False)
    is_validated = db.Column(db.Boolean, default=False)
    nom_boutique = db.Column(db.String(100), nullable=True)
    description_boutique = db.Column(db.String(300), nullable=True)
