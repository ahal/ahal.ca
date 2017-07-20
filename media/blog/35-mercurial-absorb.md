## Absorbing Changes into a Commit Series with Mercurial

Imagine this scenario. You've pushed a large series of commits to your favourite review tool
(because you are a believer in the glory of microcommits). The reviewer however has found several
problems, and worse, they are spread across all of the commits in your series. How do you fix all
the issues with minimal fuss while preserving the commit order?

If you were using the builtin [histedit][0] extension, you might make temporary "fixup" commits for
each commit that had issues. Then after running `hg histedit` you'd `roll` them up into their
respective parent. Or if you were using the [evolve][1] extension (which I definitely recommend),
you might do something like this:

```bash
$ hg update 1
# fix issues in commit 1
$ hg amend
$ hg evolve
# fix issues in commit 2
$ hg amend
$ hg evolve
etc.
```

Both methods are serviceable, but involve some jumping around through hoops to accomplish. Enter a
new extension from Facebook called [absorb][2]. The `absorb` extension will take each change in your
working directory, figure out which commits in your series modified that line, and automatically
amend the change to that commit. If there is any ambiguity (i.e multiple commits modified the same
line), then `absorb` will simply ignore that change and leave it in your working directory to be
resolved manually. So instead of the rather convoluted processes above, you can do this:

```bash
# fix all issues across all commits
$ hg absorb
```

It's magic!


## Installing Absorb

There's one big problem. The docs in the [hg-experimental][3] repo (where absorb lives) are
practically non-existent, and installation is a bit of a pain. So here are the steps I took to get
it working on Fedora. They won't hand hold you for other platforms, but they should at least point
you in the right direction.

First, clone the `hg-experimental` repo:

```bash
$ hg clone https://bitbucket.org/facebook/hg-experimental
```

Absorb depends on a compiled python module called `linelog` which also lives in `hg-experimental`.
In order to compile linelog, you'll need some dependencies:

```bash
$ sudo pip install cython
$ sudo dnf install lz4-devel python-devel openssl-devel
```

Make sure the `cython` dependency gets installed to the same python your mercurial install uses.
That may mean dropping the sudo from the `pip` command if you have mercurial running in user space.
Next, compile the `hg-experimental` repo by running:

```bash
$ cd path/to/hg-experimental
$ sudo python setup.py install
```

Again, be sure to run the install with the same python mercurial is installed with. Finally, add the
following to your ~/.hgrc:

```ini
[extensions]
absorb = path/to/hg-experimental/hgext3rd/absorb.py
```

The extension should now be installed! In the future, you can update the extension and python
modules with:

```bash
$ cd path/to/hg-experimental
$ hg pull --rebase
$ make clean
$ sudo python setup.py install
```

Let me know if there were other steps needed to get this working on your platform.

[0]: https://www.mercurial-scm.org/wiki/HisteditExtension
[1]: https://www.mercurial-scm.org/wiki/EvolveExtension
[2]: https://bitbucket.org/facebook/hg-experimental/src/tip/hgext3rd/absorb.py
[3]: https://bitbucket.org/facebook/hg-experimental
