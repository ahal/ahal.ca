## A Workflow for using Mach with multiple Object Directories

[Mach][1] is an amazing tool which facilitates a large number of common user stories in the mozilla
source tree. You can perform initial setup, execute a build, run tests, examine diagnostics, even
search Google. Many of these things require an object directory. This can potentially lead to some
confusion if you typically have more than one object directory at any given time. How does mach know
which object directory to operate on?

It turns out that mach is pretty smart. It takes a very good guess at which object directory you
want.  Here is a simplification of the steps in order:

1. If cwd is an objdir or a subdirectory of an objdir, use that
2. If a mozconfig is detected and MOZ\_OBJDIR is in it, use that
3. Attempt to guess the objdir with build/autoconf/config.guess

The cool thing about this is that there are tons of different workflows that fit nicely into this
model. For example, many people put the mach binary on their $PATH and then always make sure to 'cd'
into their objdirs before invoking related mach commands.

It turns out that mach works really well with a tool I had written quite awhile back called
[mozconfigwrapper][2]. I won't go into details about mozconfigwrapper here. For more info, see my
[previous post][3] on it. Now for the sake of example, let's say we have a regular and debug build
called 'regular' and 'debug' respectively.  Now let's say I wanted to run the 'mochitest-plain' test
suite on each build, one after the other. My workflow would be (from any directory other than an
objdir):

```bash
$ buildwith regular
$ mach mochitest-plain
$ buildwith debug
$ mach mochitest-plain
```

How does this work? Very simply, mozconfigwrapper is exporting the $MOZCONFIG environment variable
under the hood anytime you call 'buildwith'. Mach will then pick up on this due to the second step
listed above.

Your second question might be why bother installing mozconfigwrapper when you can just export
MOZCONFIG directly? This is a matter of personal preference, but one big reason for me is the
buildwith command has full tab completion, so it is easy to see which mozconfigs you have available
to choose from. Also, since they are hidden away in your home directory, you don't need to memorize
any paths. There are other advantages as well which you can see in the mozconfigwrapper [readme][4].

I've specially found this workflow useful when building several platforms at once (e.g firefox and
b2g desktop) and switching back and forth between them with a high frequency. In the end, to each
their own and this is just one possible workflow out of many. If you have a different workflow
please feel free to share it in the comments.

[1]: https://developer.mozilla.org/en-US/docs/Developer_Guide/mach
[2]: https://github.com/ahal/mozconfigwrapper
[3]: http://ahal.ca/blog/2011/mozconfigwrapper-introduction
[4]: https://github.com/ahal/mozconfigwrapper
