from flask import Flask, render_template, request, session, redirect
from werkzeug.security import check_password_hash,generate_password_hash
from model import userdata,db,todo

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///userdata.db'

app.secret_key="yamato_kudasai_aaaaaaaaahhhhhh"

db.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login',methods=['POST','GET'])
def login():

    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']

        user_verfication=userdata.query.filter_by(emailid=email).first()

        if user_verfication and check_password_hash(user_verfication.password,password):
            session['user']=user_verfication.emailid
            return redirect('/dashboard')
        
        if not user_verfication:
            return render_template('login.html', alert_messege="User not found")

        if not check_password_hash(user_verfication.password, password):
            return render_template('login.html', alert_messege="Incorrect password")
        
    
    return render_template('login.html')



@app.route("/signup",methods=['POST','GET'])

def signup():
    if request.method=='POST':
        user_name=request.form['username']
        user_mail_id=request.form['email']
        user_password=generate_password_hash(request.form['password'])
        

        existing_user=userdata.query.filter_by(emailid=user_mail_id).first()

        if existing_user:
            return render_template('signup.html' ,alert_messege='user with this e-mail already exist')

        new_user=userdata(
            username=user_name,
            emailid=user_mail_id,
            password=user_password
        )
        db.session.add(new_user)
        db.session.commit()

        return redirect('/login')




    return render_template('signup.html')


@app.route("/dashboard",methods=['GET','POST'])
def dashboard():
    
    if 'user' not in session:
        return redirect('/login')
    
    if request.method=="POST":
        json_file=request.get_json()

        if json_file.get('delete')=="True":
            todo.query.filter_by(
                taskId=json_file['task'],
                emaild=session['user']
                ).delete()
            db.session.commit()

            return {'static':'deleted'}

        #elseee

        task_name=json_file['task']
        post_time=json_file['time']

    
        new_task=todo( 
            task=task_name,
            time=post_time,
            emaild=session['user']
        )
        db.session.add(new_task)
        db.session.commit()

        return {"status":"task added"}
        


    add_task=todo.query.filter_by(emaild=session['user']).all()
    
    return render_template('dashboard.html',todo_list=add_task)
    


@app.route('/logout', methods=['POST'])
def logout():
    if request.method=='POST':
        logout_request=request.get_json()
        if logout_request['logout']=="True":
            session.clear()
            return {"status": "logged_out"}


if __name__=="__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

