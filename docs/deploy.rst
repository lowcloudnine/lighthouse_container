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
