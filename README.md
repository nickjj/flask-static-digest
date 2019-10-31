## What is Flask-Static-Digest? [![Build Status](https://secure.travis-ci.org/nickjj/flask-static-digest.png)](http://travis-ci.org/nickjj/flask-static-digest)

It is a Flask extension that will make your static files production ready with
very minimal effort on your part. It does this by md5 tagging and gzipping your
static files. It does not bundle your assets or do any type of additional asset
processing.

Other web frameworks like Django, Ruby on Rails and Phoenix all have this
feature built into their framework, and now with this extension Flask does too.

**This extension will work if you're not using any asset build tools but at the
same time it also works with Webpack, Grunt, Gulp or any other build tool you
can think of. This tool does not depend on or compete with existing asset build
tools.**

### How does it work?

There's 3 pieces to this extension:

1. It adds a custom Flask CLI command to your project. When you run this
   command it looks at your static files and then generates an md5 tagged
   version of each file along with optionally gzipping them too.

2. When the above command finishes it creates a `cache_manifest.json` file in
   your static folder which maps the regular file names, such as
   `images/flask.png` to `images/flask-f86b271a51b3cfad5faa9299dacd987f.png`.

3. It adds a new template helper called `static_url_for` which uses Flask's
   `url_for` under the hood but is aware of the `cache_manifest.json` file so
   it knows how to resolve `images/flask.png` to the md5 tagged file name.

### Installation / Quick start

*You'll need to be running Python 3.5+ and using Flask 1.0 or greater.*

`pip install Flask-Static-Digest`

#### Example directory structure for a 'hello' app

```
├── hello
│   ├── __init__.py
│   ├── app.py
│   └── static
│       └── css
│           ├── app.css
└── requirements.txt
```

#### Flask app factory example using this extension

```py
from flask import Flask
from flask_static_digest import FlaskStaticDigest

flask_static_digest = FlaskStaticDigest()


def create_app():
    app = Flask(__name__)

    flask_static_digest.init_app(app)

    @app.route("/")
    def index():
        return "Hello, World!"

    return app
```

*A more complete example app can be found in the [tests/
directory](https://github.com/nickjj/flask-static-digest/tree/master/tests/example_app).*

#### Using the newly added Flask CLI command

You'll want to make sure to at least set the `FLASK_APP` environment variable:

```sh
export FLASK_APP=hello.app
export FLASK_ENV=development
```

Then run the `flask` binary to see its help menu:

```sh
Usage: flask [OPTIONS] COMMAND [ARGS]...

  ...

Options:
  --version  Show the flask version
  --help     Show this message and exit.

Commands:
  digest  md5 tag and gzip static files.
  routes  Show the routes for the app.
  run     Run a development server.
  shell   Run a shell in the app context.
```

If all went as planned you should see the new `digest` command added to the
list of commands.

### Going over the Flask CLI commands

Running `flask digest` will produce this help menu:

```sh
Usage: flask digest [OPTIONS] COMMAND [ARGS]...

  md5 tag and gzip static files.

Options:
  --help  Show this message and exit.

Commands:
  clean    Remove generated static files and cache manifest.
  compile  Generate optimized static files and a cache manifest.
```

Each command is labeled, but here's a bit more information on what they do.

#### compile

Inspects your Flask app's `static_folder` and uses that as both the input and
output path of where to look for and create the newly digested and compressed
files.

At a high level it recursively loops over all of the files it finds in that
directory and then generates the md5 tagged and gzipped versions of each file.
It also creates a `cache_manifest.json` file in the root of your
`static_folder`.

That manifest file is machine generated meaning you should not edit it unless
you really know what you're doing.

This file maps the human readable file name of let's say `images/flask.png` to
the digested file name. It's a simple key / value set up. It's basically a
Python dictionary in JSON format.

In the end it means if your static folder looked like this originally:

- `css/app.css`
- `js/app.js`
- `images/flask.png`

And you decided to run the compile command, it would now look like this:

- `css/app.css`
- `css/app.css.gz`
- `css/app-5d41402abc4b2a76b9719d911017c592.css`
- `css/app-5d41402abc4b2a76b9719d911017c592.css.gz`
- `js/app.js`
- `js/app.js.gz`
- `js/app-098f6bcd4621d373cade4e832627b4f6.js`
- `js/app-098f6bcd4621d373cade4e832627b4f6.js.gz`
- `images/flask.png`
- `images/flask.png.gz`
- `images/flask-f86b271a51b3cfad5faa9299dacd987f.png`
- `images/flask-f86b271a51b3cfad5faa9299dacd987f.png.gz`
- `cache_manifest.json`

*Your md5 hashes will be different because it depends on what the contents of
the file are.*

#### clean

Inspects your Flask app's `static_folder` and uses that as the input path of
where to look for digested and compressed files.

It will recursively delete files that have a file extension of `.gz` and also
deletes files that have been digested. It determines if a file has been
digested based on its file name. In other words, it will delete files that
match this regexp `r"-[a-f\d]{32}"`.

In the end that means if you had these 4 files in your static folder:

- `images/flask.png`
- `images/flask.png.gz`
- `images/flask-f86b271a51b3cfad5faa9299dacd987f.png`
- `images/flask-f86b271a51b3cfad5faa9299dacd987f.png.gz`

And you decided to run the clean command, the last 3 files would be deleted
leaving you with the original `images/flask.png`.

### Configuring this extension

By default this extension will md5 tag all files it finds in your configured
`static_folder`. It will also create gzipped versions of each file. If you
don't like that behavior there's 2 options you can optionally configure:

```py
FLASK_STATIC_DIGEST_BLACKLIST_FILTER = []
# If you want specific extensions to not get md5 tagged you can add them to
# the list, such as: [".htm", ".html", ".txt"]. Make sure to include the ".".

FLASK_STATIC_DIGEST_GZIP_FILES = True
# When set to False then gzipped files will not be created but static files
# will still get md5 tagged.
```

You can override these defaults in your Flask app's config file.

### Modifying your templates to use static_url_for instead of url_for

We're all familiar with this code right?

```html
<img src="{{ url_for('static', filename='images/flask.png') }}"
     width="480" height="188" alt="Flask logo" />
```

When you put the above code into a Flask powered Jinja 2 template, it turns
into this:

```html
<img src="images/flask.png"
     width="480" height="188" alt="Flask logo" />
```

The path might vary depending on how you configured your Flask app's
`static_folder` but you get the idea.

#### Using static_url_for instead of url_for

Let's use the same example as above:

```html
<img src="{{ static_url_for('static', filename='images/flask.png') }}"
     width="480" height="188" alt="Flask logo" />
```

But now take a look at the output this produces:

```html
<img src="/images/flask-f86b271a51b3cfad5faa9299dacd987f.png"
     width="480" height="188" alt="Flask logo" />
```

Instead of using `url_for` you would use `static_url_for`. This uses Flask's
`url_for` under the hood so things like `_external=True` and everything else
`url_for` supports is available to use with `static_url_for`.

That means to use this extension you don't have to do anything other than
install it, optionally run the CLI command to generate the manifest and then
rename your static file references to use `static_url_for` instead of
`url_for`.

If your editor supports performing a find / replace across multiple files you
can quickly make the change by finding `url_for('static'` and replacing that
with `static_url_for('static'`. If you happen to use double quotes instead of
single quotes you'll want to adjust for that too.

### What about development vs production and performance implications?

You would typically only run the CLI command to prepare your static files for
production. Running `flask digest compile` would become a part of your build
process -- typically after you pip install your dependencies.

In development when the `cache_manifest.json` likely doesn't exist
`static_url_for` calls `url_for` directly. This allows the `static_url_for`
helper to work in both development and production without any fuss.

It's also worth pointing out the CLI command is expected to be run before you
even start your Flask server (or gunicorn / etc.), so there's no perceivable
run time performance hit. It only involves doing 1 extra dictionary lookup at
run time which is many orders of magnitude faster than even the most simple
database query.

**In other words, this extension is not going to negatively impact the
performance of your web application. If anything it's going to speed it up and
save you money on hosting**.

That's because gzipped files can be upwards of 5-10x smaller so there's less
bytes to transfer over the network.

Also with md5 tagging each file it means you can configure your web server such
as nginx to cache each file forever. That means if a user visits your site a
second time in the future, nginx will be smart enough to load it from their
local browser's cache without even contacting your server. It's a 100% local
look up.

This is as efficient as it gets. You can't do this normally without md5 tagging
each file because if the file changes in the future, nginx will continue
serving the old file until the cache expires so users will never see your
updates. But due to how md5 hashing works, if the contents of a file changes it
will get generated with a new name and nginx will serve the uncached new file.

This tactic is commonly referred to as "cache busting" and it's a very good
idea to do this in production. You can even go 1 step further and serve your
static files using a CDN. Using this cache busting strategy makes configuring
your CDN a piece of cake since you don't need to worry about ever expiring your
cache manually.

### How do you use this extension with Webpack or another build tool?

It works out of the box with no extra configuration or plugins needed for
Webpack or your build tool of choice.

Typically the Webpack (or another build tool) work flow would look like this:

- You configure Webpack with your source static files directory
- You configure Webpack with your destination static files directory
- Webpack processes your files in the source directory and copies them to the destination directory
- Flask is configured to serve static files from that destination directory

For example, your source directory might be `assets/` inside of your project
and the destination might be `myapp/static`.

This extension will look at your Flask configuration for the `static_folder`
and determine it's set to `myapp/static` so it will md5 tag and gzip those
files. Your Webpack source files will not get digested and compressed.

### Potentially updating your .gitignore file

If you're using something like Webpack then chances are you're already git
ignoring the static files it produces as output. It's a common pattern to
commit your Webpack source static files but ignore the compiled static files
it produces.

But if you're not using Webpack or another asset build tool then the static
files that are a part of your project might have the same source and
destination directory. If that's the case, chances are you'll want to git
ignore the md5 tagged files as well as the gzipped and `cache_manifest.json`
files from version control.

Add this to your `.gitignore` file to ignore certain files this extension
creates:

```
*-[0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f].*
*.gz
cache_manifest.json
```

This allows your original static files but ignores everything else this
extension creates. I am aware at how ridiculous that ignore rule is for the md5
hash but using `[0-9a-f]{32}` does not work. If you know of a better way,
please open a PR!

### About the author

- Nick Janetakis | <https://nickjanetakis.com> | [@nickjanetakis](https://twitter.com/nickjanetakis)

If you're interested in learning Flask I have a 17+ hour video course called
[Build a SAAS App with
Flask](https://buildasaasappwithflask.com/?utm_source=github&utm_medium=staticdigest&utm_campaign=readme).
It's a course where we build a real world SAAS app. Everything about the course
and demo videos of what we build is on the site linked above.
