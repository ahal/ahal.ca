## An Easier way to Manage Mozconfigs

[Mozconfigwrapper][1] is a tool inspired by Doug Hellman's magnificent [virtualenvwrapper][2]. In a
nutshell, mozconfigwrapper hides all of your mozconfigs into a configurable directory (defaults to
~/.mozconfigs), and lets you easily switch, create, remove, edit and list them. Mozconfigwrapper is
Unix only for now.

Mozconfigwrapper is brand new. I still need to add some better error checking and do testing on OSX.
So if you have any problems installing or using it, please let me know or [file an issue][3].

## Installation

To install first make sure you have [pip][4]. Then run the command

```bash
sudo pip install mozconfigwrapper
```

Next open up your ~/.bashrc file and add the line

```bash
source /usr/local/bin/mozconfigwrapper.sh
```

Note that it may have been installed to a different location on your system. You can use the command 'which mozconfigwrapper.sh' 
to find it.

Finally run the command

```bash
source ~/.bashrc
```

Mozconfigwrapper is now installed.

## Usage
Mozconfigwrapper allows you to create, remove, switch, list and edit mozconfigs.

To build with (activate) a mozconfig named foo, run:

```bash
buildwith foo
```

To create a mozconfig named foo, run:

```bash
mkmozconfig foo
```

To delete a mozconfig named foo, run:

```bash
rmmozconfig foo
```

To see the currently active mozconfig, run:

```bash
mozconfig
```

To list all mozconfigs, run:

```bash
mozconfig -l
```

To edit the currently active mozconfig, run (the $EDITOR variable must be set):

```bash
mozconfig -e
```

## Configuration

By default mozconfigs are stored in the ~/.mozconfigs directory, but you can override this by
setting the $BUILDWITH_HOME environment variable.
e.g, add:

```bash
export BUILDWITH_HOME=~/my/custom/mozconfig/path 
```

to your ~/.bashrc file.

When you make a new mozconfig, it will be populated with some basic build commands and the name of
the mozconfig will be appended to the end of the OBJDIR instruction. You can modify what gets
populated by default by editing the ~/.mozconfigs/.template file. For example, if I wanted my
default configuration to store object directories in a folder called objdirs and enable debugging
and tests, I'd edit the ~/.mozconfigs/.template file to look like: 

```bash
mk_add_options MOZ_OBJDIR=@TOPSRCDIR@/objdirs/
ac_add_options --enable-application=browser
ac_add_options --enable-debug
ac_add_options --enable-tests
```

Now if I ran the command 'mkmozconfig foo', foo would be populated with the above and have the word
'foo' appended to the first line.

[1]: https://github.com/ahal/mozconfigwrapper
[2]: http://www.doughellmann.com/projects/virtualenvwrapper/
[3]: https://github.com/ahal/mozconfigwrapper/issues
[4]: http://pypi.python.org/pypi/pip
