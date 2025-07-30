# django-spinproject

Opinionated version of `django-admin startproject` that intends to go further and do things that startproject can't do but most people will do anyway. Here's what you can get:

* ⚛️ **Whitenoise**: for serving static files in production (usually you don't want to set up a separate server for this).
* 🔧 **settings.py**: slightly modified to also understand environment variables and `.env` files. This functionality requires the `django-environ` package. Also, app logger is mostly pre-configured for you.
* 🔑 **Minimal login/logout pages** so you can set this up without reading the guide again.
* 🔒 **Support for marking PostgreSQL databases as read-only** to prevent accidental modification of critical data.
* 🧰 `script/bootstrap` and other [scripts to rule them all](https://github.blog/2015-06-30-scripts-to-rule-them-all/) so your fellow developers and maintainers don't ask you how to run this thing. Current versions of these scripts optimized for use with [uv](https://docs.astral.sh/uv), but you can easily adapt them for any Python package manager.
* 🏗️ **Dockerfile and .dockerignore**: one day your app will go to production, and we've got you covered.
* 🏛️ **Gitlab CI config**.
* ⚕️ **Pre-configured linter** so you can find some common problems automagically.
* 🏃 **Pre-configured pytest** because you are going to need unit tests one day.
* 🗃️ **Auto-checks if you forgot to create migrations** whenever you run tests or CI.
* *️⃣ **.gitignore**: well, you know why.

## Requirements

* \*nix system;
* `django-admin` installed and available from `$PATH`.

Generated files will work fine in Django >= 2.0, not tested in earlier versions.

## How to use

* Install the package: `pip install django-spinproject`
* Create a new project: `django-spinproject --create <path>`
* OR initialize spinproject in your existing project's folder: `django-spinproject --init`

You're all set. Now you can take a look at the list of available modules: `django-spinproject --help`

Use `django-spinproject --enable` to enable a module, `django-spinproject --upgrade` to apply changes.

## CLI commands

* `--create PATH`: create django project in specified path
* `--init`: create spinproject.json file
* `--enable MODULE_TO_ENABLE`: enable specified module; use 'all' to enable most common modules; use 'ALL' to enable all available modules;
* `--disable MODULE_TO_DISABLE`: disable specified module
* `--upgrade [MODULE_TO_UPGRADE]`: upgrade (specified or all) enabled modules

## Available modules

* `gitignore` — Creates `.gitignore` file suitable for most Django projects.
* `srta` — Creates [Scripts to Rule Them All](https://github.blog/2015-06-30-scripts-to-rule-them-all/) (simplifies life a lot, you should check it out).
* `pytest` — Creates `pytest.ini` and `.coveragerc` files.
* `dockerfile` — Creates a Dockerfile.
* `dockerignore` — Creates `.dockerignore` (you should totally do that).
* `docker-scripts` — Creates additional SRTA scripts for building and pushing your Docker image.
* `gitlab-ci` — Creates GitLab CI config, `.gitlab-ci.yml`.
* `pg-readonly` — Creates a DatabaseWrapper class for readonly connection to PostgreSQL.
* `settings` — Improves the default `settings.py`, adding support for envvars and `.env` files. Also enables Whitenoise and CLI logger.
* `login-template` — Creates minimal login/logout pages.

## Planned features

(for requests, create an issue or drop me a line at m1kc@yandex.ru)

## Changelog

See the [Releases](https://github.com/m1kc/django-spinproject/releases) page.
