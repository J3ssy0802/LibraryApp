from flask import Flask
from .models import db
from .blueprints.members import members_bp
from .blueprints.books import books_bp
from .blueprints.loans import loans_bp
from .extensions import ma, limiter, cache
from .blueprints.items import items_bp
from .blueprints.orders import orders_bp
from flask_swagger_ui import get_swaggerui_blueprint

# Swagger UI setup
SWAGGER_URL = '/api/docs' #URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.yaml' #Our API url (can of course be a local resource)

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Library Management System API"
    }
)

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')
    
    #initialize extensions
    ma.init_app(app)
    db.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)
    
    #register blueprints
    app.register_blueprint(members_bp, url_prefix='/members')
    app.register_blueprint(books_bp, url_prefix='/books')
    app.register_blueprint(loans_bp, url_prefix='/loans')
    app.register_blueprint(items_bp, url_prefix='/items')
    app.register_blueprint(orders_bp, url_prefix='/orders')
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL) # Register Swagger UI blueprint    
    
    
    return app