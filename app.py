from flask import Flask, request, jsonify
from datetime import datetime
from flask.ext.sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import os
import requests


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['IMGUR_API_KEY'] = os.environ['IMGUR_API_KEY']
db = SQLAlchemy(app)

db.init_app(app)
db.app = app
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(), unique=True)

    def __init__(self, url):
        self.url = url


@app.route('/')
def homepage():
    all_images = Image.query.all()
    return jsonify([{'url': image.url} for image in all_images])

@app.route('/images', methods=['POST'])
def upload_image():
    res = requests.post('https://api.imgur.com/3/image', 
      headers={'Authorization': 'Client-ID %s' % app.config['IMGUR_API_KEY']},
      json={'image': request.get_json()['image']})
    url = res.json()['data']['link']
    image = Image(url=url)
    db.session.add(image)
    db.session.commit()
    return jsonify({'url': url})

if __name__ == '__main__':
    manager.run()
