from yeeducli.utility.json_utils import check_boolean, check_non_empty_string, validate_integer_and_null
from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter

class MetastoreTenantSecretParser:
    def tenant_secret_parser(subparser):
        link_tenant_secret = subparser.add_parser(
            'link-tenant-secret',
            help='Link a tenant secret to a Metastore Catalog.',
            formatter_class=ArgumentDefaultsHelpFormatter
        )
        link_tenant_secret.add_argument(
            "--metastore_catalog_id",
            type=int,
            required=True,
            default=SUPPRESS,
            nargs=1,
            help="ID of the metastore catalog to which the tenant secret will be linked."
        )
        link_tenant_secret.add_argument(
            "--metastore_secrets_tenant_id",
            type=validate_integer_and_null,
            nargs=1,
            default=SUPPRESS,
            help="ID of the tenant secret used to access the metastore service (e.g., Unity/Hive)."
        )
        link_tenant_secret.add_argument(
            "--object_storage_secrets_tenant_id",
            type=validate_integer_and_null,
            nargs=1,
            default=SUPPRESS,
            help="ID of the tenant secret used to access the backing object storage."
        )
        link_tenant_secret.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        link_tenant_secret.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        update_tenant_secret = subparser.add_parser(
            'update-tenant-secret',
            help='Update an existing linked tenant secret for a Metastore Catalog.',
            formatter_class=ArgumentDefaultsHelpFormatter
        )
        update_tenant_secret.add_argument(
            "--metastore_catalog_secret_tenant_id",
            type=int,
            nargs=1,
            required=True,
            default=SUPPRESS,
            help="ID of the metastore catalog for which the tenant secret link should be updated."
        )
        update_tenant_secret.add_argument(
            "--metastore_secrets_tenant_id",
            nargs=1,
            type=validate_integer_and_null,
            default=SUPPRESS,
            help="Updated tenant secret ID used to access the metastore service."
        )
        update_tenant_secret.add_argument(
            "--object_storage_secrets_tenant_id",
            type=validate_integer_and_null,
            nargs=1,
            default=SUPPRESS,
            help="Updated tenant secret ID used to access the object storage."
        )
        update_tenant_secret.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        update_tenant_secret.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        list_linked_tenant_secrets = subparser.add_parser(
            'list-linked-tenant-secrets',
            help='List all linked tenant secrets for a Metastore Catalog.',
            formatter_class=ArgumentDefaultsHelpFormatter
        )
        list_linked_tenant_secrets.add_argument(
            "--metastore_catalog_secret_tenant_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="ID of the metastore catalog for which the tenant secrets should be listed."
        )
        list_linked_tenant_secrets.add_argument(
            "--catalog_type",
            type=check_non_empty_string,
            choices=["DATABRICKS UNITY"],
            nargs=1,
            default=SUPPRESS,
            help="Specify the type of catalog being configured."
        )
        list_linked_tenant_secrets.add_argument(
            "--metastore_catalog_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="ID of the metastore catalog for which the tenant secrets should be listed."
        )
        list_linked_tenant_secrets.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=10,
            help="Provide limit to list number of tenant secrets."
        )
        list_linked_tenant_secrets.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="Page number for pagination."
        )
        list_linked_tenant_secrets.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_linked_tenant_secrets.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        search_linked_tenant_secrets = subparser.add_parser(
            'search-linked-tenant-secrets',
            help='Search for linked tenant secrets for a Metastore Catalog.',
            formatter_class=ArgumentDefaultsHelpFormatter
        )
        search_linked_tenant_secrets.add_argument(
            "--metastore_catalog_secret_tenant_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="ID of the metastore catalog for which the tenant secrets should be searched."
        )
        search_linked_tenant_secrets.add_argument(
            "--catalog_type",
            type=check_non_empty_string,
            choices=["DATABRICKS UNITY"],
            nargs=1,
            default=SUPPRESS,
            help="Specify the type of catalog being configured."
        )
        search_linked_tenant_secrets.add_argument(
            "--metastore_catalog_name",
            type=check_non_empty_string,
            nargs=1,
            required=True,
            default=SUPPRESS,
            help="Name of the tenant secret to search for."
        )
        search_linked_tenant_secrets.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=10,
            help="Provide limit to list number of tenant secrets."
        )
        search_linked_tenant_secrets.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="Page number for pagination."
        )
        search_linked_tenant_secrets.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        search_linked_tenant_secrets.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )
        
        unlink_tenant_secret = subparser.add_parser(
            'unlink-tenant-secret',
            help='Unlink a tenant secret from a Metastore Catalog.',
            formatter_class=ArgumentDefaultsHelpFormatter
        )
        unlink_tenant_secret.add_argument(
            '--metastore_catalog_secret_tenant_id',
            type=int,
            nargs=1,
            required=True,
            default=SUPPRESS,
            help="ID of the tenant secret to be unlinked from the metastore catalog."
        )
        unlink_tenant_secret.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        unlink_tenant_secret.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )