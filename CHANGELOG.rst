Change Log
==========

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
