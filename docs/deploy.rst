Deploy
======

A cheatsheet for deploying this project.

Documentation
-------------

To deploy the sphinx documentation to GitHub Pages a python program
`ghp-import <https://github.com/c-w/ghp-import>`_ is used.

To deploy the docs:

.. code-block::

    $ cd /path/to/project/docs
    $ make html
    $ ghp-import -n -p ./_build/html

The `-n` option in the `ghp-import` command above is the no-jekyll flag and is required for the
sphinx docs to display correctly.

If you didn't run `pip install -r requirements.txt` in your Python environment you can run
`pip install ghp-import` to install ghp-import.

Docker Hub
----------

Tags in the project will match the pattern:  docker.io/lowcloudnine/lighthouse:x.y.z were x.y.z is
the semanic version number of the image release and ideally there should be a tag in the git repo
with the same version number.

An example deployment would look like:

.. code-block::

    $ cd /path/to/project
    $ docker build -t docker.io/lowcloudnine/lighthouse:2.0.1 .
    $ docker login
    $ docker push docker.io/lowcloudnine/lighthouse:2.0.1
