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
import datetime
import json
import os
import subprocess
import sys


# ----------------------------------------------------------------------------
# Class: LighthouseTest
# ----------------------------------------------------------------------------


class LighthouseTest:
    """A lighthouse test as an object.

     The class/object will include all the associated datastructures and
     functionality.

     """

    def __init__(
            self,
            url: str,
            category: str,
            report_type: str = "json",
            bucket: str = "",
            access_id: str = "",
            access_key: str = ""
    ) -> None:
        """Create a lighthouse test object to manipulate to provide test output."""
        self.category = category
        self.url = url
        self.report_type = report_type
        self.bucket = bucket
        self.access_id = access_id
        self.access_key = access_key

        dtg = datetime.datetime.now().strftime("%Y%m%d_%H%M")
        self.output_path = \
            f"/output/lighthouse_{self.category}_{dtg}.{report_type}"

    def generate_report(self, report_type) -> str:
        """Use lighthouse to generate an output file."""
        chrome_flags = " ".join([
            "--headless",
            "--window-size=821,843",
            "--no-sandbox",
            "--enable-javascript",
            "--ignore-certificate-errors",  # ignore https certificate issues
        ])

        # All the options for lighthouse can be found at:
        #  https://github.com/GoogleChrome/lighthouse#cli-options
        lighthouse_args = [
            self.url,
            f'--chrome-flags="{chrome_flags}"',
            f'--only-categories "{self.category}"',
            '--no-enable-error-reporting',
            '--quiet', f'--output {report_type}',
            f'--output-path {self.output_path}'
        ]

        subprocess.run(
            " ".join(["lighthouse", *lighthouse_args]),
            shell=True, check=True,
            stdout=subprocess.PIPE
        )

        return self.output_path

    def parse_score(self):
        """Entry point for the script."""
        report_path = self.generate_report(report_type="json")
        with open(report_path, "r", encoding="utf-8") as report:
            output = json.load(report)
        score = int(float(output['categories'][self.category]['score']) * 100)

        # Clean up the file so if there's a volume mount, there's no clutter
        if self.report_type == "html":
            os.remove(report_path)

        return str(score)


# ----------------------------------------------------------------------------
# Functions
# ----------------------------------------------------------------------------


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
        default='https://www.python.org',
        help="A valid URL to a web site to test must start with a valid protocol "
             "of http:// or https://.  Defaults to https://www.python.org"
    )
    parser.add_argument(
        '--report', '-r',
        action='store_true',
        help="Generate/Output the full HTML report to a file.  If this flag/option "
             "is set only the html file will be generated in the directory mounted "
             "with the docker volume flag, i.e. -v /home/user/reports:/output "
             "as output.html.  If the flag is not given a single number, the "
             "result of the given test which is between 0 and 100 will be piped "
             "to stdout."
    )
    parser.add_argument(
        '--bucket', '-b',
        type=str,
        default="",
        help="The bucket name to put the lighthouse report into, with full "
             "path to the object, i.e. my_awesomebucket/lh_tests/seo/"
    )
    parser.add_argument(
        '--access_id', '-i',
        type=str,
        default="",
        help="An access key from a "
    )
    parser.add_argument(
        '--debug', '-d',
        action='store_true',
        help="Enable output of more information from the container.  Should only"
             " be used by developers and related IT personnel."
    )

    all_args = parser.parse_args()
    if not (all_args.url.startswith("http://")
            or all_args.url.startswith("https://")):
        print("ERROR: Provide a valid URL, it must start with: http:// or https://")
        sys.exit(1)

    return all_args


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------


def main(
        category: str,
        url: str,
        report: bool
):
    """Run as the entrypoint and ensure the input is correct."""
    # Run Google Lighthouse for the given category and URL
    if report:
        report_type = "html"
    else:
        report_type = "json"

    lh_test = LighthouseTest(url, category, report_type)

    if report:
        print(f"The results are at: {lh_test.generate_report(report_type)}")
    else:
        print(lh_test.parse_score())  # <-- print the score to stdout


# ----------------------------------------------------------------------------
# Name
# ----------------------------------------------------------------------------


if __name__ == "__main__":
    the_args = parse_args()

    if the_args.debug:
        print(f"Category: {the_args.category}")
        print(f"URL: {the_args.url}")
        print(f"Report: {the_args.report}")

    main(the_args.category, the_args.url, the_args.report)