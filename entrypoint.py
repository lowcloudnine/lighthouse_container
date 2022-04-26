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
import json
import subprocess
import sys

# ----------------------------------------------------------------------------
# Functions
# ----------------------------------------------------------------------------


def display_help():
    """Provide a helpful well formatted message for users."""
    the_help = """
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
- $ docker run lighthouse accessibility https://redhat.com
  91
- $ docker run lighthouse best-practices https://redhat.com
  75
In a bash script:
- SCORE=$(docker run lighthouse acessibility https://redhat.com)
"""
    print(the_help)


def lighthouse(url, category, report_type="json"):
    """Use lighthouse to generate an output file."""
    report_file = f"/output/output.{report_type}"

    # All the options for lighthouse can be found at:
    #  https://github.com/GoogleChrome/lighthouse#cli-options
    lighthouse_args = [
        url,
        # chrome flags are needed to fake out sites as headless often makes them
        # not provide the data needed
        '--chrome-flags="--headless --window-size=821,843 --no-sandbox --enable-javascript"',
        f'--only-categories "{category}"',
        '--output json',
        f'--output-path {report_file}',
        '--no-enable-error-reporting',  # this keeps Google's request for reports quiet
                                        # and avoids the associated 20 second delay
        '--quiet'  # Keeps the lighthouse output quiet comment out if you are debugging
    ]

    lhouse = subprocess.run(
        " ".join(["lighthouse", *lighthouse_args]),
        shell=True, check=True,
        stdout=subprocess.PIPE
    )


def parse_score(category, report_type="json"):
    """Entry point for the script."""
    report_file = f"/output/output.{report_type}"

    with open(report_file, "r") as report:
        output = json.load(report)
    score = int(float(output['categories'][category]['score']) * 100)

    return str(score)

# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------


def main(category, url):
    """Run as the entrypoint and ensure the input is correct."""
    help_opts = ["help", "--help", "-h", "h"]
    if category in help_opts \
        or url in help_opts:
        display_help()
        sys.exit(0)

    valid_categories = [
        "accessibility",
        "best-practices",
        "performance",
        "pwa",
        "seo"
    ]
    if category not in valid_categories:
        print(f'ERROR:  Category "{category}" is not valid.')
        display_help()
        sys.exit(1)

    if url == "":
        print("ERROR:  Please provide a URL to run against.")
        display_help()
        sys.exit(2)

    if not( url.startswith("http://") or url.startswith("https://")):
        print(f"ERROR:  {url} does not start with a valid protocol.")
        display_help()
        sys.exit(3)

    # Run Google Lighthouse for the given category and URL
    lighthouse(url, category)
    print(parse_score(category))  # <-- print the score to stdout

# ----------------------------------------------------------------------------
# Name
# ----------------------------------------------------------------------------


if __name__ == "__main__":
    category = sys.argv[1]
    try:
        url = sys.argv[2]
    except IndexError:
        url = ""

    main(category, url)
