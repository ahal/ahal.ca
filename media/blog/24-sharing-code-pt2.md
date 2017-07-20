## Part 2: How to deal with IFFY requirements

My last post was basically a very long winded way of saying, "we have a problem". It kind of did a
little dance around "why is there a problem" and "how do we fix it", but I want to explore these two
questions in a bit more detail. Specifically, I want to return to the two case studies and explore
why our test harnesses don't work and why mozharness does work even though both have IFFY (in flux
for years) requirements. Then I will explore how to use the lessons learned to improve our general
test harness design.

### DRY is not everything

I talked a lot about the [DRY  principle][1] in the last article. Basically the conclusion about it
was that it is very useful, but that we tend to fixate on it to the point where we ignore other
equally useful principles. Having reached this conclusion, I did a quick internet search and found
[an article][2] by Joel Abrahamsson arguing the exact same point (albeit much more succinctly than
me). Through his article I found out about the [SOLID principles][3] of object oriented design (have
I been living under a rock?). They are all very useful guidelines, but there are two that
immediately made me think of our test harnesses in a bad way. The first is the [single
responsibility principle][4] (which I was delighted to find is meant to mitigate requirement
changes) and the second is the [open/closed principle][5].


The single responsibility principle states that a class should only be responsible for one thing,
and responsibility for that thing should not be shared with other classes. What is a responsibility?
A responsibility is defined as a *reason to change*. To use the wikipedia example, a class that
prints a block of text can undergo two changes. The content of the text can change, or the format of
the text can change. These are two different responsibilities that should be split out into
different classes.

The open/closed principle states that software should be open for extension, but closed for
modification. In other words, it should be possible to change the behaviour of the software only by
adding new code without needing to modify any existing code. A popular way of implementing this is
through abstract base classes. Here the interface is closed for modification, and each new
implementation is an extension of that.

Our test harnesses fail miserably at both of these principles. Instead of having several classes
each with a well defined responsibility, we have a single class responsible for everything. Instead
of being able to add some functionality without worrying about breaking something else, you have to
take great pains that your change won't affect some other platform you don't even care about!

Mozharness on the other hand, while not perfect, does a much better job at both principles. The
concept of actions makes it easy to extend functionality without modifying existing code. Just add a
new action to the list! The core library is also much better separated by responsibility. There is a
clear separation between general script, build, and testing related functionality.

### Inheritance is evil
This is probably old news to many people, but this is something that I'm just starting to figure out
on my own. I like Zed Shaw's [analogy from *Learn Python the Hard Way*][6] the best. Instead of
butchering it, here it is in its entirety.

> In the fairy tales about heroes defeating evil villains there's always a dark forest of some kind.
> It could be a cave, a forest, another planet, just some place that everyone knows the hero
> shouldn't go. Of course, shortly after the villain is introduced you find out, yes, the hero has
> to go to that stupid forest to kill the bad guy. It seems the hero just keeps getting into
> situations that require him to risk his life in this evil forest.
> 
> You rarely read fairy tales about the heroes who are smart enough to just avoid the whole situation
> entirely. You never hear a hero say, "Wait a minute, if I leave to make my fortunes on the high seas
> leaving Buttercup behind I could die and then she'd have to marry some ugly prince named Humperdink.
> Humperdink! I think I'll stay here and start a Farm Boy for Rent business." If he did that there'd
> be no fire swamp, dying, reanimation, sword fights, giants, or any kind of story really. Because of
> this, the forest in these stories seems to exist like a black hole that drags the hero in no matter
> what they do.
> 
> In object-oriented programming, Inheritance is the evil forest. Experienced programmers know to
> avoid this evil because they know that deep inside the Dark Forest Inheritance is the Evil Queen
> Multiple Inheritance. She likes to eat software and programmers with her massive complexity teeth,
> chewing on the flesh of the fallen. But the forest is so powerful and so tempting that nearly every
> programmer has to go into it, and try to make it out alive with the Evil Queen's head before they
> can call themselves real programmers. You just can't resist the Inheritance Forest's pull, so you go
> in. After the adventure you learn to just stay out of that stupid forest and bring an army if you
> are ever forced to go in again.
> 
> This is basically a funny way to say that I'm going to teach you something you should avoid called
> Inheritance. Programmers who are currently in the forest battling the Queen will probably tell you 
> that you have to go in. They say this because they need your help since what they've created is
> probably too much for them to handle. But you should always remember this:
> 
> Most of the uses of inheritance can be simplified or replaced with composition, and multiple
> inheritance should be avoided at all costs.

I had never heard the (apparently popular) term "composition over inheritance". Basically, unless
you really really mean it, always go for "X has a Y" instead of "X is a Y". Never do "X is a Y"
for the sole purpose of avoiding code duplication. This is exactly the mistake we made in our test
harnesses. The Android and B2G runners just inherited everything from the desktop runner, but oops,
turns out all three are actually quite different from one another. 
Mozharness, while again not perfect, does a better job at avoiding inheritance. While it makes heavy
use of the mixin pattern (which, yes, is still inheritance) at least it promotes separation of
concerns more than classic inheritance.

### Practical Lessons

So this is all well and great, but how can we apply all of this to our automation code base?

A smarter way to approach our test harness design would have been to have most of the shared code
between the three platforms in a single (relatively) bare-bones runner that *has a* target
environment (e.g desktop Firefox, Fennec or B2G in this case). In this model there is no
inheritance, and no code duplication. It is easy to extend without modifying (just add a new target
environment) and there are clear and distinct responsibilities between managing tests/results and
actually launching them. In fact this how the gaia team implemented their [marionette-js-runner][7].
I'm not sure if that pattern is common to node's [mocha runner][8] or something of their design, but
I like it.

I'd also like our test harnesses to employ mozharness' concept of actions. Each action could be
an atomic as possible setup step. For example, setting preferences in the profile is a single action.
Setting environment is another. Parsing a manifest could be a third. Each target environment would
consist of a list of actions that are run in a particular order. If code needs to be shared, simply
add the corresponding action to whichever targets need it. If not, just don't include the
action in the list for targets that don't need it.

My dream end state here is that there is no distinction between test runners and mozharness scripts.
They are both trying to do the same thing (perform setup, launch some code, collect results) so why
bother wrapping one around the other? The test harness should just *be* a mozharness script and vice
versa. This would bring actions into test harnesses, and allow mozharness scripts to live in-tree.

### Conclusion

Is it possible to avoid code duplication with a project that has IFFY requirements? I think yes. But
I still maintain it is exceptionally hard. It wasn't until after it was too late and I had a lot of
time to think about it that I realized the mistakes we made. And even with what I know now, I don't
think I would have fared much better given the urgency and time constraints we were under. Though
next time, I think I'll at least have a better chance.

[1]: http://en.wikipedia.org/wiki/DRY_principle
[2]: http://joelabrahamsson.com/the-dry-obsession
[3]: http://en.wikipedia.org/wiki/SOLID
[4]: http://en.wikipedia.org/wiki/Single_responsibility_principle
[5]: http://en.wikipedia.org/wiki/Open/closed_principle
[6]: http://learnpythonthehardway.org/book/ex44.html
[7]: https://github.com/mozilla-b2g/marionette-js-runner
[8]: http://visionmedia.github.io/mocha
