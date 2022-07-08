
⛯  A container to run Google Lighthouse tests.

Usage
------

Basic Usage
~~~~~~~~~~~

.. code-block::

    $ docker run --rm \
         docker.io/lowcloudnine/lighthouse:3.0.0 \
         --category best-practices \
         --url https://www.python.org
    83
    $ docker run --rm \
         -v /home/wodan:/workspace \
         docker.io/lowcloudnine/lighthouse:3.0.0 \
         -c accessibility \
         -u https://www.python.org \
         --report
    lighthouse_accessibility_20220708_2302.html

Getting Help
~~~~~~~~~~~~

The container can be run with help flags (--help or -h) and outputs help in a
format familiar to linux shell users.

.. code-block::

    $ docker run --rm \
        docker.io/lowcloudnine/lighthouse:3.0.0 \
        --help
    usage: docker run [various docker options] lighthouse [-h]
                                                          [--category {accessibility,best-practices,performance,pwa,seo}]
                                                          [--url URL] [--report]
                                                          [--verbose]

    Run Google Lighthouse inside a docker container with some options.

    optional arguments:
      -h, --help            show this help message and exit
      --category {accessibility,best-practices,performance,pwa,seo}, -c {accessibility,best-practices,performance,pwa,seo}
                            The category/type of test to run, defaults to
                            accessibility.
      --url URL, -u URL     A valid URL to a web site to test must start with a
                            valid protocol of http:// or https://. Defaults to
                            https://www.python.org
      --report, -r          Generate/workspace the full HTML report to a file. If
                            this flag/option is set only the html file will be
                            generated in the directory mounted with the docker
                            volume flag, i.e. -v /home/user/reports:/workspace as
                            output.html. If the flag is not given a single number,
                            the result of the given test which is between 0 and
                            100 will be piped to stdout.
      --verbose, -v         Generate more verbose output.

Verbose
~~~~~~~

If you are working on improving the image/container or you just want to see more
output the verbose flag might be helpful.

.. code-block::

    $ # for the score output
    $ docker run --rm \
        docker.io/lowcloudnine/lighthouse:3.0.0 --verbose
    ----------------------------------------
    All arguments given: Namespace(category='accessibility', report=False, url='https://www.python.org', verbose=True)

    Category: accessibility
    URL: https://www.python.org
    Report: False
    Verbose: True

    Score:
    78
    ----------------------------------------
    $ # ... or for the report output
    $ docker run --rm \
        docker.io/lowcloudnine/lighthouse:3.0.0 --verbose --report
    ----------------------------------------
    All arguments given: Namespace(category='accessibility', report=True, url='https://www.python.org', verbose=True)

    Category: accessibility
    URL: https://www.python.org
    Report: True
    Verbose: True

    Output file:
    lighthouse_accessibility_20220708_2302.html
    ----------------------------------------

Please see the full `documentation <https://lowcloudnine.github.io/lighthouse_container/>`_
and/or visit the `GitHub repository <https://github.com/lowcloudnine/lighthouse_container>`_.

Overview
--------

An OCI compliant image available on
`docker hub <https://hub.docker.com/repository/docker/lowcloudnine/lighthouse>`_ to run
Google Lighthouse tests against a given URL.  It can be used to generate a single score or output
the HTML file.  The goal is to provide a tool that can be used in CI/CD pipelines to ensure any
front-end product achieves a given level and doesn't regress.

Acknowledgements
----------------

Thank you to `Raoul du Plessis <https://unsplash.com/@raouldp>`_ for open sourcing the image of the
lighthouse used on this site.  The fav-icon for the site is provided by
`flaticon <https://www.flaticon.com/free-icons/lighthouse>`_.
