## A Tired Developer's non-Illustrated Primer to B2G Testing

As B2G continues to trod onwards to its release, there is still a lot of confusion about the level
and state of test coverage it has.  Back in November we started running mochitests, reftests and
marionette/webapi tests on ARM emulators. Now we've also added xpcshell tests and for the most part
we have these nice green letters to look at on TBPL that make us feel good about ourselves. But what
is really being run?  What is the meaning behind these letters "M", "R", "Mn" and "X"? Are there any
causes for concern? Are there other tests being run that don't show up on TBPL? What are the current
automation priorities? What are the next platforms to use after emulators?

This blog post aims to answer these questions and more. It is a comprehensive snapshot of the
current state of automated testing on B2G.

* <a href="#Pandaboards">Pandaboards</a>
* <a href="#Mochitests">Mochitests</a>
* <a href="#Reftests">Reftests</a>
* <a href="#Marionette_Webapi">Marionette/Webapi Tests</a>
* <a href="#XPCShell">XPCShell Tests</a>
* <a href="#Gaia_UI">Gaia UI Tests</a>
* <a href="#Gaia_Integration">Gaia Integration Tests</a>
* <a href="#Eideticker">Eideticker</a>
* <a href="#Application_Startup">Application Startup Tests</a>

## <a name="Pandaboards">Pandaboards</a>
Pandaboards are still the future of automated testing on B2G. We've hit many problems with them over
the course of the last two quarters, but all the pieces are starting to fall together. In fact we
have [tests running on pandas][1] on the [Cedar branch][2] already (N.B that these are to test the
infrastructure, not the product).

#### Mozpool, Lifeguard and BlackMobileMagic

[Mozpool][3] is the system that will be used to control and assign pandas. The build system will
send a job request to mozpool which will analyze the available devices and return the IP of a device
that meets all of the requirements.  Before doing so, it will invoke [lifeguard][4] which will
perform diagnostic tests on the device and remove it from the pool if it is unsuitable for testing.
Lifeguard will use [BlackMobileMagic][5] to perform it's low-level operations on the device, such as
diagnosing network issues, restarting, retrieving device info etc. All of these components are
currently completed, tested and awaiting the test harnesses.

#### Test Schedule

<ul>
<li>
Gaia UI Tests: the first target to get running on pandas
<ul>
<li>Nearly finished, but is mainly being blocked by [bug 820617][6]</li>
<li>Also take a look at the [full dependency tree][7]</li>
<li>End of Q4 or early Q1</li>
</ul>
</li>

<li>
Unittests (mochitest, reftest, etc): targetted after Gaia smoketests are running reliably
<ul>
<li>Sometime in Q1</li>
<li>[Full dependency tree][8] (you can see why they're taking awhile)</li>
</ul>
</li>
</ul>

#### How to help

Getting Gaia UI tests running on pandas is well under way. After that we will be shifting focus on
the B2G unittests (mochitest, reftest, marionette/webapi and xpcshell tests).  [Bug 807126][9] comes
to mind as an important bug that we'll need to complete before we can even start running unittests
on pandaboards.  It is currently on my radar for sometime in Q1 but has been slipping down my
priority list lately.

## <a name="Mochitests">Mochitests</a>

A subset of [mochitest-plain][10] are being run on the emulator. There are no plans for
mochitest-chrome. Mochitests will also be used for B2G permissions testing.  Mochitests are rolled
out to all branches and are being staged on the [Cedar branch][11]. These are denoted "M" on
[TBPL][12].

#### What's being run

See the [full list of mochitests running on b2g][13]. Currently it's only some of the DOM 
and layout tests, but these are in the process of getting expanded ([bug 793045][14]).

#### Causes for concern

Overall mochitests have been pretty stable save for a few intermittent harness issues.

* B2G/emulator instability problems ([bug 814551][15] and [bug 802877][16])
* Runs slowly on emulators using linux 32 slave load (the set of enabled tests takes ~60 minutes on a debug build)
* There are a fair amount of mochitest failures (see tracking [bug 781696][17])

#### Future work
* Enable a larger set of mochitests ([bug 793045][18])
* Run mochitests on pandaboards
* Create mochitest permissions tests
* Expand mochitest-plain with additional b2g tests
* Emulators are slow, test runs take a long time

#### Try Syntax

try: -b o -p ics\_armv7a\_gecko -u mochitests -t none

#### How to help
* See the [instructions on MDN][19] for information on running mochitests
* Fix a bug on the tracking bug's [dependency tree][20]
* Harness performance improvements
* General refactoring and improvements (consolidate code between the harnesses)

##<a name="Reftests">Reftests</a>

[Reftests][21] are being run against the ARM emulators. They are rolled out to all branches and are
being staged on [Cedar][11]. These are denoted "R" on [TBPL][12].

#### What's being run

Only the reftest-sanity tests!!! Yes, there is practically no test coverage here at the moment. The
tracking bug to expand the set of tests is [bug 811779][22].  The patch in this bug should give a
relatively green run of all the reftests but we simply don't have the capacity to turn them on.
Instead I'm in the process of triaging a subset of reftests that Chris Jones deemed "important" on
Cedar. These should be ready to turn on soon which is why there are so many chunks.

#### Causes for concern

See the [main reftest tracking bug][23] for a full list of issues associated with reftests on B2G.
Some of the highlights include:

* B2G/emulator instability problems ([bug 814551][24] and [bug 802877][25])
* In general there are *a lot* of intermittent failures with the B2G reftests
* Enabling &lt;iframe mozbrowser&gt; causes additional failures ([bug 785074][26])
* The harness is not quite getting launched properly ([bug 807970][27])
* No crashtests or jsreftests being run yet
* Emulators are slow, test runs take a long time

#### Future work
    
* Fix remaining harness issues
* Enable a larger set of reftests ([bug 811779][28])
* Run reftests on pandaboards
* Add crashtests and jsreftests

#### Try Syntax
try: -b o -p ics\_armv7a\_gecko -u reftest-1,reftest-2,reftest-3,reftest-4,reftest-5,reftest-6,reftest-7,reftest-8,reftest-9,reftest-10 -t none

#### How to help
    
* See the [instructions on MDN][29] for information on running reftests
* Pick up a bug listed in the [dependency tree][30]
* Harness performance improvements
* Try running them locally and file/attempt to fix any issues you come across (the dependency list above is definitely not exhaustive)


## <a name="Marionette_Webapi">Marionette and WebAPI tests</a>

[Marionette and WebAPI tests][31] are a combination of marionette unittests for testing marionette
itself and some B2G webapi tests.  These are rolled out to all branches and are being staged on
[Cedar][11]. They are denoted with an "Mn" on [TBPL][12].

#### What's being run

All of the [marionette unit tests][32]. In addition there are many other [webapi tests][33] being
run. These include tests for telephony, battery, sms, network and more.

#### Causes for concern

The webapi tests tend to be much more crashy than any of the other unit tests. Currently there are a
lot of instability issues caused by B2G process crashes and full out emulator crashes. 
    
* B2G/emulator instability problems ([bug 814551][34] and [bug 802877][35])
* Recently the gaia/gonk snapshot got updated and we see a 70% crash rate now, but oddly not on the b2g18 branch! (see [bug 823076][36] to track fixing it)
* Emulators are slow, test runs take a long time

#### Future work
* Add some screen orientation tests
* Expand existing test coverage in general
* Some of the tests require the emulator (for synthesizing events). Run the ones that don't on pandaboards
* Fix stability issues on the emulator

#### Try Syntax
try: -b o -p ics\_armv7a\_gecko -u marionette-webapi -t none

#### How to help

* See the documentation on [running marionette tests][37]
* Pick up a bug from the [dependency tree][38]
* Expand the set of marionette/webapi tests


## <a name="XPCShell">XPCShell Tests</a>

[XPCShell tests][39] were just recently added. They are rolled out on all branches and are being
staged on [Cedar][11]. These are denoted "X" on [TBPL][12].

#### What's being run

The [xpcshell tests being run][40] include the update tests, the ril tests, the debugger tests and a
handful of others.  This is just a small subset of tests that were chosen to start out with. If you
know of any other tests that should be getting run feel free to let me know (or just add them
yourself after verifying that they pass).

#### Causes for concern

The xpcshell tests seem to be quite reliable on B2G. There are a few open bugs, but nothing near as
bleak as e.g reftests or marionette/webapi.

* B2G/emulator instability problems ([bug 814551][41] and [bug 802877][42])
* See the general [tracking bug for xpcshell related problems][43]
* Test return codes are always "1" ([bug 773703][44])
* Segfaults happen in between tests ([bug 816086][45])
* Emulators are slow, test runs take a long time

#### Future work
* Run xpcshell tests on pandas
* Expand set of tests being run
* Fix remaining issues
* Speed up test runs

#### Try Syntax

try: -b o -p ics\_armv7a\_gecko -u xpcshell -t none

#### How to help
    
* Expand the set of tests being run (be mindful of test time and chunks)
* Grab a bug from the [dependency tree][46]


## <a name="Gaia_UI">Gaia UI Tests</a>

The [gaia UI tests][47] (aka gaia smoketests) are a set of tests being run by the WebQA team. They
are running automatically in a Jenkins instance but are not currently being reported in TBPL. You
can [see the results][48] (you must be on the MV network to see that link, sorry).

#### What is being run

You can check out the [current set of tests being run][49] from github.

#### Causes for concern

There are some test stability issues and some issues that appear to be legitimate failures. There
are ~13 tests (roughly half) that are currently passing and stable on the pandaboards. The others
require things which a pandaboard doesn't have (e.g camera) and can't be run.

* Most of the [gaia ui test issues][50] can be seen on github
* Pandas don't recognize the SD card which is needed by a fair chunk of the tests (see [bug 820833][51]) 
* The two main blockers for getting this going on pandas are [bug 820617][52] and [bug 821379][53]

#### Future work

* Get them running in a Jenkins C-I on a Unagi (see [bug 801898][54])
* Get them running in TBPL on a pandaboard (see [bug 802317][55])
* Expand set of tests
* Fix stability issues

#### How to help
    
* Read the [documentation on running them][56]
* Check out the dependency trees for [bug 801898][57] and [bug 802317][58]
* Contribute additional tests (see [writeing unit tests][59])


## <a name="Gaia_Integration">Gaia Integration Tests</a>

Some of the [Gaia integration tests][60] are being run by the WebQA team in a Jenkins CI. Others are
being run manually on shipping devices by gaia developers. These are targetted to run on pandaboards
after the Gaia UI tests are finished and running stable.


## <a name="Eideticker">Eideticker</a>

[Eideticker][61] is a performance testing harness that captures HDMI out and performs frame by frame
analysis.  There should be B2G specific eideticker tests running by end of Q4 or early Q1.

#### Causes for concern
* There is a problem where the HDMI output seems to go to sleep ([bug 819431][62])
* Pandaboards become unresponsive after idling for too long ([bug 821379][63])


## <a name="Application_Startup">Application Startup Tests</a>

These tests are currently running on unagis and are reporting data to datazilla. Once the remaining
panda issues have been ironed out, these will provide some basic per push performance numbers.

[1]: http://armenzg.blogspot.ca/2012/12/b2g-test-jobs-running-on-panda-boards.html
[2]: http://tbpl.mozilla.org/?tree=Cedar
[3]: https://wiki.mozilla.org/Auto-tools/Projects/MozPool
[4]: https://wiki.mozilla.org/Auto-tools/Projects/Lifeguard
[5]: https://wiki.mozilla.org/ReleaseEngineering/BlackMobileMagic
[6]: https://bugzilla.mozilla.org/show_bug.cgi?id=820617
[7]: https://bugzilla.mozilla.org/showdependencytree.cgi?id=802317&amp;hide_resolved=0
[8]: https://bugzilla.mozilla.org/showdependencytree.cgi?id=777714&amp;hide_resolved=0
[9]: https://bugzilla.mozilla.org/show_bug.cgi?id=807126
[10]: https://developer.mozilla.org/en-US/docs/Mochitest
[11]: https://tbpl.mozilla.org/?tree=Cedar
[12]: http://tbpl.mozilla.org/
[13]: http://mxr.mozilla.org/mozilla-central/source/testing/mochitest/b2g.json
[14]: https://bugzilla.mozilla.org/show_bug.cgi?id=793045
[15]: https://bugzilla.mozilla.org/show_bug.cgi?id=814551
[16]: https://bugzilla.mozilla.org/show_bug.cgi?id=802877
[17]: https://bugzilla.mozilla.org/show_bug.cgi?id=b2g-mochitests
[18]: https://bugzilla.mozilla.org/show_bug.cgi?id=793045
[19]: https://developer.mozilla.org/en-US/docs/Mozilla/Boot_to_Gecko/B2G_Mochitests
[20]: https://bugzilla.mozilla.org/showdependencytree.cgi?id=781696&amp;hide_resolved=1
[21]: https://developer.mozilla.org/en-US/docs/Creating_reftest-based_unit_tests
[22]: https://bugzilla.mozilla.org/show_bug.cgi?id=811779
[23]: https://bugzilla.mozilla.org/show_bug.cgi?id=773482
[24]: https://bugzilla.mozilla.org/show_bug.cgi?id=814551
[25]: https://bugzilla.mozilla.org/show_bug.cgi?id=802877
[26]: https://bugzilla.mozilla.org/show_bug.cgi?id=785074
[27]: https://bugzilla.mozilla.org/show_bug.cgi?id=807970
[28]: https://bugzilla.mozilla.org/show_bug.cgi?id=811779
[29]: https://developer.mozilla.org/en-US/docs/Mozilla/Boot_to_Gecko/B2G_Reftests
[30]: https://bugzilla.mozilla.org/showdependencytree.cgi?id=773482&amp;hide_resolved=1
[31]: https://developer.mozilla.org/en-US/docs/Marionette/Tests
[32]: http://mxr.mozilla.org/mozilla-central/source/testing/marionette/client/marionette/tests/unit
[33]: http://mxr.mozilla.org/mozilla-central/source/testing/marionette/client/marionette/tests/unit-tests.ini
[34]: https://bugzilla.mozilla.org/show_bug.cgi?id=814551
[35]: https://bugzilla.mozilla.org/show_bug.cgi?id=802877
[36]: https://bugzilla.mozilla.org/show_bug.cgi?id=823076
[37]: https://developer.mozilla.org/en-US/docs/Marionette/Running_Tests
[38]: https://bugzilla.mozilla.org/showdependencytree.cgi?id=823076&amp;hide_resolved=1
[39]: https://developer.mozilla.org/en-US/docs/Writing_xpcshell-based_unit_tests
[40]: http://mxr.mozilla.org/mozilla-central/source/testing/xpcshell/xpcshell_b2g.ini
[41]: https://bugzilla.mozilla.org/show_bug.cgi?id=814551
[42]: https://bugzilla.mozilla.org/show_bug.cgi?id=802877
[43]: https://bugzilla.mozilla.org/show_bug.cgi?id=820380
[44]: https://bugzilla.mozilla.org/show_bug.cgi?id=773703
[45]: https://bugzilla.mozilla.org/show_bug.cgi?id=816086
[46]: https://bugzilla.mozilla.org/showdependencytree.cgi?id=820380&amp;hide_resolved=1
[47]: https://developer.mozilla.org/en-US/docs/Mozilla/Boot_to_Gecko/Gaia_Unit_Tests
[48]: http://qa-selenium.mv.mozilla.com:8080/view/B2G/
[49]: https://github.com/mozilla/gaia-ui-tests/tree/master/gaiatest/tests
[50]: https://github.com/mozilla/gaia-ui-tests/issues
[51]: https://bugzilla.mozilla.org/show_bug.cgi?id=820833
[52]: https://bugzilla.mozilla.org/show_bug.cgi?id=820617
[53]: https://bugzilla.mozilla.org/show_bug.cgi?id=821379
[54]: https://bugzilla.mozilla.org/show_bug.cgi?id=801898
[55]: https://bugzilla.mozilla.org/show_bug.cgi?id=802317
[56]: https://developer.mozilla.org/en-US/docs/Mozilla/Boot_to_Gecko/Gaia_Unit_Tests
[57]: https://bugzilla.mozilla.org/showdependencytree.cgi?id=801898&amp;hide_resolved=1
[58]: https://bugzilla.mozilla.org/showdependencytree.cgi?id=802317&amp;hide_resolved=1
[59]: https://developer.mozilla.org/en-US/docs/Mozilla/Boot_to_Gecko/Gaia_Unit_Tests#Writing_unit_tests
[60]: https://developer.mozilla.org/en-US/docs/Mozilla/Boot_to_Gecko/Gaia_Integration_Tests
[61]: https://wiki.mozilla.org/Project_Eideticker
[62]: https://bugzilla.mozilla.org/show_bug.cgi?id=819431
[63]: https://bugzilla.mozilla.org/show_bug.cgi?id=821379
