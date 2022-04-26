
⛯  A container to run Google Lighthouse tests.

Why?
----

An organization I was working for needed an automated way to run accessibility (508)
tests against a given application.  The application was going to run in an Openshift
environment.  The tool available for generating a report and associated score was
Google Lighthouse.  After some research I was able to create an image using a 
Dockerfile with the right options to do so and this repository is the result.

Tool Set
--------

The included Dockerfile will build with both Docker and podman.  I've attempted
to be as container agnostic my knowledge allows.  The created images on
`docker hub <https://hub.docker.com/repository/docker/lowcloudnine/lighthouse>`_
should run in docker, kubernetes and Openshift.

The entrypoint is a Python script.  This was chosen as it's what I know.

Usage
-----



Change Log
----------

Verion 2.0.0
~~~~~~~~~~~~

.. warning::
    This version incorporated argparse into the mix and is a breaking change from the
    API of version 1.0.0.

Version 1.0.0
~~~~~~~~~~~~~

The first working version and does the job but didn't incorporate some flags when
running Chrome in headless mode and won't work against sites that 