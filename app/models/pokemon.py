from app import db

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    types = db.Column(db.JSON)
    abilities = db.Column(db.JSON)
    sprite_url = db.Column(db.String(200))

    def __repr__(self):
        return f'<Pokemon {self.name}>'