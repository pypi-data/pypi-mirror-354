from yeeducli.utility.json_utils import check_boolean, check_non_empty_string
from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter

class MetastoreWorkspaceSecretParser:
    def workspace_secret_parser(subparser):
        # Link
        link_workspace_secret = subparser.add_parser(
            'link-workspace-secret',
            help='Link a workspace secret to a Metastore Catalog.',
            formatter_class=ArgumentDefaultsHelpFormatter
        )
        link_workspace_secret.add_argument(
            "--metastore_catalog_id",
            type=int,
            nargs=1,
            required=True,
            default=SUPPRESS,
            help="ID of the metastore catalog to which the workspace secret will be linked."
        )
        link_workspace_secret.add_argument(
            "--metastore_secrets_workspace_id",
            type=int,
            nargs=1,
            required=True,
            default=SUPPRESS,
            help="ID of the workspace secret used to access the metastore service."
        )
        link_workspace_secret.add_argument(
            "--object_storage_secrets_workspace_id",
            type=int,
            nargs=1,
            required=True,
            default=SUPPRESS,
            help="ID of the workspace secret used to access the backing object storage."
        )
        link_workspace_secret.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        link_workspace_secret.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        # Update
        update_workspace_secret = subparser.add_parser(
            'update-workspace-secret',
            help='Update an existing linked workspace secret for a Metastore Catalog.',
            formatter_class=ArgumentDefaultsHelpFormatter
        )
        update_workspace_secret.add_argument(
            "--metastore_catalog_secret_workspace_id",
            type=int,
            nargs=1,
            required=True,
            default=SUPPRESS,
            help="ID of the metastore catalog whose workspace secret will be updated."
        )
        update_workspace_secret.add_argument(
            "--metastore_secrets_workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Updated workspace secret ID for the metastore service."
        )
        update_workspace_secret.add_argument(
            "--object_storage_secrets_workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Updated workspace secret ID for object storage access."
        )
        update_workspace_secret.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        update_workspace_secret.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        # List
        list_linked_workspace_secrets = subparser.add_parser(
            'list-linked-workspace-secrets',
            help='List linked workspace secrets for a Metastore Catalog.',
            formatter_class=ArgumentDefaultsHelpFormatter
        )
        list_linked_workspace_secrets.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="ID of the workspace."
        )
        list_linked_workspace_secrets.add_argument(
            "--catalog_type",
            type=check_non_empty_string,
            choices=["DATABRICKS UNITY"],
            nargs=1,
            default=SUPPRESS,
            help="Specify the type of catalog being configured."
        )
        list_linked_workspace_secrets.add_argument(
            "--metastore_catalog_secret_workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Secret mapping ID."
        )
        list_linked_workspace_secrets.add_argument(
            "--metastore_catalog_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Catalog ID."
        )
        list_linked_workspace_secrets.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=10,
            help="Limit for pagination."
        )
        list_linked_workspace_secrets.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="Page number for pagination."
        )
        list_linked_workspace_secrets.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_linked_workspace_secrets.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        # Search
        search_linked_workspace_secrets = subparser.add_parser(
            'search-linked-workspace-secrets',
            help='Search linked workspace secrets for a Metastore Catalog.',
            formatter_class=ArgumentDefaultsHelpFormatter
        )
        search_linked_workspace_secrets.add_argument(
            "--workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="ID of the workspace."
        )
        search_linked_workspace_secrets.add_argument(
            "--catalog_type",
            type=check_non_empty_string,
            choices=["DATABRICKS UNITY"],
            nargs=1,
            default=SUPPRESS,
            help="Specify the type of catalog."
        )
        search_linked_workspace_secrets.add_argument(
            "--metastore_catalog_secret_workspace_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Secret mapping ID."
        )
        search_linked_workspace_secrets.add_argument(
            "--metastore_catalog_name",
            type=check_non_empty_string,
            required=True,
            nargs=1,
            default=SUPPRESS,
            help="Catalog name to search secrets for."
        )
        search_linked_workspace_secrets.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=10,
            help="Limit for pagination."
        )
        search_linked_workspace_secrets.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="Page number for pagination."
        )
        search_linked_workspace_secrets.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        search_linked_workspace_secrets.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        # Unlink
        unlink_workspace_secret = subparser.add_parser(
            'unlink-workspace-secret',
            help='Unlink a workspace secret from a Metastore Catalog.',
            formatter_class=ArgumentDefaultsHelpFormatter
        )
        unlink_workspace_secret.add_argument(
            '--metastore_catalog_secret_workspace_id',
            type=int,
            nargs=1,
            required=True,
            default=SUPPRESS,
            help="Secret mapping ID to be unlinked."
        )
        unlink_workspace_secret.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        unlink_workspace_secret.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )
