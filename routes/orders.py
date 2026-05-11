from flask import Blueprint, request, jsonify
from app import db
from app.models.order import Order, OrderItem

orders = Blueprint('orders', __name__)

@orders.route('/orders', methods=['GET'])
def get_orders():
    liste = Order.query.all()
    result = []
    for o in liste:
        items = []
        for item in o.items:
            items.append({
                'id_produit': item.id_produit,
                'quantite': item.quantite,
                'prix_unitaire': item.prix_unitaire
            })
        result.append({
            'id': o.id,
            'id_acheteur': o.id_acheteur,
            'total': o.total,
            'statut': o.statut,
            'produits': items
        })
    return jsonify(result), 200


@orders.route('/orders', methods=['POST'])
def add_order():
    data = request.get_json(force=True)
    
    nouvelle_commande = Order(
        id_acheteur=data['id_acheteur'],
        total=data['total'],
        statut='en attente'
    )
    db.session.add(nouvelle_commande)
    db.session.flush()  # pour récupérer l'id avant commit

    for item in data['produits']:
        order_item = OrderItem(
            id_order=nouvelle_commande.id,
            id_produit=item['id_produit'],
            quantite=item['quantite'],
            prix_unitaire=item['prix_unitaire']
        )
        db.session.add(order_item)

    db.session.commit()
    
    return jsonify({'message': 'Commande créée avec succès'}), 201