
⛯  A container to run Google Lighthouse tests.

.. code-block::

    $ docker run --rm \
         lowcloudnine/lighthouse:2.0.0 \
         --category best-practices \
         --url https://www.python.org
    83
    $ docker run --rm \
         -v /home/wodan:/output \
         lowcloudnine/lighthouse:2.0.0 \
         -c accessibility \
         -u https://www.python.org \
         --report
    The results are in: ./output.html

Please see the full `documentation <https://lowcloudnine.github.io/lighthouse_container/>`_.

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
