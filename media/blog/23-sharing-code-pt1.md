## Part 1: Sharing code is not always a good thing

### Dry versus Wet

As programmers, we are taught early on that code duplication is bad and should be avoided at all
cost. It makes code less maintainable, reusable and readable. The [DRY principle][1] is very basic
and fundamental to how most of us approach software design. If you aren't familiar with the DRY
principle, please take a minute to read the wikipedia page on it. The counterpart of DRY, is WET
(write everything twice).  In general, I agree that DRY is good and WET is bad. But I think there
are a class of problems where the DRY approach can actually be harmful. For these types of problems,
I will make a claim that a WET approach can actually work better.

### IFFY Requirements

So what are these problems? They are problems that have continuously evolving unpredictable
requirements. Continuously evolving means that the project will continue to receive additional
requirements indefinitely. Unpredictable means that you won't know when the requirements will
change, how often they'll change, or what they might be.

Hold on a second, you might be thinking. If the requirements are so unpredictable, then shouldn't we
be creating a new project to address them instead of trying to morph an old one to meet them? Yes!
But there's a catch (hey, and isn't starting a new project just a form of code duplication?). The
catch is that the requirements are continuously evolving. They change a little bit at a time over
long periods (years). Usually at the beginning of a project it is not possible to tell whether the
requirements will be unpredictable, or even if they will be continuously evolving. It isn't until
the project has matured, and feature creep vines are firmly entrenched that these facts become
apparent and by this time it is often too late. Because "continuously evolving unpredictable
requirements" is a mouthful to say, I've invented an acronym to describe them.  From here on out I
will refer to them as IFFY (in flux for years) requirements.

### An IFFY Example

This probably sounds very hand wavy at the moment, so let me give an example of a problem that has
IFFY requirements. This example is what I primarily work on day to day and is the motivation behind
this post, test harnesses. A test harness is responsible for testing some other piece of software.
As that other piece of software evolves, so too must the test harness. If the system under test adds
support for a wizzlebang, then the harness must also add support for testing a wizzlebang. Or closer
to home, if the system under test suddenly becomes multiprocess, then the harness needs to support
running tests in both parent and child processes. Usually the developer working on the test harness
does not know when or how the system under test will evolve in a way that requires changes to the
harness. The requirements are in flux for as long as the system under test continues to evolve. The
requirements are IFFY.

Hopefully you now have some idea about what types of problems might benefit from a WET approach. But
so far I haven't talked about why WET might be helpful and why DRY might be harmful. To do this, I'd
like to present two case studies. The first is an example of where sticking to the DRY principle
went horribly wrong. The second is an example of where duplicating code turned out to be a huge
success.

### Case Study #1: Mochitest, Reftest, XPCShell, etc.

Most of our test harnesses have life cycles that follow a common pattern. Originally they were
pretty simple, consisting of a single file that unsurprisingly ran the test suite in Firefox. But as
more harnesses were created, we realized that they all needed to do some common things. For example
they all needed to launch Firefox, most of them needed to modify the profile in some way, etc. So we
factored out the code that would be useful across test harnesses into a file called automation.py.
As Firefox became more complicated, we needed to add more setup steps to the test harnesses.
Automation.py became a dumping ground for anything that needed to be shared across harnesses (or
even stuff that wasn't shared across harnesses, but in theory might need to be in the future).  So
far, there wasn't really a huge problem. We were using inheritance to share code, and sure maybe it
could have been organized better, but this was more the fault of rushed developers than anything
inherently wrong with the design model.

Then Mozilla announced they would be building an Android app. We scrambled to figure out how we
could get our test suites running on a mobile device at production scale. We wrote a new Android
specific class which inherited from the main Firefox one. This worked alright, but there was a lot
of shoe-horning and finagling to get it working properly. At the end, we were sharing a fair amount
of code with the desktop version, but we were also overriding and ignoring a lot of code from the
desktop version.  A year or so later, Mozilla announced that it would be working on B2G, an entire
operating system!  We went through the same process, again creating a new subclass and trying our
darndest to not duplicate any code. The end result was a monstrosity of overrides, subtle changing
of state, no separation of concerns, different command line options meaning different things on
different platforms, the list goes on. Want to add something to the desktop Firefox version of the
test harness? Good luck, chances are you'd break both Fennec and B2G in the process. Want to try and
follow the execution path to understand how the harness works? Ha!

At this point you are probably thinking that this isn't the fault of the DRY principle. This is
simply a case of not architecting it properly. And I completely agree! But this brings me to a point
I'd like to make. Projects that have IFFY requirements are *insanely* difficult to implement
properly in a way that adheres to DRY. Fennec and B2G were both massive and unpredictable
requirement changes that came out of nowhere. In both cases, we were extremely behind on getting
tests running in continuous integration.  We had developers and product managers yelling at us to
get *something* running as quickly as possible.  The longer we took, the bigger the backlog of even
newer requirement changes became. We didn't have time to sit down and think about the future, to
implement everything perfectly. It was a mad dash to the finish line. The problem is exacerbated
when you have many people all working on the same set of issues. Now you've thrown people problems
into the mix and it's all but impossible to design anything coherent.

Had we simply started anew for both Fennec and B2G instead of trying to share code with the desktop
version of the harness, we would have been much better off.

To re-iterate my opening paragraph, I'm not arguing that DRY is bad, or that code duplication is
good. At this point I simply hope to have convinced you that there exist scenarios where striving
for DRY can lead you into trouble. Next, I'll try to convince you that there exist scenarios where a
WET approach can be beneficial.

### Case Study #2: Mozharness

Ask anyone on releng what their most important design considerations are when they approach a
problem. My guess is that somewhere on that list you'll see something about "configurability" or
"being explicit". This basically means that it needs to be as easy as possible to adapt to a
changing requirement. Adaptability is a key skill for a release engineer, they've been dealing with
changing requirements since the dawn of computer science. The reality is that most release engineers
have already learned the lesson I'm just starting to understand now (a lesson I am only beginning to
see because I happen to work pretty closely with a large number of really awesome release
engineers).

Hopefully if I'm wrong about anything in this next part, someone from releng will correct me. Releng
was in a similar situation as our team, except instead of test harnesses, it was buildbotcustom.
Buildbotcustom was where most of the Mozilla-specific buildbot code lived. That is, it was the code
responsible for preparing a slave with all of the  build systems, harnesses, tests, environment and
libraries needed to execute a test or build job. Similar to our test harnesses, changes in
requirements quickly made buildbotcustom very difficult to update or maintain (Note: I don't know
whether it was DRY or WET, but that's not really important for this case study).

To solve the problem, Aki created a tool called mozharness. At the end of the day, mozharness is
just a glorified execution context for running a python script. You pass in some configuration and
run a script that uses said configuration. In addition to that, mozharness itself provides lots of
"libraries" (yes, shared code) for the scripts to use. But mozharness is genius for a few reasons.
First, logging is built into its core. Second it is insanely configurable. But the third is this
concept of actions. An action is just a function, a script is just a series of actions. Actions are
meant to be as atomic and independent as possible. Actions can live as a library in mozharness core,
or be defined by the script author themselves.

What is so special about actions? It allowed us to quickly create a large number of scripts that all
did similar, but not quite the same things. Instead of worrying about whether the scripts share the
same code or not, we just banged out a new one in ten minutes. Instead of having one complicated
script trying to abstract the shared code into one place, we have one script per platform. As you
may imagine, many of these scripts look very similar, there is quite a bit of code duplication going
on. At first we had intended to remove the duplicated code, since we assumed it would be a pain to
maintain. Instead it turned out to be a blessing in disguise.

Like with buildbotcustom and the test harnesses themselves, mozharness scripts also suffer from IFFY
requirements. The difference is, now when someone says something like "We need to pass in
--whizzlebang to B2G emulator reftests and only B2G emulator reftests", it's easy to make that
change. Before we'd need to do some kind of complicated special casing that doesn't scale to make
sure none of the other platforms are affected (not to mention B2G desktop in this case). Now? Just
change a configuration variable that gets passed into the B2G emulator reftest script. Or worst case
scenario, a quick change to the script itself. It is guaranteed that our change won't affect any of
the other platforms or test harnesses because the code we need to modify is not shared.

We are now able to respond to IFFY requirements really quickly. Instead of setting us back days or
weeks, a new requirement might only set us back a few hours or even minutes. With all this extra
time, we can focus on improving our infrastructure, rather than always playing catchup. It's true
that once in awhile we'll need to change duplicated code in more than one location, but in my
experience the number of times this happens (in this particular instance at least) is exceedingly
rare.

Oh, by the way, remember how I said this was a lesson releng had already learned? Take a look at
[these][2] [files][3]\*.  You'll notice that the same configuration is repeated over and over again,
not only for different platforms and test harnesses, but also just different slave types! This may
seem like a horrible idea, until you realize that all this duplication allows releng to be extremely
flexible about what jobs get run on which branches and which types of slaves. It's a lot less work
to maintain some duplication, than it is to figure out a way to share the configuration while
maintaining the same level of speed and flexibility when dealing with IFFY requirements.

### The Takeaway

Hopefully by now I've convinced you that code duplication is not necessarily a bad thing, and that
in some cases it isn't wise to blindly follow the DRY principle. If there's one takeaway from this
post, it's to not take design principles for granted. Yes, code duplication is almost always bad,
but that's not the same thing as always bad. Just be aware of the distinction, and use the case
studies to try to avoid making the same mistakes.

### FAQ (actually, no one has ever asked these)

**So my project has IFFY requirements, should I just duplicate code whenever possible?**  
No.

**Okay.. How do I know if I should use a DRY or WET approach then?**  
I don't think there is a sure fire way, but I have a sort of litmus test. Anytime you are wondering
whether to consolidate some code, ask the question "If I duplicate this code in multiple places and
the requirements change, will I need to update the code in every location? Or just one?". If you
answered the former, then DRY is what you want. But if you answered the latter, then a WET approach
just might be better. This is a difficult question to answer, and the answer is not black and white,
usually it falls somewhere in-between. But at least the question gets you thinking about the answer
in the first place which is already a big step forward. Another thing to take into consideration is
how much time you have to architect your solution properly.

**But if you could somehow have a solution that is both DRY and flexible to incoming requirement
changes, wouldn't that be better?**  
Yes! Inheritance is one of the most obvious and common ways to share code, so I was a bit surprised
at how horribly it failed us. It turns out that DRY is just one principle. And while we succeeded at
not duplicating code, we failed at several other principles (like the [Open/closed principle][4] or
the [Single responsibility principle][5]).  I plan on doing a part 2 blog post that explores these
other principles and possible implementations further.  Stay tuned!

**Edit** - I've since been informed by members of releng that config.py and friends are generally
not well liked. Though there is still consensus that the duplication within them provides
flexibility and that there aren't any other good short term solutions to the problem they are
solving. So I think my point still stands.

[1]: http://en.wikipedia.org/wiki/DRY_principle
[2]: http://mxr.mozilla.org/build/source/buildbot-configs/mozilla-tests/config.py
[3]: http://mxr.mozilla.org/build/source/buildbot-configs/mozilla-tests/b2g_config.py
[4]: http://en.wikipedia.org/wiki/Open/closed_principle
[5]: http://en.wikipedia.org/wiki/Single_responsibility_principle
