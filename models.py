from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.orm import relationship

db = SQLAlchemy()

# Define the association table with foreign keys
favorite = db.Table('favorite',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('car_id', db.Integer, db.ForeignKey('cars.id'), primary_key=True)
)

# Define SQLAlchemy models
class Car(db.Model):
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(200), nullable=True)
    link = db.Column(db.String(200), nullable=True)
    price = db.Column(db.String(50), nullable=True)
    condition = db.Column(db.String(50), nullable=True)
    mileage = db.Column(db.String(50), nullable=True)
    engine = db.Column(db.String(50), nullable=True)
    transmission = db.Column(db.String(50), nullable=True)
    body_type = db.Column('Body Type', db.String(50), nullable=True)
    location = db.Column(db.String(100), nullable=True)
    loan_term_years = db.Column('Loan Term Years', db.Integer)
    coverage_type = db.Column('Coverage Type', db.String(20))
    ncd = db.Column('NCD', db.String(20))

    def __repr__(self):
        return f'<Car {self.id}: {self.brand}>'

    def to_dict(self):
        return {
            'id': self.id,
            'Brand': self.brand,
            'Image': self.image,
            'Link': self.link,
            'Price': self.price,
            'Condition': self.condition,
            'Mileage': self.mileage,
            'Engine': self.engine,
            'Transmission': self.transmission,
            'Body Type': self.body_type,
            'Location': self.location,
            'Loan term years': self.loan_term_years,
            'Coverage Type': self.coverage_type,
            'NCD': self.ncd
        }

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)  # Add this line


    # Relationship with the Car model via the favorite association table
    favorite_cars = relationship('Car', secondary='favorite', backref='users')

