from flask import Blueprint, request, jsonify
from app.models.product import Product
from app.models.order import Order, OrderItem

recommandations = Blueprint('recommandations', __name__)

@recommandations.route('/recommandations/<int:id_user>', methods=['GET'])
def get_recommandations(id_user):
    # Trouver les catégories achetées par l'utilisateur
    commandes = Order.query.filter_by(id_acheteur=id_user).all()
    
    categories_achetees = set()
    produits_achetes = set()

    for commande in commandes:
        for item in commande.items:
            produit = Product.query.get(item.id_produit)
            if produit:
                categories_achetees.add(produit.categorie)
                produits_achetes.add(produit.id)

    # Si aucun achat, retourner les 5 premiers produits
    if not categories_achetees:
        produits = Product.query.limit(5).all()
    else:
        # Retourner produits de même catégorie non encore achetés
        produits = Product.query.filter(
            Product.categorie.in_(categories_achetees),
            Product.id.notin_(produits_achetes)
        ).limit(5).all()

    result = []
    for p in produits:
        result.append({
            'id': p.id,
            'nom': p.nom,
            'description': p.description,
            'prix': p.prix,
            'categorie': p.categorie,
            'photo': p.photo
        })

    return jsonify(result), 200