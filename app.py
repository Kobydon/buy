
from flask.helpers import make_response
from sqlalchemy.sql.functions import current_time
from  application.extensions import *
from  application.settings import *
from  application.setup import app
from application.forms import LoginForm
from application.db import db,Ads,User,Promote,Promo_request, news_letter,Cart
from sqlalchemy import or_,desc,and_
from datetime import datetime
from datetime import date
from flask import session
# from flask_login import login_manager, login_required, current_user

# from flask_login  import LoginManager,UserMixin,login_user,login_required,logout_user,current_user

#app = Flask(__name__)

#ap = SQLAlchemy(app)





    

    
    #doctor_id = db.Column(db.Integer,db.ForeignKey('user.id'))

class AdSchema(ma.Schema):
    class Meta:
        # Fields to ,,"category","post_on","price","image"
        fields = ("id","brand","category","post_on","price","image",
        "negotiable","phone","price","description","condition","city"
        
        )


class Userchema(ma.Schema):
    class Meta:
        # Fields to ,,"category","post_on","price","image"
        fields = ("id","username"
        
        )
     # Smart hyperlinking
   
ad_schema = AdSchema()
ads_schema = AdSchema(many=True)

user_schema = AdSchema()
users_schema = AdSchema(many=True)
  
  



 

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized_callback():
    flash('Register to access')
    return redirect(url_for('register'))

# @login_manager.unauthorized_handler
# def unauthorized_callback():
#      flash('register to access')
#      return redirect(url_for('register'))


#from admin.second import second


#app.register_blueprint(second,url_prefix ="/admin")'





# Initialize flask app for the example


# Initialize the flask-praetorian instance for the app


#================== veiws=============#
@app.route('/')

def home():
    all_goods = Promote.query.all()
    #all = Ads.query.all()
    current_time = datetime.now()
    page = request.args.get('page',1,type=int)
    allm = Ads.query.paginate(per_page=20,page =page,error_out=True)
  #  if current_user.is_authenticated: 
        #respurn redirect(url_for('dashboard'))

    #else:
    return render_template('index.html',all_goods=all_goods,allm=allm)




@app.route("/header")
def header():
    return render_template('header.html')

@app.route("/register")
def register():
    form = LoginForm()
    return render_template('register.html',form=form)


@app.route("/login")
def login():
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
     logout_user()
     return redirect('/login') 
    



@app.route("/userprofile/<id>")
def userprofile(id):
    user = User.query.get(id)
    results = user_schema.dump(user)
    return jsonify(results)


@app.route('/edit_profile')
@login_required
def edit_profile():
    owner = User.query.filter_by(username=current_user.username,hashed_password=current_user.hashed_password,roles="operator").first()
    #imb = Ads.query.filter_by(post_by_id=current_user.id).all()
    #mimetype = db.session.query(Ads).filter_by(mimetype=True).all()
    #roww = db.session.query(Appointments).filter_by(asked_by_id = current_user.id).count()
    #m_count = db.session.query(Notiication).filter_by(receive_by_id = current_user.id).count()
    if not owner:

          flash("Kindly login to access page")
          return redirect(url_for('home'))
     
    else:
          
        return render_template('edit_profile.html') 



@app.route('/buy')
@login_required
def buy():
    owner = User.query.filter_by(username=current_user.username,password=current_user.password,admin=False).first()
    #imb = Ads.query.filter_by(post_by_id=current_user.id).all()
    #mimetype = db.session.query(Ads).filter_by(mimetype=True).all()
    #roww = db.session.query(Appointments).filter_by(asked_by_id = current_user.id).count()
    #m_count = db.session.query(Notiication).filter_by(receive_by_id = current_user.id).count()
    if not owner:

          flash("Kindly login to access page")
          return redirect(url_for('home'))
     
    else:
          
        return render_template('buy.html') 



@app.route('/post')
@login_required
def post():
    return render_template('post.html')

@app.route('/dashboard')
@login_required
def dashboard():
    # Current logged-in user
    user = current_user

    # Fetch all ads posted by the current user
    all_goods = Ads.query.filter_by(post_by_id=current_user.id).all()

    # Pagination for ads with filtering based on the current date
    page = request.args.get('page', 1, type=int)
    imb = Ads.query.filter(Ads.post_by_id == current_user.id).paginate(per_page=20, page=page, error_out=True)

    # Count the number of ads posted by the user
    roww = Ads.query.filter_by(post_by_id=current_user.id).count()

    return render_template('dashboard.html', imb=imb, all_goods=all_goods, row=roww)


@app.route('/all_ads')
@login_required
def all_ads():

  
    owner = User.query.filter_by(username=current_user.username,hashed_password=current_user.hashed_password,roles="admin").first()
    all_goods = db.session.query(Ads).all()
    imb = db.session.query(Ads).all()
   
    roww = db.session.query(Ads).count()
    roww_user = db.session.query(User).count()
    #m_count = db.session.query(Notiication).filter_by(receive_by_id = current_user.id).count()
    if not owner:

          flash("Kindly login to access page")
          return redirect(url_for('home'))
     
    else:
          
          return render_template('all_ads.html',imb=imb,all_goods=all_goods,row=roww,roww_user=roww_user)






@app.route('/all_promo')
@login_required
def all_promo():

  
    owner = User.query.filter_by(username=current_user.username,hashed_password=current_user.hashed_password,roles="admin").first()
    all_goods = db.session.query(Promo_request).all()
    prms = db.session.query(Promote).all()
   
    roww = db.session.query(Ads).count()
    roww_user = db.session.query(User).count()
    #m_count = db.session.query(Notiication).filter_by(receive_by_id = current_user.id).count()
    if not owner:

          flash("Kindly login to access page")
          return redirect(url_for('home'))
     
    else:
          
          return render_template('promo_request.html',prms=prms,all_goods=all_goods,row=roww,roww_user=roww_user)


#=========terms  ====================#

@app.route("/terms")
def terms():
    return render_template('terms.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/google")
def google():
    return render_template('googlef15c7c66cdfca88d.html')


@app.route("/contact")
def contact():
    return render_template('contact.html')

#====================================#
  #============= category===============  

@app.route('/electronics')
def electronics():
    #owner = User.query.filter_by(username=current_user.username,password=current_user.password,admin=False).first()
    page = request.args.get('page',1,type=int)
    current_time = datetime(datetime.today().year,
    datetime.today().month,
    datetime.today().day)
   
    
    start = datetime(year=2021,month=5,day=1)
    end = datetime(year=2021,month=9,day=1)




    imb = Ads.query.filter_by(category='electronics').order_by(Ads.post_on>=current_time).paginate(per_page=20,page =page,error_out=True)
    prmo = Promote.query.all()
    selected_page = request.args.get('type')
    
   
    #roww = db.session.query(Appointments).filter_by(asked_by_id = current_user.id).count()
    #m_count = db.session.query(Notiication).filter_by(receive_by_id = current_user.id).count()

    if  selected_page == 'vehicle_new':

                
        
                 imb = Ads.query.filter(Ads.post_on<=current_time,Ads.condition=='new' , Ads.category=='vehicle').paginate(per_page=20,page =page,error_out=True)
                 return render_template('electronics.html',imb=imb,prmo=prmo)
                



    if selected_page == 'vehicle_old':

                 imb = Ads.query.filter(Ads.post_on<=current_time,Ads.condition=='old',Ads.category=='vehicle').paginate(per_page=20,page =page,error_out=True)
                 return render_template('electronics.html',imb=imb,prmo=prmo)



    if  selected_page == 'electronics_new':

        
                 imb = Ads.query.filter(Ads.post_on<=current_time,Ads.condition=='new', Ads.category=='electronics').paginate(per_page=20,page =page,error_out=True)
                 return render_template('electronics.html',imb=imb,prmo=prmo)
                
            

    if selected_page == 'electronics_old':
        

                 imb = Ads.query.filter() .paginate(per_page=20,page =page,error_out=True)
                 return render_template('electronics.html',imb=imb,prmo=prmo)






    if  selected_page == 'electronics':
            

        
                 query_list = db.session.query(Ads).filter(Ads.category=="electronics")
                 imb =  query_list.order_by(desc(Ads.post_on)).paginate(per_page=20,page =page,error_out=True)
                 return render_template('electronics.html',imb=imb,prmo=prmo)

                

    if selected_page == 'education':

                 imb = Ads.query.filter(Ads.post_on<=current_time,Ads.category=='education').paginate(per_page=20,page =page,error_out=True)
                 return render_template('electronics.html',imb=imb,prmo=prmo)


    if  selected_page == 'sports':

        
                 imb = Ads.query.filter(Ads.post_on<=current_time,Ads.category=='sports').paginate(per_page=20,page =page,error_out=True)
                 return render_template('electronics.html',imb=imb,prmo=prmo)
                
                

    if selected_page == 'vehicle':

                 imb = Ads.query.filter(Ads.post_on<=current_time,Ads.category=='vehicle').paginate(per_page=20,page =page,error_out=True)
                 return render_template('electronics.html',imb=imb,prmo=prmo)

    if  selected_page == 'others':

        
                 imb = Ads.query.filter(Ads.post_on<=current_time,Ads.category=='other').paginate(per_page=20,page =page,error_out=True)
                 return render_template('electronics.html',imb=imb,prmo=prmo)
                
    if  selected_page == 'clothing':

        
                 imb = Ads.query.filter(Ads.post_on<=current_time,Ads.category=='clothing').paginate(per_page=20,page =page,error_out=True)
                 return render_template('electronics.html',imb=imb,prmo=prmo)
               
                          

    if selected_page == 'jobs':

                 imb = Ads.query.filter(Ads.post_on<=current_time,Ads.post_on<=current_time,Ads.category=='jobs').paginate(per_page=20,page =page,error_out=True)
                 return render_template('electronics.html',imb=imb,prmo=prmo)
               
                 
    if  selected_page == 'property':

        
                 imb = Ads.query.filter(Ads.post_on<=current_time,Ads.category=='property').paginate(per_page=20,page =page,error_out=True)
                 return render_template('electronics.html',imb=imb,prmo=prmo)
                
                

                 
    else:
 
        return render_template('electronics.html',imb=imb,prmo=prmo)



@app.route('/ads/<int:id>')
def ads(id):
    #owner = User.query.filter_by(username=current_user.username,password=current_user.password,admin=False).first()
    imb = db.session.query(Promote).filter_by(id=id).all()
  
   # gt= Promote.query.get(id)
    # User.query.get(request.form.get('id'))
    prmo = db.session.query(Promote).filter_by(promo_by_id=User.id).all()
   
    #roww = db.session.query(Appointments).filter_by(asked_by_id = current_user.id).count()
    #m_count = db.session.query(Notiication).filter_by(receive_by_id = current_user.id).count()
 
    return render_template('ads.html',imb=imb,prmo=prmo)

    

@app.route('/ads_link/<int:id>')
def ads_link(id):
    #owner = User.query.filter_by(username=current_user.username,password=current_user.password,admin=False).first()
    imb = db.session.query(Ads).filter_by(id=id).all()
  
   # gt= Promote.query.get(id)
    # User.query.get(request.form.get('id'))
    prmo = db.session.query(Ads).filter_by(post_by_id=User.id).all()
   
    #roww = db.session.query(Appointments).filter_by(asked_by_id = current_user.id).count()
    #m_count = db.session.query(Notiication).filter_by(receive_by_id = current_user.id).count()
 
    return render_template('ads_link.html',imb=imb,prmo=prmo)

    

@app.route('/education')
def education():
    #owner = User.query.filter_by(username=current_user.username,password=current_user.password,admin=False).first()
    page = request.args.get('page',1,type=int)
    imb = Ads.query.filter_by(category='education').paginate(per_page=20,page =page,error_out=True)
    prmo = Promote.query.all()
   
    #roww = db.session.query(Appointments).filter_by(asked_by_id = current_user.id).count()
    #m_count = db.session.query(Notiication).filter_by(receive_by_id = current_user.id).count()
 
    return render_template('education.html',imb=imb,prmo=prmo)

    

@app.route('/sports')
def sports():
    #owner = User.query.filter_by(username=current_user.username,password=current_user.password,admin=False).first()
    page = request.args.get('page',1,type=int)
    imb = Ads.query.filter_by(category='sports').paginate(per_page=20,page =page,error_out=True)
    prmo = Promote.query.all()
   
    #roww = db.session.query(Appointments).filter_by(asked_by_id = current_user.id).count()
    #m_count = db.session.query(Notiication).filter_by(receive_by_id = current_user.id).count()
 
    return render_template('sports.html',imb=imb,prmo=prmo)

    

@app.route('/clothing')
def clothing():
    #owner = User.query.filter_by(username=current_user.username,password=current_user.password,admin=False).first()
    page = request.args.get('page',1,type=int)
    imb = Ads.query.filter_by(category='clothing').paginate(per_page=20,page =page,error_out=True)
    prmo = Promote.query.all()
   
    #roww = db.session.query(Appointments).filter_by(asked_by_id = current_user.id).count()
    #m_count = db.session.query(Notiication).filter_by(receive_by_id = current_user.id).count()
 
    return render_template('clothing.html',imb=imb,prmo=prmo)




    

@app.route('/property')
def property():
    #owner = User.query.filter_by(username=current_user.username,password=current_user.password,admin=False).first()
    page = request.args.get('page',1,type=int)
  
    imb = Ads.query.filter_by(category='property').paginate(per_page=20,page =page,error_out=True)
    prmo = Promote.query.all()
   
    #roww = db.session.query(Appointments).filter_by(asked_by_id = current_user.id).count()
    #m_count = db.session.query(Notiication).filter_by(receive_by_id = current_user.id).count()
 
    return render_template('property.html',imb=imb,prmo=prmo)


@app.route('/jobs')
def jobs():
    #owner = User.query.filter_by(username=current_user.username,password=current_user.password,admin=False).first()
    page = request.args.get('page',1,type=int)
  
    imb = Ads.query.filter_by(category='jobs').paginate(per_page=1,page =page,error_out=True)
   
    #roww = db.session.query(Appointments).filter_by(asked_by_id = current_user.id).count()
    #m_count = db.session.query(Notiication).filter_by(receive_by_id = current_user.id).count()
 
    return render_template('jobs.html',imb=imb)

@app.route('/vehicle')
def vehicle():
    #owner = User.query.filter_by(username=current_user.username,password=current_user.password,admin=False).first()
    imb = Ads.query.filter_by(category='vejicle').all()
    prmo = Promote.query.all()
   
    #roww = db.session.query(Appointments).filter_by(asked_by_id = current_user.id).count()
    #m_count = db.session.query(Notiication).filter_by(receive_by_id = current_user.id).count()
 
    return render_template('vehicle.html',imb=imb,prmo=prmo)



@app.route('/other')
def other():
    #owner = User.query.filter_by(username=current_user.username,password=current_user.password,admin=False).first()
    page = request.args.get('page',1,type=int)
    imb = Ads.query.filter_by(category='other').paginate(per_page=1,page =page,error_out=True)
    prmo = Promote.query.all()
   
    #roww = db.session.query(Appointments).filter_by(asked_by_id = current_user.id).count()
    #m_count = db.session.query(Notiication).filter_by(receive_by_id = current_user.id).count()
 
    return render_template('other.html',imb=imb,prmo=prmo)

#======================= city ================#
@app.route('/kumasi')
def kumasi():
    #owner = User.query.filter_by(username=current_user.username,password=current_user.password,admin=False).first()
    page = request.args.get('page',1,type=int)
  
    imb = Ads.query.filter_by(city='Kumasi').paginate(per_page=20,page =page,error_out=True)
    prmo = Promote.query.all()
   
    #roww = db.session.query(Appointments).filter_by(asked_by_id = current_user.id).count()
    #m_count = db.session.query(Notiication).filter_by(receive_by_id = current_user.id).count()
 
    return render_template('Kumasi.html',imb=imb,prmo=prmo)

@app.route('/accra')
def accra():
    #owner = User.query.filter_by(username=current_user.username,password=current_user.password,admin=False).first()
    page = request.args.get('page',1,type=int)
  
    imb = Ads.query.filter_by(city='Accra').paginate(per_page=20,page =page,error_out=True)
    prmo = Promote.query.all()
   
    #roww = db.session.query(Appointments).filter_by(asked_by_id = current_user.id).count()
    #m_count = db.session.query(Notiication).filter_by(receive_by_id = current_user.id).count()
 
    return render_template('accra.html',imb=imb,prmo=prmo)

@app.route('/takoradi')
def takoradi():
    #owner = User.query.filter_by(username=current_user.username,password=current_user.password,admin=False).first()
    page = request.args.get('page',1,type=int)
  
    imb = Ads.query.filter_by(city='Sekondi').paginate(per_page=20,page =page,error_out=True)
    prmo = Promote.query.all()
   
    #roww = db.session.query(Appointments).filter_by(asked_by_id = current_user.id).count()
    #m_count = db.session.query(Notiication).filter_by(receive_by_id = current_user.id).count()
 
    return render_template('takoradi.html',imb=imb,prmo=prmo)


#=====================Subscribe============================#
@app.route('/Subscribe',methods=['POST','GET'])
def Subscribe():
    em = request.form['email']
    news_letter(email=em)
    
    flash("you have successfully subscribed")
    return redirect(url_for('home'))


#======================= Register ============================#



@app.route('/register_client', methods=['POST', 'GET'])
def register_client():
    if request.method == 'POST':
        username = request.form.get('username')
        unhashed_password = request.form.get('password')
        pswrepeat = request.form.get('pswrepeat')

        # Validate form data
        if not username or not unhashed_password or not pswrepeat:
            flash("Please fill in all fields")
            return redirect(url_for('register'))

        if unhashed_password != pswrepeat:
            flash("Passwords do not match")
            return redirect(url_for('register'))

        # Hash the password
        hashed_password = generate_password_hash(unhashed_password, method='sha256')

        # Create a new user
        user = User(username=username, hashed_password=hashed_password, roles="operator")
        db.session.add(user)
        db.session.commit()

        # Log the user in
        login_user(user)

        flash("Registration successful")
        return redirect(url_for('dashboard'))

    # Render the registration page (GET request)
    return render_template('register.html')


 #=================== Login =====================# 
    






# @app.route('/protected')
# @flask_praetorian.auth_required
# def protected():
#     """
#     A protected endpoint. The auth_required decorator will require a header
#     containing a valid JWT
#     .. example::
#        $ curl http://localhost:5000/protected -X GET \
#          -H "Authorization: Bearer <your_token>"
#     """
#     return jsonify(message='protected endpoint (allowed user {})'.format(
#         flask_praetorian.current_user().username,
#     ))


# @app.route('/disable_user', methods=['POST'])
# @flask_praetorian.auth_required
# @flask_praetorian.roles_required('admin')
# def disable_user():
#     """
#     Disables a user in the data store
#     .. example::
#         $ curl http://localhost:5000/disable_user -X POST \
#           -H "Authorization: Bearer <your_token>" \
#           -d '{"username":"Walter"}'
#     """
#     req = request.get_json(force=True)
#     usr = User.query.filter_by(username=req.get('username', None)).one()
#     usr.is_active = False
#     db.session.commit()
#     return jsonify(message='disabled user {}'.format(usr.username))



@app.route('/get_signin_client', methods=['GET', 'POST'])
def get_signin_client():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Retrieve the user from the database
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.hashed_password, password):
            # Log the user in
            login_user(user)
            flash("Sign in successful")
            return redirect(url_for('dashboard'))
        else:
            flash("Wrong username or password")

    # Render the sign-in form
    return render_template('signin.html')


# @app.route("/current_user")
# @flask_praetorian.auth_required
# def current_user():
#     return jsonify( message="protected endpoint (allowed user {})".format(
#             flask_praetorian.current_user().username,))



@app.route('/get_signin_admin',methods=['GET','POST'] )
#@login_required
def get_signin_admin(): 
      #user_man = User.query.all()  
      #doc_appoint = Appointments.query.filter_by(doctor_id =current_user.id).all()
      #rows = db.session.query(Appointments.doctor_id == current_user.id).count()
      username = request.form['username']
      password = request.form['password']
      owner =  owner= User.query.filter_by(username=username).first()
      if not owner or  not check_password_hash(owner.hashed_password,password):
          flash("wrong email or password !")
          return redirect(url_for('home'))

      else:
        login_user(owner)
        flash("welcome")
     
        return redirect(url_for('admin_dashboard'))

@app.route("/login_admin")
def login_admin():
    return render_template("login_admin.html")
     
@app.route("/admin_dashboard")
@login_required
def admin_dashboard():
    
    owner = User.query.filter_by(username=current_user.username,hashed_password=current_user.hashed_password,roles="admin").first()
    all_goods = Ads.query.filter_by(post_by_id = current_user.id).all()
    imb = db.session.query(Ads).all()
   
    roww = db.session.query(Ads).count()
    roww_user = db.session.query(User).count()
    #m_count = db.session.query(Notiication).filter_by(receive_by_id = current_user.id).count()
    if not owner:

          flash("Kindly login to access page")
          return redirect(url_for('home'))
     
    else:
          
          return render_template('admin_dash.html',imb=imb,row=roww,roww_user=roww_user)

@app.route("/all_users")
@login_required
def all_users():
    
    owner = User.query.filter_by(username=current_user.username,hashed_password=current_user.hashed_password,roles="admin").first()
    all_goods = Ads.query.filter_by(post_by_id = current_user.id).all()
    imb = db.session.query(Ads).all()
    users = db.session.query(User).all()
   
   
    roww = db.session.query(Ads).count()
    roww_user = db.session.query(User).count()
    #m_count = db.session.query(Notiication).filter_by(receive_by_id = current_user.id).count()
    if not owner:

          flash("Kindly login to access page")
          return redirect(url_for('home'))
     
    else:
          
          return render_template('all_users.html',imb=imb,all_goods=all_goods,row=roww,roww_user=roww_user,users=users)

     
 


    #---------------------angular => API -------------------------------------#
@app.route("/ads_by_user/")
# @flask_praetorian.auth_required

def ads_by_user():
    #row= db.session.query(User)
   
    #if 'username' in session:
    
    all_ads = Ads.query.filter_by(post_by_id = flask_praetorian.current_user().id)
    results = ads_schema.dump(all_ads)
    resp =  make_response(jsonify(results), 201) 
    # resp.status_code = 200
   
    return  (resp)

@app.route("/cart",methods=['GET','POST'])
def cart():
        req = request.get_json()
        json_data = request.form
        for  s in range(len(json_data)):
            # if json_data[s]["brand"]:
            #     name =json_data[s]["brand"]
            # if json_data[s]["sr_no"]:
            #     sr_no = json_data[s]["sr_no"]

            if json_data[s]["quantity" and "price" and "descritpion"
                and "brand" and "total"]:

                quantity =json_data[s]["quantity"]
                name =json_data[s]["brand"]
                price = json_data[s]["price"]
                description = json_data[s]["description"]
                totalcost =json_data[s]["total"]
           
            # if json_data[s]["price"]:
            #     price = json_data[s]["price"]
            #     name =json_data[s]["price"]

            # if json_data[s]["description"]:
            #     description = json_data[s]["description"]

            # if json_data[s]["total"]:
            #     totalcost =json_data[s]["total"]
       
        # quantity =json_data["quantity"]
        # price = json_data["price"]
        # description = json_data["description"]
        # totalcost = json_data["totalcost"]
            cart = Cart(sr_no=1,name=name,quantity=quantity,price=price,description=description,totalcost=totalcost)
            db.session.add(cart)
            db.session.commit()
            db.session.close()
            resp = jsonify("success")
        return(resp,201)

@app.route('/update_ad_by_user', methods=['PUT'])
# @flask_praetorian.auth_required
def update_ad_by_user():
    my_Data = Ads.query.get(request.form.get('id'))
    my_Data.brand = request.form['brand']
    my_Data.condition = request.form['condition']
    my_Data.category = request.form['category']
    image = request.form['image']
    
   
  
    # my_Data.image = image
    my_Data.description = request.form['description']
    # my_Data.phone = request.form['phone']
    my_Data.image = image
    # #filename = secure_filename(image_r.filename)

    my_Data.post_by_id = flask_praetorian.current_user().id
    # my_Data.image_name = secure_filename(image_r.filename)
    # my_Data.mimetype =  image_r.mimetype


    # my_Data.length = request.form['length']
    my_Data.negotiable = request.form['negotiable']

    # my_Data.password = request.form['password']
    db.session.commit()    
    resp = jsonify("success")
    # resp.status_code =200
    db.session.close()
    return (resp,201)
    






@app.route("/ads_to_get/<id>")
def ads_to_get(id):
    ad = db.session.query(Ads).get(id)
    results = ad_schema.dump(ad)
    
    return jsonify(results)

    #------------------------------------------------------------------#
           
     #=================== Post =============================#

@app.route('/post_add',methods =['POST','GET'])
@login_required

def post_add():
         
    #  condit = request.form['condition']
     category = request.form['category']
     image = request.files['image']
     mimetype= image.mimetype
     
   # image_filename = image.save(image)
     brand  = request.form['brand']
     city  = request.form['city']
     phone  = request.form['phone']
     price = request.form['price']
     negotiable = request.form['negotiable']
     phone = request.form['phone']
     description = request.form['description']
     condition = request.form['condit']
     filename = secure_filename(image.filename)
     owner = Ads(condition =condition ,mimetype=mimetype,category =category,post_by_id=  current_user.id,city=city,brand = brand, phone = phone,description =description, price=price,negotiable = negotiable,image=image.read(),image_name=filename)
     db.session.add(owner)
     db.session.commit()
     flash("success")
     return  redirect(url_for('dashboard'))



@app.route('/promo_add',methods =['POST','GET'])
def promo_add():
         
     condit = request.form['condit']
     category = request.form['category']
     image = request.files['image']
     filename = secure_filename(image.filename)
   # image_filename = image.save(image)
     brand  = request.form['brand']
     city  = request.form['city']
     phone  = request.form['phone']
     price = request.form['price']
     negotiable = request.form['negotiable']
     mimetype = image.mimetype
     phone = request.form['phone']
     description = request.form['description']
     owner = Promo_request(condition =condit ,mimetype=mimetype,category =category,city=city,brand = brand, phone = phone,description =description, price=price,negotiable = negotiable,image=image.read(),image_name =filename,promo_by_id=current_user.id)
     db.session.add(owner)
     db.session.commit()
     flash('Ad promo request sent for approval')
     return redirect(url_for('dashboard'))



@app.route('/accept_promo',methods =['POST','GET'])
def accept_promo():
     myid = request.form.get('id')   
     condit = request.form['condit']
     category = request.form['category']
     image = request.files['image']
     filename = secure_filename(image.filename)
   # image_filename = image.save(image)
     brand  = request.form['brand']
     city  = request.form['city']
     phone  = request.form['phone']
     price = request.form['price']
     negotiable = request.form['negotiable']
     mimetype = image.mimetype
     phone = request.form['phone']
     description = request.form['description']
     owner = Promote(condition =condit ,mimetype=mimetype,category =category,city=city,brand = brand, phone = phone,description =description, price=price,negotiable = negotiable,image=image.read(),image_name =filename,promo_by_id=myid)
     db.session.add(owner)
     db.session.commit()
     flash('Ad Promo successful')
     return redirect(url_for('admin_dashboard'))


# @app.route('/image/<int:image_id>')
# def get_image(image_id):
#     ad = Ads.query.get_or_404(image_id)
#     return Response(ad.image, mimetype=ad.mimetype)


# #============== image view ========#
@app.route('/get_image/<int:id>')
def get_image(id):
    img = db.session.query(Ads).filter_by(id=id).first()
    if img:
        return Response(img.image, mimetype=img.mimetype)
    return "Image not found", 404


@app.route('/get_image_electronics/<int:id>')
def get_image_electronics(id):
     img = db.session.query(Ads).filter_by(id=id).first()
     return Response(img.image,mimetype=img.mimetype)
     

@app.route('/get_image_ads/<int:id>')
def get_image_ads(id):
     img =  db.session.query(Promote).filter_by(id=id).first()
     return Response(img.image,mimetype=img.mimetype)
     


@app.route('/get_image_promo/<int:id>')
def get_image_promo(id):
     img = db.session.query(Promo_request).filter_by(id=id).first()
     return Response(img.image,mimetype=img.mimetype)
     

@app.route('/get_image_accept_promo/<int:id>')
def get_image_accept_promo(id):
     img = db.session.query(Promote).filter_by(id=id).first()
     return Response(img.image,mimetype=img.mimetype)
     
@app.route("/date")
def date():
    current_time = datetime.now()
    return str(current_time)

 
@app.route('/get_image_accept_ads_link/<int:id>')
def get_image_accept_ads_link(id):
     img = db.session.query(Ads).filter_by(id=id).first()
     return Response(img.image,mimetype=img.mimetype)
     
     
#==================update client's profile ======#

@app.route('/update_client',methods = [ 'POST'])
def update_client():
     #if request.method == 'POST':
          my_Data = User.query.get(request.form.get('id'))
          
          my_Data.username = request.form['username']
          my_Data.unhashed_password = request.form['password']
          oldpassword = request.form['oldpassword']
          #my_Data.date = request.form['date']

          #if oldpassword == current_user.password :
               
          db.session.commit()
          flash("Profile updated successful")

          return redirect(url_for('dashboard'))

          #else:
           #   flash('please check old password')
              #return redirect(url_for('edit_profile'))

@app.route('/curent_p')
def current_p():
    if current_user.password == 'pbkdf2:sha256:260000$muWO3rx5xRwn8B6M$c0fbc7b341c58f2b4b25a6fe10de06a5c51161e79b1adc7c069734fb04f54a69':
        flash(current_user.password)
        return redirect(url_for('home'))

    else:
        flash('No')
        return redirect(url_for('home'))

#admin==#

#========== update=================#
@app.route('/update')
@login_required
def update():
    #id = Ads.query.get(request.form.get('id'))
    owner = User.query.filter_by(username=current_user.username,password=current_user.password,admin=True).first()
    imb = Ads.query.filter_by(post_by_id=current_user.id).all()
   
    #all_goods = Ads.query.filter_by(post_by_id = current_user.id).all()
    all_goods = db.session.query(Ads).filter_by(post_by_id = current_user.id).all()
   
    #roww = db.session.query(Appointments).filter_by(asked_by_id = current_user.id).count()
    #m_count = db.session.query(Notiication).filter_by(receive_by_id = current_user.id).count()
    if not owner:

          flash("Kindly login to access page")
          return redirect(url_for('home'))
     
    else:
       
   
        return render_template('edit_good.html',all_goods=all_goods)

#================ brand==============================#

@app.route('/brand',methods=['GET','POST'])
def brand():
    #owner = User.query.filter_by(username=current_user.username,password=current_user.password,admin=False).first()
    page = request.args.get('page',1,type=int)
    selected_brand = request.args.get('type')
    imb = Ads.query.filter_by(brand=selected_brand).paginate(per_page=20,page =page,error_out=True)
    prmo = Promote.query.all()
    current_time = datetime.now()

    if  selected_brand == 'iphone':

                 
                 imb = db.session.query(Ads).filter(Ads.brand.contains("iPhone")).paginate(per_page=20,page =page,error_out=True)
                 return render_template('brand.html',imb=imb,prmo=prmo)
                
                

    if selected_brand == 'samsung':

                 imb = db.session.query(Ads).filter(Ads.brand.contains("Samsung")).paginate(per_page=20,page =page,error_out=True)
                 return render_template('brand.html',imb=imb,prmo=prmo)


    if  selected_brand == 'lg':

        
                 imb = db.session.query(Ads).filter(Ads.brand.contains("Lg")).paginate(per_page=20,page =page,error_out=True)
                 return render_template('brand.html',imb=imb,prmo=prmo)
                
                

    if selected_brand == 'infinix':

                 imb = db.session.query(Ads).filter(Ads.brand.contains("Infinix")).paginate(per_page=20,page =page,error_out=True)
                 return render_template('brand.html',imb=imb,prmo=prmo)

    if  selected_brand == 'techno':

        
                 imb = db.session.query(Ads).filter(Ads.brand.contains("Techno")).paginate(per_page=20,page =page,error_out=True)
                 return render_template('brand.html',imb=imb,prmo=prmo)
                
                

    if selected_brand == 'motorola':

                 imb = Ads.query.filter_by(brand='Motorola' ).paginate(per_page=20,page =page,error_out=True)
                 return render_template('brand.html',imb=imb,prmo=prmo)
               
                 
    if  selected_brand == 'acatel':

         
                 imb = db.session.query(Ads).filter(Ads.brand.contains("Acatel")).paginate(per_page=20,page =page,error_out=True)
                 return render_template('brand.html',imb=imb,prmo=prmo)
                
                

    if selected_brand == 'sony':

                 imb = db.session.query(Ads).filter(Ads.brand.contains("Sony")).paginate(per_page=20,page =page,error_out=True)
                 return render_template('brand.html',imb=imb,prmo=prmo)


   
                

    if selected_brand == 'htc':

                 imb = db.session.query(Ads).filter(Ads.brand.contains("Htc")).paginate(per_page=20,page =page,error_out=True)
                 return render_template('brand.html',imb=imb,prmo=prmo)
                         
                 
    else:
   
    #roww = db.session.query(Appointments).filter_by(asked_by_id = current_user.id).count()
    #m_count = db.session.query(Notiication).filter_by(receive_by_id = current_user.id).count()
 
        return render_template('brand.html',imb=imb,prmo=prmo)


#====================================================#

@app.route('/update_good',methods = [ 'POST'])
@login_required
def update_good():
     #if request.method == 'POST':
          my_Data = Ads.query.get(request.form.get('id'))
          
          my_Data.conditon = request.form['condit']
          my_Data.phone = request.form['phone']
          my_Data.category = request.form['category']
          my_Data.description = request.form['description']
          my_Data.negotiable = request.form['negotiable']
          my_Data.price = request.form['price']
          my_Data.city = request.form['city']
          image = request.files['image']
          my_Data.image = image.read()

          my_Data.post_by_id = current_user.id
          my_Data.image_name = secure_filename(image.filename)
          my_Data.mimetype =  image.mimetype
          
          

         # my_Data.image = request.files['image']

          #my_Data.filename = secure_filename( my_Data.image.filename)
          #my_Data.mimetype = my_Data.image.mimetype


          db.session.commit()
          flash("Profile updated successful")

          return redirect(url_for('dashboard'))

#=====  delete====================#



@app.route('/search',methods=['GET','POST'])
def search():
     find = request.form['Product']
    # imb = Ads.query.filter_by(or_(city= boah ,category = boah , brand =boah)).all()
     imb = db.session.query(Ads).filter(Ads.brand.contains(find)).all()
     #elif search.data['select'] == 'Album':
          #  qry = db_session.query(Album).filter(
             #   Album.title.contains(search_string))
     
     return render_template('search.html',imb=imb)
   


@app.route('/delete_ads_admin/<id>/',methods=['GET','POST'])
def delete_ads_admin(id):
     my_Data = Ads.query.get(id)
     db.session.delete(my_Data)
     db.session.commit()
     flash("Ad Deleted ") 
     return redirect(url_for('all_ads'))

@app.route('/delete_user/<id>/',methods=['GET','POST'])
def delete_user(id):
     my_Data = User.query.get(id)
     db.session.delete(my_Data)
     db.session.commit()
     flash("User deleted ") 
     return redirect(url_for('admin_dashboard'))


@app.route('/delete_add/<id>/',methods=['GET','DELETE'])

@flask_praetorian.auth_required
def delete_add(id):
     my_Data = Ads.query.get(id)
     db.session.delete(my_Data)
     db.session.commit()
     resp =jsonify("deleted") 
    
     return  (resp,201)


@app.route('/delete_ads_promo/<id>/', methods=['GET', 'POST'])
def delete_ads_promo(id):
    my_Data = Promote.query.filter_by(id=id).first()
    
    if my_Data is None:
        flash("Ad not found")
        return redirect(url_for('all_promo'))

    db.session.delete(my_Data)
    db.session.commit()
    flash("Ad deleted") 

    return redirect(url_for('all_promo'))


     
@app.route("/delete/<id>/",methods=['Get','Post'])
def delete(id):

    my_Data = Ads.query.get(id)
    db.session.delete(my_Data)
    db.session.commit()
    flash("Ad deleted ") 

    return redirect(url_for('dashboard'))

 #=======Message===============#
@app.route("/mymessage" ,methods= ['POST','GET'])
def mymessage():


    em = request.form['email']
    mm = request.form['subject']
    msg = Message('Hello', sender = 'jxkalmhefacbuk@gmail.com', recipients = ['kevinfiadzeawu@gmail.com'])
    msg.body = mm + " " + 'email address of  client :' + em
    mail.send(msg)
    flash("Message sent successful")  
    return redirect(url_for('contact'))       
     



if __name__ =='__main__':
    with app.app_context():
        db.create_all()
        app.run(debug='True')