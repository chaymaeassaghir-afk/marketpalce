from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User

admin = Blueprint('admin', __name__)

@admin.route('/admin/users', methods=['GET'])
def get_users():
    users = User.query.all()
    result = []
    for u in users:
        result.append({
            'id': u.id,
            'nom': u.nom,
            'email': u.email,
            'role': u.role,
            'is_validated': u.is_validated,
            'nom_boutique': u.nom_boutique
        })
    return jsonify(result), 200


@admin.route('/admin/users/<int:id>/valider', methods=['PUT'])
def valider_user(id):
    user = User.query.get(id)

    if not user:
        return jsonify({'message': 'Utilisateur introuvable'}), 404

    user.is_validated = True
    db.session.commit()

    return jsonify({'message': f'Compte de {user.nom} validé avec succès'}), 200
