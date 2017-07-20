How to bulk install Firefox Addons

Firefox is known for its extensibility. In fact, over 2.4 *billion* addons have been downloaded to date,
meaning there are a lot of people using a lot of addons. While having 20+ addons can undoubtedly personalize your
browsing experience, it can also be a pain in the ass to manually install them every time you set up a new
Firefox profile. As a developer working on Firefox related automation tools, this is twice as
true since I create a separate profile for each and every project I work on, installing a constant set of
addons on each one.  

Enter mozprofile. Mozprofile is a python package that is used by our UI test automation tool called [Mozmill][1],
and handles anything related to Firefox profiles. While mozprofile has always allowed users to install addons to their
profile, it wasn't very useful for the above use case. First of all, you had to pass in the .xpi file. Secondly
there was no stand alone command line interface, it was mainly meant to be used as an API.

I made some tweaks to mozprofile which adds the ability to specify a manifest of addons to install. You have the
option of passing the url of the addon's .xpi file, a path to a .xpi on your filesystem, the AMO
([addons.mozilla.org][2]) id of the addon, or failing all that, allow mozprofile to search for the addon using
AMO's REST api.
 
This tutorial assumes you have Python installed and that you know how to [install Python packages][3].  
Steps:

1. Install mozprofile from pypi or checkout the source at [http://github.com/mozautomation/mozmill][4].  I'd recommend using a [virtualenv][5].

    pip install mozprofile

2. Create a manifest describing the addons to install. Lets call the manifest addons.ini.<br>
The below is an example manifest that demonstrates all of the possible methods to install Firebug.

```ini
# install from a url
[https://getfirebug.com/releases/firebug/1.8/firebug-1.8.0a1.xpi]

# install from local file path, can be relative or absolute
[path/to/firebug.xpi]

# install from a directory containing a bunch of addons
# this is more useful for automated testing
[path/to/directory/of/addons]

# sometimes the url or file path doesn't reveal the name of the addon
# makes the manifest a bit more human readable (path can be a url or a file path)
[firebug]
path = https://getfirebug.com/releases/firebug/1.8/firebug-1.8.0a1.xpi

# install from amo id
[firebug]
amo_id = 1843

# you can also specify a different locale
[firebug]
amo_id = 1843
amo_locale = fr

# install from amo search
# this will install the top hit returned from search and isn't guaranteed to be the one you want
# use one of the other methods if you need to be absolutely sure
[firebug]

# search with different locale
[firebug]
amo_locale = fr
```

3. Find the path to the profile you want to install the addons to. If you don't know where your profile is type 'about:support' in your location bar and look for 'Profile Directory'.<br>
4. Run the command:<br>
    
    mozprofile -p /path/to/profile/ -m /path/to/addons.ini
     
Use <pre>mozprofile --help</pre> for other options and more information<br>

That's it! The addons you specified should now be installed.

I also attached a manifest that installs all 45 of AMO's
'featured' addons. Installing them all at once results in this somewhat hilarious behaviour upon opening your
profile for the first time (do not try this at home!).

<img src="/static/img/blog/2011/featured-addons.png" style="width:100%;">

One more thing to note, mozprofile can also be used as an API.  We're working on documentation but for now see the repo for more [details][6].

[1]: https://developer.mozilla.org/en/Mozmill
[2]: https://addons.mozilla.org/
[3]: http://pypi.python.org/pypi/pip
[4]: http://github.com/mozautomation/mozmill
[5]: http://pypi.python.org/pypi/virtualenv
[6]: https://github.com/mozautomation/mozmill/tree/master/mozprofile 
