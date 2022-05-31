

from dataclasses import dataclass, field
from uuid import uuid4
from datetime import datetime
import re


@dataclass
class Post:
    _id: str = field(default_factory=lambda: uuid4().hex)
    created_at: datetime = field(default_factory=datetime.now)
    content: str = ""


@dataclass
class User:
    name: str
    email: str
    dl_number: str
    posts: dict[str, Post] = field(default_factory=dict)

    def create_post(self, content):
        post = Post(content=content)
        self.posts[post._id] = post

    def delete_post(self, post_id):
        del self.posts[post_id]

    def update_post(self, post_id, content):
        self.posts[post_id].content = content

    def get_posts(self):
        return self.posts.values()

    def get_post(self, post_id):
        return self.posts[post_id]

    def find_posts_with_string(self, string):
        for post in self.posts.values():
            if string in post.content:
                yield post

    def find_posts_matching_regex(self, regex):
        for post in self.posts.values():
            if regex.search(post.content):
                yield post


def main():
    print("Creating new user John")
    user = User(name="John", email="john@gmail.com", dl_number="123456789")

    print("\nAdding a few posts")
    user.create_post("Hello, World!")
    user.create_post("Goodbye, World!")
    user.create_post("Goodbye, Heaven!")

    print("\nGetting all posts")
    print(user.get_posts())

    print("\nGetting all posts with string 'World'")
    for post in user.find_posts_with_string("World"):
        print(post)

    print("\nGetting all posts matching regex '^Goodbye'")
    for post in user.find_posts_matching_regex(regex=re.compile("^Goodbye")):
        print(post)

    print("\nDeleting the first post with the string 'Goodbye'")
    user.delete_post(next(iter(user.get_posts()))._id)

    print("\nGetting all posts")
    print(user.get_posts())


if __name__ == '__main__':
    main()
