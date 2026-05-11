from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json(force=True)

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email déjà utilisé'}), 400

    # si vendeur, nom_boutique obligatoire
    if data['role'] == 'vendeur' and not data.get('nom_boutique'):
        return jsonify({'message': 'nom_boutique obligatoire pour un vendeur'}), 400

    nouveau_user = User(
        nom=data['nom'],
        email=data['email'],
        mot_de_passe=generate_password_hash(data['mot_de_passe']),
        role=data['role'],
        is_admin=False,
        is_validated=False,
        nom_boutique=data.get('nom_boutique'),
        description_boutique=data.get('description_boutique')
    )

    db.session.add(nouveau_user)
    db.session.commit()

    return jsonify({'message': 'Compte créé avec succès'}), 201


@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json(force=True)

    user = User.query.filter_by(email=data['email']).first()

    if not user or not check_password_hash(user.mot_de_passe, data['mot_de_passe']):
        return jsonify({'message': 'Email ou mot de passe incorrect'}), 401

    return jsonify({
        'message': 'Connexion réussie',
        'user': {
            'id': user.id,
            'nom': user.nom,
            'role': user.role,
            'is_admin': user.is_admin,
            'is_validated': user.is_validated,
            'nom_boutique': user.nom_boutique
        }
    }), 200