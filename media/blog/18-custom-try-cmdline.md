## How to Push a Custom Test Command Line to Try

### OUTDATED

The steps in this article are no longer accurate. Pushing a custom command line is easier now. See
[here][1] for more details.

 -------------------------------------------------------

Have you ever wanted to see the test results of a custom command line in try? Things like
--test-manifest, --shuffle or --run-slower?  Now you can! The process isn't exactly optimized for
the developer use case, but neither is it really difficult to do once you know how.

Basically, you just edit the 'testing/config/mozharness\_config.py' file. Add a new key called
'&lt;test\_suite&gt;_options' and set its value to a list containing the <b>full command line</b> you
want to pass into the test suite. Substitute '&lt;test_suite&gt;' with the name of the test suite
(e.g mochitest, reftest, xpcshell etc). It's important to note that there is no way to simply extend
the official list, doing this will replace the original list wholesale.

For example, lets say I wanted to add the --shuffle option to all mochitests, my diff would be:

```
diff --git a/testing/config/mozharness_config.py b/testing/config/mozharness_config.py
--- a/testing/config/mozharness_config.py
+++ b/testing/config/mozharness_config.py
@@ -20,9 +20,15 @@ mochitests.
 
 You must also provide the complete command line to avoid errors. The official
 configuration files containing the default values live in:
     https://hg.mozilla.org/build/mozharness/configs
 """
 
 config = {
     # Add custom mozharness config options here
+    "mochitest_options": [
+        "--appname=%(binary_path)s", "--utility-path=tests/bin",
+        "--extra-profile-file=tests/bin/plugins", "--symbols-path=%(symbols_path)s",
+        "--certificate-path=tests/certs", "--autorun", "--close-when-done",
+        "--console-level=INFO", "--setpref=webgl.force-enabled=true", "--shuffle",
+    ],
 }
```

There are a few limitatons to this system I want to call out.

<ol>
<li>You need to know the official options to use as a baseline for your changes. You can inspect official command lines by looking at the mozharness repo:
<ul>
<li>Windows: <a href="/web/20150907231521/http://mxr.mozilla.org/build/source/mozharness/configs/unittests/win_unittest.py">http://mxr.mozilla.org/build/source/mozharness/configs/unittests/win_unittest.py</a></li>
<li>OSX: <a href="/web/20150907231521/http://mxr.mozilla.org/build/source/mozharness/configs/unittests/mac_unittest.py">http://mxr.mozilla.org/build/source/mozharness/configs/unittests/mac_unittest.py</a></li>
<li>Linux: <a href="/web/20150907231521/http://mxr.mozilla.org/build/source/mozharness/configs/unittests/linux_unittest.py">http://mxr.mozilla.org/build/source/mozharness/configs/unittests/linux_unittest.py</a></li>
<li>B2G: <a href="/web/20150907231521/http://mxr.mozilla.org/build/source/mozharness/configs/b2g/emulator_automation_config.py">http://mxr.mozilla.org/build/source/mozharness/configs/b2g/emulator_automation_config.py</a></li>
</ul>
Note: Android doesn't currently use mozharness so this trick is not yet possible on Fennec.
</li>
<li>There is no way to specify separate command lines for different platforms. For example the mochitest command lines for B2G and desktop are very different. There is no way to specify a custom command line 
for one without breaking the other. To get around this you'll just need to do two separate try pushes with two separate command lines.</li>
<li>Certain options (like --this-chunk and --total-chunks) might confuse the automation and have unintended consequences. For example specifying '--this-chunk 1' will tell every job (even chunks 2+) to run the first chunk.</li>
</ol>

In conclusion, there are many things we can do to make this easier for developers. The current
solution was really implemented to allow tree specific mozharness config values, the fact that you
can push custom command lines to try was just a useful side effect. I hope in the future someone
will make the developer story around this less confusing, but I'm not sure how high of a priority it
is at the moment.

[1]: https://groups.google.com/forum/#!topic/mozilla.dev.platform/AKDyoQShFEs
