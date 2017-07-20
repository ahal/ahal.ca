### Like a Bump on a Tinderbox Push Log

Contrary to popular belief, we (the A-Team) have been running mochitests, reftests, marionette tests
and webapi tests on B2G in some form of continuous integration or another for about 5 months now.
They've been reporting results to a TBPL look-alike called [autolog][1], and were run on Amazon EC2
VM's with emulators. This was a temporary solution to get something stood up quickly while we moved
towards our ultimate B2G automation goal - tests running on Pandaboards and reporting to TBPL.

As of this week, while there are still no tests running on Pandaboards, I'm happy to say we have
emulators running mochitests, reftests and marionette/webapi tests, all reporting to TBPL.

It might seem surprising (dismaying?) that it has taken as long as it has to get to this point.
Especially seeing as it's only emulators running very bare subsets of tests. The fact is I am
saddened as well, though not surprised. I could go on a very long rant about how we managed to get
this far without proper continuous integration, but I'll leave that for another post.  The short
version is that automation tends to be very fickle and error prone by nature. When the thing you are
testing is in a constant state of flux (like B2G was) it makes for a bad  combination. If the thing
you are testing has many different components, each with differing development processes, it gets
worse. When you throw in platforms with poor performance characteristics (like emulators and
devices) and when said platforms need to be controlled remotely, you are bound to become sad.

But the point of this post isn't to make you sad, it's to assure you that things are getting better.
In the near to mid-future look for:

* Gaia smoketests (in Jenkins)
* Tests running on Aurora (v1)
* Moar reftests and mochitests enabled on the emulators
* Additional webapi tests
* Xpcshell tests on TBPL
* Tests running on pandas

A massive amount of work that spans many different teams is needed to accomplish all this. I think I
have the next couple of weeks cut out for me.

[1]: http://brasstacks.mozilla.com/autolog/?tree=b2g&amp;source=autolog
