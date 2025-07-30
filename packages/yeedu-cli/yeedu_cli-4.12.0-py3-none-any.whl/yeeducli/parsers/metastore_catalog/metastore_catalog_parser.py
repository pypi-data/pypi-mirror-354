from argparse import SUPPRESS
from yeeducli.utility.json_utils import check_boolean, check_non_empty_string
from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter, ArgumentParser
from yeeducli.utility.logger_utils import Logger

from yeeducli.parsers.metastore_catalog.unity_catalog_parser import UnityCatalogParser
from yeeducli.parsers.metastore_catalog.hive_catalog_parser import HiveCatalogParser


import sys

logger = Logger.get_logger(__name__, True)

class MetastoreCatalogParser:
    def metastore_catalog_parser(subparser):
        #hive
        hive_parser = subparser.add_parser(
          'hive',
          help='For hive catalog',
          formatter_class=ArgumentDefaultsHelpFormatter
        )
        HiveCatalogParser.hive_catalog_parser(hive_parser)

        # databricks-unity
        unity_parser = subparser.add_parser(
          'databricks-unity',
          help='For Databricks Unity catalog',
          formatter_class=ArgumentDefaultsHelpFormatter
        )
        UnityCatalogParser.unity_catalog_parser(unity_parser)
        
        #list
        list_parser = subparser.add_parser(
            "list",
            help="List metastore catalogs",
            formatter_class=ArgumentDefaultsHelpFormatter
        )
        list_parser.add_argument(
            "--catalog_type",
            type=check_non_empty_string,
            choices=["DATABRICKS UNITY", "HIVE"],
            default=SUPPRESS,
            nargs=1,
            help="Filter results by catalog type"
        )
        list_parser.add_argument(
            "--metastore_catalog_id",
            type=int,
            default=SUPPRESS,
            nargs=1,
            help="Filter by specific metastore catalog ID"
        )
        list_parser.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Number of records to return"
        )
        list_parser.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="Page number for pagination"
        )
        list_parser.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_parser.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the output in YAML format if set to true."
        )

        # search
        search_parser = subparser.add_parser(
            "search",
            help="Search for metastore catalogs",
            formatter_class=ArgumentDefaultsHelpFormatter
        )
        search_parser.add_argument(
            "--metastore_catalog_name",
            type=check_non_empty_string,
            required=True,
            default=SUPPRESS,
            nargs=1,
            help="Filter by catalog name"
        )
        search_parser.add_argument(
            "--catalog_type",
            type=check_non_empty_string,
            choices=["DATABRICKS UNITY", "HIVE"],
            default=SUPPRESS,
            nargs=1,
            help="Filter results by catalog type"
        )
        search_parser.add_argument(
            "--limit",
            type=int,
            default=100,
            nargs=1,
            help="Number of records to return"
        )
        search_parser.add_argument(
            "--page_number",
            type=int,
            default=1,
            nargs=1,
            help="Page number for pagination"
        )
        search_parser.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        search_parser.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the output in YAML format if set to true."
        )

