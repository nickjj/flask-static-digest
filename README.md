# What is Flask-Static-Digest? ![CI](https://github.com/nickjj/flask-static-digest/workflows/CI/badge.svg?branch=master)

It is a Flask extension that will help make your static files production ready
with very minimal effort on your part. It does this by md5 tagging and gzipping
your static files after running a `flask digest compile` command that this
extension adds to your Flask app. It should be the last thing you do to your
static files before uploading them to your server or CDN.

Other web frameworks like Django, Ruby on Rails and Phoenix all have this
feature built into their framework, and now with this extension Flask does too.

**This extension will work if you're not using any asset build tools but at the
same time it also works with Webpack, Grunt, Gulp or any other build tool you
can think of. This tool does not depend on or compete with existing asset build
tools.**

If you're already using Webpack or a similar tool, that's great. Webpack takes
care of bundling your assets and helps convert things like SASS to CSS and ES6+
JS to browser compatible JS. That is solving a completely different problem
than what this extension solves. This extension will further optimize your
static files after your build tool produces its output files.

This extension does things that Webpack alone cannot do because in order for
things like md5 tagging to work Flask needs to be aware of how to map those
hashed file names back to regular file names you would reference in your Jinja
2 templates.

## How does it work?

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

### Demo video

This 25 minute video goes over using this extension but it also spends a lot
of time on the "why" where we cover topics like cache busting and why IMO you
might want to use this extension in all of your Flask projects.

If you prefer reading instead of video, this README file covers installing,
configuring and using this extension too.

[![Demo
Video](https://img.youtube.com/vi/-Xd84hlIjkI/0.jpg)](https://www.youtube.com/watch?v=-Xd84hlIjkI)

#### Changes since this video

- `FLASK_STATIC_DIGEST_HOST_URL` has been added to configure an optional external host, aka. CDN ([explained here](#configuring-this-extension))

## Table of Contents

- [Installation](#installation)
- [Using the newly added Flask CLI command](#using-the-newly-added-flask-cli-command)
- [Going over the Flask CLI commands](#going-over-the-flask-cli-commands)
- [Configuring this extension](#configuring-this-extension)
- [Modifying your templates to use static_url_for instead of url_for](#modifying-your-templates-to-use-static_url_for-instead-of-url_for)
- [Potentially updating your .gitignore file](#potentially-updating-your-gitignore-file)
- [FAQ](#faq)
  - [What about development vs production and performance implications?](#what-about-development-vs-production-and-performance-implications)
  - [Why bother gzipping your static files here instead of with nginx?](#why-bother-gzipping-your-static-files-here-instead-of-with-nginx)
  - [How do you use this extension with Webpack or another build tool?](#how-do-you-use-this-extension-with-webpack-or-another-build-tool)
  - [Migrating from Flask-Webpack](#migrating-from-flask-webpack)
  - [How do you use this extension with Docker?](#how-do-you-use-this-extension-with-docker)
  - [What about user uploaded files?](#what-about-user-uploaded-files)
- [About the author](#about-the-author)

## Installation

*You'll need to be running Python 3.5+ and using Flask 1.0 or greater.*

`pip install Flask-Static-Digest`

### Example directory structure for a 'hello' app

```
├── hello
│   ├── __init__.py
│   ├── app.py
│   └── static
│       └── css
│           ├── app.css
└── requirements.txt
```

### Flask app factory example using this extension

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

## Using the newly added Flask CLI command

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

## Going over the Flask CLI commands

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

### compile

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

### clean

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

## Configuring this extension

By default this extension will md5 tag all files it finds in your configured
`static_folder`. It will also create gzipped versions of each file and it won't
prefix your static files with an external host.

If you don't like any of this behavior, you can optionally configure:

```py
FLASK_STATIC_DIGEST_BLACKLIST_FILTER = []
# If you want specific extensions to not get md5 tagged you can add them to
# the list, such as: [".htm", ".html", ".txt"]. Make sure to include the ".".

FLASK_STATIC_DIGEST_GZIP_FILES = True
# When set to False then gzipped files will not be created but static files
# will still get md5 tagged.

FLASK_STATIC_DIGEST_HOST_URL = None
# When set to a value such as https://cdn.example.com and you use static_url_for
# it will prefix your static path with this URL. This would be useful if you
# host your files from a CDN. Make sure to include the protocol (aka. https://).
```

You can override these defaults in your Flask app's config file.

## Modifying your templates to use static_url_for instead of url_for

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

Or if you set `FLASK_STATIC_DIGEST_HOST_URL = "https://cdn.example.com"` it
would produce:

```html
<img src="https://cdn.example.com/images/flask-f86b271a51b3cfad5faa9299dacd987f.png"
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

## Potentially updating your .gitignore file

If you're using something like Webpack then chances are you're already git
ignoring the static files it produces as output. It's a common pattern to
commit your Webpack source static files but ignore the compiled static files
it produces.

But if you're not using Webpack or another asset build tool then the static
files that are a part of your project might have the same source and
destination directory. If that's the case, chances are you'll want to git
ignore the md5 tagged files as well as the gzipped and `cache_manifest.json`
files from version control.

For clarity, you want to ignore them because you'll be generating them on your
server at deploy time or within a Docker image if you're using Docker.  They
don't need to be tracked in version control.

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

## FAQ

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

### Why bother gzipping your static files here instead of with nginx?

You would still be using nginx's gzip features, but now instead of nginx having
to gzip your files on the fly at run time you can configure nginx to use the
pre-made gzipped files that this extension creates.

This way you can benefit from having maximum compression without having nginx
waste precious CPU cycles gzipping files on the fly. This gives you the best of
both worlds -- the highest compression ratio with no noticeable run time
performance penalty.

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

### Migrating from Flask-Webpack

[Flask-Webpack](https://github.com/nickjj/flask-webpack) is another extension I
wrote a long time ago which was specific to Webpack but had a similar idea to
this extension. Flask-Webpack is now deprecated in favor of
Flask-Static-Digest. Migrating is fairly painless. There are a number of
changes but on the bright side you get to delete more code than you add!

#### Dependency / Flask app changes

- Remove `Flask-Webpack` from `requirements.txt`
- Remove all references to Flask-Webpack from your Flask app and config
- Remove `manifest-revision-webpack-plugin` from `package.json`
- Remove all references to this webpack plugin from your webpack config
- Add `Flask-Static-Digest` to `requirements.txt`
- Add the Flask-Static-Digest extension to your Flask app

#### Jinja 2 template changes

- Replace `stylesheet_tag('main_css') | safe` with `static_url_for('static', filename='css/main.css')`
- Replace `javascript_tag('main_js') | safe` with `static_url_for('static', filename='js/main.js')`
- Replace any occurrences of `asset_url_for('foo.png')` with `static_url_for('static', filename='images/foo.png')`

### How do you use this extension with Docker?

It's really no different than without Docker, but instead of running `flask
digest compile` on your server directly at deploy time you would run it inside
of your Docker image at build time. This way your static files are already set
up and ready to go by the time you pull and use your Docker image in
production.

You can see a fully working example of this in the open source version of my
[Build a SAAS App with
Flask](https://github.com/nickjj/build-a-saas-app-with-flask) course. It
leverages Docker's build arguments to only compile the static files when
`FLASK_ENV` is set to `production`. The key files to look at are the
`Dockerfile`, `docker-compose.yml` and `.env` files. That wires up the build
arguments and env variables to make it work.

### What about user uploaded files?

Let's say that besides having static files like your logo and CSS / JavaScript
bundles you also have files uploaded by users. This could be things like a user
avatar, blog post images or anything else.

**You would still want to md5 tag and gzip these files but now we've run into a
situation**. The `flask digest compile` command is meant to be run at deploy
time and it could potentially be run from your dev box, inside of a Docker
image, on a CI server or your production server. In these cases you wouldn't
have access to the user uploaded files.

But at the same time you have users uploading files at run time. They are
changing all the time.

**Needless to say you can't use the `flask digest compile` command to digest
user uploaded files**. The `cache_manifest.json` file should be reserved for
files that exist in your code repo (such as your CSS / JS bundles, maybe a
logo, fonts, etc.).

The above files do not change at run time and align well with running the
`flask digest compile` command at deploy time.

For user uploaded content you wouldn't ever write these entries to the manifest
JSON file. Instead, you would typically upload your files to disk, S3 or
somewhere else and then save the file name of the file you uploaded into your
local database.

So now when you reference a user uploaded file (let's say an avatar), you would
loop over your users from the database and reference the file name from the DB.

There's no need for a manifest file to store the user uploaded files because
the database has a reference to the real name and then you are dynamically
referencing that in your template helper (`static_url_for`), so it's never a
hard coded thing that changes at the template level.

What's cool about this is you already did the database query to retrieve the
record(s) from the database, so there's no extra database work to do. All you
have to do is reference the file name field that's a part of your model.

But that doesn't fully solve the problem. You'll still want to md5 tag and gzip
your user uploaded content at run time and you would want to do this before you
save the uploaded file into its final destination (local file system, S3,
etc.).

This can be done completely separate from this extension and it's really going
to vary depending on where you host your user uploaded content. For example
some CDNs will automatically create gzipped files for you and they use things
like an ETag header in the response to include a unique file name (and this is
what you can store in your DB).

So maybe md5 hashing and maybe gzipping your user uploaded content becomes an
app specific responsibility, although I'm not opposed to maybe creating helper
functions you can use but that would need to be thought out carefully.

However the implementation is not bad. It's really only about 5 lines of code
to do both things. Feel free to `CTRL + F` around the [code
base](https://github.com/nickjj/flask-static-digest/blob/master/flask_static_digest/digester.py)
for `hashlib` and `gzip` and you'll find the related code.

**So with that said, here's a work flow you can do to deal with this today:**

- User uploads file
- Your Flask app potentially md5 tags / gzips the file if necessary
- Your Flask app saves the file name + gzipped file to its final destination (local file system, S3, etc.)
- Your Flask app saves the final unique file name to your database

That final unique file name would be the md5 tagged version of the file that
you created or the unique file name that your CDN returned back to you. I hope
that clears up how to deal with user uploaded files and efficiently serving
them!

## About the author

- Nick Janetakis | <https://nickjanetakis.com> | [@nickjanetakis](https://twitter.com/nickjanetakis)

If you're interested in learning Flask I have a 17+ hour video course called
[Build a SAAS App with
Flask](https://buildasaasappwithflask.com/?utm_source=github&utm_medium=staticdigest&utm_campaign=readme).
It's a course where we build a real world SAAS app. Everything about the course
and demo videos of what we build is on the site linked above.
