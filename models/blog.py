import shortuuid
import datetime
from database import Database
from models.post import Post

class Blog(object):
    def __init__(self, author, title, description, id=None):
        self.author=author
        self.title=title
        self.description=description
        self.id=shortuuid.ShortUUID().random(length=5) if id is None else id

    def new_post(self):
        title = input("\nName your post: ")
        content = input("\nWhat's on yout mind today? ")
        date = input("\nEnter post date (DDMMYYY), may leave blank: ")
        if date == "":
            date = datetime.datetime.utcnow()
        else:
            date = datetime.datetime.strptime(date, "%d%m%Y")
        # SELF - ID & AUTHOR  are those of the Blog class, not of the Post class:
        post = Post(blog_id=self.id,
                    title=title,
                    content=content,
                    author=self.author,
                    date=date)
        post.save_to_mongo()

    # Get all posts from the blog:
    def get_posts(self):
        return Post.from_blog(self.id)

    # Save new information to the database:
    def save_to_mongo(self):
        Database.insert(collection='blogs',
                        data=self.json())

    def json(self):
        return {
        'author': self.author,
        'title': self.title,
        'description': self.description,
        'id': self.id,
        }

    # Instead of using staticmethod, use classmethod. CLS=Blog. Returns object of type blog
    @classmethod
    def from_mongo(cls, id):
        blog_data = Database.find_one(collection='blogs',
                                query={'id': id})
        return cls(author=blog_data['author'],
                    title=blog_data['title'],
                    description=blog_data['description'],
                    id=blog_data['id'])
