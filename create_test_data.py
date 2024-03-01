from models import db, Pigeon, User, PigeonHierarchy

# Create a test user
user = User(email="aw3338@drexel.edu", password="password", name="Ao Wang")
db.session.add(user)
db.session.commit()

# Create a test pigeons
