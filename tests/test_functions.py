# No tests yet
from marshmallow_more_delimeters.functions import get_results
from marshmallow import Schema, fields

class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.friends = []
        self.employer = None


class Blog:
    def __init__(self, title, author):
        self.title = title
        self.author = author  # A User object

class SubBlog:
    def __init__(self, title, blog):
        self.blog = blog  # A Blog object
        self.title = title

class SubSubBlog:
    def __init__(self, subblog):
        self.subblog = subblog  # A SubBlog object

class CollectionOfSubSubBlogs:
    def __init__(self):
        self.subsubblogs = []




class UserSchema(Schema):
    name = fields.String()
    email = fields.Email()
    created_at = fields.DateTime()

class BlogSchema(Schema):
    title = fields.String()
    author = fields.Nested(UserSchema)

class SubBlogSchema(Schema):
    blog = fields.Nested(BlogSchema)
    title = fields.String()

class SubSubBlogSchema(Schema):
    subblog = fields.Nested(SubBlogSchema)

class CollectionOfSubSubBlogsSchema(Schema):
    subsubblogs = fields.List(fields.Nested(SubSubBlogSchema))


user = User(name="Monty", email="monty@python.org")
user2 = User(name="Harry", email="harry@potter.com")

blog = Blog(title="Something Completely Different", author=user)
blog2 = Blog(title="Something Completely", author=user)
blog3 = Blog(title="Something", author=user2)

subblog = SubBlog(title="Lorem", blog=blog)
subblog2 = SubBlog(title="Lorem2", blog=blog)
subblog3 = SubBlog(title="Lorem2", blog=blog2)
subblog4 = SubBlog(title="Lorem2", blog=blog3)

subsubblog = SubSubBlog(subblog=subblog)
subsubblog2 = SubSubBlog(subblog=subblog2)
subsubblog3 = SubSubBlog(subblog=subblog3)
subsubblog4 = SubSubBlog(subblog=subblog4)

collectionOfSubSubBlogs = CollectionOfSubSubBlogs()
collectionOfSubSubBlogs.subsubblogs.append(subsubblog)
collectionOfSubSubBlogs.subsubblogs.append(subsubblog2)
collectionOfSubSubBlogs.subsubblogs.append(subsubblog3)
collectionOfSubSubBlogs.subsubblogs.append(subsubblog4)

def test_no_fields():
    res = get_results(BlogSchema, blog, [""])
    assert res["results"]["title"] == "Something Completely Different"

def test_not_nested():
    res = get_results(BlogSchema, blog, ["title"])
    assert res["results"]["title"] == "Something Completely Different"

def test_nested():
    res = get_results(BlogSchema, blog, ["author"])
    assert res["results"]["author"] == {'email': 'monty@python.org', 'name': 'Monty'}

    res = get_results(BlogSchema, blog, ["author.name"])
    assert res["results"]["author"] == {'name': 'Monty'}

def test_nested_nested():
    res = get_results(SubBlogSchema, subblog, ["blog.author"])
    assert res["results"] == {'blog': {'author': {'email': 'monty@python.org', 'name': 'Monty'}}}

    res = get_results(SubBlogSchema, subblog, ["blog.author.name"])
    assert res["results"] == {'blog': {'author': {'name': 'Monty'}}}

def test_nested_nested_nested():
    res = get_results(SubSubBlogSchema, subsubblog, ["subblog.blog.author"])
    assert res["results"] == {'subblog': {'blog': {'author': {'email': 'monty@python.org', 'name': 'Monty'}}}}

    res = get_results(SubSubBlogSchema, subsubblog, ["subblog.blog.author.name"])
    assert res["results"] == {'subblog': {'blog': {'author': {'name': 'Monty'}}}}

def test_collection():
    res = get_results(CollectionOfSubSubBlogsSchema, collectionOfSubSubBlogs, ["subsubblogs.subblog.title"])
    assert res["results"] == {'subsubblogs': [
        {'subblog': {'title': 'Lorem'}},
        {'subblog': {'title': 'Lorem2'}},
        {'subblog': {'title': 'Lorem2'}},
        {'subblog': {'title': 'Lorem2'}}]}

    res = get_results(CollectionOfSubSubBlogsSchema, collectionOfSubSubBlogs, ["subsubblogs.subblog.blog.author.name"])
    assert res["results"] == {'subsubblogs': [
        {'subblog': {'blog': {'author': {'name': 'Monty'}}}},
        {'subblog': {'blog': {'author': {'name': 'Monty'}}}},
        {'subblog': {'blog': {'author': {'name': 'Monty'}}}},
        {'subblog': {'blog': {'author': {'name': 'Harry'}}}}]}


def test_incorrect_fields():
    # TODO : Make sure this throws an exception
    res = get_results(SubSubBlogSchema, subsubblog, ["subblog.blog.author.badfield"])
    assert res["results"] == None and res["errors"][0]["code"] == 2

    # TODO : Make sure this throws an exception
    res = get_results(SubSubBlogSchema, subsubblog, ["subblog.blog.author.name.someextra"])
    assert res["results"] == None and res["errors"][0]["code"] == 2

    res = get_results(SubSubBlogSchema, subsubblog, ["subblog.blog.badobject.badfield"])
    assert res["results"] == None and res["errors"][0]["code"] == 2


    res = get_results(CollectionOfSubSubBlogsSchema, collectionOfSubSubBlogs, ["subsubblogs.subblog.badfield"])
    assert res["results"] == {'subsubblogs': [
        {'subblog': {}},
        {'subblog': {}},
        {'subblog': {}},
        {'subblog': {}}]}

    res = get_results(CollectionOfSubSubBlogsSchema, collectionOfSubSubBlogs, ["subsubblogs.subblog.blog.author.badfield"])
    assert res["results"] == {'subsubblogs': [
        {'subblog': {'blog': {'author': {}}}},
        {'subblog': {'blog': {'author': {}}}},
        {'subblog': {'blog': {'author': {}}}},
        {'subblog': {'blog': {'author': {}}}}]}
