from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter, ArgumentParser
from yeeducli.utility.json_utils import check_boolean, check_non_empty_string, validate_string_and_null
from yeeducli.utility.logger_utils import Logger
import sys

logger = Logger.get_logger(__name__, True)



class UnityCatalogParser:
    def unity_catalog_parser(subparser):
        databricks_subparsers = subparser.add_subparsers(dest="action", required=True)
        
        # create
        create_parser = databricks_subparsers.add_parser(
            "create",
            help="Create a new Databricks unity metastore catalog",
            formatter_class=ArgumentDefaultsHelpFormatter
        )
        create_parser.add_argument("--name", type=check_non_empty_string, nargs=1, required=True, default=SUPPRESS, help="Specify the name of the databricks unity metastore catalog.")
        create_parser.add_argument("--description", type=check_non_empty_string, nargs=1, default=SUPPRESS, help="Specify the description of the databricks unity metastore catalog.")
        create_parser.add_argument("--endpoint", type=check_non_empty_string, nargs=1, required=True, default=SUPPRESS, help="Specify the Databricks endpoint URL.")
        create_parser.add_argument("--default_catalog", type=check_non_empty_string, nargs=1, required=True, default=SUPPRESS, help="Specify the default catalog name.")
        create_parser.add_argument("--storage_path", type=check_non_empty_string, nargs=1, required=True, default=SUPPRESS, help="Specify the storage path (e.g., S3 or ADLS).")
        create_parser.add_argument("--json-output", type=check_non_empty_string, nargs='?', choices=['pretty', 'default'], default='pretty', help="Specifies the format of JSON output.")
        create_parser.add_argument("--yaml-output", type=check_boolean, nargs='?', choices=['true', 'false'], default='false', help="Displays the information in YAML format if set to 'true'.")

        # edit
        edit_parser = databricks_subparsers.add_parser(
            "edit",
            help="Edit an existing databricks unity metastore catalog",
            formatter_class=ArgumentDefaultsHelpFormatter
        )
        edit_parser.add_argument("--metastore_catalog_id", type=int, required=True, default=SUPPRESS, help="ID of the catalog to edit")
        edit_parser.add_argument("--name", type=check_non_empty_string, nargs=1, default=SUPPRESS, help="Specify the name of the databricks unity metastore catalog.")
        edit_parser.add_argument("--description", type=validate_string_and_null, nargs=1, default=SUPPRESS, help="Specify the description of the databricks unity metastore catalog.")
        edit_parser.add_argument("--endpoint", type=check_non_empty_string, nargs=1, default=SUPPRESS, help="Specify the Databricks endpoint URL.")
        edit_parser.add_argument("--default_catalog", type=check_non_empty_string, nargs=1, default=SUPPRESS, help="Specify the default catalog name.")
        edit_parser.add_argument("--storage_path", type=check_non_empty_string, nargs=1, default=SUPPRESS, help="Specify the storage path (e.g., S3 or ADLS).")
        edit_parser.add_argument("--json-output", type=check_non_empty_string, nargs='?', choices=['pretty', 'default'], default='pretty', help="Specifies the format of JSON output.")
        edit_parser.add_argument("--yaml-output", type=check_boolean, nargs='?', choices=['true', 'false'], default='false', help="Displays the information in YAML format if set to 'true'.")

        # delete
        delete_parser = databricks_subparsers.add_parser(
            "delete",
            help="Delete a databricks unity metastore catalog",
            formatter_class=ArgumentDefaultsHelpFormatter
        )
        delete_parser.add_argument(
            "--metastore_catalog_id",
            type=int,
            nargs=1,
            required=True,
            default=SUPPRESS,
            help="ID of the databricks unity metastore catalog to delete"
        )
        delete_parser.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        delete_parser.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the output in YAML format if set to true."
        )
    
