## Peptest: A new harness for testing responsiveness

While responsiveness is one of the main goals for Firefox this quarter, we still don't quite have
the means to measure and test our progress towards this goal. The good news is that there are, and
have been for some time, several efforts to fix this problem. Back in June, Ted wrote some [event
tracing instrumentation][1] that gives us a reasonable idea of when the browser becomes
unresponsive. This event tracer is already being used by some Talos tests which gives us a good
general idea of whether or not Firefox is more or less responsive than it was previously. What it
doesn't give us is a method for developers to write their own tests and determine whether a specific
action or feature they are working on is causing unresponsivness.

[Peptest][2] is designed for the missing use case. Namely, it can be used to automate user
interactions in the browser and determine whether those actions are causing unresponsiveness. This
may be useful for creating a suite of responsiveness regression tests, or for developers working on
a responsiveness related feature or fix. The Peptest harness is designed to be lightweight (so as
not to interfere with results), simple to run and easy to write tests for.

[Tests][3] are nothing but Javascript files that will be executed in chrome scope. This means that
Peptests are basically browser-chrome tests without any of the assertions (since assertions aren't
needed in this context). However, since many Peptests will likely need to perform some kind of UI
automation, the Peptest harness also exposes [Mozmill's][4] driver for convenience. I feel it's
important to note, that importing Mozmill is completely optional (though recommended if you need to
do any automation). I also feel it's important to note that I did some work to [isolate Mozmill's
driver][5] which means that the actual test harness bits of Mozmill have been completely stripped
out. What's left over is surprisingly lightweight and lives in a handful of JS files.

Currently, it is possible to [run tests][6] locally on your machine, though I could potentially add
features or change any aspect of the harness. I've also been working on a Mozharness script in [bug
692091][7] so we can run tests automatically for tinderbox builds.

Finally, I'd like to say: **I need feedback!** The requirements of this harness have been very vague
from the outset. I've been doing my best to interpret the requirements in a way that makes sense,
but I'm still kind of flying blind so to speak. What I mean is, I'm not sure what developers want
and/or need. I'm also not sure how useful what I've thrown together so far will be. So if you have
any ideas or general comments, please ping ahal on irc, or email ahalberstadt@mozilla.com and I'd be
very grateful.

[1]: http://blog.mozilla.com/ted/2011/06/27/measuring-ui-responsiveness/
[2]: https://wiki.mozilla.org/Auto-tools/Projects/peptest 
[3]: https://wiki.mozilla.org/Auto-tools/Projects/peptest#Test_Format
[4]: https://developer.mozilla.org/en/Mozmill
[5]: http://ahal.ca/blog/2011/isolating-mozmill-driver
[6]: https://wiki.mozilla.org/Auto-tools/Projects/peptest#Running_Tests
[7]: https://bugzilla.mozilla.org/show_bug.cgi?id=692091
