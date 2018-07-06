from flask import *
from functools import wraps

app=Flask(__name__)
app.config ['secret_key']="mish"
dict = {}
comments=[]

def tokens(k):
    @wraps(k)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'message' : 'Token is missing'}), 403

        try:
            data = jwt.decode(token, app.config['secret_key'])

        except:
            return jsonify({'message' : 'Token is invalid'}), 403

        return k(*args, **kwargs)
    return decorated

@app.route("/login", methods=['POST','GET'])
def login():
    username=request.get_json()["username"]
    password=request.get_json()["password"]
    if username in dict:
        if password==dict[username]["password"]:
             token=jwt.encode({'username':username,'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}),app.config['secret_key']    
             return jsonify({'token':token.decode ('UTF-8')}) 
        else:
            return jsonify({"message": "your password is wrong"})
    else:
        return jsonify({"message": "check your username"})

@app.route("/public")
def public():
         return({"message": "anyone can view"})

@app.route("/private")
@tokens
def private():
          return({"message": "available to people with valid tokens"})

@app.route("/register", methods=['POST','GET'])
def register():
    name= request.get_json()['name']
    email= request.get_json()['email']
    password= request.get_json()['password']
    username=request.get_json()['username']
    dict.update({username:{"name": name,"email": email,"password": password}})
    return jsonify({"message": "you have been registered"})

@app.route("/comment", methods=['POST','GET'])
@tokens
def comment():
    comment=request.get_json()["comment"]
    comments.append(comment)
    return jsonify(comment)

@app.route("/users", methods=['POST','GET'])
@tokens
def users():
    return jsonify(dict) 
    return jsonify({"message": "you have been logged in"})


@app.route("/delete_comment/<int:commentID>", methods=['DELETE'])
def delete_comment(commentID):
    del comments[commentID]
    return jsonify({"message: comment succesfuly deleted"})
  
@app.route("/retrieve_comment", methods=['GET'])
@tokens
def retrieve_comment():
    if len(comments) > 0:
        return jsonify(comment)
    else:
        return jsonify({"message: no comment"})

if __name__ =="__main__":
    app.run(debug=True)