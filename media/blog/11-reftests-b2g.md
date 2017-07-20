## State of Reftests on B2G

This quarter I've been focusing on getting reftests running on B2G, triaging them and fixing various
issues. The purpose of this post is to outline their status, go over the work that still needs to be
done and point out where I will need some help.

## What is Finished

Reftests currently run on B2G. I put up some [instructions on how to run them][1] on MDN. If these
instructions don't work for you for whatever reason, please let me know.

Reftests are also being [reported to autolog][2] (a tbpl look-alike that is maintained by the
ateam). The tests are only being run against nightly B2G builds by a stand alone desktop machine
that sits under my desk. This is hopefully only a very temporary solution. There are also massive
amounts of tests that are currently disabled on B2G for various reasons which I will talk about in
the next section.

## What Needs to be Done

There is still a lot of work to be done before reftests will enjoy a similar level of stability and
exposure they receive on desktop Firefox.

### Triaging and Fixing Tests

The main tracking bug I'm using is [bug 773482][3].  I haven't had a lot of time to look into all of
the various causes of failure, but some of the main ones I've already filed include:

* Several failures in reftest sanity: [bug 774396][4]
* Broken link images in encoders-lossless: [bug 783621][5]
* pngsuite-\* images rendered in top left instead of center: [bug 783632][6]
* Many failures in editor/reftest: [bug 783658][7]
* Running reftests oop means the tests don't get rendered to the canvas: [bug 784810][8]
* Using &lt;iframe mozbrowser&gt; instead of &lt;browser&gt; introduces additional failures: [bug 785074][9]

There are many more failures that I haven't bothered filing bugs for yet. I figure that the bugs
above will account for most of the failures and should be fixed before too much time is spent
triaging/filing additional bugs. I plan on looking into these issues when I have some time, but I
have exactly 0 graphics/layout experience. So if you think you know why some of the tests are
failing, or want to tackle one of the aforementioned bugs, please ping me (ahal) on irc. I'd
certainly appreciate it.

### Changing the Default Resolution

Reftests require a resolution of 800x1000 to run. However the development boards we will be using to
run them (pandaboards) only have a height of 720. This means that there are a lot of tests that will
lose coverage since they will be cut off. On Firefox for Android, we've noticed that using a large
resolution like 800x1000 consumes too much memory and causes many failures/timeouts/random oranges.

I've done some work to identify affected tests in [bug 737961][10] and posted to dev platform a few
times. The current consensus seems to be that we need to work with W3C and other browser vendors to
get the default resolution changed from 800x1000 to something smaller like 600x600. If you have any
contacts, please let myself or jmaher know.

### Getting Reftests Running on Pandaboards

Currently reftests are running against the emulator. I need to make a few changes (such as using our
SUTAgent instead of adb) to get them running on the pandaboards (as well as other dev boards and
phones). This shouldn't be too hard and I simply haven't had time to do it yet.  Expect this to be
finished within a week or two.

### Getting Reftests Running in Continuous Integration

Like I mentioned above, reftests are only running on emulators and being reported to autolog. I'll
need to do some work to get them running in production, per checkin and reported to tbpl.
Unfortunately this is blocked on several things:

* Getting them running on pandaboards
* The ability to flash B2G on pandas
* Infrastructure (getting enough pandas to support load)
* Releng (for build support, git repo support etc.)

As such, there is no timetable for this and it is likely a month or two out at the least.

## Summary

There is still a lot of work to do before reftests are running at 100% coverage and in C-I for B2G.
I would appreciate any help I can get, especially with regards to fixing and triaging the tests. If
you have any questions, you can post in comments or ping ahal on irc.

Thanks!

[1]: https://developer.mozilla.org/docs/Mozilla/Boot_to_Gecko/B2G_Reftests
[2]: http://brasstacks.mozilla.com/autolog/?tree=b2g&amp;source=autolog
[3]: https://bugzilla.mozilla.org/show_bug.cgi?id=773482
[4]: https://bugzilla.mozilla.org/show_bug.cgi?id=774396
[5]: https://bugzilla.mozilla.org/show_bug.cgi?id=783621
[6]: https://bugzilla.mozilla.org/show_bug.cgi?id=783632
[7]: https://bugzilla.mozilla.org/show_bug.cgi?id=783658
[8]: https://bugzilla.mozilla.org/show_bug.cgi?id=784810
[9]: https://bugzilla.mozilla.org/show_bug.cgi?id=785074
[10]: https://bugzilla.mozilla.org/show_bug.cgi?id=737961
