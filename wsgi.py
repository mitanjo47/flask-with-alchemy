# wsgi.py
# pylint: disable=missing-docstring

BASE_URL = '/api/v1'

from flask import Flask, request
from config import Config
app = Flask(__name__)
app.config.from_object(Config)

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow 
db = SQLAlchemy(app)
ma = Marshmallow(app)

from models import Product
from flask_migrate import Migrate
from schemas import many_product_schema, one_product_schema

migrate = Migrate(app, db)

@app.route('/hello', methods=['GET'])
def hello():
    return "Hello World!", 200

@app.route(f'{BASE_URL}/products', methods=['GET'])
def get_many_product():
    products = db.session.query(Product).all() # SQLAlchemy request => 'SELECT * FROM products'
    return many_product_schema.jsonify(products), 200

@app.route(f'{BASE_URL}/products/<int:id>', methods=['GET'])
def get_one_product(id):
    product = db.session.query(Product).get(id)
    return one_product_schema.jsonify(product), 200

@app.route(f'{BASE_URL}/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    if db.session.query(Product).filter(Product.id == id).first() is None: return '', 404
    
    db.session.query(Product).filter(Product.id == id).delete()
    db.session.commit()
    
    return '', 204

@app.route(f'{BASE_URL}/products', methods=['PUT'])
def update_product():
    req = request.get_json()
    product_id = req['id']
    
    if db.session.query(Product).filter(Product.id == product_id).first() is None: return '', 404
    
    product = db.session.query(Product).filter(Product.id == product_id).first()
    if product is not None:
        product.name = req['name']
        product.descrpition = req['description']
        db.session.commit()

    return '', 204

@app.route(f'{BASE_URL}/products', methods=['POST'])
def save_product():
    req = request.get_json()
    
    product = Product()
    product.name = req['name']
    product.descrpition = req['description']
    
    db.session.add(product)
    db.session.commit()

    return '', 204