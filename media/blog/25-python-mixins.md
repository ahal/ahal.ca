## When would you use a Python mixin?

That's not a rhetorical question. I'd like to know in which scenarios a mixin in python really is
the best option. I can't seem to think of any, but maybe I'm not thinking outside the box enough.

The basic idea of a mixin is to create a small re-usable class that can "plug-in" to other larger
classes. From the [wikipedia definition][1], a mixin is a way to compose classes together *without*
using inheritance. The problem is unlike ruby, python mixins are a purely conceptual construct.
Python mixins *are* inheritance (the only difference is that the class name usually contains
'Mixin'). It is up to the developer to remember this, and to manually avoid all of the common
pitfalls of multiple inheritance. This kind of defeats the whole purpose of the mixin in the first
place. What's more is that most people use python mixins improperly.

Consider the following example:

```python
from book import Book
from index import IndexMixin

class TextBook(Book, IndexMixin):
    def __init__(self, name, contents, edition='1st'):
        Book.__init__(self, name, contents)
        self.edition = edition

t = TextBook('Learn Python the Hard Way')
t.search('python')
>>> 0 results found
```

Here we correctly use inheritance to denote `Book` as a base class, a textbook *is a* book. We use
an `IndexMixin` because textbooks aren't indices, they *have an* index. We then instantiate it and
search the book for the string 'python'. Wait a minute, how can a textbook about python not contain
the word python? In python, the multiple inheritance chain is read *right to left*, this means
that IndexMixin is technically the base class here. It just so happens that `IndexMixin` also has a
function called `search` which overrides the one defined in `Book`.

It turns out there's another way to compose classes together without using inheritance. Just *use*
the class (or module) directly:

```python
from book import Book
from index import Index

class TextBook(Book):
    def __init__(self, name, contents, edition='1st'):    
        Book.__init__(self, name, contents)
        self.edition = edition
        self.index = Index()

t = TextBook('Learn Python the Hard Way')
t.search('python')
>>> Many results found

t.index.search('python')
>>> 0 results found
```

If the relationship between objects A and B is "A is a B", then B is a base class, not a mixin. If
the relationship is "A has a B", then why not use composition? What benefit does a mixin give you?

[1]: http://en.wikipedia.org/wiki/Mixin
