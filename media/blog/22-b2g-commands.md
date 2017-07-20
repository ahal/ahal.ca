## Add more mach to your B2G

#### Getting Started

tl;dr - It is possible to add more mach to your B2G repo! To get started, install pip:

```bash
$ wget https://raw.github.com/pypa/pip/master/contrib/get-pip.py -O - | python
```

Install b2g-commands:

```bash
$ pip install b2g-commands
```

To play around with it, cd to your [B2G repo][1] and run:

```bash
$ git pull                 # make sure repo is up to date
$ ./mach help              # see all available commands
$ ./mach help &lt;command&gt;    # see additional info about a command
```

#### Details

Most people who spend the majority of their time working within mozilla-central have probably been
acquainted with [mach][2]. In case you aren't acquainted, mach is a generic command dispatching
tool. It is possible to write scripts called 'mach targets' which get registered with mach core and
transformed into commands. Mach targets in mozilla-central have access to all sorts of powerful
hooks into the build and test infrastructure which allow them to do some really cool things, such as
bootstrapping your environment, running builds and tests, and generating diagnostics.

A contributor (kyr0) and I have been working on a side project called [b2g-commands][3] to start
bringing some of that awesomeness to B2G. At the moment b2g-commands wraps most of the major B2G
shell scripts, and provides some brand new ones as well. Here is a summary of its current features:

* Bootstrap your environment - sets up system packages needed to build (includes setting up gcc-4.6)
* Easy to discover arguments - no need to memorize or look up random environment variables
* Helpful error messages where possible - clear explanations of what went wrong and how to fix it
* Fully compatible with existing build system including .userconfig
* List Android vendor ids for udev rules
* Clobber objdir/out directories

I feel it's important to re-iterate, that this is *not* a replacement for the current build system.
You can have b2g-commands installed and still keep your existing workflows if desired. Also
important to note is that there's a good chance you'll find bugs (especially related to the
bootstrap command on varying platforms), or arguments missing from your favourite commands. In this
case please don't hesitate to contact me or [file an issue][4]. Or, even better, submit a pull
request!

If the feature set feels a bit underwhelming, that's because this is just a first iteration. I think
there is a lot of potential here to [add some really useful things][5].  Unfortunately, this is just
a side project I've been working on and I don't have as much time to devote to it as I would like.
So I encourage you to submit pull requests (or at least submit an issue) for any additional
functionality you would like to see. In general I'll be very open to adding new features.

#### Future Plans

In the end, because this module lives outside the build system, it will only ever be able to wrap
existing commands or create new ones from scratch. This means it will be somewhat limited in what it
is capable of providing. The targets in this module don't have the same low-level hooks into the B2G
and gaia repos like the targets for desktop do into gecko. My hope is that if a certain feature in
this module turns out to be especially useful and/or widely used it'll get merged into the B2G repo
and be available by default.

Eventually my hope is that we implement some deeper mach integration into the various B2G repos
(especially gaia) which would allow us to create even more powerful commands. I guess time will
tell.

[1]: https://github.com/mozilla-b2g/B2G
[2]: https://developer.mozilla.org/en-US/docs/Developer_Guide/mach
[3]: https://github.com/ahal/b2g-commands
[4]: https://github.com/ahal/b2g-commands/issues/new
[5]: https://github.com/ahal/b2g-commands/issues
