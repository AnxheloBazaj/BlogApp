from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.show import Show
from flask_app.models.user import User

@app.route('/add/show')
def addShow():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    loggedUser = User.get_user_by_id(data)
    return render_template('addShow.html', loggedUser=loggedUser)

@app.route('/create/show', methods = ['POST'])
def createShow():
    if 'user_id' not in session:
        return redirect('/')
    if not Show.validate_show(request.form):
        return redirect(request.referrer)
    data={
        'title': request.form['title'],
        'network': request.form['network'],
        'releaseDate': request.form['releaseDate'],
        'description': request.form['description'],
        'user_id': session['user_id'],
    }
    Show.create(data)
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

@app.route('/delete/show/<int:id>')
def deleteShow(id):
    if 'user_id' not in session:
        return redirect('/')
    data={
        'show_id':id,
        'id':session['user_id']
    }
    show=Show.get_show_by_id(data)
    if not show:
        return redirect('/')
    loggedUser=User.get_user_by_id(data)
    if loggedUser['id']==show['user_id']:
        Show.delete_all_likes(data)
        Show.delete_show(data)
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


