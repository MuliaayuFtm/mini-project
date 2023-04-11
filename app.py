from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:ujicoba@cluster0.vasc50z.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
     bucket_receive = request.form["bucket_give"]
     count = db.wishlist.count_documents({})
     num = count + 1
     doc =  {
        'num':num,
        'bucket': bucket_receive,
        'done':0
     }
     db.wishlist.insert_one(doc)
     return jsonify({'msg': 'data saved!!'})

@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    num_receive = request.form["num_give"]
    db.wishlist.update_one(
        {'num': int(num_receive)},
        {'$set': {'done': 1}}
    )
    return jsonify({'msg': 'Update Done!'})

@app.route("/bucket/delete", methods=["POST"])
def bucket_delete():
    num_receive = request.form["num_give"]
    db.wishlist.delete_one(
        {'num': int(num_receive)}
    )
    return jsonify({'msg': 'Delete Success!'})



@app.route("/bucket", methods=["GET"])
def bucket_get():
    buckets_list = list(db.wishlist.find({},{'_id':False}))
    return jsonify({'buckets':buckets_list})



if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)