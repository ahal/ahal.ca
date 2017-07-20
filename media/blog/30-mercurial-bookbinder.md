## Making mercurial bookmarks more git-like

I mentioned in my previous post a mercurial extension I wrote for making bookmarks easier to
manipulate. Since then it has undergone a large overhaul, and I believe it is now stable and
intuitive enough to advertise a bit more widely.

## Introducing bookbinder

When working with bookmarks (or anonymous heads) I often wanted to operate on the
entire series of commits within the feature I was working on. I often found myself digging out
revision numbers to find the first commit in a bookmark to do things like rebasing, grafting or
diffing. This was annoying. I wanted bookmarks to work more like a git-style branch, that has a
definite start as well as an end. And I wanted to be able to easily refer to the set of commits
contained within. Enter [bookbinder][0].

First, you can install bookbinder by cloning:

```bash
$ hg clone https://bitbucket.org/halbersa/bookbinder
```

Then add the following to your hgrc:

```ini
[extensions]
bookbinder = path/to/bookbinder
```

Usage is simple. Any command that accepts a revset with --rev, will be wrapped so that bookmark
labels are replaced with the series of commits contained within the bookmark.

For example, let's say we create a bookmark to work on a feature called foo and make two commits:

```bash
$ hg log -f
changeset:   2:fcd3bdafbc88
bookmark:    foo 
summary:     Modify foo

changeset:   1:8dec92fc1b1c
summary:     Implement foo

changeset:   0:165467d1f143
summary:     Initial commit
```

Without bookbinder, bookmarks are only labels to a commit:

```bash
$ hg log -r foo
changeset:   2:fcd3bdafbc88
bookmark:    foo 
summary:     Modify foo
```

But with bookbinder, bookmarks become a logical series of related commits. They are more similar
to git-style branches:

```bash
$ hg log -r foo
changeset:   2:fcd3bdafbc88
bookmark:    foo 
summary:     Modify foo

changeset:   1:8dec92fc1b1c
summary:     Implement foo
```

Remember `hg log` is just one example. Bookbinder automatically detects and wraps all commands that have a --rev option and that can
receive a series of commits. It even finds commands from arbitrary extensions that may be installed!
Here are few examples that I've found handy in addition to `hg log`:

```bash
$ hg rebase -r <bookbark> -d <dest>
$ hg diff -r <bookmark>
$ hg graft -r <bookmark>
$ hg grep -r <bookmark>
$ hg fold -r <bookmark>
$ hg prune -r <bookmark>
# etc.
```

They all replace the single commit pointed to by the bookmark with the series of commits within the
bookmark. But what if you actually only want the single commit pointed to by the bookmark label?
Bookbinder uses '.' as an escape character, so using the example above:

```bash
$ hg log -r .foo
changeset:   2:fcd3bdafbc88
bookmark:    foo 
summary:     Modify foo
```

Bookbinder will also detect if bookmarks are based on top of one another:

```bash
$ hg rebase -r my_bookmark_2 -d my_bookmark_1
```

Running `hg log -r my_bookmark_2` will not print any of the commits contained by `my_bookmark_1`.

## The gory details

But how does bookbinder know where one feature ends, and another begins? Bookbinder implements a new
revset called "feature". The feature revset is roughly equivalent to the following alias
(kudos to smacleod for coming up with it):

```ini
[revsetalias]
feature($1) = ($1 or (ancestors($1) and not (excludemarks($1) or hg ancestors(excludemarks($1))))) and not public() and not merge()
excludemarks($1) = ancestors(parents($1)) and bookmark()
```

Here is a formal definition. A commit C is "within" a feature branch ending at revision R if all of
the following statements are true:

1. C is R or C is an ancestor of R
2. C is not public
3. C is not a merge commit
4. no bookmarks exist in [C, R) for C != R
5. all commits in (C, R) are also within R for C != R

In easier to understand terms, this means all ancestors of a revision that aren't public, a merge
commit or part of a different bookmark, are within that revision's 'feature'. One thing to be aware
of, is that this definition allows empty bookmarks. For example, if you create a new bookmark on a
public commit and haven't made any changes yet, that bookmark is "empty". Running `hg log -r` with
an empty bookmark won't have any output.

The feature revset that bookbinder exposes, works just as well on revisions that don't have any
associated bookmark. For example, if you are working with an anonymous head, you could do:

```bash
$ hg log -r 'feature(<rev>)'
```

In fact, when you pass in a bookmark label to a supported command, bookbinder is literally just
substituting `-r <bookmark>` with `-r feature(<bookmark>)`. All the hard work is happening in the
feature revset.

In closing, bookbinder has helped me make a lot more sense out of my bookmark based workflow. It's solving a
problem I think should be handled in mercurial core, maybe one day I'll attempt to submit a patch
upstream. But until then, I hope it can be useful to others as well.

[0]: https://bitbucket.org/halbersa/bookbinder
