## A Course of Action for Replacing Try Syntax

I've previously [blogged][0] about why I believe try syntax is an antiquated development process
that should be replaced with something more modern and flexible. What follows is a series of ideas
that I'm trying to convert into a concrete plan of action to bring this about. This is not an
*Intent to Implement* or anything like that, but my hope is that this outline is detailed enough
that it could be used as a solid starting point by someone with enough time and motivation to
work on it.

This plan of action will operate on the rather large assumption that all tasks are scheduled with
taskcluster (either natively or over BuildbotBridge). I also want to be clear that I'm not talking
about removing try syntax completely. I simply think it should be parsed client side, *before* any
changes get pushed to try.


## Brief Overview of How Try Syntax Currently Works in Taskcluster

In order to understand where we're going, I think it's important to be aware of where we're coming
from. This is a high level explanation of how a try syntax string currently gets turned into running
tasks:

1. A developer pushes a commit to try with a 'try:' token somewhere in the commit message.
2. The pushlog mercurial extension picks this up on the server, and publishes a [JSON stream][1].
3. After getting triggered via a pulse message, the [mozilla-taskcluster][2] module [queries][3]
   this URL and [pulls in][4] the relevant push.
4. Then, [mozilla-taskcluster][2] grabs the last commit in the push, extracts the try syntax from
   the description, and uses it to create a [templating variable][5].
5. This template variable is substituted into the [decision task's][6] configuration, and ultimately
   ends up getting [passed into][7] `mach taskgraph decision` with the `--message` parameter.
6. The decision task kicks off the [taskgraph generation][8] process. When it comes time to
   [optimize][9], the try syntax is finally passed into the [TryOptionSyntax][10] parser, which
   filters out tasks that don't match any of the try options.
7. The optimized task graph is then submitted to taskcluster, and the relevant tasks start running
   on try.


## An Improved Data Transport

A key thing to realize, is that the decision task runs from within a mozilla-central clone. In other
words the try syntax string starts in version control, gets published to a webserver, gets
downloaded by a node module, gets substituted into a task configuration, only to be passed into a
process that had full access to the original version control all along. Steps 2-5 in the previous
section, could be replaced with:

* The decision task extracts the try syntax from the appropriate commit message.

If we stopped there, this change wouldn't be worth making. It might make some code a bit cleaner,
but would hardly make things faster or more efficient since mozilla-taskcluster would still need to
query the pushlog either way. But this method has another, more important benefit: it gives the
decision task access to the entire commit instead of limiting it to whatever the pushlog extension
decides to publish.

That means there would be no particular reason we'd need to store try syntax strings in the commit
message at all. We could instead stuff it into the commit as arbitrary metadata using the commit's
`extra` field. To get this working, we could use the [push-to-try][11] extension to stuff the try
syntax into the `extra` field like [this][12]. Then the decision task could extract that syntax out
of the commit metadata like this:

```bash
$ hg log -r $GECKO_HEAD_REV -T "{extras}"
```

## An Improved Data Format

Again, these changes mostly amount to a refactoring and wouldn't be worth making just for the sake
of it. But once we are using arbitrary commit metadata to pass information to the decision task,
there's no reason for us to limit ourselves to a single line syntax string. We could use data
structures of arbitrary complexity.

One possibility (which I'll run with for the rest of the post), is simply to use a list of
taskcluster task labels as the data format. This has several advantages:

* It's unambiguous (what is passed in, is what will be scheduled)
* It's an easy target for tools to generate to
* It provides flexibility in how we could potentially interact with try (via said tools)

The last two points are pretty big, have you ever attempted to write a tool that tries to convert
inputs into a try sytnax? It's very hard, and involves lots of hard coding in the tool and
memorization on the part of the users.

What we've done to this point is transform the data transport from a human friendly format to a
machine friendly format on top of which human friendly tools can be built. Probably the first tool
that will need to be built, will be a legacy try syntax specifier for those of us who enjoy writing
out try syntax strings. But that's not very interesting. There are probably a hundred different ways
we could dream of specifying tasks, but because my imagination is limited, I'll just talk about one
potential idea.


## Fuzzy Finding Tasks

I've recently discovered and become a huge fan of [fuzzyfinder][13]. Fuzzyfinder the project
consists of two parts:

1. A binary called `fzf`
2. A vast multitude of shell and editor integrations that utilize `fzf`

The integrations allow you to quickly find things like file paths, processes and shell history (both
on the terminal or within an editor) with an intelligent [approximate matching][14] algorithm at
blazing speeds. While the integrations are insanely useful, it's the binary itself that would come
in useful here.

The `fzf` binary is actually quite simple. It receives a list of strings through `stdin`, allows the
user to select one or more of them using the fuzzy finding algorithm and a text based gui, then
prints all selected strings to `stdout`. The input is completely arbitrary, for example, I could
fuzzy select running processes with:

```bash
$ ps -ef | fzf
```

Or lines in a file:

```bash
$ cat foo.txt | fzf
```

Or the numbers 1-100:

```bash
$ seq 100 | fzf
```

You get the idea. The other day I was thinking, what if we could pipe a list of every single task,
expanded over both chunks and platforms, into `fzf`? How useful would that be? Luckily, a list of
all taskcluster tasks can be generated with a mach command, so it was easy to test this out:

```bash
$ mach taskgraph tasks -p artifacts/parameters.yml -q > all-tasks.json
$ cat all-tasks.json | fzf -m
```

The `parameters.yml` file can be downloaded from any decision task on treeherder. I piped it into a
file because the `mach taskgraph` command takes a bit of time to complete, it's not a penalty we'd
want to incur on subsequent runs unless it was necessary. The `-m` tells `fzf` to allow
multi-selection.

The results were wonderful. But rather than try to describe how awesome the new (potential) try
choosing experience was, I created a demo. In this scenario, pretend I want to select all linux32
opt mochitest-chrome tasks:

<video width="100%" height="100%" controls>
<source src="/static/vid/blog/2016/try-fzf.mp4" type="video/mp4">
</video>

Now instead of printing the task labels to `stdout`, imagine if this theoretical try chooser stuffed
that output into the commit's metadata. This is the last piece of the puzzle, to what I believe is a
comprehensive outline towards a viable replacement for try syntax.


## No Plan Survives Breakfast

As Mike Conley is fond of saying, no plan survives breakfast. I'm sure my outline here is full of
holes that will need to be patched, but I think (hope) that at least the overall direction is solid.
While I'd love to work on this, I won't have the time or mandate to do so until later in the year.
With this post I hope to accomplish three things:

1. Serve as a brain dump so when (or if) I do get back to it, I'll remember everything
2. Motivate others to push in this direction in the meantime (or better yet, implement the whole
   thing!)
3. Provide an excuse to plug [fuzzyfinder][13]. It's been months and using it still makes me giddy.
   Seriously, give it a try, you'll be glad you did!

Let me know if you have any feedback, and especially if you have any other crazy ideas for selecting
tasks on try!


[0]: https://ahal.ca/blog/2015/try-syntax/
[1]: https://hg.mozilla.org/try/json-pushes?full=1
[2]: https://github.com/taskcluster/mozilla-taskcluster
[3]: https://github.com/taskcluster/mozilla-taskcluster/blob/4c45d5d0d1da012fcc541998ec7f611175464189/src/pushlog/client.js#L109
[4]: https://github.com/taskcluster/mozilla-taskcluster/blob/4c45d5d0d1da012fcc541998ec7f611175464189/src/jobs/taskcluster_graph.js#L82
[5]: https://github.com/taskcluster/mozilla-taskcluster/blob/4c45d5d0d1da012fcc541998ec7f611175464189/src/jobs/taskcluster_graph.js#L96
[6]: http://gecko.readthedocs.io/en/latest/taskcluster/taskcluster/taskgraph.html#decision-task
[7]: https://dxr.mozilla.org/mozilla-central/rev/d11c29c1db3a1bc96ad5792ebf8a89b2fbadcf85/.taskcluster.yml#107
[8]: http://gecko.readthedocs.io/en/latest/taskcluster/taskcluster/taskgraph.html#graph-generation
[9]: http://gecko.readthedocs.io/en/latest/taskcluster/taskcluster/taskgraph.html#optimization
[10]: https://dxr.mozilla.org/mozilla-central/rev/d11c29c1db3a1bc96ad5792ebf8a89b2fbadcf85/taskcluster/taskgraph/try_option_syntax.py#253
[11]: https://hg.mozilla.org/hgcustom/version-control-tools/file/tip/hgext/push-to-try
[12]: https://hg.mozilla.org/hgcustom/version-control-tools/file/6a5b4c985ffc/hgext/overlay/__init__.py#l130
[13]: https://github.com/junegunn/fzf
[14]: https://en.wikipedia.org/wiki/Approximate_string_matching
