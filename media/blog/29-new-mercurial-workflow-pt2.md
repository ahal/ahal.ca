## The New Mercurial Workflow - Part 2

This is a continuation of my previous post called [The New Mercurial Workflow][0]. It assumes that
you have at least read and experimented with it a bit. If you haven't, stop right now, read it, get
set up and try playing around with bookmarks and mozreview a bit.

I've had several requests for examples of more advanced usage with this workflow. The previous post
covered the basics, but it skipped many important concepts for the sake of brevity. Well that and
the fact that I'm still figuring out all of this myself. Rather than a step by step tutorial, each
section is its own independent concept which you can either use or choose to ignore. After all,
there is more than one way to skin a cat (apparently), and I make no claims that my way is the best.


## Pushing to Try

Probably the biggest thing I left out from the last post, is how to push to try. The easiest way is
to simply edit the commit message of the top most commit in your bookmark:

```bash
$ hg update my_feature
$ hg commit --amend -m "try: -b o -p linux -u mochitest-1 -t none"
$ hg push -f try
```

However this method isn't ideal for two reasons:

1. you have to re-edit your commit message back to something appropriate.
2. --amend will overwrite your old commit with whatever you have in the working directory. It is
easy to accidentally commit unintended changes, and unless you have the evolve extension installed
(more on this later) the old commit will be lost forever.

A better approach is to push an empty changeset with try syntax on top of your bookmark. The bad
news is that there is no good way to do this without using `mq`. The good news is that there is an
extension that will make this a lot easier (though you'll still need `mq` installed in your hgrc).
I'd recommend sfink's [trychooser extension][1] because it lets you choose syntax via a curses ui,
or manually (note the original extension of the same name by pbiggar is different). After cloning
and installing it, push to try:

```bash
$ hg update my_feature
$ hg trychooser
```

This opens a curses ui from which you can build your syntax (note it may be slightly out of date).
Alternatively, just specify the syntax manually:

```bash
$ hg update my_feature
$ hg trychooser -m "try: -b o -p linux -u mochitest-1 -t none"
```

There is a [bug on file][2] to move this extension into the standard [version-control-tools][3]
repository.

The mozreview folks are also working on the ability to autoland changesets pushed to review on try,
which should greatly simplify the common use case.


## Mutating History and Mozreview

In the last post, I showed you an example of addressing review comments by making an additional
commit and then squashing it later. But what if you push multiple commits to review and you intend
to land them all separately, without squashing them at the end? Here is the setup:

```bash
hg update my_feature
# ... add foo ...
hg commit -m "Bug 1234567 - Part 1: add the foo api"
# ... add bar ...
hg commit -m "Bug 1234567 - Part 2: add the bar api"
hg push -r my_feature review
```

Now you add a reviewer for each of the two commits and publish. Except the reviewer gives an r- to
the first commit and r+ to the second. Pushing a third commit to the review will make it difficult
to squash later. It is possible with rebasing, but there is a better way.

Mercurial has a new(ish) feature called [Changeset Evolution][4]. I won't go into detail here, but
you know how with git you can mutate history and then force push with `-f` and people say don't do
that since it could leave someone else in an unrecoverable state? This is because when you mutate
history in git, the old changeset is lost forever. With changeset evolution, the old changesets are
not thrown out, instead they are marked obsolete. It is then possible to push mutated history and
remote repositories can use these obsolescence markers to "do the right thing" without putting
someone else into an unrecoverable state. The mozreview repository is set up to use obsolescence
markers, which means mutating history and pushing to review is perfectly acceptable.

The first step is to clone and install the [evolve][5] extension (update to the stable branch).
Going back to the original example, we need to amend the first commit of our review push while
leaving the second one intact. First, let's update to the commit we'll be amending:

```bash
$ hg update "my_feature^"
# ... fix review comments ...
$ hg commit --amend
$ hg push -r my_feature review
```

Remember in the last section I said --amend would cause you to lose your old commit? In this case
`evolve` has actually modified the behaviour of --amend to mark the old changeset obsolete instead.
The review repository can then use this information to see that you have amended an existing commit
and update the review request accordingly. The end result is the review request will still only
contain two commits, but a second entry on the push slider will show up, allowing the reviewer to
see the original diff, the full diff and the interdiff with just the review fixes.

Amending is just one way to mutate history with `evolve`. You can also `prune` (delete), `uncommit`
and `fold` (squash). If you are interested in how `evolve` works, or want more details on what
it can do, I'd highly recommend [this tutorial][6].


## Tips for Working with Bookmarks

One thing that took me a little while to understand, was that bookmarks are not the same as git
branches. Yes, they are very similar and can be used in much the same way. But a bookmark is just a
label that automatically updates itself when activated. Unlike a git branch, there is no concept of
ownership between a bookmark and a commit. This can lead to some confusion when rebasing bookmarks on a
multi-headed repository like the unified firefox repo we set up in the previous post. Let's see what
might happen:

```bash
$ hg pull -u inbound 
$ hg rebase -b my_feature -d inbound 
$ hg pull -u fx-team
$ hg rebase -b my_feature -d fx-team
abort: can't rebase immutable changeset ad2042b4c668
```

What happened here? The important thing to understand is that the `-b` argument to `rebase` doesn't
stand for `bookmark`, it stands for `base`. You are telling hg to take every changeset from
`my_feature` all the way back to the common ancestor with `fx-team` and rebase them all on top of
`fx-team`. In this case, that includes all the public changesets that have landed on `inbound`, but
haven't yet landed on `fx-team`. And you can't rebase public changesets (rightfully so). Luckily,
it's still possible to rebase bookmarks automatically using [revsets][7]:

```bash
$ hg rebase -r "reverse(only(my_feature) and draft())" -d fx-team
```

This same revset can be used to log a bookmark and only that bookmark (log -f is useful, but
includes all ancestors of the bookmark, so it's not always obvious where the bookmark starts):

```bash
$ hg log -r "reverse(only(my_feature) and draft())"
```

The revset is somewhat long, so it helps to add an alias to your ~/.hgrc:

```ini
[revsetalias]
b($1) = reverse(only($1) and draft())
```

Now you can use it like so:

```bash
$ hg log -r "b(my_feature)"
```
    
This revset works for most simple cases, but it isn't perfect:

1. It will show an incorrect range if you pushed your bookmark to a publishing repo (e.g it is no longer draft).
2. It will show an incorrect range if you rebase your bookmark on top of draft changesets (e.g another bookmark).
3. It is slightly more annoying to write `-r "b(my_feature)"` than it is to write `-r my_feature`.

These shortcomings were annoying enough to me that I wrote an extension called [bookbinder][8].
Essentially if you pass in `-r <bookmark>` to a supported command, logbook will replace the
bookmark's revision with a revset containing all changesets "in" the bookmark. So far `log`,
`rebase`, `prune` and `fold` are wrapped by bookbinder. Bookbinder will also detect if bookmarks are
based on top of one another, and only use commits that actually belong to the bookmark you want to
see.  For example, the following does what you'd expect:

```bash
$ hg rebase -r bookmark_2 -d bookmark_1
$ hg rebase -r bookmark_3 -d bookmark_2
$ hg log -r bookmark_1
$ hg log -r bookmark_2
$ hg log -r bookmark_3
```

Because bookbinder only considers draft changesets, the following won't print anything:

```bash
$ hg update central
$ hg bookmark new_bookmark
$ hg log -r new_bookmark
```

If you actually want to treat the bookmark as a label to a revision instead, it's still possible by
escaping the bookmark with a period:

```bash
$ hg log -r .my_feature 
```

Bookbinder likely has some bugs to work out, so let me know if you run into problems using it.


## Shelving Changes

Finally I'd like to briefly mention `hg shelve`. It is more or less identical to `git stash` and is
an official extension. To install it add the following to ~/.hgrc:

```ini
[extensions]
shelve= 
```

I mostly use it for debug changes that I don't want to commit, but want to test both with and
without a particular change. My basic usage is:

```bash
# ... add debug statements ...
# ... test ...
hg shelve
hg update <rev>
hg unshelve
# ... test ...
hg revert -a
```

Edit: As of mercurial 3.3, you can update to another revision with uncommitted changes in your
working directory. This makes shelve much less useful, though it can still be handy from time to
time.

Closing Words
-------------

That more or less wraps up what I've learnt since the first post and I can't remember any other
pain points I had to work around. This workflow is still based on a lot of new tools that are still
under heavy development, but all things considered I think it has gone remarkably smoothly. The
setup involves installing a lot of extensions, but this should hopefully get better over time as
they move into core mercurial or version-control-tools. Have you run into any other pain points
using this workflow? If so, have you solved them?


[0]: http://ahal.ca/blog/2014/new-mercurial-workflow/
[1]: https://bitbucket.org/sfink/trychooser
[2]: https://bugzilla.mozilla.org/show_bug.cgi?id=974224
[3]: http://mozilla-version-control-tools.readthedocs.org/en/latest/
[4]: http://mercurial.selenic.com/wiki/ChangesetEvolution
[5]: http://42.netv6.net/evolve-main/
[6]: http://www.gerg.ca/evolve/user-guide.html
[7]: http://selenic.com/hg/help/revsets
[8]: https://bitbucket.org/halbersa/bookbinder
