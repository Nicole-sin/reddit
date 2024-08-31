import json
from flask import Flask, make_response
from flask import jsonify
from flask import request

app = Flask(__name__)

posts = {
    0: {
      "id": 0,
      "upvotes": 1,
      "title": "My cat is the cutest!",
      "link": "https://i.imgur.com/jseZqNK.jpg",
      "username": "alicia98"},
      
    1: {
      "id": 1,
      "upvotes": 3,
      "title": "Cat loaf",
      "link": "https://i.imgur.com/TJ46wX4.jpg",
      "username": "alicia98"
    }
}

comments = [{
    0: {"id":0,
        "upvotes":8,
        "text":"Wow, my first Reddit gold!",
        "username":"alicia98"}
    }
]

task_id_counter = 2
comment_id_counter = 1

@app.route("/")
@app.route("/api/posts/", methods=["GET"])

def get_all_posts():
    """
    Gets all the posts
    """
    if len(posts) == 0:
        response = {"error": "No posts found"}
        return make_response(json.dumps(response),404)
    else: #if posts not found
        response = {"posts": list(posts.values())}
        return json.dumps(response), 200

@app.route("/api/posts/", methods=["POST"])
def create_post():
    """
    Creates a post
    """
    global task_id_counter
    body = json.loads(request.data)
    title = body.get("title")
    link = body.get("link")
    username = body.get("username")

    #Check if any field is missing
    if not all([title,link,username]):
        response = {"error": "Missing field(s)"}
        return make_response(json.dumps(response), 400)

    response = {"id": task_id_counter,
                "upvotes": 1, 
                "title": title,
                "link": link,
                "username": username}
    posts[task_id_counter] = response
    #make the id unique
    task_id_counter += 1
    return json.dumps(response), 201

@app.route("/api/posts/<int:post_id>/")
def get_post(post_id):
    """
    Get a specific post
    """
    post = posts.get(post_id)
    if not post: #if posts not found
        return json.dumps({"error": "Post not found"}), 404
    return json.dumps(post), 200

@app.route("/api/posts/<int:post_id>/", methods=["DELETE"])
def delete_post(post_id):
    """
    Deletes a post
    """
    post = posts.get(post_id)
    if not post:
        return json.dumps({"error": "Task not found"}), 404
    del posts[post_id]
    return json.dumps(post), 200
    
@app.route("/api/posts/<int:post_id>/comments/", methods=["GET"])
def get_comments(post_id):
    """
    Get comments for a specific post
    """
    post = posts.get(post_id)
    if not post:
        return json.dumps({"error": "Comments not found"}), 404
    
    retrieve_comments = {}
    for x, comment in comments.items():
        if comment["id"] == post_id:
            retrieve_comments[x] = comment
    
    y = {"comments": list(retrieve_comments.values())}
    return json.dumps(y),200


@app.route("/api/posts/<int:post_id>/comments/", methods=["POST"])
def create_comments(post_id):
    """
    Creates a comment for a specific post
    """
    if post_id not in posts: #if post is not found
        return json.dumps({"error": "Post not found"}), 404
    
    global comment_id_counter
    body = json.loads(request.data)
    text = body.get("text")
    username = body.get("username")

    #Check if any field is missing
    if not all([text,username]):
        response = {"error": "Missing field(s)"}
        return make_response(json.dumps(response), 400)
    
    #Create the comment for the specific post
    response = {"id": comment_id_counter, 
                "upvotes": 1,
                "text":text,
                "username": username}
    comments[comment_id_counter] = response
    #make the id unique
    comment_id_counter += 1
    return json.dumps(response), 201

@app.route("/api/posts/<int:post_id>/comments/<int:comment_id>/", methods=["POST"])
def edit_comment(post_id, comment_id):
    """
    Updates a specific post's comment
    """
    post = posts.get(post_id)
    #checking if comment exists
    if not post:
        return json.dumps({"error": "Post not found"}), 404
    
    comment = comments.get(comment_id)
    if not comment:
        return json.dumps({"error": "Comment not found"}), 404
    
    body = json.loads(request.data)
    new_text = body.get("text",comments["text"])

    comments["text"] = new_text
    return json.dumps(comment),200

        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
