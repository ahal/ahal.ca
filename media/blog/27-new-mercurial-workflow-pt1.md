## The New Mercurial Workflow

There's a good chance you've heard something about a new review tool coming to Mozilla and how it will *change
everything*. There's an even better chance you've stumbled across one of gps' [blog posts][0] on how
we use mercurial at Mozilla.

With [mozreview entering beta][1], I decided to throw out my old mq based workflow and
try to use all the latest and greatest tools. That means [mercurial bookmarks][2], a [unified
mozilla-central][3], using [mozreview][4] and completely [expunging mq][5] from my workflow.

Making all these changes at the same time was a little bit daunting, but the end result seems to be
a much easier and more efficient workflow. I'm writing the steps I took down in case it helps
someone else interested in making the switch. Everything in this post is either repeating the
mozreview documentation or one of gps' blog posts, but I figured it might help for a step by step
tutorial that puts all the pieces together, from someone who is also a mercurial noob.

## Setup

#### Mercurial

Before starting you need to do a bit of setup. You'll need the mercurial `reviewboard` and
`firefoxtree` extensions and mercurial 3.0 or later. Luckily you can run:

```bash
$ mach mercurial-setup
```

And hitting 'yes' to everything should get you what you need. Make sure you at least enable the
rebase extension. In my case, mercurial > 3.0 didn't exist in my package repositories (Fedora 20)
so I had to [download][6] and install it manually.

#### MozReview

There is also some setup required to use the mozreview tool. Follow the [instructions][7] to get
started.


#### Tagging the Baseline

Because we enabled the `firefoxtree` extension, anytime we pull a remote repo from hg.mozilla.org, a
local tag will be created for us. So before proceeding further, make sure we have our baseline
tagged:

```bash
$ hg pull https://hg.mozilla.org/mozilla-central
$ hg log -r central
```

Now we know where mozilla-central tip is. This is important because we'll be pulling mozilla-inbound
on top later.


#### Create path Aliases

Edit: Apparently the [firefoxtree][11] extension provides built-in aliases so there's no need to do
this step. The aliases follow the `central`, `inbound`, `aurora` convention. Just be aware that you
won't be able to push to these default aliases. If you want to push, you'll need to add your own
custom aliases with ssh:// urls, e.g `ssh://hg.mozilla.org/mozilla-central`.

<strike>
Typing the url out each time is tiresome, so I recommend creating path aliases in your ~/.hgrc:

```ini
[paths]
m-c = https://hg.mozilla.org/mozilla-central
m-i = https://hg.mozilla.org/integration/mozilla-inbound
m-a = https://hg.mozilla-org/releases/mozilla-aurora
m-b = https://hg.mozilla-org/releases/mozilla-beta
m-r = https://hg.mozilla-org/releases/mozilla-release
```
</strike>

#### Learning Bookmarks

It's a good idea to be at least somewhat familiar with bookmarks before starting. Reading [this
tutorial][7] is a great primer on what to expect.


## Start Working on a Bug

Now that we're all set up and we understand the basics of bookmarks, it's time to get started.
Create a bookmark for the feature work you want to do:

```bash
$ hg bookmark my_feature
```

Make changes and commit as often as you want. Make sure at least one of the commits has the bug number
associated with your work, this will be used by mozreview later:

```bash
... do some changes ...
$ hg commit -m "Bug 1234567 - Fix that thing that is broken"
... do more changes ...
$ hg commit -m "Only one commit message needs a bug number"
```

Maybe you want to pull central again and rebase your changes on top of it. No problem:

```bash
$ hg update central
$ hg pull m-c
$ hg rebase -b my_feature -d central
```


## Pushing a Bookmark for Review

When you are ready for review, all you do is:

```bash
$ hg update my_feature
$ hg push review
```

Mercurial will automatically push the currently active bookmark to the review repository. This is
equivalent (no need to update):

```bash
$ hg push -r my_feature review
```

At this point you should see some links being dumped to the console, one for each commit in your
bookmark as well as a parent link to the overall review. Open this last link to see your review
request. At this stage, the review is unpublished, you'll need to add some reviewers and publish it
before anyone else can see it. Instead of explaining how to do this, I highly recommend reading the
[mozreview instructions][9] carefully. I would have saved myself a lot of time if I had just paid
closer attention to them.

Once published, mozreview will automatically update the associated bug with appropriate information.


## Fixing Review Comments

If all went well, someone has received your review request. If you need to make some follow up
changes, it's super easy. Just activate the bookmark, make a new commit and re-push:

```bash
$ hg update my_feature
... fix review comments ...
$ hg commit -m "Address review comments"
$ hg push review
```

Mozreview will automatically detect which commits have been pushed to the review server and update
the review accordingly. In the reviewboard UI it will be possible for reviewers to see both the
interdiff and the full diff by moving a push slider around.


## Pushing to Inbound

Once you've received the r+, it's time to push to mozilla-inbound. Remember that `firefoxtree` makes
local tags when you pull from a remote repo on hg.mozilla.org, so let's do that:

```bash
$ hg update central
$ hg pull m-i
$ hg log -r inbound
```

Next we rebase our bookmark on top of inbound. In this case I want to use the --collapse argument to
fold the review changes into the original commit:

```bash
$ hg rebase -b my_feature -d inbound --collapse
```

A file will open in your default editor where you can modify the commit message to whatever you
want. In this case I'll just delete everything except the original commit message and add "r=".

And now everything is ready! Verify you are pushing what you expect and push:

```bash
$ hg outgoing -r my_feature m-i
$ hg push -r my_feature m-i
```


## Pushing to other Branches

The beauty of this system is that it is trivial to land patches on any tree you want. If I wanted to
land `my_feature` on aurora:

```bash
$ hg pull m-a
$ hg rebase -b my_feature -d aurora
$ hg outgoing -r my_feature m-a
$ hg push -r my_feature m-a
```


## Syncing work across Computers

You can use a remote clone of mozilla-central to sync bookmarks between computers. Instead of
pushing with `-r`, push with `-B`. This will publish the bookmark on the remote server:

```bash
$ hg push -B my_feature <my remote mercurial server>
```

From another computer, you can pull the bookmark in the same way:

```bash
$ hg pull -B my_feature <my remote mercurial server>
```

WARNING: Mercurial repositories are publishing by default! This means that when you push a commit to
them, they will mark the commit as public on your local clone which means you won't be able to push
them to either the review server or mozilla-inbound. If you did this by accident and a commit was
made public when it shouldn't be, you can run:

```
$ hg phase -f --draft <rev>
```

To prevent this, you can make a repository non-publishing by adding the following to its `.hg/hgrc`
file:

```ini
[phases]
publish=false
```

## Conclusion

I'll need to play around with things a little more, but so far everything has been working exactly
as advertised. Kudos to everyone involved in making this workflow possible!

    
[0]: http://gregoryszorc.com/blog/category/mercurial/
[1]: https://groups.google.com/forum/#!topic/mozilla.dev.platform/RMkSXq2ckFk
[2]: http://mercurial.selenic.com/wiki/Bookmarks
[3]: http://gregoryszorc.com/blog/2014/06/30/track-firefox-repositories-with-local-only-mercurial-tags/
[4]: http://mozilla-version-control-tools.readthedocs.org/en/latest/mozreview.html
[5]: http://gregoryszorc.com/blog/2014/06/23/please-stop-using-mq/
[6]: http://mercurial.selenic.com/downloads
[7]: http://mozilla-version-control-tools.readthedocs.org/en/latest/mozreview/install.html
[8]: http://mercurial.aragost.com/kick-start/en/bookmarks/
[9]: http://mozilla-version-control-tools.readthedocs.org/en/latest/mozreview/reviewboard.html
[11]: https://mozilla-version-control-tools.readthedocs.org/en/latest/hgmozilla/firefoxtree.html
