
from application.extensions import *
from application.setup import app
from application.settings import *
from flask_login import UserMixin
db = SQLAlchemy(app)

migrate = Migrate(app, db)




class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    hashed_password = db.Column(db.Text, nullable=False)
    roles = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True, server_default="true")
    created_date = db.Column(db.DateTime(timezone=True), default=func.now())

    @property
    def unhashed_password(self):
        raise AttributeError('This is a write-only field.')

    @unhashed_password.setter
    def unhashed_password(self, password):
        # Implement password hashing here
        self.hashed_password = generate_password_hash(password)

    Receive_by  = db.relationship('Notiication', 
    foreign_keys ='Notiication.receive_by_id',
    backref = 'reciever',
    lazy=True
    
    )


    Sender_by  = db.relationship('Notiication', 
    foreign_keys ='Notiication.doctor_id',
    backref = 'sender',
    lazy=True
    
    )
    
    

  


    answers_requested  = db.relationship('Ads', 
    foreign_keys ='Ads.post_by_id',
    backref = 'seller',
    lazy=True
    
    )


    promo_by  = db.relationship('Promo_request', 
    foreign_keys ='Promo_request.promo_by_id',
    backref = 'promoter',
    lazy=True
    
    )



class Notiication(db.Model):

    id = db.Column(db.Integer,primary_key =True)
    name = db.Column(db.String(100))
    message = db.Column(db.String(100))
    #email = db.Column(db.String(100))
   # date = db.Column(db.String(100))request.args
    receive_by_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    doctor_id = db.Column(db.Integer,db.ForeignKey('user.id'))



class Ads(db.Model):
   
    id = db.Column(db.Integer,primary_key =True)
    condition = db.Column(db.String(255))
    phone = db.Column(db.String(233))
    category = db.Column(db.String(255))
    description = db.Column(db.String(255))
    brand = db.Column(db.String(255))
    negotiable = db.Column(db.String(255))
    price = db.Column(db.String(255))
    city = db.Column(db.String(255))
    post_by_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    image = db.Column(db.String(4000))
    image_name = db.Column(db.String(255))
    mimetype =  db.Column(db.String(255))
    post_on = db.Column(DateTime(timezone=True), default=func.now())
    


class Promote(db.Model):

    id = db.Column(db.Integer,primary_key =True)
    condition = db.Column(db.String(255))
    phone = db.Column(db.String(233))
    category = db.Column(db.String(255))
    description = db.Column(db.String(255))
    brand = db.Column(db.String(255))
    negotiable = db.Column(db.String(255))
    price = db.Column(db.String(255))
    city = db.Column(db.String(255))
    promo_by_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    image = db.Column(LargeBinary)
    image_name = db.Column(db.String(255))
    mimetype =  db.Column(db.String(255))
    post_on = db.Column(DateTime(timezone=True), default=func.now())
    promoted_on = db.Column(DateTime(timezone=True), default=func.now())

class  news_letter(db.Model):
    id = db.Column(db.Integer,primary_key =True)
    email = db.Column(db.String(200),unique=True)

class Promo_request(db.Model):

    id = db.Column(db.Integer,primary_key =True)
    condition = db.Column(db.String(255))
    phone = db.Column(db.String(233))
    category = db.Column(db.String(255))
    description = db.Column(db.String(255))
    brand = db.Column(db.String(255))
    negotiable = db.Column(db.String(255))
    price = db.Column(db.String(255))
    city = db.Column(db.String(255))
    promo_by_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    image = db.Column(LargeBinary)
    image_name = db.Column(db.String(255))
    mimetype =  db.Column(db.String(255))
    post_on = db.Column(DateTime(timezone=True), default=func.now())
    #post_by_id = db.Column(db.Integer,db.ForeignKey('user.id'))

class Cart(db.Model):

        id = db.Column(db.Integer,primary_key =True)
        sr_no = db.Column(db.String(200))
        name = db.Column(db.String(255))
        quantity = db.Column(db.String(233))
        price = db.Column(db.String(255))
        description = db.Column(db.String(255))
        totalcost = db.Column(db.String(255))
   
    
    