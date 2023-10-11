import os
from os.path import join, dirname
from dotenv import load_dotenv

from flask import Flask, request, render_template, jsonify
from pymongo import MongoClient
import requests

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

app = Flask(__name__)

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Post Req, memasukkan input client ke dalam database
@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form['bucket_give']
    # Menghitung jumlah dalam database bucket
    count = db.bucket.count_documents({})
    num = count + 1 # untuk id unik setiap baris kegiatan+1
    doc = {
        'num': num,
        'bucket': bucket_receive,
        'done': 0
        }
    db.bucket.insert_one(doc)
    return jsonify({'msg':'Data Saved!'})

# Done, menargetkan num yang unik
@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    num_receive = request.form['num_give']
    db.bucket.update_one(
        {'num': int(num_receive)}, # mengubah data string menjadi int
        {'$set':{'done':1}} # mengubah value done = 1
    )
    return jsonify({'msg': 'Update Complete!'})

@app.route("/bucket", methods=["GET"])
def bucket_get():
    buckets_list = list(db.bucket.find({},{'_id': False}))
    return jsonify({'buckets': buckets_list})

@app.route("/bucket/delete/<int:num>", methods=["POST"])
def bucket_delete(num):
    db.bucket.delete_one({'num': num})
    return jsonify({'msg': 'Item Deleted!'})
    
if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)