## The Zen of Mach

Mach is the Mozilla developer's swiss army knife. It gathers all the important commands you'll ever
need to run, and puts them in one convenient place. Instead of hunting down documentation, or asking
for help on irc, often a simple |mach help| is all that's needed to get you started. Mach is great.
But lately, mach is becoming more like the Mozilla developer's toolbox. It still has everything you
need but it weighs a ton, and it takes a good deal of rummaging around to find anything.

Frankly, a good deal of the mach commands that exist now are either poorly written, confusing to use,
or even have no business being mach commands in the first place. Why is this important? What's wrong
with having a toolbox?

Here's a quote from an [excellent article][0] on engineering effectiveness from the Developer
Productivity lead at Twitter:

> Finally there’s a psychological aspect to providing good tools to engineers that I have to
> believe has a really (sic) impact on people’s overall effectiveness. On one hand, good tools are
> just a pleasure to work with. On that basis alone, we should provide good tools for the same
> reason so many companies provide awesome food to their employees: it just makes coming to work
> every day that much more of a pleasure. But good tools play another important role: because the
> tools we use are themselves software, and we all spend all day writing software, having to do so
> with bad tools has this corrosive psychological effect of suggesting that maybe we don’t
> actually know how to write good software. Intellectually we may know that there are different
> groups working on internal tools than the main features of the product but if the tools you use
> get in your way or are obviously poorly engineered, it’s hard not to doubt your company’s
> overall competence.

Working with good tools is a pleasure. Rather than breaking mental focus, they keep you in the zone.
They do not deny you your zen. Mach is the frontline, it is the main interface to Mozilla for most 
developers. For this reason, it's especially important that mach and all of its commands are an
absolute joy to use.

There is already [good][1] [documentation][2] for building a mach command, so I'm not going to go
over that. Instead, here are some practical tips to help keep your mach command simple, intuitive
and enjoyable to use.

## Keep Logic out of It

As awesome as mach is, it doesn't sprinkle magic fairy dust on your messy jumble of code to make it
smell like a bunch of roses. So unless your mach command is trivial, don't stuff all your logic into
a single `mach_commands.py`. Instead, create a dedicated python package that contains all your functionality,
and turn your `mach_commands.py` into a dumb dispatcher. This python package will henceforth be
called the 'underlying library'.

Doing this makes your command more maintainable, more extensible and more re-useable. It's a
no-brainer!

## No Global Imports

Other than things that live in the stdlib, mozbuild or mach itself, don't import anything in a
`mach_commands.py`'s global scope. Doing this will evaluate the imported file any time the `mach`
binary is invoked. No one wants your module to load itself when running an unrelated command or
|mach help|.

It's easy to see how this can quickly add up to be a huge performance cost.

## Re-use the Argument Parser

If your underlying library has a CLI itself, don't redefine all the arguments with
`@CommandArgument` decorators. Your redefined arguments will get out of date, and your users will
become frustrated. It also encourages a pattern of adding 'mach-only' features, which seem like a
good idea at first, but as I explain in the next section, leads down a bad path.

Instead, import the underlying library's `ArgumentParser` directly. You can do this by using the
`parser` argument to the `@Command` decorator. It'll even conveniently accept a callable so you
can avoid global imports. Here's an example:

```python
def setup_argument_parser():
    from mymodule import MyModuleParser
    return MyModuleParser()

@CommandProvider
class MachCommands(object):
    @Command('mycommand', category='misc', description='does something',
             parser=setup_argument_parser):
    def mycommand(self, **kwargs):
        # arguments from MyModuleParser are in kwargs 
```

If the underlying `ArgumentParser` has arguments you'd like to avoid exposing to your mach command,
you can use [`argparse.SUPPRESS`][3] to hide it from the help.

## Don't Treat the Underlying Library Like a Black Box

Sometimes the underlying library is a huge mess. It can be very tempting to treat it like a black
box and use your mach command as a convenient little fantasy-land wrapper where you can put all the
nice things without having to worry about the darkness below.

This situation is temporary. You'll quickly make the situation way worse than before, as not only
will your mach command devolve into a similar state of darkness, but now changes to the underlying
library can potentially break your mach command. Just suck it up and pay a little technical debt
now, to avoid many times that debt in the future. Implement all new features and UX improvements
directly in the underlying library.

## Keep the CLI Simple

The command line is a user interface, so put some thought into making your command useable and
intuitive. It should be easy to figure out how to use your command simply by looking at its help. If
you find your command's list of arguments growing to a size of epic proportions, consider breaking
your command up into [subcommands][4] with an `@SubCommand` decorator.

Rather than putting the onus on your user to choose every minor detail, make the experience more
magical than a Disney band.

## Be Annoyingly Helpful When Something Goes Wrong

You want your mach command to be like one of those super helpful customer service reps. The ones
with the big fake smiles and reassuring voices. When something goes wrong, your command should calm
your users and tell them everything is ok, no matter what crazy environment they have.

Instead of printing an error message, print an error paragraph. Use natural language. Include all
relevant paths and details. Format it nicely. Create separate paragraphs for each possible failure.
But most importantly, only be annoying *after* something went wrong.

## Use Conditions Liberally

A mach command will only be enabled if all of its [condition functions][5] return True. This keeps
the global |mach help| free of clutter, and makes it painfully obvious when your command is or isn't
supposed to work. A command that only works on Android, shouldn't show up for a Firefox desktop
developer. This only leads to confusion.

Here's an example:

```python
from mozbuild.base import (
    MachCommandBase,
    MachCommandConditions as conditions,
)

@CommandProvider
class MachCommands(MachCommandBase):
    @Command('mycommand', category='post-build', description='does stuff'
             conditions=conditions.is_android):
    def mycommand(self):
        pass
```

If the user does not have an active fennec objdir, the above command will not show up by default in
|mach help|, and trying to run it will display an appropriate error message.

## Design Breadth First

Put another way, keep the big picture in mind. It's ok to implement a mach command with super
specific functionality, but try to think about how it will be extended in the future and build with
that in mind. We don't want a situation where we clone a command to do something only slightly
differently (e.g |mach mochitest| and |mach mochitest-b2g-desktop| from back in the day) because the
original wasn't extensible enough.

It's good to improve a very specific use case that impacts a small number of people, but it's better
to create a base upon which other slightly different use cases can be improved as well.

## Take a Breath

Congratulations, now you are a mach guru. Take a breath, smell the flowers and revel in the
satisfaction of designing a great user experience. But most importantly, enjoy coming into work and
getting to use kick-ass tools.


[0]: http://www.gigamonkeys.com/flowers/
[1]: http://gecko.readthedocs.org/en/latest/python/mach/commands.html
[2]: https://developer.mozilla.org/en-US/docs/Mozilla/Developer_guide/mach#Adding_Features_to_mach
[3]: https://docs.python.org/2.7/library/argparse.html#default
[4]: https://dxr.mozilla.org/mozilla-central/rev/904f3554c08488c53d24deb20a486600ddddd56b/python/mach/mach/decorators.py#241
[5]: http://gecko.readthedocs.org/en/latest/python/mach/commands.html#conditionally-filtering-commands
