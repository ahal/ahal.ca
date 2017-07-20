## An Open Invitation to Enable your Favourite tests on B2G

Throughout most of our B2G test automation deployment, we've been very conscious about not enabling
too many tests simply because we didn't have enough capacity on our test slaves to run them all.
Regardless it was still bad enough as it was (many of you probably experienced very long wait times
for results). Thanks to releng (and especially Rail Aliiev) we are now running most of our B2G tests
in Amazon AWS which means we can be much more flexible in accomodating load.

One thing this means is we don't need to be *as* cautious about enabling larger sets of tests for
B2G. So if you have a mochitest, xpcshell test, marionette/webapi, reftest or crashtest that you
would like to see running on B2G emulators, now is the time to make sure it's enabled!

### Determining if the test is already being run

Unfortunately not all harnesses have the same manifest format, so here is a quick guide for finding
them:

* Mochitest: look at **testing/mochitest/b2g.json**. Make sure the test is contained within a manifest specified by the 'runtests' attribute and that it isn't listed in the 'excludetests' attribute
* Xpcshell: look at **testing/xpcshell/xpcshell_b2g.ini**. Make sure your test's root manifest is listed there and that it isn't skipped further down in a child manifest
* Marionette/Webapi: look at **testing/marionette/client/marionette/tests/unit-tests.ini**. Once again make sure the test's root manifest is listed and the test isn't skipped in a child manifest
* Reftest: look at **layout/reftests/reftest.list**. Same as above.
* Crashtest: look at **testing/crashtest/crashtests.list**. Same as above.

Alternatively you can open a full log on tbpl of a test run for the branch/suite you are 
interested in and do a ctrl-f for your test. Just note that if there are multiple chunks 
you'll need to do this for each chunk before you can be certain.

### Enabling the test

Please file a bug in the test harness component (e.g testing/mochitest, testing/reftest, etc) 
and cc me (:ahal). Then write a patch to enable the test (or suite of tests) and push it to try 
with the syntax "**try: -b o -p ics\_armv7a\_gecko -u &lt;suite name&gt; -t none**". If you are 
trying to enable the test on a branch without try (e.g b2g18) then I can help test it and 
get it landed there.

If the test was specifically disabled, there's a good chance that it had failures or was 
intermittent. In this case I can help get you set up to run it locally so you can investigate 
if you want.
