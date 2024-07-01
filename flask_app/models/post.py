from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Post:
    db_name = 'blogApp'
    def __init__( self , data ):
        self.category = data['category']
        self.description = data['description']
        self.image = data['image']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at= data['updated_at']

    @classmethod
    def create(cls,data):
        if data['image']:
            query = 'INSERT INTO posts (description, image, user_id) VALUES ( %(description)s, %(image)s, %(user_id)s);'
        else:
            query = 'INSERT INTO posts (description, user_id) VALUES ( %(description)s, %(user_id)s);'
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def getAllposts(cls):
        query = 'SELECT * FROM posts left join users on posts.user_id = users.id;'
        results = connectToMySQL(cls.db_name).query_db(query)
        posts= []
        if results:
            for post in results:
                posts.append(post)
        return posts
    
    # @classmethod
    # def getAllposts(cls):
    #     query = "SELECT * FROM posts;"
    #     try:
    #         results = connectToMySQL(cls.db_name).query_db(query)
    #         print(f"Fetched posts: {results}")
    #         return results
    #     except Exception as e:
    #         print(f"An error occurred in getAllposts: {e}")
    #         return []


    @classmethod
    def get_logged_posts(cls,data):
        query = "SELECT * FROM posts where user_id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        posts=[]
        if results:
            for post in results:
                posts.append(post)
        return posts
            

    @classmethod
    def get_post_by_id(cls,data):
        query = "SELECT * FROM posts left join users on posts.user_id = users.id WHERE posts.id = %(post_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
    
    @classmethod
    def delete_post(cls,data):
        query = 'DELETE FROM posts WHERE id=%(post_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def update_post(cls,data):
        query = 'UPDATE posts set title = %(title)s, network = %(network)s, releaseDate = %(releaseDate)s, description = %(description)s WHERE id = %(id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def delete_users_posts(cls,data):
        query = 'DELETE FROM posts Where posts.user_id=%(user_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    # @classmethod
    # def addLike(cls,data):
    #     query= 'INSERT INTO likes (user_id, posts_id) VALUES (%(id)s, %(posts_id)s);'
    #     return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def addLike(cls, data):
        try:
            query = 'INSERT INTO likes (user_id, posts_id) VALUES (%(id)s, %(posts_id)s);'
            return connectToMySQL(cls.db_name).query_db(query, data)
        except Exception as e:
            print(f"An error occurred in addLike: {e}")
            raise e  # Re-raise the exception for further handling
    
    @classmethod
    def removeLike(cls,data):
        query= 'DELETE FROM likes where posts_id = %(post_id)s and user_id = %(id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_likers(cls,data):
        query = 'SELECT user_id from likes where likes.post_id = %(post_id)s;'
        results =connectToMySQL(cls.db_name).query_db(query, data)
        likers=[]
        if results:
            for person in results:
                likers.append(person['user_id'])
        return likers
    
    @classmethod
    def get_likers_info(cls,data):
        query = 'SELECT * FROM likes left join users on likes.user_id = user_id where likes.post_id=%(post_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        likers =[]
        if results:
            for person in results:
                likers.append(person)
        return likers
    
    @classmethod
    def delete_all_likes(cls,data):
        query = 'DELETE FROM likes Where post_id =%(post_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @staticmethod
    def validate_post(data):
        is_valid = True
        if len(data['description'])<2:
            is_valid=False
            flash('Description should include more than 3 characters!', 'description')
            is_valid=False
        return is_valid