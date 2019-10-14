import datetime
import os, config
import random
import sys
import ast
from string import ascii_uppercase
from random import choice
from flask_pymongo import PyMongo
from flask import Flask, render_template, redirect, request, url_for,session, json
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId

app = config.app

app.config["MONGO_URI"] = config.app.config["MONGO_URI"]

mongo = config.mongo

# holds the board per user, so every users plays with their own board. Needed in case of multiple players at the same time.
users = {}


@app.route('/')
def main():
    """ Main page, offering instruction and login/registration """
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    """ SignUp page, offering to create a registration """
    return render_template('signup.html')

@app.route('/SignUp',methods=['POST','GET'])
def SignUp():
    """ Signup function, validate and create a user in the database if all checks are good"""
    _name = request.form[('username')]
    _password = request.form[('password_one')]
    _passwordcheck = request.form[('password_two')]
    _avatar = request.form[('avatar')]
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
    """ if user is in session, it will return the game page (userHome.html)"""
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

@app.route('/showSignin')
def showSignin():
    """if there is no valid session, redirect to signin page, if there is a valid session, userHome will be shown"""
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('signin.html')

@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    """Validate the signin action, check username exists, check is provided password matches"""
    _username = request.form[('username')]
    _password = request.form[('password_one')]
    if _username and _password:
        # connect to MongoDB
        uName = mongo.db.tblUsers.find_one({'username':_username})
        if uName:
            pwd_hash = uName['pwd']
            if check_password_hash(str(pwd_hash),_password):
                session['user'] = request.form[('username')]

                return render_template('userHome.html', user=session['user'])
            else:
                return render_template('signin.html',error = 'Invalid Password')
        else:
            return render_template('signin.html',user_error = 'Username does not exist')
    else:
        return render_template('signin.html',error = 'Invalid Password')

@app.route('/logout')
def logout():
    """Log the current user out, remove from active session"""
    session.pop('user',None)
    return redirect('/')

@app.route("/create_game", methods = ["POST"])
def create_game():
    """Create a game based on the boardsize choice, active session user"""
    post_obj = request.json
    post_obj["board"] = make_board(post_obj["size"])
    users[post_obj["username"]] = post_obj

    if 'user' in session:
        username = session["user"]
        userName = mongo.db.tblUsers.find_one({'username':username})
        userAvatar = userName['avatar']
        uName = mongo.db.tblGamesPlayed.find_one({'Username':username})
        if uName:
            UserGameId = uName['_id']
            mongo.db.tblGamesPlayed.update(
            {'_id': ObjectId(UserGameId)},
            {
                'Username': uName['Username'],
            'Games': int(uName['Games']) + 1,
            'Avatar': userAvatar
            })
        else:
            mongo.db.tblGamesPlayed.insert_one({'Username': username, 'Games': 1, 'Avatar': userAvatar})
    else:
        return render_template('error.html',error = 'Unauthorized Access')
    return json.dumps(post_obj), 200

@app.route('/submitScore',methods=['POST'])
def submitScore():
    """submit a score based on the boardsize to the correct collection in the mongo database"""
    if 'user' in session:
        dt = datetime.datetime.now()
	username = session["user"]
        uName = mongo.db.tblUsers.find_one({'username':username})
        userAvatar = uName['avatar']
        post_obj = request.json
        username = post_obj["username"]
        turns = post_obj["turns"]
        size = post_obj["size"]
        time = post_obj["time"]
        if size == "4":
            tbl_scores = mongo.db.tblBeginner
        else:
            tbl_scores = mongo.db.tblExpert
        tbl_scores.insert_one({'playdate': dt, 'Username': username, 'Size': size, 'Moves': turns, 'Time': time,  'Avatar': userAvatar})
        
        return json.dumps("Success"), 200
    else:
        return render_template('error.html',error = 'Unauthorized Access')

@app.route('/LeaderBoards')
def LeaderBoards():
    """Only visible for active session users, gets top10 entries from tblBeginner, tblExpert, tblGamesPlayed"""
    if 'user' in session:
        
        Beginner=mongo.db.tblBeginner.find({ "$query": {}, "$orderby": { 'Moves' : 1, 'Time': 1 }}).limit(10)
        Expert=mongo.db.tblExpert.find({ "$query": {}, "$orderby": { 'Moves' : 1 , 'Time': 1 }}).limit(10)
        GamesPlayed=mongo.db.tblGamesPlayed.find({ "$query": {}, "$orderby": { 'Games' : -1 }}).limit(10)
        
        return render_template('LeaderBoards.html', beginnerList=Beginner, expertList=Expert, Games=GamesPlayed, user=session['user'])
    else:
        return render_template('error.html',error = 'Unauthorized Access')

# Function to create a board with numbers. Numbers are based on the size of the board.
# returns a nested array which contains every number 2 times

def make_board(size):
	sizeint = int(size)
	double = int(size) * int(size)
	set_one = []
	set_two = []

	board = []
	for i in range(int(double / 2)): # define the numbers to play with
		set_one.append(i) # first set of numbers
		set_two.append(i) # second set of numbers to make sure we have pairs
		
	combined_pool = []
	for i in range(double):
		if len(set_one) != 0:
			random_draw = set_one[random.randint(0, len(set_one) - 1)]
			set_one.remove(random_draw)
			combined_pool.append(random_draw)
		elif len(set_one) == 1:
			random_draw = set_one[0] #no need for random draw since there is 1 left
			set_one.remove(random_draw)
			combined_pool.append(random_draw)
		if len(set_two) != 0:
			random_draw = set_two[random.randint(0, len(set_two) - 1)]
			set_two.remove(random_draw)
			combined_pool.append(random_draw)
		elif len(set_two) == 1: #no need for random draw since there is 1 left
			random_draw = set_two[0]
			set_two.remove(random_draw)
			combined_pool.append(random_draw)
		
            
	for i in range(sizeint):	# convert the combined pool of numbers to the board and give them a location
		mini_board = []
		for j in range(sizeint):
			mini_board.append(combined_pool[0])
			combined_pool.remove(combined_pool[0])
		board.append(mini_board)	
	return board

# translates the tile that is clicked to a value from the board which is send back to the frontend where it is transformed based on the value to a icon
@app.route("/tile_click", methods = ["POST"])
def tile_click():
	post_obj = request.json
	choice = post_obj["choice"]
	choice = ast.literal_eval(choice) # converts the str to dict
	client_name = post_obj["username"] # check which player is making the request
	client = users[client_name] # get the players info
	client_board = client["board"] #get the current board that the user is playing on
	info = {}
	info["value"] = client_board[int(choice["row"])][int(choice["col"])]
	info["id"] = choice["id"]
	return json.dumps(info), 200

if __name__ == '__main__':
    app.secret_key = config.secret_key
    app.run(host=os.getenv('IP'), 
            port=int(os.getenv('PORT')),
            )
