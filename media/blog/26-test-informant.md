## How many tests are disabled?

tl;dr Look for [reports like this][0] in the near future!

At Mozilla, platform developers are culturally bound to [tbpl][1]. We spend a lot of time staring at
those bright little letters, and their colour can mean the difference between hours, days or even
weeks of work. With so many people performing over [420 pushes per day][2], all watching,
praying, rejoicing and cursing, it's paramount that the whole process operates like a well oiled
machine.

So when a test starts intermittently failing, and there aren't any obvious changesets to blame,
it'll often get disabled in the name of keeping things running. A bug will be filed, some people
will be cc'ed, and more often than not, it will languish. People who really care about tests know
this. They have an innate and deep fear that there are tests out there that would catch major and
breaking regressions, but for the fact that they are disabled. Unfortunately, there was never a good
way to see, at a high level, which tests were disabled for a given platform. So these people who
care so much have to go about their jobs with a vague sense of impending doom. Until now.

A Concrete Sense of Impending Doom
----------------------------------

[Test Informant][3] is a new service which aims to bring some visibility into the state of tests for
a variety of suites and platforms. It listens to [pulse messages][4] from mozilla-central for a
variety of build configurations, downloads the associated tests bundle, parses as many manifests as
it can and saves the results to a mongo database.

There is a script that queries the database and can generate reports (e.g [like this][0]), including
how many tests have been enabled or disabled over a given period of time. This means instead of a
vague sense of impending doom, you can tell at a glance exactly how doomed we are.

There are still a few manual steps required to generate and post the reports, but I intend to fully
automate the process (including a weekly digest link posted to dev.platform).

Over the Hill and Far Away
--------------------------

There are a number of improvements that can be made to this system. We may or may not implement them
based on the initial feedback we get from these reports. Possible improvements include:

* Support for additional suites and platforms.
* A web dashboard with graphs and other visualizations.
* Email notifications when tests are enabled/disabled on a per-module basis.
* Exposing the database publicly so other tools can use it (e.g a mach command).

There are also some known limitations:

* No data for b2g or android platforms (blocked by bugs [1071642][5] and [1066735][6] respectively).
* No data for suite \*. At the moment, only suites that live in the tests bundle and that have
    manifestparser based manifests (the .ini format) are supported. We may extend the tool to other
    formats at a later date.
* Run-time filters not taken into account. Because the tool doesn't actually run any tests, it doesn't
    know about any filters added by the test harness at run-time. Because all of reftest's filtering
    happens at runtime, it's unlikely reftest will be supported anytime soon.

If you would like to contribute, or just take a look at the source, it's [all on github][7]. 

As always, let me know if you have any questions!

[0]: http://people.mozilla.org/~ahalberstadt/informant-reports/daily/2014-09-29.informant-report.html 
[1]: http://tbpl.mozilla.org
[2]: http://relengofthenerds.blogspot.ca/2014/09/mozilla-pushes-august-2014.html
[3]: https://wiki.mozilla.org/Auto-tools/Projects/Test-Informant
[4]: https://wiki.mozilla.org/Auto-tools/Projects/Pulse
[5]: https://bugzilla.mozilla.org/show_bug.cgi?id=1071642
[6]: https://bugzilla.mozilla.org/show_bug.cgi?id=1066735
[7]: https://github.com/ahal/test-informant
