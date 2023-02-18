from flask import Flask, abort, request
from detoxify import Detoxify
from instagramy import InstagramUser, InstagramPost
from flask_cors import CORS

app = Flask(__name__)
#cors = CORS(app, resources={r"/*": {"origins": "*"}})
CORS(app)

modello = Detoxify('multilingual', device="cpu")

print("Ok!")

@app.route('/frase/', methods=['POST'])
def index():
  req = request.json
  try:
    frase = req["frase"]
  except:
    abort(400)
  ris = modello.predict([frase]) 
  for j in ris:
    ris[j] = round(ris[j][0]*1,4)
  ris["frase"] = frase
  return [ris]

@app.route("/user/", methods=['POST'])
def user():
  req = request.json
  try:
    userName = req["username"]
  except:
    abort(400)
  ris = [];
  try:
    user = InstagramUser(userName, from_cache=False)
  except:
    abort(404)
  posts = user.posts
  try:
    post = InstagramPost(posts[0].shortcode)
  except:
    abort(404)  
  commenti = post.post_data["edge_media_to_parent_comment"]["edges"]
  for i in commenti:
    temp = modello.predict(i["node"]["text"])
    for j in temp:
      temp[j] = round(temp[j]*1,4)
    
    temp["frase"]=i["node"]["text"]
    ris.append(temp)  

  return sorted(ris, key=lambda d: d['toxicity'], reverse=True) 
    
    


if __name__ == '__main__':
  
  app.run() #go to http://localhost:5000/ to view the page.






