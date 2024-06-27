from flask_app import socketio
from flask_socketio import emit, join_room, leave_room

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    emit('status', {'msg': f'{username} has entered the room.'}, room=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    emit('status', {'msg': f'{username} has left the room.'}, room=room)

@socketio.on('new_comment')
def handle_new_comment(data):
    emit('comment', data, room=data['post_id'])

# routes/blog.py
# from app import socketio

# # ... (other imports)

# emit events when new posts or comments created
# @bp.route('/post/<int:post_id>/comment', methods=['POST'])
# @login_required
# def add_comment(post_id):
#     # ... (existing comment creation logic)
    
#     socketio.emit('new_comment', {
#         'post_id': post_id,
#         'author': current_user.username,
#         'content': comment.content
#     }, room=str(post_id))

#     return redirect(url_for('blog.view_post', post_id=post_id))



# real time notifications
# @bp.route('/create', methods=['POST'])
# @login_required
# def create_post():
#     # ... (existing post creation logic)
    
#     socketio.emit('new_post', {
#         'id': post.id,
#         'title': post.title,
#         'author': current_user.username
#     })

#     return redirect(url_for('blog.view_post', post_id=post.id))