from flask import Flask,url_for,request
from flask_pymongo import PyMongo

app = Flask(__name__)   
app.config['MONGO_URI'] = 'mongodb+srv://username:passwordroot@cluster0.lhxac.mongodb.net/imager?retryWrites=true&w=majority'
mongo = PyMongo(app)

@app.route('/')
def index():
    return '''
        <form method = "POST" action = "/app2/create" enctype = "multipart/form-data">
            <input type="text" name="name" placeholder="Vault Name">
            <input type="file" name="image">
            <input type="submit">
        </form>
    '''

@app.route('/create',methods=['POST'])
def create():
    if 'image' in request.files:
        imager = request.files['image']  
        mongo.save_file(imager.filename, imager)
        mongo.db.images.insert({'name' : request.form.get('name'), 'image_name' : imager.filename})
    
    return "Done!"
@app.route('/app2/file/<filename>')
def file(filename):
    return mongo.send_file(filename)

@app.route ('/image/<name>')
def image(name):
    user = mongo.db.images.find_one({'name': name})
    return f'''
        <h1>{name}</h1>
        <img src="{url_for('file',filename=user['image_name'])}">
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0')
