"""
Parquet Path Rewriter CLI
This script provides a command-line interface to rewrite parquet paths in Python source files.
"""

import argparse
import logging
import sys
from pathlib import Path

from .rewriter import rewrite_parquet_paths_in_code

logger = logging.getLogger(__name__)


def main(argv=None):
    """
    Main entry point for the CLI.
    Parses command-line arguments and rewrites parquet paths in the specified Python source file.
    If the --in-place flag is set, it overwrites the original file;
    otherwise, it prints the modified code.
    """
    parser = argparse.ArgumentParser(
        description="Rewrite parquet paths in a Python source file"
    )
    parser.add_argument("file", help="Python source file to rewrite")
    parser.add_argument(
        "--base-path", required=True, help="Base directory for rewrites"
    )
    parser.add_argument("--s3-prefix", help="S3 rewrite prefix")
    parser.add_argument(
        "-i", "--in-place", action="store_true", help="Rewrite file in place"
    )

    args = parser.parse_args(argv)

    with open(args.file, "r", encoding="utf-8") as fh:
        original_code = fh.read()

    modified_code, _, _ = rewrite_parquet_paths_in_code(
        code_string=original_code,
        base_path=Path(args.base_path),
        s3_rewrite_prefix=args.s3_prefix,
        filename=args.file,
    )

    if args.in_place:
        try:
            with open(args.file, "w", encoding="utf-8") as fh:
                fh.write(modified_code)
        except OSError as e:
            logger.error("Failed to write file '%s': %s", args.file, e)
            sys.exit(1)
    else:
        print(modified_code)


if __name__ == "__main__":
    main()
