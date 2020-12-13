from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb+srv://username:passwordroot@cluster0.lhxac.mongodb.net/imager?retryWrites=true&w=majority'
mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username'],'password' : request.form['pass']})

    if login_user:
        return redirect("http://localhost:8000//app2", code=302)

        

    return redirect(url_for('register'))
    

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            hashpass = request.form['pass']
            users.insert({'name' : request.form['username'], 'password' : hashpass})
            return redirect("http://localhost:8000//app2", code=302)
        
        return redirect("http://localhost:8000//app1", code=302)

    return render_template('register.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')