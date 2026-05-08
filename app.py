from flask import Flask
from flask_cors import CORS
from config import db, Config
from routes.member_routes import members_bp
from routes.trainer_routes import trainer_bp
from routes.plan_routes import plan_bp
from routes.subscription_routes import subscription_bp
from routes.payment_routes import payment_bp
from routes.class_routes import class_bp
from routes.booking_routes import booking_bp
from routes.attendance_routes import attendance_bp


# Create Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS for all routes
CORS(app)

# Initialize database
db.init_app(app)

# Register routes
app.register_blueprint(members_bp, url_prefix='/api')
app.register_blueprint(trainer_bp, url_prefix='/api')
app.register_blueprint(plan_bp, url_prefix='/api')
app.register_blueprint(subscription_bp, url_prefix='/api')
app.register_blueprint(payment_bp, url_prefix='/api')
app.register_blueprint(class_bp, url_prefix='/api')
app.register_blueprint(booking_bp, url_prefix='/api')
app.register_blueprint(attendance_bp, url_prefix='/api')


# Create tables
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)