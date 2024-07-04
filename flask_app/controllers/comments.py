from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.post import Post
from flask_app.models.user import User
from flask_app.models.comment import Comment

@app.route("/create/comment/<int:id>", methods=["POST"])
def comment(id):
    if "user_id" not in session:
        return redirect("/")
    # return request.form
    if not Comment.validate_comment(request.form):
        return redirect(request.referrer)
    data = {
        "comment": request.form["comment"],
        "post_id": id,
        "user_id": session["user_id"],
    }
    Comment.create(data)
    return redirect(request.referrer)

@app.route("/delete_comment/<int:id>")
def delete_comment(id):
    if "user_id" not in session:
        return redirect("/")
    # return request.form
    comment=Comment.get_comment_by_id({'id':id})
    loggedUser=User.get_user_by_id({'id':session['user_id']})
    if loggedUser['id']== comment['user_id'] or loggedUser['role'] =='admin':
        Comment.delete_comment({'id':id})
    return redirect(request.referrer)

@app.route("/update_comment/<int:id>", methods=["POST"] )
def edit_comment(id):
    if "user_id" not in session:
        return redirect("/")
    # return request.form
    comment=Comment.get_comment_by_id({'id':id})
    loggedUser=User.get_user_by_id({'id':session['user_id']})
    
    if not Comment.validate_comment(request.form):
        return redirect(request.referrer)
    data = {
        "comment": request.form["comment"],
        'id':id
    }
    if loggedUser['id']== comment['user_id']:
        Comment.editComment(data)
    return redirect(request.referrer)