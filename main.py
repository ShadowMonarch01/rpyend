from flask import Flask,request,abort,jsonify
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from models import db,Users,Projects
import sqlite3 as sql

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///company.db'
app.config["JWT_SECRET_KEY"] = "kwehhehojowoojow"  #

conn = sql.connect('company.db',check_same_thread= False)

cur = conn.cursor()

jwt = JWTManager(app)

bcrypt = Bcrypt(app)

db.init_app(app)


with app.app_context():
    db.create_all()






@app.route("/register", methods= ["POST"])
def register_user():
    email = request.json["email"]
    password = request.json["password"]
    name = request.json["name"]

    user_exist = Users.query.filter_by(email = email).first() is not None

    if user_exist:
        #abort(409)
        return jsonify({"msg": "User exists"}), 401

    hashed_password = bcrypt.generate_password_hash(password)
    new_user = Users(name=name,email=email, password = hashed_password)
    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=new_user.email)

    the_info = [new_user.adm, new_user.id,new_user.email]

    return jsonify({
        "token": access_token,
        "info":the_info,
        "Admstats":new_user.adm,
        "email": new_user.email,
        "status": 'success'
    })


@app.route("/login", methods=["POST"])
def login_user():
    email = request.json["email"]
    password = request.json["password"]

    user = Users.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"msg": "User does not exist"}), 401

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"msg": "incorrect password"}), 401

    #session["user_id"] = user.id

    access_token = create_access_token(identity=user.email)

    return jsonify({
        "id": str(user.id),
        "name": user.name,
        "propic": user.profilepic,
        "about": user.about,
        "phone": user.phone,
        "adm": str(user.adm),
        "token": access_token,
        "status": 'success'
    })

@app.route("/newproject", methods= ["POST"])
def create_Project():
    name = request.json["name"]
    details = request.json["details"]


    project_exist = Projects.query.filter_by(name = name).first() is not None

    if project_exist:
        #abort(409)
        return jsonify({"msg": "project name exists"}), 401


    new_project = Projects(name=name,details=details)
    db.session.add(new_project)
    db.session.commit()

    #access_token = create_access_token(identity=new_user.email)

    the_info = [new_project.id,new_project.name,new_project.details]

    return jsonify({
        "info":the_info,
        "name":new_project.name,
        "details": new_project.details,
        "id": new_project.id,
        "status": 'success'
    })
#Upload image
@app.route('/uploadimage',methods =['POST'])
def update_images():
    id = request.json["id"]
    image = request.json["image"]
    i=int(id)


    #cur.execute('UPDATE Users SET name = (name||?|| ?) WHERE id = ?', (',', a, 5))

    cur.execute('SELECT photos FROM projects WHERE id="%s"'%(i))

    for et in cur:
        print(et)
        for q in et:
            print(q)
            if q != None:
                cur.execute('UPDATE projects SET photos = (?|| ?||photos) WHERE id = ?', (image,',', i))
                conn.commit()
                return jsonify({"data": "update sucessfullll",
                                "status": 'success'})

            if q == None:
                cur.execute('UPDATE projects SET photos = ? WHERE id = ?', (image, id))
                conn.commit()
                return jsonify({"data": "update sucessful",
                                "status": 'success'})



#Upload documents
@app.route('/pdfupload',methods =['POST'])
def update_pdfs():
    id = request.json["id"]
    documents = request.json["pdf"]
    docname = request.json["docname"]
    i=int(id)

    dk = documents+":"+docname
    #cur.execute('UPDATE Users SET name = (name||?|| ?) WHERE id = ?', (',', a, 5))

    cur.execute('SELECT documents FROM projects WHERE id="%s"'%(i))

    for et in cur:
        print(et)
        for q in et:
            print(q)
            if q != None:
                cur.execute('UPDATE projects SET documents = (?|| ?||documents) WHERE id = ?', (dk,',', i))
                conn.commit()
                return jsonify({"data": "update sucessfullll",
                                "status": 'success'})

            if q == None:
                cur.execute('UPDATE projects SET documents = ? WHERE id = ?', (dk, id))
                conn.commit()
                return jsonify({"data": "update sucessful",
                                "status": 'success'})



#Upload task
@app.route('/taskupload',methods =['POST'])
def update_tasks():
    id = request.json["id"]
    task = request.json["task"]
    i=int(id)


    #cur.execute('UPDATE Users SET name = (name||?|| ?) WHERE id = ?', (',', a, 5))

    cur.execute('SELECT tasks FROM projects WHERE id="%s"'%(i))

    for et in cur:
        print(et)
        for q in et:
            print(q)
            if q != None:
                cur.execute('UPDATE projects SET tasks = (?|| ?||tasks) WHERE id = ?', (task,',', i))
                conn.commit()
                return jsonify({"data": "update sucessfullll",
                                "status": 'success'})

            if q == None:
                cur.execute('UPDATE projects SET tasks = ? WHERE id = ?', (task, id))
                conn.commit()
                return jsonify({"data": "update sucessful",
                                "status": 'success'})

#returns all project names and details
@app.route('/getprojects',methods =['GET'])
def get_articles():
    b2 = cur.execute('SELECT id,name,details FROM projects')
    ls = []

    for i in b2:
         ls.append({"id":i[0],"name":i[1],"details":i[2]})
    print(ls)
    print(len(ls))
    return jsonify({"data": ls})

#returns all info
@app.route('/getprojectimgs',methods =['POST'])
def get_imgs():
    id = request.json["id"]
    i = int(id)
    b2=cur.execute('SELECT photos FROM projects WHERE id="%s"'%(i))

    ls = []
    s=''
    for j in b2:
        for i in j:
            s=i
            #ls.append(i)
    e = s.split(',')
    #length = len(e)
    d=0
    for t in e:
            ls.append({"id": d, "images":t})
            d=d+1


    print(ls)
    print(len(e))
    print(e)

    return jsonify({"data":ls})

@app.route('/getprojectdocs',methods =['POST'])
def get_docs():
    id = request.json["id"]
    i = int(id)
    b2=cur.execute('SELECT documents FROM projects WHERE id="%s"'%(i))

    ls = []
    s = ''
    for j in b2:
        for i in j:
            s = i
            # ls.append(i)
    e = s.split(',')
    # length = len(e)
    d = 0
    for t in e:
        s=t.split(':')
        ls.append({"id": d, "documents": s[0],"name":s[1]})
        d = d + 1

    print(ls)
    print(len(e))
    print(e)

    return jsonify({"data": ls})


@app.route('/getprojecttask', methods=['POST'])
def get_tasks():
    id = request.json["id"]
    i = int(id)
    b2 = cur.execute('SELECT tasks FROM projects WHERE id="%s"' % (i))

    ls = []
    s = ''
    for j in b2:
        for i in j:
            s = i
            # ls.append(i)
    e = s.split(',')
    # length = len(e)
    d = 0
    for t in e:
        ls.append({"id": d, "task": t})
        d = d + 1

    print(ls)
    print(len(e))
    print(e)

    return jsonify({"data": ls})

##############################
#returns all info
@app.route('/updpics',methods =['POST'])
def upd_pics():
    id = request.json["id"]
    ids = request.json["ids"]
    val = request.json["val"]
    k = int(id)
    z = int(ids)
    b2=cur.execute('SELECT photos FROM projects WHERE id="%s"'%(k))



    ls = []

    ps=[]

    s=''
    for j in b2:
        for i in j:
            s=i
            #ls.append(i)
    e = s.split(',')
    e[z]= val
    h= ','.join(str(x) for x in e)


    cur.execute('UPDATE projects SET photos = ? WHERE id = ? ', (h,k,))
    conn.commit()



    #length = len(e)
    d=0
    for t in e:
            ls.append({"id": d, "images":t})
            d=d+1


    print(ls)
    print(len(e))
    print(e)

    return jsonify({"data":ls})
##############################


########################
@app.route("/updateproimage", methods= ["POST"])
def update_image():
    id = request.json["id"]
    img = request.json["image"]

    i=int(id)


    cur.execute('UPDATE users SET profilepic = ? WHERE id = ? ', (img,i,))
    conn.commit()

    b2 = cur.execute('SELECT profilepic FROM users WHERE id="%s"' % (i))

    tt=''
    for s in b2:
        for p in s:
            tt = p
    print(tt)
    return jsonify({
        "propic":tt,
        "status": 'success'
    })
#######################

######################
@app.route("/updateprodata", methods= ["POST"])
def update_data():
    id = request.json["id"]
    name = request.json["name"]
    info = request.json["info"]
    phone = request.json["phone"]

    i=int(id)


    cur.execute('UPDATE users SET name = ? ,about = ? ,phone = ? WHERE id = ? ', (name,info,phone,i,))
    conn.commit()

    b2 = cur.execute('SELECT name,about,phone,adm FROM users WHERE id="%s"' % (i))

    tt=[]

    for s in b2:
         for e in s:

            tt.append(e)

    print(tt)
    return jsonify({
        "name":tt[0],
        "about":tt[1],
        "phone":tt[2],
        "adm":str(bool(tt[3])),
        "status": 'success'
    })
######################

if __name__ == '__main__':
    app.run(debug=True)

