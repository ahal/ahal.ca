## Python Logging - Format a message without printing it

I came across an odd python problem the other day. I wanted to format a log message without printing
it with python's logging module. But I couldn't find any examples or others who wanted to do the
same thing.

You might ask why I would want to do this. In my case, I was using sys.stdout.write() to display the
progress of a download as a percentage. Python's logging module automatically appends a newline to
your message and there didn't seem to be a way to change this without a subclass. Anytime you want
to overwrite something on the previous line with python logging, you will run into trouble.

Luckily after a quick look at the source, there's a relatively simple solution to the problem:    

```python
def format_message(log, level, msg, *args):
    fn, lno, func = log.findCaller()
    record = log.makeRecord(log.name, level, fn, lno, msg, args, False, func=func)
    return log.handlers[0].format(record)

log = logging.getLogger('MyCustomLogger')
message = format_message(log, logging.INFO, '%s is happening', 'Something')

# Now you can do stuff like this with the proper formatting
sys.stdout.write(message)
for i in range(0,101):
    percent = '(%0.0f%%)' % i 
    sys.stdout.write(' %s%s' % (percent, '\b' * (len(percent) + 1)))
    sys.stdout.flush()
sys.stdout.write('\n')
```

Depending on your logger's formatter, the output might look like:

```
MyCustomLogger INFO | Something is happening (100%)
```

Be careful, this solution will only format the message based on the first handler in the handlers
list.  If there are no handlers or multiple handlers, you'll probably want some additional logic to
take care of this.
