Documentation API
Marketplace Multi-Vendeurs Intelligente
Backend Flask + MySQL
Équipe : Assaghir Chaymae · Riabi Bouchra · Messaudi Israe
1. Informations Générales
URL de base	http://127.0.0.1:5000
Format	JSON (Content-Type: application/json)
Framework	Python Flask + SQLAlchemy
Base de données	MySQL via phpMyAdmin

2. Sprint 1 — Authentification & Comptes
2.1 Inscription
Méthode	URL	Description
POST	/register	Créer un compte client ou vendeur
Corps de la requête (JSON) :
  "nom": "string"   // Nom complet
  "email": "string"   // Email unique
  "mot_de_passe": "string"   // Mot de passe
  "role": "acheteur" | "vendeur"   // Rôle de l'utilisateur
  "nom_boutique": "string"   // Obligatoire si vendeur
  "description_boutique": "string"   // Optionnel
Exemple de réponse :
{ "message": "Compte créé avec succès" }  → 201

2.2 Connexion
Méthode	URL	Description
POST	/login	Connexion et récupération des infos utilisateur
Corps de la requête (JSON) :
  "email": "string"   // Email
  "mot_de_passe": "string"   // Mot de passe
Exemple de réponse :
{
  "message": "Connexion réussie",
  "user": { "id": 1, "nom": "...", "role": "acheteur",
            "is_admin": false, "is_validated": false }
}  → 200

2.3 Administration des comptes
Méthode	URL	Description
GET	/admin/users	Lister tous les utilisateurs
PUT	/admin/users/<id>/valider	Valider un compte utilisateur
Exemple de réponse :
GET  → liste des utilisateurs avec statut is_validated
PUT  → { "message": "Compte de X validé avec succès" }  → 200

3. Sprint 2 — Produits & Stock
3.1 Ajouter un produit
Méthode	URL	Description
POST	/products	Ajouter un nouveau produit (vendeur)
Corps de la requête (JSON) :
  "nom": "string"   // Nom du produit
  "description": "string"   // Description (optionnel)
  "prix": number   // Prix en MAD
  "stock": number   // Quantité disponible
  "categorie": "string"   // Catégorie (optionnel)
  "photo": "string"   // Chemin image (optionnel)
  "id_vendeur": number   // ID du vendeur
Exemple de réponse :
{ "message": "Produit ajouté avec succès" }  → 201

3.2 Lister & Rechercher les produits
Méthode	URL	Description
GET	/products	Lister tous les produits
GET	/products/search	Rechercher par catégorie et prix
Exemple de réponse :
GET /products/search?categorie=Electronique&prix_min=100&prix_max=3000
→ liste filtrée des produits  → 200

3.3 Alertes stock
Méthode	URL	Description
GET	/products/stock-alerte	Produits avec stock <= seuil
Exemple de réponse :
GET /products/stock-alerte?seuil=5
→ [{ "id": 1, "nom": "...", "stock": 3, "id_vendeur": 1 }]  → 200

4. Commandes
4.1 Créer une commande
Méthode	URL	Description
POST	/orders	Créer une commande avec produits
Corps de la requête (JSON) :
  "id_acheteur": number   // ID de l'acheteur
  "total": number   // Montant total
  "produits": [...]   // Liste des produits commandés
  "  id_produit": number   // ID du produit
  "  quantite": number   // Quantité commandée
  "  prix_unitaire": number   // Prix unitaire
Exemple de réponse :
{ "message": "Commande créée avec succès" }  → 201

4.2 Lister les commandes
Méthode	URL	Description
GET	/orders	Lister toutes les commandes avec produits
Exemple de réponse :
[{ "id": 1, "id_acheteur": 1, "total": 2500.0,
   "statut": "en attente",
   "produits": [{ "id_produit": 1, "quantite": 1, "prix_unitaire": 2500 }] }]

5. Sprint 3 — Recommandations & Dashboard
5.1 Recommandations personnalisées
Méthode	URL	Description
GET	/recommandations/<id_user>	Produits recommandés pour un utilisateur
Exemple de réponse :
GET /recommandations/1
→ liste de 5 produits basée sur les achats précédents  → 200
→ Si aucun achat : 5 premiers produits du catalogue

5.2 Tableau de bord admin
Méthode	URL	Description
GET	/admin/dashboard	Statistiques globales de la plateforme
Exemple de réponse :
{
  "total_commandes": 1,
  "chiffre_affaires": 2500.0,
  "total_acheteurs": 2,
  "total_vendeurs": 1,
  "produits_rupture": 0,
  "top_produits": [{ "id": 1, "nom": "...", "quantite_vendue": 3 }]
}  → 200

6. Sprint 4 — Paiement
6.1 Paiement PayPal
Méthode	URL	Description
POST	/paiement/paypal	Simuler un paiement via PayPal
Corps de la requête (JSON) :
  "id_order": number   // ID de la commande à payer
Exemple de réponse :
{
  "message": "Paiement PayPal simulé avec succès",
  "id_order": 1, "montant": 2500.0,
  "statut": "payée via PayPal"
}  → 200

6.2 Paiement CMI (Carte Bancaire Marocaine)
Méthode	URL	Description
POST	/paiement/cmi	Simuler un paiement via CMI
Corps de la requête (JSON) :
  "id_order": number   // ID de la commande
  "numero_carte": "string"   // 16 chiffres obligatoires
Exemple de réponse :
{
  "message": "Paiement CMI simulé avec succès",
  "statut": "payée via CMI"
}  → 200

Erreur: { "message": "Numéro de carte invalide" }  → 400

7. Codes de Réponse HTTP
Code	Statut	Description
200	OK	Requête réussie
201	Created	Ressource créée avec succès
400	Bad Request	Données invalides ou manquantes
401	Unauthorized	Email ou mot de passe incorrect
404	Not Found	Ressource introuvable

8. Structure du Projet
marketplace-backend/
├── app/
│   ├── __init__.py          ← Configuration Flask & DB
│   ├── models/
│   │   ├── user.py          ← Table User
│   │   ├── product.py       ← Table Product
│   │   └── order.py         ← Tables Order & OrderItem
│   └── routes/
│       ├── auth.py          ← /register, /login
│       ├── products.py      ← /products, /products/search
│       ├── orders.py        ← /orders
│       ├── admin.py         ← /admin/users
│       ├── dashboard.py     ← /admin/dashboard
│       ├── recommandations.py ← /recommandations
│       └── paiement.py      ← /paiement/paypal, /paiement/cmi
└── run.py                   ← Point d'entrée
