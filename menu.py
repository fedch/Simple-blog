from database import Database
from models.blog import Blog

class Menu(object): # extends from object
    def __init__(self):
        # Ask the user for author name
        self.user = input("What's your login? ")
        # Make an instance of user_blog, to which blog will equal to if exists:
        self.user_blog = None
        if self._user_has_account():
            print (f"Welcome back, {self.user}")
        else:
            self._prompt_user_for_account()

    # Check if user already got an account:
    def _user_has_account(self):
        # Search for the blog author:
        blog = Database.find_one(collection='blogs', query={'author': self.user})
        if blog is not None:
            # Assign an object of type blog to user blog
            self.user_blog = Blog.from_mongo(blog['id'])
            return True
        else:
            return False

    # If user has no account yet, prompt them to create one:
    def _prompt_user_for_account(self):
        title = input("Enter blog title: ")
        description = input("Enter blog description: ")
        blog = Blog(author=self.user,
                    title=title,
                    description=description)
        blog.save_to_mongo()
        self.user_blog = blog


    def run_menu(self):
        # User read or write blogs?
        read_or_write = input("Are you here to read or write? R/W: ")
        if read_or_write == "R":
            # List blogs in Database:
            self._list_blogs()
            # Allow the user to pick one and display posts:
            self._view_blog()

        elif read_or_write == "W":
            # Prompt to write a post:
            self.user_blog.new_post()
        else:
            print("Thanks and bye!")

    def _list_blogs(self):
        blogs = Database.find(collection='blogs',
                            query={})
        for blog in blogs:
            print("ID: {}, Title: {}, Author: {}".format(blog['id'], blog['title'], blog['author']))

    def _view_blog(self):
        blog_to_see = input("Copy and paste the blog ID to read the blog: ")
        blog = Blog.from_mongo(blog_to_see)
        posts = blog.get_posts()
        for post in posts:
            print("Date: {}, Title: {}\n\n{}".format(post['created_date'], post['title'], post['content']))