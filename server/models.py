# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import MetaData
# from sqlalchemy.orm import validates
# from sqlalchemy.ext.associationproxy import association_proxy
# from sqlalchemy_serializer import SerializerMixin

# convention = {
#     "ix": "ix_%(column_0_label)s",
#     "uq": "uq_%(table_name)s_%(column_0_name)s",
#     "ck": "ck_%(table_name)s_%(constraint_name)s",
#     "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
#     "pk": "pk_%(table_name)s"
# }

# metadata = MetaData(naming_convention=convention)

# db = SQLAlchemy(metadata=metadata)


# class Activity(db.Model, SerializerMixin):
#     __tablename__ = 'activities'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     difficulty = db.Column(db.Integer)

#     # Add relationship
    
#     # Add serialization rules
    
#     def __repr__(self):
#         return f'<Activity {self.id}: {self.name}>'


# class Camper(db.Model, SerializerMixin):
#     __tablename__ = 'campers'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, nullable=False)
#     age = db.Column(db.Integer)

#     # Add relationship
    
#     # Add serialization rules
    
#     # Add validation
#     @validates('age')
#     def validateAge(self, key, age):
#         if age and 8 <= int(age) <=18:
#             return age
#         else:
#             raise ValueError('Not a valid age')
    
    
    
    
#     def __repr__(self):
#         return f'<Camper {self.id}: {self.name}>'


# class Signup(db.Model, SerializerMixin):
#     __tablename__ = 'signups'

#     id = db.Column(db.Integer, primary_key=True)
#     time = db.Column(db.Integer)

#     # Add relationships
#     camper_id = db.Column(db.String, db.ForeignKey('campers.id'))
#     activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'))

#     camper = db.relationship("Camper", "signups")
#     activity = db.relationship("Activity", "signups")
    
#     # Add serialization rules
    
#     # Add validation
#     @validates('time')
#     def validateTime(self, key, time):
#         if time and 0<= int(time) <=23:
#             return time
#         else:
#             raise ValueError('Not a valid time')
    
#     def __repr__(self):
#         return f'<Signup {self.id}>'


# add any models you may need.











from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    difficulty = db.Column(db.Integer)

    # Add relationship
    signups = db.relationship("Signup", backref="activity",cascade="all, delete-orphan")

    # Add serialization rules
    serialize_rules = ('-signups.activity',)
    def __repr__(self):
        return f'<Activity {self.id}: {self.name}>'


class Camper(db.Model, SerializerMixin):
    __tablename__ = 'campers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)

    # Add relationship
    
    # Add serialization rules
    serialize_rules = ("-signups.camper",)
    # Add validation
    @validates("age")
    def ageValidator(self, key, value):
        if value and 8<=value<=18:
            return value
        else:
            raise ValueError("Not valid Age")
    
    
    def __repr__(self):
        return f'<Camper {self.id}: {self.name}>'


class Signup(db.Model, SerializerMixin):
    __tablename__ = 'signups'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer)
    camper_id = db.Column(db.Integer, db.ForeignKey("campers.id"))
    activity_id = db.Column(db.Integer, db.ForeignKey("activities.id"))

    # Add relationships
    camper = db.relationship("Camper", backref="signups")
    # activity = db.relationship("Activity", backref=(backref("signups"),cascade="all, delete-orphan"))
    # Add serialization rules
    serialize_rules = ("-camper.signups","-activity.signups")
    # Add validation
    @validates("time")
    def ageValidator(self, key, value):
        if 0<=int(value)<=23:
            return value
        else:
            raise ValueError("Not valid Time")

    def __repr__(self):
        return f'<Signup {self.id}>'
