from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.post import Post
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
import os
from datetime import datetime
from .env import UPLOAD_FOLDER
from .env import ALLOWED_EXTENSIONS

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
from werkzeug.utils import secure_filename

bcrypt = Bcrypt(app)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# @app.route("/add/item", methods=["GET", "POST"])
# def addItem():
    if "user_id" not in session:
        return redirect("/login")

    data = {"id": session["user_id"]}
    loggeduser = User.get_user_by_id(data)

    if loggeduser["role"] != "admin":
        return redirect("/")

    if request.method == "GET":
        return render_template("addItem.html", categories=Product.getCategories())

    if request.method == "POST":
        if not Product.validate_product(request.form):
            return redirect(request.referrer)

        if not request.files["image"]:
            flash("Show image is required!", "image")
            return redirect(request.referrer)

        image = request.files["image"]
        if not allowed_file(image.filename):
            flash("Image should be in png, jpg, jpeg format!", "image")
            return redirect(request.referrer)

        if image and allowed_file(image.filename):
            filename1 = secure_filename(image.filename)
            current_time = datetime.now().strftime("%d%m%Y%S%f")
            filename1 = current_time + filename1
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename1))

        data = {
            "product_name": request.form["product_name"],
            "description": request.form["description"],
            "price": request.form["price"],
            "stock_quantity": request.form["stock_quantity"],
            "image": filename1,
            "category_id": request.form["category_id"],
        }
        Product.create(data)
        return redirect("/all/products/")

# @app.route('/add/post')
# def addPost():
#     if 'user_id' not in session:
#         return redirect('/')
#     data = {
#         'id': session['user_id']
#     }
#     loggedUser = User.get_user_by_id(data)
#     return render_template('addShow.html', loggedUser=loggedUser)

@app.route('/create/post', methods = ['POST'])
def createPost():
    if 'user_id' not in session:
        return redirect('/')
    # return request.form
    if not Post.validate_post(request.form):
        return redirect(request.referrer)
    
    if request.files["image"]:
        image = request.files["image"]
        if not allowed_file(image.filename):
            flash("Image should be in png, jpg, jpeg format!", "image")
            return redirect(request.referrer)

        if image and allowed_file(image.filename):
            filename1 = secure_filename(image.filename)
            current_time = datetime.now().strftime("%d%m%Y%S%f")
            filename1 = current_time + filename1
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename1))
    else:
        filename1= 0
    data={
        'description': request.form['description'],
        "image": filename1,
        'user_id': session['user_id'],
    }
    Post.create(data)
    return redirect('/')

@app.route('/view/show/<int:id>')
def viewShow(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'show_id': id,
        'id': session['user_id']
    }
    show = Show.get_show_by_id(data)
    loggedUser = User.get_user_by_id(data)
    usersWhoLiked=Show.get_likers(data)
    return render_template('show.html', show=show, loggedUser=loggedUser, usersWhoLiked=usersWhoLiked)

@app.route('/delete/post/<int:id>')
def deletePost(id):
    if 'user_id' not in session:
        return redirect('/')
    data={
        'post_id':id,
        'id':session['user_id']
    }
    post=Post.get_post_by_id(data)
    if not post:
        return redirect('/')
    loggedUser=User.get_user_by_id(data)
    if loggedUser['id']==post['user_id'] or loggedUser['role'] == 'admin':
        # Post.delete_all_likes(data)
        Post.delete_post(data)
    return redirect('/')

@app.route('/edit/show/<int:id>')
def editShow(id):
    if 'user_id' not in session:
        return redirect('/')
    data={
        'show_id':id,
        'id':session['user_id']
    }
    show=Show.get_show_by_id(data)
    loggedUser=User.get_user_by_id(data)
    if loggedUser['id']==show['user_id']:
        return render_template('edit.html', show=show, loggedUser=loggedUser)
    return redirect('/')

@app.route('/update/show/<int:id>', methods=['POST'])
def updateShow(id):
    if 'user_id' not in session:
        return redirect('/')
    data={
        'show_id':id,
        'id':session['user_id'],    
    }
    show=Show.get_show_by_id(data)
    if not show:
        return redirect('/')
    
    loggedUser=User.get_user_by_id(data)
    if loggedUser['id']!=show['user_id']:
        return redirect('/')
    updateData={
        'title':request.form['title'],
        'network':request.form['network'],
        'releaseDate':request.form['releaseDate'],
        'description':request.form['description'],
        'id':id
    }
    if not Show.validate_show(updateData):
        return redirect(request.referrer)
    Show.update_show(updateData)
    #return redirect('/view/show/'+str(id))           this redirects to the updated page after the changes 
    return redirect('/')
    
@app.route('/like/<int:id>')
def addLike(id):
    if 'user_id' not in session:
        return redirect('/')
    data ={
        'show_id':id,
        'id': session['user_id']
    }
    print(f"Data for addLike: {data}")
    usersWhoLiked=Show.get_likers(data)
    print(f"Users who liked show {id}: {usersWhoLiked}")
    if session['user_id'] not in usersWhoLiked:
        try:
            Show.addLike(data)
        except Exception as e:
            print(f"Error adding like: {e}")
        return redirect(request.referrer)
    return redirect(request.referrer)

@app.route('/unlike/<int:id>')
def removeLike(id):
    if 'user_id' not in session:
        return redirect('/')
    data ={
        'show_id':id,
        'id': session['user_id']
    }
    Show.removeLike(data)
    return redirect(request.referrer)


