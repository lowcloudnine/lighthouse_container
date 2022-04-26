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
import os
import subprocess
import sys

# ----------------------------------------------------------------------------
# Functions
# ----------------------------------------------------------------------------


def lighthouse(url, category, report):
    """Use lighthouse to generate an output file."""
    # All the options for lighthouse can be found at:
    #  https://github.com/GoogleChrome/lighthouse#cli-options
    chrome_flags = " ".join([
        "--headless",
        "--window-size=821,843",
        "--no-sandbox",
        "--enable-javascript",
        "--ignore-certificate-errors",  # ignore https certificate issues
    ])

    lighthouse_args = [
        url,
        # chrome flags are needed to fake out sites as headless often makes them
        # not provide the data needed
        f'--chrome-flags="{chrome_flags}"',
        f'--only-categories "{category}"',
        '--no-enable-error-reporting',  # this keeps Google's request for reports quiet
                                        # and avoids the associated 20 second delay
        '--quiet'  # Keeps the lighthouse output quiet comment out if you are debugging
    ]

    if report:
        lighthouse_args.append('--output html')
        lighthouse_args.append('--output-path /output/output.html')
    else:
        lighthouse_args.append('--output json')
        lighthouse_args.append('--output-path /output/output.json')

    subprocess.run(
        " ".join(["lighthouse", *lighthouse_args]),
        shell=True, check=True,
        stdout=subprocess.PIPE
    )


def parse_score(category, report):
    """Entry point for the script."""
    report_json = "/output/output.json"

    with open(report_json, "r", encoding="utf-8") as report:
        output = json.load(report)
    score = int(float(output['categories'][category]['score']) * 100)

    # Clean up the file so if there's a volume mount, there's no clutter
    os.remove("/output/output.json")

    return str(score)


def parse_args():
    """Return a namespace of the parsed arguments for the program."""
    parser = argparse.ArgumentParser(
        prog="docker run [various docker options] lighthouse",
        description='Run Google Lighthouse inside a docker container with some options.'
    )
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
        help="The category/type of test to run, defaults to accessibility."
    )
    parser.add_argument(
        '--url', '-u',
        type=str,
        default='https://python.org',
        help="A valid URL to a web site to test must start with a valid protocol " \
             "of http:// or https://.  Defaults to https://www.python.org"
    )
    parser.add_argument(
        '--report', '-r',
        action='store_true',
        help="Generate/Output the full HTML report to a file.  If this flag/option " \
             "is set only the html file will be generated in the directory mounted " \
             "with the docker volume flag, i.e. -v /home/user/reports:/output " \
             "as output.html.  If the flag is not given a single number, the " \
             "result of the given test which is between 0 and 100 will be piped " \
             "to stdout."
    )

    all_args = parser.parse_args()
    if not(all_args.url.startswith("http://")
            or all_args.url.startswith("https://")):
        print("ERROR: Provide a valid URL, it must start with: http:// or https://")
        sys.exit(1)

    return all_args

# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------


def main(category, url, report):
    """Run as the entrypoint and ensure the input is correct."""
    # Run Google Lighthouse for the given category and URL
    lighthouse(url, category, report)
    if report:
        print("The results are in: ./output.html")
    else:
        print(parse_score(category, report))  # <-- print the score to stdout

# ----------------------------------------------------------------------------
# Name
# ----------------------------------------------------------------------------


if __name__ == "__main__":
    the_args = parse_args()
    main(the_args.category, the_args.url, the_args.report)
