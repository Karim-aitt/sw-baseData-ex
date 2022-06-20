from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    uid = db.Column(db.Integer, unique=True)
    # favorites = db.relationship('Favorite', backref='people', lazy=True)
    favorites2 = db.relationship('PeopleFavorites', backref='people', lazy=True)

    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "uid": self.uid
            # do not serialize the password, its a security breach
        }

class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    uid = db.Column(db.Integer, unique=True)
    # favorites = db.relationship('Favorite', backref='planets', lazy=True)
    favorites2 = db.relationship('PlanetsFavorites', backref='planets', lazy=True)

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "uid": self.uid
            # do not serialize the password, its a security breach
        }

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)
    # favorites = db.relationship('Favorite', backref='user', lazy=True)
    favorites2 = db.relationship('PeopleFavorites', backref='user', lazy=True)
    favorites3 = db.relationship('PlanetsFavorites', backref='user', lazy=True)


    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            # do not serialize the password, its a security breach
        }

# class Favorite(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     people_id = db.Column(db.Integer, db.ForeignKey('people.id'))
#     planets_id = db.Column(db.Integer, db.ForeignKey('planets.id'))

#     def __repr__(self):
#         return '<Favorite %r>' % self.user_id
         

#     def serialize(self):
#         return {
#             "user_id": self.user_id,
#             "people_id": self.people_id,
#             "planets_id": self.planets_id
#             # do not serialize the password, its a security breach
#         }

class PeopleFavorites(db.Model):
    __tablename__ = 'peoplefavorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'))
    favorites = db.relationship('Favorites', backref='peoplefavorites', lazy=True)

    def __repr__(self):
        return 'PeopleFavorites %r>' % self.user_id
    
    def serialize(self):
        return {
            'user_id': self.user_id,
            'people_id': self.people_id
        }

class PlanetsFavorites(db.Model):
    __tablename__ = 'planetsfavorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    planets_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    favorites = db.relationship('Favorites', backref='planetsfavorites', lazy=True)

    def __repr__(self):
        return 'PlanetsFavorites %r>' % self.user_id
    
    def serialize(self):
        return {
            'user_id': self.user_id,
            'planets_id': self.planets_id
        }

class Favorites(db.Model):
    __tablename__= 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    people_id = db.Column(db.Integer, db.ForeignKey('peoplefavorites.id'))
    planets_id = db.Column(db.Integer, db.ForeignKey('planetsfavorites.id'))

    def __repr__(self):
        return 'PeopleFavorites %r>' % self.user_id
    
    def serialize(self):
        return {
            'user_id': self.user_id,
            'people_id': self.people_id,
            'planets_id': self.planets_id
        }
