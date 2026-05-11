from flask import Blueprint, request, jsonify
from app import db
from app.models.order import Order

paiement = Blueprint('paiement', __name__)

@paiement.route('/paiement/paypal', methods=['POST'])
def payer_paypal():
    data = request.get_json(force=True)
    id_order = data['id_order']

    commande = Order.query.get(id_order)
    if not commande:
        return jsonify({'message': 'Commande introuvable'}), 404

    commande.statut = 'payée via PayPal'
    db.session.commit()

    return jsonify({
        'message': 'Paiement PayPal simulé avec succès',
        'id_order': id_order,
        'montant': commande.total,
        'statut': commande.statut
    }), 200


@paiement.route('/paiement/cmi', methods=['POST'])
def payer_cmi():
    data = request.get_json(force=True)
    id_order = data['id_order']
    numero_carte = data.get('numero_carte', '')

    commande = Order.query.get(id_order)
    if not commande:
        return jsonify({'message': 'Commande introuvable'}), 404

    if len(numero_carte) != 16 or not numero_carte.isdigit():
        return jsonify({'message': 'Numéro de carte invalide'}), 400

    commande.statut = 'payée via CMI'
    db.session.commit()

    return jsonify({
        'message': 'Paiement CMI simulé avec succès',
        'id_order': id_order,
        'montant': commande.total,
        'statut': commande.statut
    }), 200