import os
import sys
from flask_pymongo import PyMongo
from flask import Flask, render_template, redirect, request, url_for,session, json
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = "randomsecretkey"
app.config["MONGO_DBNAME"] = 'memory'
app.config["MONGO_URI"] = 'mongodb://admin:Admin123@ds155045.mlab.com:55045/memory'

mongo = PyMongo(app)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/SignUp',methods=['POST','GET'])
def SignUp():
    _name = request.form[('username')]
    _password = request.form[('password_one')]
    _passwordcheck = request.form[('password_two')]
    _avatar = request.form[('avatar')]
    print(_avatar)
    # validate the received values
    if _name and _password and _passwordcheck and _avatar:
        uName = mongo.db.tblUsers.find_one({'username':_name})
        if uName:
            return render_template('signup.html', user_error="Username is already taken")
        else:
            if _passwordcheck == _password:
                Av = mongo.db.tblAvatar.find_one({'avatar_id':_avatar})
                avLink = Av['link']
                _hashed_password = generate_password_hash(_password)
                tbl_u = mongo.db.tblUsers
                tbl_u.insert_one({'username': _name, 'pwd': _hashed_password, 'avatar': avLink})
                session['user'] = request.form[('username')]
                return redirect('/userHome')
            else:
                return render_template('signup.html', error="password does not match")
    else:
        return render_template('signup.html', error="Fill in all required fields")

@app.route('/userHome')
def userHome():
    if 'user' in session:
        username = session["user"]
        uName = mongo.db.tblUsers.find_one({'username':username})

        if uName:
            userid = uName['_id']
            return render_template('userHome.html', user=username, userid=userid)
        else:
            return render_template('error.html',error = 'Username not found')
    else:
        return render_template('error.html',error = 'Unauthorized Access')
        
if __name__ == '__main__':
    app.run(host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=True)