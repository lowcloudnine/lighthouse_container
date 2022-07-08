Change Log
==========

3.0.0 2022-07-08 Changes base to ubi8-minimal
---------------------------------------------
- Based on the fix in 2.2.1 to latest image and reading security reports,
  changed the base image to ubi8-minimal:latest to reduce vulnerabilities and
  reduced the container size to 1.05GB
- Added an ENV for USER and then updated the appropriate places in the
  Dockerfile
- Updated the documentation with the new version numbers and added tagging
  instructions as a latest version was added to docker hub

2.2.1 2022-07-08 Changed base to latest
---------------------------------------
- Based on a recommendation from Snyk, changed the base container image to latest

2.2.0 2022-05-03 More explicit entrypoint
-----------------------------------------
- Dockerfile has more explicit code pointing to the entrypoint with notes about
  why it was done that way
- entrypoint.py get the output directory from the environment as it's provided
  by the Dockerfile
- Verbose is now actually more verbose and provides semi-useful information
- Updated README with more examples such as using the --help flag

2.1.0 2022-05-03 Better file names for output
---------------------------------------------
- Refactored entrypoint.py to:
    - output file names with dates and times in them
    - create LighthouseTest class to easy working with tests
    - ran entrypoint through black and pylint
- Added ARG to Dockerfile for the output/workspace directory
- Updated documentation with the changes

2.0.1 2022-04-27 Add documentation
----------------------------------
- Add sphinx generated documentation
- In documentation show how to deploy to github pages

2.0.0 2022-04-19 Better Argument Handling
-----------------------------------------
- Refactor to use argparse library for argument handling

1.0.0 2022-04-12 Initial release
--------------------------------
- Initial release, container size 882MB
