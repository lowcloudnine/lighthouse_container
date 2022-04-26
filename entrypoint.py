"""
Entrypoint
----------
A short script to parse the "score" from the JSON output of Google Lighthouse and
to work as the entry point for a docker container.
"""
# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------


# ---- System
import argparse
import json
import subprocess
import sys

# ----------------------------------------------------------------------------
# Functions
# ----------------------------------------------------------------------------


def display_help():
    """Provide a helpful well formatted message for users."""
    return """
Welcome to the "lighthouse container"!
The goal is to be a simple interface to automate generating tests from
Google's Lighthouse testing/scoring application.  The container prints a
single integer to stdout from a given URL and category of tests to run.
URL should be the full URL including protocol examples:
- http://google.com
- https://redhat.com
The category must be one of:
- accessibility
- best-practices
- performance
- pwa
- seo
Example usage:
CLI with output:
- $ docker run lighthouse -c accessibility -u https://redhat.com
  91
- $ docker run lighthouse --category best-practices --url https://redhat.com
  75
- $ docker run lighthouse -c accessibility -u https://redhat.com --report
In a bash script:
- SCORE=$(docker run lighthouse -c acessibility -u https://redhat.com)
"""


def lighthouse(url, category, report):
    """Use lighthouse to generate an output file."""
    # All the options for lighthouse can be found at:
    #  https://github.com/GoogleChrome/lighthouse#cli-options
    lighthouse_args = [
        url,
        # chrome flags are needed to fake out sites as headless often makes them
        # not provide the data needed
        '--chrome-flags="--headless --window-size=821,843 --no-sandbox --enable-javascript"',
        f'--only-categories "{category}"',
        '--output json',
        '--output-path /output/output.json',
        '--no-enable-error-reporting',  # this keeps Google's request for reports quiet
                                        # and avoids the associated 20 second delay
        '--quiet'  # Keeps the lighthouse output quiet comment out if you are debugging
    ]

    if report:
        lighthouse_args.append('--output html')
        lighthouse_args.append('--output-path /output/output.html')

    subprocess.run(
        " ".join(["lighthouse", *lighthouse_args]),
        shell=True, check=True,
        stdout=subprocess.PIPE
    )


def parse_score(category):
    """Entry point for the script."""
    report_json = "/output/output.json"

    with open(report_json, "r", encoding="utf-8") as report:
        output = json.load(report)
    score = int(float(output['categories'][category]['score']) * 100)

    return str(score)


def parse_args():
    """Return a namespace of the parsed arguments for the program."""
    parser = argparse.ArgumentParser(description='Run Google Lighthouse with options.')
    parser.add_argument(
        '--category', '-c',
        type=str,
        default='accessibility',
        choices=[
            "accessibility",
            "best-practices",
            "performance",
            "pwa",
            "seo"
        ],
        help="The category of 'test' to run, defaults to accessibility."
    )
    parser.add_argument(
        '--url', '-u',
        type=str,
        default='https://www.fbi.gov',
        help="A valid URL to a web site to test must start with a valid protocol " \
             "of http:// or https://"
    )
    parser.add_argument(
        '--report', '-r',
        action='store_true',
        help="Generate/Output the full HTML report to a file in addition to " \
             "printing a single value."
    )

    all_args = parser.parse_args()
    if not(all_args.url.startswith("http://")
            or all_args.url.startswith("https://")):
        print("ERROR: Please provide a valid URL.")
        print(display_help())
        sys.exit(1)

    return all_args

# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------


def main(category, url, report):
    """Run as the entrypoint and ensure the input is correct."""
    # Run Google Lighthouse for the given category and URL
    lighthouse(url, category, report)
    print(parse_score(category))  # <-- print the score to stdout


# ----------------------------------------------------------------------------
# Name
# ----------------------------------------------------------------------------


if __name__ == "__main__":
    the_args = parse_args()
    main(the_args.category, the_args.url, the_args.report)
