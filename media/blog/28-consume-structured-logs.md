## How to Consume Structured Test Results

You may not know that most of our test harnesses are now outputting structured logs (thanks in large
part to :chmanchester's tireless work). Saying a log is structured simply means that it is in a
machine readable format, in our case each log line is a JSON object. When streamed to a terminal or
treeherder log, these JSON objects are first formatted into something that is human readable, aka
the same log format you're already familiar with (which is why you may not have noticed this).

While this might not seem all that exciting it lets us do many things, such as change the human
readable formats and add metadata, without needing to worry about breaking any fragile regex
based log parsers. We are now in the process of updating much of our internal tooling to consume
these structured logs. This will let us move faster and provide a foundation on top of which we can
build all sorts of new and exciting tools that weren't previously possible.

But the benefits of structured logs don't need to be constrained to the Tools and Automation team.
As of today, anyone can consume structured logs for use in whatever crazy tools they can think of.
This post is a brief guide on how to consume structured test results.


## A High Level Overview

Before diving into code, I want to briefly explain the process at a high level.

1. The test harness is invoked in such a way that it streams a human formatted log to stdout, and a
   structured log to a file.
2. After the run is finished, [mozharness][0] uploads the structured log to a server on AWS using a
   tool called blobber. Mozharness stores a map of uploaded file names to blobber urls as a buildbot
   property. The structured logs are just one of several files uploaded via blobber.
3. The pulse `build` exchange publishes buildbot properties. Though the messages are based on
   buildbot events and can be difficult to consume directly.
4. A tool called [pulsetranslator][1] consumes messages from the `build` exchange, cleans them up a
   bit and re-publishes them on the `build/normalized` exchange.
5. Anyone creates a NormalizedBuildConsumer in pulse, finds the url to the structured log and
   downloads it.

Sound complicated? Don't worry, the only step you're on the hook for is step 5.


## Creating a Pulse Consumer

For anyone not aware, [pulse][2] is a system at Mozilla for publishing and subscribing to arbitrary
events. Pulse has all sorts of different applications, one of which is receiving notifications
whenever a build or test job has finished.


### The Setup

First, head on over to [https://pulse.mozilla.org/][3] and create an account. You can sign in with
Persona, and then create one or more pulse users. Next you'll need to install the [mozillapulse][4]
python package. First make sure you [have pip installed][5], then:

```bash
$ pip install mozillapulse
```

As usual, I recommend doing this in a [virtualenv][6]. That's it, no more setup required!


### The Execution

Creating a pulse consumer is pretty simple. In this example we'll download all logs pertaining to
mochitests on mozilla-inbound and mozilla-central. This example depends on the `requests` package,
you'll need to `pip install` it if you want to run it locally:

```python
import json
import sys
import traceback

import requests

from mozillapulse.consumers import NormalizedBuildConsumer

def run(args=sys.argv[1:]):
    pulse_args = {
        # a string to identify this consumer when logged into pulse.mozilla.org
        'applabel': 'mochitest-log-consumer',

        # each message contains a topic. Only messages that match the topic specified here will
        # be delivered. '#' is a wildcard, so this topic matches all messages that start with
        # 'unittest'.
        'topic': 'unittest.#',

        # durable queues will store messages inside pulse even if your consumer goes offline for
        # a bit. Otherwise, any messages published while the consumer is not explicitly
        # listeneing will be lost forever. Keep it set to False for testing purposes.
        'durable': False,

        # the user you created on pulse.mozilla.org
        'user': 'ahal',

        # the password you created for the user
        'password': 'hunter1',

        # a callback that will get invoked on each build event
        'callback': on_build_event,
    }


    pulse = NormalizedBuildConsumer(**pulse_args)

    while True:
        try:
            pulse.listen()
        except KeyboardInterrupt:
            # without this ctrl-c won't work!
            raise
        except IOError:
            # sometimes you'll get a socket timeout. Just call listen again and all will be
            # well. This was fairly common and probably not worth logging.
            pass
        except:
            # it is possible for rabbitmq to throw other exceptions. You likely
            # want to log them and move on.
            traceback.print_exc()


def on_build_event(data, message):
    # each message needs to be acknowledged. This tells the pulse queue that the message has been
    # processed and that it is safe to discard. Normally you'd want to ack the message when you know
    # for sure that nothing went wrong, but this is a simple example so I'll just ack it right away.
    message.ack()

    # pulse data has two main properties, a payload and metadata. Normally you'll only care about
    # the payload.
    payload = data['payload']
    print('Got a {} job on {}'.format(payload['test'], payload['tree']))

    # ignore anything not from mozilla-central or mozilla-inbound
    if payload['tree'] not in ('mozilla-central', 'mozilla-inbound'):
        return

    # ignore anything that's not mochitests
    if not payload['test'].startswith('mochitest'):
        return

    # ignore jobs that don't have the blobber_files property
    if 'blobber_files' not in payload:
        return

    # this is a message we care about, download the structured log!
    for filename, url in payload['blobber_files'].iteritems():
        if filename == 'raw_structured_logs.log':
            print('Downloading a {} log from revision {}'.format(
                   payload['test'], payload['revision']))
            r = requests.get(url, stream=True)

            # save the log
            with open('mochitest.log', 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
            break

    # now time to do something with the log! See the next section.

if __name__ == '__main__':
    sys.exit(run())
```


### A Note on Pulse Formats

Each pulse publisher can have its own custom topics and data formats. The best way to discover these
formats is via a tool called [pulse-inspector][7]. To use it, type in the exchange and routing key,
click `Add binding` then `Start Listening`. You'll see messages come in which you can then inspect
to get an idea of what format to expect. In this case, use the following:

```
Pulse Exchange: exchange/build/normalized
Routing Key Pattern: unittest.#
```


## Consuming Log Data

In the last section we learned how to obtain a structured log. Now we learn how to use it. All
structured test logs follow the same structure, which you can see in the [mozlog documentation][8].
A structured log is a series of line-delimited JSON objects, so the first step is to decode each
line:

```python
lines = [json.loads(l) for l in log.splitlines()]
for line in lines:
    # do something
```

If you have a large number of log lines, you'll want to use a generator. Another common use case is
registering callbacks on specific actions. Luckily, mozlog provides several [built-in functions][9]
for dealing with these common cases. There are two main approaches, registering callbacks or
creating log handlers.


### Examples ###

The rest depends on what you're trying to accomplish. It now becomes a matter of reading the
[docs][10] and figuring out how to do it. Below are several examples to help get you started.

List all failed tests by registering callbacks:

```python
from mozlog.structured import reader

failed_tests = []
def append_if_failed(log_item):
    if 'expected' in log_item:
        failed_tests.append(log_item['test'])

with open('mochitest.log', 'r') as log:
    iterator = reader.read(log)
    action_map = { 'test_end': append_if_failed }
    reader.each_log(iterator, action_map)

print('\n'.join(failed_tests))
```

List the time it took to run each test using a log handler:

```python
import json

from mozlog.structured import reader

class TestDurationHandler(reader.LogHandler):
    test_duration = {}
    start_time = None

    def test_start(self, item):
        self.start_time = item['timestamp']

    def test_end(self, item):
        duration = item['timestamp'] - self.start_time
        self.test_duration[item['test']] = duration

handler = TestDurationHandler()
with open('mochitest.log', 'r') as log:
    iterator = reader.read(log)
    reader.handle_log(iterator, handler)

print(json.dumps(handler.test_duration, indent=2))
```

How to consume the log is really up to you. The built-in methods can be helpful, but are by no means
required. Here is a [more complicated example][11] that receives structured logs over a socket, and
spawns an arbitrary number of threads to process and execute callbacks on them.

If you have questions, comments or suggestions, don't hesitate to speak up!

Finally, I'd also like to credit Ahmed Kachkach an intern who not only worked on structured logging
in mochitest over the summer, but also created the system that manages pulse users and queues.


[0]: https://wiki.mozilla.org/ReleaseEngineering/Mozharness
[1]: https://github.com/mozilla/pulsetranslator
[2]: https://wiki.mozilla.org/Auto-tools/Projects/Pulse
[3]: https://pulse.mozilla.org/
[4]: https://hg.mozilla.org/automation/mozillapulse
[5]: https://pip.pypa.io/en/latest/installing.html
[6]: http://virtualenv.readthedocs.org/en/latest/virtualenv.html#installation
[7]: https://tools.taskcluster.net/pulse-inspector/
[8]: http://mozbase.readthedocs.org/en/latest/mozlog_structured.html#data-format
[9]: http://mozbase.readthedocs.org/en/latest/mozlog_structured.html#processing-log-files
[10]: http://mozbase.readthedocs.org/en/latest/mozlog_structured.html
[11]: https://github.com/ahal/corredor/blob/master/corredor/handler.py
