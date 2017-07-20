## A Mercurial extension to version multiple patch queues

[qqver][1] is a Mercurial extension that forces mq to version all patch queues in the same
repository. The syntax is the exact same as when doing normal patch queue versioning (i.e 'hg init
--mq'), except the repo is created one directory higher so it is able to track all patch queues. As
with stock queue repos, new and existing patches are added automatically.

qqver solves a very specific use case, it probably isn't useful for the majority of Mercurial users.
If you answer yes to both of the following questions, you might want to look into qqver:

* Do you like to work with multiple patch queues in a single repository (i.e using hg qq)?
* Do you like to version your patch queues with mq's patch versioning system (i.e using the --mq flag)?

Versioning all patch queues in the same repo makes it a lot easier to create and manage remote
repos, e.g on an hg.m.o [user repository][2]. Instead of having to create N user repositories for N
patch queues, you only need to create one.

qqver works by monkeypatching the mq extension in an unobtrusive way. This gives it some nice
properties. First, the syntax is the exact same as what you are already used to:

```bash
# create queue repo and push remote
hg init --mq
hg commit --mq
hg push --mq
```

Another nice property is that it is fully compatible with Steve Fink's [mqext][3] extension. This
means if you want to autocommit your patch queue anytime you make a change, you can easily do so by
configuring mqext. One thing I'd still like to implement, is to monkeypatch mqext so it adds the
current patch queue to the commit messages (in addition to the patch name).

### Installation

```bash
hg clone http://hg.mozilla.org/users/ahalberstadt_mozilla.com/qqver/
```

Then edit your ~/.hgrc file and add:

```ini
[extensions]
mq=
qqver=&lt;path/to/qqver&gt;
```

Note that the mq extension needs to be installed, otherwise qqver makes no sense! Also note that
this is still fairly untested, so please let me know of any problems you encounter or features you'd
like implemented. Or feel free to send me a patch ;).

[1]: http://hg.mozilla.org/users/ahalberstadt_mozilla.com/qqver/
[2]: https://developer.mozilla.org/en-US/docs/Creating_Mercurial_User_Repositories#Mercurial_Queue_User_Repository_Workflow
[3]: https://bitbucket.org/sfink/mqext
