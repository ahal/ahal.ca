## Try Fuzzy: A Try Syntax Alternative

It's no secret that I'm not a fan of try syntax, it's a topic I've blogged about on [several][0]
[occasions][1] before. Today, I'm pleased to announce that there's a real alternative now landed on
mozilla-central. It works on all platforms with mercurial and git. For those who just like to dive in:

```bash
$ mach mercurial-setup --update  # only if using hg
$ mach try fuzzy
```

This will prompt you to install [fzf][2]. After bootstrapping is finished, you'll enter an interface
populated with a list of all possible taskcluster tasks. Start typing and the list will be filtered
down using a fuzzy matching algorithm. I won't go into details on how to use this tool in this blog
post, for that see:

```bash
$ mach try fuzzy --help  # or
$ man fzf
```

For who prefer to look before you leap, I've recorded a demo:

<video width="100%" height="100%" controls>
<source src="/static/vid/blog/2017/mach-fuzzy.mp4" type="video/mp4">
</video>

Like the existing `mach try` command, this should work with mercurial via the `push-to-try`
extension or git via `git-cinnabar`. If you encounter any problems or bad UX, please file a bug
under Testing :: General.


## Try Task Config

The following section is all about the implementation details, so if you're curious or want to write
your own tools for selecting tasks on try, read on!

This new try selector is not based on try syntax. Instead it's using a brand new scheduling
mechanism called [try task config][3]. Instead of encoding scheduling information in the commit
message, `mach try fuzzy` encodes it in a JSON file at the root of the tree called
`try_task_config.json`. Very simply (for now), the decision task knows to look for that file on try.
If found, it will read the JSON object and schedule every task label it finds.  There are also hooks
to prevent this file from accidentally being landed on non-try branches.

What this means is that anything that can generate a list (or dict) of task labels can be a try
selector. This new JSON format is much easier for tools to write, and for taskgraph to read.


### Creating a Try Selector

There are currently two ways to schedule tasks on try (syntax and fuzzy). But I envision 4-5 different
methods in the future. For example, we might implement a `TestResolver` based try selector which
given a path can determine all affected jobs. Or there could be one that uses globbing/regex to
filter down the task list which would be useful for saving "presets". Or there could be one that
uses a curses UI like the `hg trychooser` extension.

To manage all this, each try selector is implemented as an `@SubCommand` of `mach try`. The regular
syntax selector, is implemented under `mach try syntax` now (though `mach try` without any
subcommand will dispatch to syntax to maintain backwards compatibility). All this lives in a newly
created [tryselect][4] module.

If you have want to create a new try selector, you'll need two things:

1. A list of task labels as input.
2. The ability to write those labels to `try_task_config.json` and push it to try.

Luckily tryselect provides both those things. The first, can be obtained using the [tasks.py][5]
module. It basically does the equivalent of running `mach taskgraph target`, but will also
automatically cache the resulting task list so future invocations run much quicker.

The second can be achieved using the [vcs.py][6] module. This uses the same approach that the old
syntax selector has been using all along. It will commit `try_task_config.json` temporarily and
then remove all traces of the commit (and of `try_task_config.json`).

So to recap, creating a new try selector involves:

1. Add an `@SubCommand` to the [mach\_commands.py][7], which dispatches to a file under
   the [selectors][8] directory.
2. Generate a list of tasks using [tasks.py][5].
3. Somehow filter down that list (this part is up to you)
4. Push the filtered list using [vcs.py][6]

You can inspect the [fuzzy][9] implementation to see how all this ties together.


### Future Considerations

Right now, the `try_task_config.json` method only allows specifying a list of task labels. This is
good enough to say *what* is running, but not *how* it should run. In the future, we could expand
this to be a dict where task labels make up the keys. The values would be extra task metadata that
the taskgraph module would know how to apply to the relevant tasks.

With this scheme, we could do all sorts of crazy things like set prefs/env/arguments directly from
a try selector specialized to deal with those things. There are no current plans to implement any of
this, but it would definitely be a cool ability to have!


[0]: https://ahal.ca/blog/2015/try-syntax/
[1]: https://ahal.ca/blog/2017/fuzzy-try-chooser/
[2]: https://github.com/junegunn/fzf
[3]: http://gecko.readthedocs.io/en/latest/taskcluster/taskcluster/how-tos.html#schedule-a-task-on-try
[4]: http://dxr.mozilla.org/mozilla-central/source/tools/tryselect
[5]: http://dxr.mozilla.org/mozilla-central/source/tools/tryselect/tasks.py
[6]: http://dxr.mozilla.org/mozilla-central/source/tools/tryselect/vcs.py
[7]: http://dxr.mozilla.org/mozilla-central/source/tools/tryselect/mach_commands.py
[8]: http://dxr.mozilla.org/mozilla-central/source/tools/tryselect/selectors
[9]: http://dxr.mozilla.org/mozilla-central/source/tools/tryselect/selectors/fuzzy.py
