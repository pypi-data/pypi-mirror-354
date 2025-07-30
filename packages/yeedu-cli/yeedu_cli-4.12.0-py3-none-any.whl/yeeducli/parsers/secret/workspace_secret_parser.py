from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter
from yeeducli.parsers.secret.secret_parser import add_secret_type_specific_args, add_common_args, SECRET_TYPE_ARGS, add_secret_type_specific_args_edit
from yeeducli.utility.json_utils import check_boolean, check_non_empty_string
from yeeducli.utility.logger_utils import Logger
import argparse
import sys

logger = Logger.get_logger(__name__, True)

class WorkspaceSecretParser:
    def workspace_secret_parser(subparser):
        initial_parser = argparse.ArgumentParser(add_help=False)
        initial_parser.add_argument("--secret_type", type=check_non_empty_string, required=False)
        known_args = initial_parser.parse_known_args(sys.argv[2:])[0]
        secret_type = known_args.secret_type

        if secret_type and secret_type not in SECRET_TYPE_ARGS:
            logger.error(
                f"Error: Invalid secret_type '{secret_type}'.\n"
                f"Supported types: {', '.join(SECRET_TYPE_ARGS.keys())}"
            )
            sys.exit(1)

        # ---------- CREATE ----------
        create_secret = subparser.add_parser(
            'create-workspace-secret',
            help='Create a new workspace secret.',
            formatter_class=ArgumentDefaultsHelpFormatter
        )
        create_secret.add_argument("--name", type=check_non_empty_string, nargs=1, required=True, default=SUPPRESS, help="Specify the name of the secret.")
        add_common_args(create_secret, is_workspace=True)
        add_secret_type_specific_args(create_secret, secret_type)

        # ---------- EDIT ----------
        edit_secret = subparser.add_parser(
            'edit-workspace-secret',
            help='Edit an existing workspace secret.',
            formatter_class=ArgumentDefaultsHelpFormatter
        )
        edit_secret.add_argument("--workspace_secret_id", type=int, required=True, default=SUPPRESS, help="ID of the workspace secret to be updated.")
        add_common_args(edit_secret, is_workspace=True)
        add_secret_type_specific_args_edit(edit_secret, secret_type)

        list_secrets = subparser.add_parser(
            'list-workspace-secrets',
            help='Retrieve a list of workspace secrets.',
            formatter_class=ArgumentDefaultsHelpFormatter
        )
        list_secrets.add_argument(
            "--workspace_id",
            type=int,
            default=SUPPRESS,
            help="Specify the workspace ID."
        )
        list_secrets.add_argument(
            "--workspace_name",
            type=check_non_empty_string,
            default=SUPPRESS,
            help="Specify the workspace name."
        )
        list_secrets.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="Specifies the page number for results pagination."
        )
        list_secrets.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Specifies the maximum number of configurations to list per page."
        )
        list_secrets.add_argument(
            "--secret_type",
            type=check_non_empty_string,
            choices=[
                "HIVE KERBEROS", "HIVE BASIC", "DATABRICKS UNITY TOKEN",
                "ENVIRONMENT VARIABLE", "AWS ACCESS SECRET KEY PAIR", "AZURE SERVICE PRINCIPAL",
                "GOOGLE SERVICE ACCOUNT"
            ],
            nargs=1,
            required=False,
            default=SUPPRESS,
            help="Type of the tenant secret to search for."
        )
        list_secrets.add_argument(
            "--workspace_secret_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=False,
            help="Specify the workspace secret ID."
        )
        list_secrets.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_secrets.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        search_secrets = subparser.add_parser(
            'search-workspace-secrets',
            help='Search for tenant secrets based on various criteria.',
            formatter_class=ArgumentDefaultsHelpFormatter
        )
        search_secrets.add_argument(
            "--workspace_id",
            type=int,
            default=SUPPRESS,
            help="Specify the workspace ID."
        )
        search_secrets.add_argument(
            "--workspace_name",
            type=check_non_empty_string,
            default=SUPPRESS,
            help="Specify the workspace name."
        )
        search_secrets.add_argument(
            "--secret_name",
            type=check_non_empty_string,
            required=True,
            default=SUPPRESS,
            nargs=1,
            help="ID of the tenant secret to search for."
        )
        search_secrets.add_argument(
            "--secret_type",
            type=check_non_empty_string,
            choices=[
                "HIVE KERBEROS", "HIVE BASIC", "DATABRICKS UNITY TOKEN",
                "ENVIRONMENT VARIABLE", "AWS ACCESS SECRET KEY PAIR", "AZURE SERVICE PRINCIPAL",
                "GOOGLE SERVICE ACCOUNT"
            ],
            nargs=1,
            default=SUPPRESS,
            help="Type of the tenant secret to search for."
        )
        search_secrets.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="Specifies the page number for results pagination."
        )
        search_secrets.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Specifies the maximum number of configurations to list per page."
        )
        search_secrets.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        search_secrets.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        delete_secret = subparser.add_parser(
            'delete-workspace-secret',
            help='Delete a workspace secret.',
            formatter_class=ArgumentDefaultsHelpFormatter
        )
        delete_secret.add_argument(
            "--workspace_id",
            type=int,
            default=SUPPRESS,
            help="Specify the workspace ID."
        )
        delete_secret.add_argument(
            "--workspace_name",
            type=check_non_empty_string,
            default=SUPPRESS,
            help="Specify the workspace name."
        )
        delete_secret.add_argument(
            "--workspace_secret_id",
            type=int,
            nargs=1,
            required=True,
            default=SUPPRESS,
            help="ID of the workspace secret to be deleted."
        )
        delete_secret.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        delete_secret.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )