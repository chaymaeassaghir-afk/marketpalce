from flask import Blueprint, jsonify
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.models.user import User

dashboard = Blueprint('dashboard', __name__, url_prefix='/admin')

@dashboard.route('/dashboard', methods=['GET'])
def get_dashboard():
    # Total commandes
    total_commandes = Order.query.count()

    # Chiffre d'affaires total
    toutes_commandes = Order.query.all()
    chiffre_affaires = sum(o.total for o in toutes_commandes)

    # Total utilisateurs
    total_users = User.query.filter_by(role='acheteur').count()
    total_vendeurs = User.query.filter_by(role='vendeur').count()

    # Produits en rupture de stock
    produits_rupture = Product.query.filter(Product.stock <= 5).count()

    # Produits les plus commandés
    items = OrderItem.query.all()
    compteur = {}
    for item in items:
        compteur[item.id_produit] = compteur.get(item.id_produit, 0) + item.quantite

    top_produits = []
    for id_produit, quantite in sorted(compteur.items(), key=lambda x: x[1], reverse=True)[:5]:
        produit = Product.query.get(id_produit)
        if produit:
            top_produits.append({
                'id': produit.id,
                'nom': produit.nom,
                'quantite_vendue': quantite
            })

    return jsonify({
        'total_commandes': total_commandes,
        'chiffre_affaires': chiffre_affaires,
        'total_acheteurs': total_users,
        'total_vendeurs': total_vendeurs,
        'produits_rupture': produits_rupture,
        'top_produits': top_produits
    }), 200