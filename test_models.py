from app import app, db
from models import Member

with app.app_context():
    members = Member.query.all()
    for m in members:
        print(m.full_name, m.phone_number, m.email, m.gender)