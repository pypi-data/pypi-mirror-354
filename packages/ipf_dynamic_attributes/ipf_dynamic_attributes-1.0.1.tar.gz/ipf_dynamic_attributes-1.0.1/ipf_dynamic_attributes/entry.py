import argparse
import os
import sys

from ipf_dynamic_attributes import AttributeSync


def _check_excel(outfile: str) -> str:
    if not outfile:
        raise SyntaxError("Output file '-o|--outfile' must be specified with Excel format.")
    try:
        import xlsxwriter  # noqa: F401

        return "xlsxwriter"
    except ImportError:
        pass
    try:
        import openpyxl  # noqa: F401

        return "openpyxl"
    except ImportError:
        raise ImportError(
            "Excel format requires either 'xlsxwriter' or 'openpyxl' to be installed. "
            "Please install one of them using pip, recommended to use 'xlsxwriter'."
        )


def main():
    arg_parser = argparse.ArgumentParser(
        description="IP Fabric Dynamic Attribute.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
    This script will run the AttributeSync with the provided configuration file which defaults to 'config.yml'.
    You can specify a different configuration file by passing the filename as an argument:
    ipf_dynamic_attributes example_configs/mgmt-ip.yml
    """,
    )
    arg_parser.add_argument(
        "filename",
        nargs="?",
        default="config.yml",
        help="Configuration filename, defaults to 'config.yml'.",
    )
    arg_parser.add_argument(
        "-f",
        "--format",
        choices=["csv", "json", "excel"],
        default="csv",
        help="Output format for the report. Default is 'csv'. Use 'json' for JSON output.",
    )
    arg_parser.add_argument(
        "-o",
        "--outfile",
        type=str,
        help="Output filename to send report instead of standard out.",
    )
    args = arg_parser.parse_args()
    if not os.path.isfile(args.filename):
        raise FileNotFoundError(f"Configuration file '{args.filename}' does not exist.")

    engine = None
    if args.format == "excel":
        engine = _check_excel(args.outfile)

    sync = AttributeSync(config=args.filename)
    report = sync.run()

    outfile = args.outfile or sys.stdout
    columns = [*sync.config.inventory.df_columns, "correct", "update", "create"]
    if args.format == "json":
        report.to_json(outfile, index=False, orient="records")
    elif args.format == "csv":
        report.to_csv(outfile, index=False, columns=columns)
    else:
        report.to_excel(outfile, index=False, columns=columns, engine=engine)


if __name__ == "__main__":
    main()
