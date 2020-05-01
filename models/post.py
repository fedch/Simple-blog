from database import Database
import shortuuid
import datetime

class Post(object):
    # ID=NONE - if no value is given to the ID parameter, it by default will be NONE, and then given a value with UUID.
    # DATETIME.UTCNOW automatically sets the date to the current one by Grinwitch = easy to translate in to the needed one:
    def __init__(self, blog_id, title, author, content, date=datetime.datetime.utcnow(), id=None):
        self.blog_id = blog_id
        self.title = title
        self.author = author
        self.content = content
        self.created_date = date
        # ELSE use ID given in the INIT method:
        self.id = shortuuid.ShortUUID().random(length=5) if id is None else id

    def save_to_mongo(self):
        Database.insert(collection='posts',
                        data=self.json())

    # Translate the data into JSON format for the correct output:
    def json(self):
        return {
        'id': self.id,
        'blog_id': self.blog_id,
        'title': self.title,
        'author': self.author,
        'content': self.content,
        'created_date': self.created_date
        }

    @classmethod
    def from_mongo(cls, id):
        post_data = Database.find_one(collection='posts',
                                query={'id': id})
        return cls(blog_id=post_data['blog_id'],
                    title=post_data['title'],
                    author=post_data['author'],
                    content=post_data['content'],
                    date=post_data['created_date'],
                    id=post_data['id'])

    @staticmethod
    def from_blog(id):
        # To return a collectino of posts in the blog, and not just a cursor to that collection, use post for post in ...:
        return [post for post in Database.find(collection='posts',
                                query={'blog_id': id})]
