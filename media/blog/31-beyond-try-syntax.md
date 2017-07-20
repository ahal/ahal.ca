## Looking beyond Try Syntax

Today marks the 5 year anniversary of try syntax. For the uninitiated, try syntax is a string that
you put into your commit message which a [parser][0] then uses to determine the set of builds and
tests to run on your try push. A common try syntax might look like this:

    try: -b o -p linux -u mochitest -t none

Since inception, it has been a core part of the Mozilla development workflow.
For many years it has served us well, and even today it serves us passably. But it is almost time
for try syntax to don the wooden overcoat, and this post will explain why.

## A brief history on try syntax

In the old days, pushing to try involved a web interface called [`sendchange.cgi`][19]. Pushing is
probably the wrong word to use, as at no point did the process involve version control. Instead, patches
were uploaded to the web service, which in turn invoked a buildbot sendchange with all the
required arguments. Like today try server was often overloaded, sometimes taking over 4 hours for
results to come back. Unlike today there was no way to pick and choose which builds and tests you
wanted, every try push ran the full set.

The obvious solution was to create a mechanism for people to do that. It was while brainstorming
this problem that ted, bhearsum and jorendorff came up with the idea of encoding this information
in the commit message. Try syntax was first implemented by lsblakk in [bug 473184][1] and landed
on August 27th, 2010. It was a simple time; the list of valid builders could fit into a
[single 30 line config file][2]; Fennec still hadn't picked up full steam; and B2G wasn't even
a figment of anyone's wildest imagination.

It's probably not a surprise to anyone that as time went on, things got more complicated. As more
build types, platforms and test jobs were added, the try syntax got harder to memorize. To help
deal with this, lsblakk created the [trychooser syntax builder][3] just a few months later. In
2011, pbiggar created the [trychooser mercurial extension][4] (which was later
[forked and improved][5] by sfink). These tools were (and still are) the canonical way to
build a try syntax string. Little has changed since then, with the exception of the [mach try][6]
command that chmanchester implemented around June 2015.

## One step forward, two steps back

Since around 2013, the number of platforms and test configurations have grown at an unprecendented
rate. So much so, that the various trychooser tools have been perpetually out of date. Any time
someone got around to adding a new job to the tools, two other jobs had already sprung up in its
place. Another problem caused by this rapid growth, was that try syntax became finicky.
There were a lot of edge cases, exceptions to the rule and arbitrary aliases. Often jobs would
mysteriously not show up when they should, or mysteriously show up when they shouldn't.

Both of those problems were exacerbated by the fact that the actual [try parser][0] code has never
had a definite owner. Since it was first created, there have never been more than 11 commits in a
year. There have been only two commits to date in 2015.

## Two key insights

At this point, there are two things that are worth calling out:

1. Generating try strings from memory is getting harder and harder, and for many cases is nigh
   impossible. We rely more and more on tools like trychooser.
2. Try syntax is sort of like an API on which these tools are built on top of.

What this means is that primary generators of try syntax have shifted from humans to tools. A
command line encoded in a commit message is convenient if you're a human generating the syntax
manually. But as far as tooling goes, try syntax is one god awful API. Not only do the tools need to
figure out the magic strings, they need to interact with version control, create an empty commit and
push it to a remote repository.

There is also tooling on the other side of the see saw, things that process the try syntax post
push. We've already seen buildbot's [try parser][0] but taskcluster has a [separate try parser][15] as
well. This means that your try push has different behaviour, depending on whether the jobs are scheduled
in buildbot or taskcluster. There are other one off tools that do some try syntax parsing as well, including but
not limited to [try tools][7] in mozharness, the try re-trigger bot and the [AWSY][8] dashboard. These
tools are all forced to share and parse the same try syntax string, so they have to be careful not to
step on each other's toes.

The takeaway here is that for tools, a string encoded as a commit message is quite limiting and a lot less
convenient than say, calling a function in a library.

## Despair not, young Padawan

So far we've seen how try syntax is finicky, how the tools that use it are often outdated and how
it fails as an API. But what is the alternative? Fortunately, over the course of 2015 a lot of
progress has been made on projects that for the first time, give us a viable alternative to try
syntax.

First and foremost, is [mozci][9]. Mozci, created by [armenzg][17] and [adusca][16], is a tool that hooks into
the build api (with early support for taskcluster as well). It can do things like schedule builds and
tests against any arbitrary pushes, and is being used on the backend for tools like adusca's
[try-extender][10] with integration directly into treeherder planned.

Another project that improves the situation is [taskcluster][11] itself. With taskcluster, job
configuration and scheduling all lives in tree. Thanks to bhearsum's [buildbot bridge][12], we can even use
taskcluster to schedule jobs that still live in buildbot. There's an opportunity here to leverage
these new tools in conjunction with mozci to gain complete and total control over how jobs are
scheduled on try.

Finally I'd like to call out [mach try][6] once more. It is more than a thin wrapper around try
syntax that handles your push for you. It actually lets you control *how the harness gets run within
a job*. For now this is limited to test paths and tags, but there is a lot of potential to do some cool
things here. One of the current limiting factors is the unexpressiveness of the try syntax API.
Hopefully this won't be a problem too much longer. Oh yeah, and [mach try][6] also works with git.

## A glimpse into the crystal ball

So we have several different projects all coming together at once. The hard part is figuring out how they
all tie in together. What do we want to tackle first? How might the future look? I want to be clear
that none of this is imminent. This is a look into what might be, not what will be.

There are two places we mainly care about scheduling jobs on try.

First imagine you push your change to try. You open up treeherder, except no jobs are scheduled.
Instead you see every possible job in a distinct greyed out colour. Scheduling what you want is as
simple as clicking the desired job icons. Hold on a sec, you don't have to imagine it. Adusca
already has a [prototype][13] of what this might look like. Being able to schedule your try jobs
this way has a huge benefit: you don't need to mentally correlate job symbols to job names. It's as
easy as point and click.

Second, is pushing a predefined set of jobs to try from the command line, similar to how things work
now. It's often handy to have the try command for a specific job set in your shell history and it's
a pain to open up treeherder for a simple push that you've memorized and run dozens of times. There are
a few improvements we can do here:

* We can move the curses ui feature of the [hg trychooser extension][5] into [mach try][6].
* We can use [mozci][9] to automatically keep the known list of jobs up to date. This is useful for
  things like generating the curses ui on the fly, validation and tab completion.
* We can use mozci + taskcluster + buildbot bridge to provide a much more expressive API for
  scheduling jobs. For example, you could easily push a [T-style][14] try run.
* We can expand some of the functionality in [mach try][6] for controlling how the harnesses are run,
  for example we could use it to enable some of the debugging features of the harness while
  investigating test failures.

Finally for those who are stuck in their ways, it should still be possible to have a "classic try syntax"
front-end to the new [mozci backend][18]. As large as this change sounds, it could be mostly 
transparent to the user. While I'm certainly not a fan of the current try syntax, there's no reason
to begrudge the people who are.

## Closing words ##

Try syntax has served us well for 5 long years. But it's almost time to move on to something better.
Soon a lot of new avenues will be open and tools will be created that none of us have thought of
yet. I'd like to thank all of the people mentioned in this post for their contributions in this
area and I'm very excited for what the future holds.

The future is bright, and change is for the better.


[0]: http://hg.mozilla.org/build/buildbotcustom/file/tip/try_parser.py
[1]: https://bugzilla.mozilla.org/show_bug.cgi?id=473184
[2]: http://hg.mozilla.org/build/buildbotcustom/file/f3e7d89cae13/valid_builders.py
[3]: http://trychooser.pub.build.mozilla.org/
[4]: https://github.com/pbiggar/trychooser
[5]: https://bitbucket.org/sfink/trychooser
[6]: http://chmanchester.github.io/blog/2015/07/26/introducing-mach-try/
[7]: https://dxr.mozilla.org/mozilla-central/source/testing/mozharness/mozharness/mozilla/testing/try_tools.py#16
[8]: https://areweslimyet.com/
[9]: http://mozilla-ci-tools.readthedocs.org/en/latest/
[10]: http://try-extender.herokuapp.com/
[11]: http://docs.taskcluster.net/
[12]: https://github.com/mozilla/buildbot-bridge
[13]: https://drive.google.com/folderview?id=0B7rHgvgC7s4ZflY4cmtSSUJjcHVqQktIMGljcE5nLW9jaWx5T21CQ3F5QllSVGtDQl9sSGM&usp=sharing
[14]: https://wiki.mozilla.org/Sheriffing/How:To:Recommended_Try_Practices
[15]: http://hg.mozilla.org/mozilla-central/file/tip/testing/taskcluster/taskcluster_graph/commit_parser.py
[16]: http://explique.me/
[17]: http://armenzg.blogspot.ca/
[18]: https://bugzilla.mozilla.org/show_bug.cgi?id=1198341
[19]: https://github.com/jrmuizel/mozilla-cvs-history/blob/master/webtools/buildbot-try/sendchange.cgi
