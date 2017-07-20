## Running B2G unittests with Mach

Before now running 'classic' unittests (mochitest, reftest, xpcshell, etc.) on B2G emulators has
been a massive pain. The new recommended way of running them is through mach.

1. Update B2G repo if you haven't already: `git pull`
2. Configure an emulator: `BRANCH=master ./config.sh emulator`
3. Build: `./build.sh`
4. Run: `./mach mochitest-remote`

Substitute 'mochitest' with 'reftest', 'crashtest' or 'xpcshell' to run those test suites instead.
By default all tests will be run, but you can pass in a test path like so:

```bash
./mach mochitest-remote gecko/dom/tests/mochitest/dom-level0
```

For more details and a full list of command arguments, run:

```bash
./mach help
./mach help mochitest-remote
```

Currently, these commands will not be available if your B2G repo is configured for anything other than an
emulator. [Bug 915810][1] tracks progress
towards getting them working on a device, but I'm not sure when the ETA of that will be. For more
information on running these tests, see [Firefox OS automated testing][2].

Finally, if you come across any bugs, please file and cc me, ahal on irc. Or if you want to
implement a B2G related mach command and don't know where to start, feel free to give me a shout.

Cheers,  
Andrew

[1]: https://bugzilla.mozilla.org/show_bug.cgi?id=915810
[2]: https://developer.mozilla.org/en-US/docs/Mozilla/Firefox_OS/Platform/Automated_testing
