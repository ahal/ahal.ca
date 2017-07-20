## Using One Click Loaner to Debug Failures 

One of the most painful aspects of a developer's work cycle is trying to fix failures that show up
on try, but which can't be reproduced locally. When this happens, there were really only two
options (neither of them nice):

1. You could spam try with print debugging. But this isn't very powerful, and takes forever to get
   feedback.
2. You could request a loaner from releng. But this is a heavy handed process, and once you have the
   loaner it is very hard to get tests up and running.


I'm pleased to announce there is now a third option, which is easy, powerful and 100% self-serve.
Rather than trying to explain it in words, here is a ~5 minute demo:

<video width="100%" height="100%" controls>
<source src="https://people.mozilla.org/~ahalberstadt/demo/taskcluster-interactive-loaner.mp4" type="video/mp4">
</video>

Because I'm too lazy to re-record, I want to clarify that when I said |mach reftest| was "identical"
to the command line that mozharness would have run, I meant other than the test selection arguments.
You'll still need to either pass in a test path or use chunking arguments to select which tests to
run.


## Caveats and Known Issues

Before getting too excited, here is the requisite list of caveats.

1. This only works with taskcluster jobs that have one-click-loaner enabled. This means there is no
   Windows or OS X support. Getting support here is obviously the most important thing we can do to
   improve this system, but it's a hard problem with lots of unsolved dependencies. The biggest
   blocker is even just getting these platforms to work on AWS in the first place.
2. The test package mach environment doesn't support all test harnesses yet. I've got the major 3
   (mochitest, reftest, xpcshell) working so far and plan to add support for more harnesses later on
   in the quarter.
3. There are many rough edges. I consider this workflow to be "beta" quality. Though I think it is
   already useful enough to advertise, it is a long shot from being perfect. Please file bugs or
   ping me with any issues or annoyances you come across. See the next session for known issues.


### Issues

* No Windows or OS X support
* Hard to find "One-Click Loaner" link in treeherder
* Confusing error message if not logged into taskcluster-tools
* Interactive tasks should be high priority so they're never "pending"
* Scrolling in the interactive shell is broken
* No support for harnesses other than mochitest, reftest and xpcshell
* Android workflow needs to be ironed out
* Cloning gecko using interactive wizard is slow


## Thanks

Finally I want to thank the taskcluster team (especially jonasfj and garndt) for implementing the
One-Click Loaner, it is seriously cool. I also want to thank armenzg for helping with reviews and
dustin for helping me navigate taskcluster and docker.

As always, please let me know if you have any problems, questions or suggestions!
