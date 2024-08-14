#================ wt forms ====#
from application.extensions import *
from application.setup import app
from application.settings import *
# from application.db import User,db

app.config['RECAPTCHA_PUBLIC_KEY']= '6LccceQaAAAAAFVTwhHp1SNNwddLxhpybkazgKYw'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LccceQaAAAAALRTre2F1LYBWHpykc9Fgv5ATkcd'



app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'jxkalmhefacbuk@gmail.com'
app.config['MAIL_PASSWORD'] = 'dfilwxnwpcalytdv'


"""
app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'jxkalmhefacbuk@gmail.com',
    MAIL_PASSWORD = 'kelvin7322',

))
"""
ma = Marshmallow(app)
api =Api(app)
mail = Mail(app)
cors =CORS(app)
guard = flask_praetorian.Praetorian()

app.secret_key = 'secrete key'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ovxhjvutjqmfvj:91d29e4a9e788f1c2119cd262283c6941168af9371cbe7a650f95dbcfd027d7e@ec2-54-147-93-73.compute-1.amazonaws.com:5432/d3u17er50p9k52'
#
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'
#local_database = tempfile.NamedTemporaryFile(prefix="local", suffix=".db")
app.config['SECRET_KEY'] = '0527'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TESTING'] = False
app.config["JWT_ACCESS_LIFESPAN"] = {"hours": 24}
app.config["JWT_REFRESH_LIFESPAN"] = {"days": 30}


login_manager = LoginManager()
login_manager.init_app(app )
login_manager.login_view = 'login'

# guard.init_app(app, User)

