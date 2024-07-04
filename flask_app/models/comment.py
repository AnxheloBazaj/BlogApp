from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Comment:
    db_name = "blogApp"

    def __init__(self, data):
        self.id = data["id"]
        self.text = data["text"]
        self.user_id = data["user_id"]
        self.post_id = data["post_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def create(cls, data):
        query = "INSERT INTO comments (text, user_id, post_id) VALUES ( %(comment)s, %(user_id)s, %(post_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def editComment(cls, data):
        query = "UPDATE comments set text = %(comment)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all_comments_post(cls, data):
        query = "SELECT comments.*, users.first_name, users.last_name FROM comments JOIN users ON comments.user_id = users.id WHERE comments.post_id = %(post_id)s ORDER BY comments.created_at DESC;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        comments = []
        if results:
            for comment in results:
                comments.append(comment)
        return comments

    @classmethod
    def get_all_comments(cls, data):
        query = "SELECT comments.*, users.first_name, users.last_name FROM comments JOIN users ON comments.user_id = users.id  ORDER BY comments.created_at DESC;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        comments = []
        if results:
            for comment in results:
                comments.append(comment)
        return comments

    @classmethod
    def removeComment(cls, data):
        query = "DELETE FROM comments where post_id = %(post_id)s and user_id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def delete_all_comments(cls, data):
        query = "DELETE FROM comments Where post_id =%(post_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def delete_comment(cls, data):
        query = "DELETE FROM comments Where id =%(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_comment_by_id(cls, data):
        query = "Select * from comments where id=%(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False

    @classmethod
    def removeUsersComments(cls, data):
        query = "DELETE FROM comments where user_id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @staticmethod
    def validate_comment(data):
        is_valid = True
        if len(data["comment"]) < 1:
            is_valid = False
            flash("Comment should include more than 3 characters!", "description")
            is_valid = False
        return is_valid
