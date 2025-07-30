from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter, ArgumentParser
from yeeducli.utility.json_utils import check_boolean, check_non_empty_string, validate_string_and_null
from yeeducli.utility.logger_utils import Logger

logger = Logger.get_logger(__name__, True)

class HiveCatalogParser:
    def hive_catalog_parser(subparser):
        databricks_subparsers = subparser.add_subparsers(dest="action", required=True)
        
        # create
        create_parser = databricks_subparsers.add_parser(
            "create",
            help="Create a new Hive metastore catalog",
            formatter_class=ArgumentDefaultsHelpFormatter
        )
        create_parser.add_argument("--name", type=check_non_empty_string, nargs=1, default=SUPPRESS, required=True, help="Specify the name of the Hive metastore catalog.")
        create_parser.add_argument("--description", type=check_non_empty_string, nargs=1, default=SUPPRESS, help="Specify the description of the hive metastore catalog.")
        create_parser.add_argument("--hive_site_xml_file_path", type=check_non_empty_string, nargs=1, required=False, default=SUPPRESS, help="Specify the HIVE-SITE.xml.")
        create_parser.add_argument("--core_site_xml_file_path", type=check_non_empty_string, nargs=1, required=False, default=SUPPRESS, help="Specify the CORE-SITE.xml")
        create_parser.add_argument("--hdfs_site_xml_file_path", type=check_non_empty_string, nargs=1, required=False, default=SUPPRESS, help="Specify the HDFS-SITE.xml")
        create_parser.add_argument("--krb5_conf_file_path", type=check_non_empty_string, nargs=1, required=False, default=SUPPRESS, help="Specify the krb5_conf_file_path")
        create_parser.add_argument("--json-output", type=check_non_empty_string, nargs='?', choices=['pretty', 'default'], default='pretty', help="Specifies the format of JSON output.")
        create_parser.add_argument("--yaml-output", type=check_boolean, nargs='?', choices=['true', 'false'], default='false', help="Displays the information in YAML format if set to 'true'.")
        
        # edit
        edit_parser = databricks_subparsers.add_parser(
            "edit",
            help="Edit an existing Hive metastore catalog",
            formatter_class=ArgumentDefaultsHelpFormatter
        )
        edit_parser.add_argument("--metastore_catalog_id", type=int, required=True, default=SUPPRESS, help="ID of the catalog to edit")
        edit_parser.add_argument("--name", type=check_non_empty_string, nargs=1, default=SUPPRESS, required=False, help="Specify the name of the Hive metastore catalog.")
        edit_parser.add_argument("--description", type=validate_string_and_null, nargs=1, default=SUPPRESS, help="Specify the description of the hive metastore catalog.")
        edit_parser.add_argument("--hive_site_xml_file_path", type=check_non_empty_string, nargs=1, required=False, default=SUPPRESS, help="Specify the HIVE-SITE.xml.")
        edit_parser.add_argument("--core_site_xml_file_path", type=check_non_empty_string, nargs=1, required=False, default=SUPPRESS, help="Specify the CORE-SITE.xml")
        edit_parser.add_argument("--hdfs_site_xml_file_path", type=check_non_empty_string, nargs=1, required=False, default=SUPPRESS, help="Specify the HDFS-SITE.xml")
        edit_parser.add_argument("--krb5_conf_file_path", type=check_non_empty_string, nargs=1, required=False, default=SUPPRESS, help="Specify the krb5_conf_file_path")
        edit_parser.add_argument("--json-output", type=check_non_empty_string, nargs='?', choices=['pretty', 'default'], default='pretty', help="Specifies the format of JSON output.")
        edit_parser.add_argument("--yaml-output", type=check_boolean, nargs='?', choices=['true', 'false'], default='false', help="Displays the information in YAML format if set to 'true'.")

        # delete
        delete_parser = databricks_subparsers.add_parser(
            "delete",
            help="Delete a hive metastore catalog",
            formatter_class=ArgumentDefaultsHelpFormatter
        )
        delete_parser.add_argument(
            "--metastore_catalog_id",
            type=int,
            nargs=1,
            required=True,
            default=SUPPRESS,
            help="ID of the Hive metastore catalog to delete"
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
    
