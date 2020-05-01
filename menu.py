from database import Database
from models.blog import Blog
import pymongo

class Menu(object): # extends from object
    def __init__(self):
        # Ask the user for author name
        self.user = input("\nHi! What's your login? ")
        # Make an instance of user_blog, to which blog will equal to if exists:
        self.user_blog = None
        if self._user_has_account():
            print (f"\nWelcome back, {self.user}")
        else:
            self._prompt_user_for_account()

    # Check if user already got an account:
    def _user_has_account(self):
        # Search for the blog author:
        blog = Database.find_one(collection='blogs', query={'author': self.user})
        if blog is not None:
            # Assign an object of type blog to user blog
            self.user_blog = Blog.from_mongo_id(blog['id'])
            return True
        else:
            return False

    # If user has no account yet, prompt them to create one:
    def _prompt_user_for_account(self):
        title = input("\nEnter blog title: ")
        description = input("\nEnter blog description: ")
        blog = Blog(author=self.user,
                    title=title,
                    description=description)
        blog.save_to_mongo()
        self.user_blog = blog


    def run_menu(self):
        # User read or write blogs?
        action = input("""\nWhat would you like to do today?\n\nChoose one of the following options:
        Read a blog entrees (R)
        Write a post (W)
        Delete a blog (DB)
        Delete an entree from your blog (DE)\n""")
        if action == "R" or action == "r":
            # List blogs in Database:
            self._list_blogs()
            # Allow the user to pick one and display posts:
            self._view_blog()

        elif action == "W" or action == "w":
            # Prompt to write a post:
            self.user_blog.new_post()

        elif action == "DB" or action == "db":
            # List blogs in Database:
            self._list_blogs()
            # ALlow user to delete a blog:
            self._delete_blog()

        elif action == "DE" or action == "de":
            # Let the user to delete an entree:
            self._delete_entree()

        else:
            print("\nThanks and bye!\n")

    def _delete_blog(self):
        blog_to_delete = input("\nCopy and paste the blog ID to delete it: ")
        Database.delete_one(collection='blogs', query={'id': blog_to_delete})
        print(f"\nBlog {blog_to_delete} deleted!\n")

    def _delete_entree(self):
        blog = Blog.from_mongo_author(self.user)
        # Show all posts
        posts = blog.get_posts()
        print("\nHere are all your posts: ")
        for post in posts:
            print(f"\nID: {post['id']}, Date: {post['created_date']}, Title: {post['title']}\n\n{post['content']}\n")
        entree_to_delete = input("\nCopy and paste the ID of an entree to delete it: ")
        Database.delete_one(collection='posts', query={'id': entree_to_delete})
        print(f"\nEntree {entree_to_delete} deleted!\n")

    def _list_blogs(self):
        blogs = Database.find(collection='blogs',
                            query={})
        for blog in blogs:
            print(f"\nID: {blog['id']}, Title: {blog['title']}, Author: {blog['author']}")
            # Blog ID: {blog['blog_id']},

    def _view_blog(self):
        blog_to_see = input("\nCopy and paste the blog ID to read the blog: ")
        blog = Blog.from_mongo_id(blog_to_see) # found blog object
        posts = blog.get_posts()
        for post in posts:
            print(f"\nID: {post['id']}, Date: {post['created_date']}, Title: {post['title']}\n\n{post['content']}\n")
