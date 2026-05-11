from flask import Blueprint, request, jsonify
from app import db
from app.models.product import Product

products = Blueprint('products', __name__)

@products.route('/products', methods=['GET'])
def get_products():
    liste = Product.query.all()
    result = []
    for p in liste:
        result.append({
            'id': p.id,
            'nom': p.nom,
            'description': p.description,
            'prix': p.prix,
            'stock': p.stock,
            'categorie': p.categorie,
            'photo': p.photo,
            'id_vendeur': p.id_vendeur
        })
    return jsonify(result), 200


@products.route('/products', methods=['POST'])
def add_product():
    data = request.get_json(force=True)

    nouveau_produit = Product(
        nom=data['nom'],
        description=data.get('description'),
        prix=data['prix'],
        stock=data['stock'],
        categorie=data.get('categorie'),
        photo=data.get('photo'),
        id_vendeur=data['id_vendeur']
    )

    db.session.add(nouveau_produit)
    db.session.commit()

    return jsonify({'message': 'Produit ajouté avec succès'}), 201


@products.route('/products/search', methods=['GET'])
def search_products():
    categorie = request.args.get('categorie')
    prix_min = request.args.get('prix_min', 0, type=float)
    prix_max = request.args.get('prix_max', 999999, type=float)

    query = Product.query.filter(
        Product.prix >= prix_min,
        Product.prix <= prix_max
    )

    if categorie:
        query = query.filter(Product.categorie == categorie)

    liste = query.all()
    result = []
    for p in liste:
        result.append({
            'id': p.id,
            'nom': p.nom,
            'description': p.description,
            'prix': p.prix,
            'stock': p.stock,
            'categorie': p.categorie,
            'photo': p.photo,
            'id_vendeur': p.id_vendeur
        })
    return jsonify(result), 200


@products.route('/products/stock-alerte', methods=['GET'])
def stock_alerte():
    seuil = request.args.get('seuil', 5, type=int)
    liste = Product.query.filter(Product.stock <= seuil).all()
    result = []
    for p in liste:
        result.append({
            'id': p.id,
            'nom': p.nom,
            'stock': p.stock,
            'id_vendeur': p.id_vendeur
        })
    return jsonify(result), 200