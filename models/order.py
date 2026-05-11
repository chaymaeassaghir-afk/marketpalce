from app import db

class Order(db.Model):
    __tablename__ = 'commande'
    id = db.Column(db.Integer, primary_key=True)
    id_acheteur = db.Column(db.Integer)
    total = db.Column(db.Float)
    statut = db.Column(db.String(50))
    items = db.relationship('OrderItem', backref='order', lazy=True)

class OrderItem(db.Model):
    __tablename__ = 'commande_item'
    id = db.Column(db.Integer, primary_key=True)
    id_order = db.Column(db.Integer, db.ForeignKey('commande.id'))
    id_produit = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantite = db.Column(db.Integer)
    prix_unitaire = db.Column(db.Float)