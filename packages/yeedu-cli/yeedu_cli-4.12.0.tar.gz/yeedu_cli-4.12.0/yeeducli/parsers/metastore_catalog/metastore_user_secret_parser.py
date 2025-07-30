from yeeducli.utility.json_utils import check_boolean, check_non_empty_string, validate_integer_and_null
from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter

class MetastoreUserSecretParser:
    def user_secret_parser(subparser):
        link_user_secret = subparser.add_parser(
            'link-user-secret',
            help='Link a user secret to a Metastore Catalog.',
            formatter_class=ArgumentDefaultsHelpFormatter
        )
        link_user_secret.add_argument(
            "--metastore_catalog_id",
            type=int,
            nargs=1,
            required=True,
            default=SUPPRESS,
            help="ID of the metastore catalog to which the user secret will be linked."
        )
        link_user_secret.add_argument(
            "--metastore_secrets_user_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="ID of the user secret used to access the metastore service (e.g., Unity/Hive)."
        )
        link_user_secret.add_argument(
            "--object_storage_secrets_user_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="ID of the user secret used to access the backing object storage."
        )
        link_user_secret.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        link_user_secret.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        update_user_secret = subparser.add_parser(
            'update-user-secret',
            help='Update an existing linked user secret for a Metastore Catalog.',
            formatter_class=ArgumentDefaultsHelpFormatter
        )
        update_user_secret.add_argument(
            "--metastore_catalog_secret_user_id",
            type=int,
            nargs=1,
            required=True,
            default=SUPPRESS,
            help="ID of the metastore catalog for which the user secret link should be updated."
        )
        update_user_secret.add_argument(
            "--metastore_secrets_user_id",
            type=validate_integer_and_null,
            nargs=1,
            default=SUPPRESS,
            help="Updated user secret ID used to access the metastore service."
        )
        update_user_secret.add_argument(
            "--object_storage_secrets_user_id",
            type=validate_integer_and_null,
            nargs=1,
            default=SUPPRESS,
            help="Updated user secret ID used to access the object storage."
        )
        update_user_secret.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        update_user_secret.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        list_linked_user_secrets = subparser.add_parser(
            'list-linked-user-secrets',
            help='List all linked user secrets for a Metastore Catalog.',
            formatter_class=ArgumentDefaultsHelpFormatter
        )
        list_linked_user_secrets.add_argument(
            "--user_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="User ID associated with the linked secrets."
        )
        list_linked_user_secrets.add_argument(
            "--catalog_type",
            type=check_non_empty_string,
            choices=["DATABRICKS UNITY"],
            nargs=1,
            default=SUPPRESS,
            help="Specify the type of catalog being configured."
        )
        list_linked_user_secrets.add_argument(
            "--metastore_catalog_secret_user_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Metastore catalog secret user ID."
        )
        list_linked_user_secrets.add_argument(
            "--metastore_catalog_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="ID of the metastore catalog."
        )
        list_linked_user_secrets.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=10,
            help="Limit number of results."
        )
        list_linked_user_secrets.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="Page number for pagination."
        )
        list_linked_user_secrets.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_linked_user_secrets.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        search_linked_user_secrets = subparser.add_parser(
            'search-linked-user-secrets',
            help='Search linked user secrets for a Metastore Catalog.',
            formatter_class=ArgumentDefaultsHelpFormatter
        )
        search_linked_user_secrets.add_argument(
            "--user_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="User ID associated with the search."
        )
        search_linked_user_secrets.add_argument(
            "--catalog_type",
            type=check_non_empty_string,
            choices=["DATABRICKS UNITY"],
            nargs=1,
            default=SUPPRESS,
            help="Specify the type of catalog being configured."
        )
        search_linked_user_secrets.add_argument(
            "--metastore_catalog_secret_user_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Metastore catalog secret user ID."
        )
        search_linked_user_secrets.add_argument(
            "--metastore_catalog_name",
            type=check_non_empty_string,
            required=True,
            nargs=1,
            default=SUPPRESS,
            help="Name of the metastore catalog."
        )
        search_linked_user_secrets.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=10,
            help="Limit number of results."
        )
        search_linked_user_secrets.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="Page number for pagination."
        )
        search_linked_user_secrets.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        search_linked_user_secrets.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        unlink_user_secret = subparser.add_parser(
            'unlink-user-secret',
            help='Unlink a user secret from a Metastore Catalog.',
            formatter_class=ArgumentDefaultsHelpFormatter
        )
        unlink_user_secret.add_argument(
            '--metastore_catalog_secret_user_id',
            type=int,
            nargs=1,
            required=True,
            default=SUPPRESS,
            help="ID of the user secret to be unlinked from the metastore catalog."
        )
        unlink_user_secret.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        unlink_user_secret.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )