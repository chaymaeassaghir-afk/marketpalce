from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/marketplace_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        from app.models.user import User
        from app.models.product import Product
        from app.models.order import Order, OrderItem
        db.create_all()

        from app.routes.auth import auth
        from app.routes.products import products
        from app.routes.admin import admin
        from app.routes.recommandations import recommandations
        from app.routes.dashboard import dashboard
        from app.routes.paiement import paiement
        from app.routes.orders import orders
        
        app.register_blueprint(orders)
        app.register_blueprint(auth)
        app.register_blueprint(products)
        app.register_blueprint(admin)
        app.register_blueprint(recommandations)
        app.register_blueprint(dashboard)
        app.register_blueprint(paiement)

    return app