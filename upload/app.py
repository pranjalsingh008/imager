from flask import Flask,url_for,request
from flask_pymongo import PyMongo

app = Flask(__name__)   
app.config['MONGO_URI'] = 'mongodb+srv://username:passwordroot@cluster0.lhxac.mongodb.net/imager?retryWrites=true&w=majority'
mongo = PyMongo(app)

@app.route('/')
def index():
    return '''
        <form method = "POST" action = "/create" enctype = "multipart/form-data">
            <input type="text" name="name">
            <input type="file" name="image">
            <input type="submit">
        </form>
    '''

@app.route('/create',methods=['POST'])
def create():
    if 'image' in request.files:
        imager = request.files['image']  
        mongo.save_file(imager.filename, imager)
        mongo.db.images.insert({'name' : request.form.get('name'), 'image_name' : image.filename})
    
    return "Done!"

@app.route('/file/<filename>')
def file(filename):
    return mongo.send_file(filename)

@app.route ('/image/<username>')
def image(username):
    user = mongo.db.images.find_one_404({'username': username})
    return f'''
        <h1>{username}</h1>
        <img src="{url_for('file',filename=user['image_name'])}">
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0')
