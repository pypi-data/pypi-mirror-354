from argparse import SUPPRESS
from yeeducli.utility.json_utils import check_boolean, check_non_empty_string

# Dictionary defining valid arguments for each secret type
SECRET_TYPE_ARGS = {
    "HIVE KERBEROS": {"--principal", "--keytab"},
    "HIVE BASIC": {"--username", "--password"},
    "DATABRICKS UNITY TOKEN": {"--token"},
    "ENVIRONMENT VARIABLE": {"--value"},
    "AWS ACCESS SECRET KEY PAIR": {"--aws_access_key_id", "--aws_secret_access_key", "--aws_default_region"},
    "AZURE SERVICE PRINCIPAL": {
        "--tenant_id", "--client_id", "--client_secret",
        "--storage_account_name", "--container_name"
    },
    "GOOGLE SERVICE ACCOUNT": {
        "--type", "--project_id", "--private_key_id", "--private_key",
        "--client_email", "--client_id", "--auth_uri", "--token_uri",
        "--auth_provider_x509_cert_url", "--client_x509_cert_url",
        "--access_key", "--secret_key"
    }
}

# Common arguments used by all secrets
COMMON_ARGS = {"--name", "--description", "--secret_type", "--json-output", "--yaml-output"}


def add_common_args(parser, is_workspace=False):
    """Adds common arguments for create & edit commands."""

    if is_workspace:
        parser.add_argument("--workspace_id", type=int, nargs=1, default=SUPPRESS, help="Specify the Workspace ID.")
        parser.add_argument("--workspace_name", type=check_non_empty_string, nargs=1, default=SUPPRESS, help="Specify the Workspace Name")

    parser.add_argument("--description", type=check_non_empty_string, nargs=1, default=SUPPRESS, help="Provide a description for the secret.")

    parser.add_argument(
        "--secret_type",
        type=check_non_empty_string,
        choices=[
            "HIVE KERBEROS", "HIVE BASIC", "DATABRICKS UNITY TOKEN",
            "ENVIRONMENT VARIABLE", "AWS ACCESS SECRET KEY PAIR", "AZURE SERVICE PRINCIPAL",
            "GOOGLE SERVICE ACCOUNT"
        ],
        nargs=1,
        required=True,
        default=SUPPRESS,
        help="Specify the type of authentication secret."
    )

    parser.add_argument("--json-output", type=check_non_empty_string, nargs='?', choices=['pretty', 'default'], default='pretty', help="Specifies the format of JSON output.")
    parser.add_argument("--yaml-output", type=check_boolean, nargs='?', choices=['true', 'false'], default='false', help="Displays the information in YAML format if set to 'true'.")


def add_secret_type_specific_args(parser, secret_type):
    """Adds arguments specific to each secret type grouped logically."""

    if secret_type == "HIVE KERBEROS":
        kerberos_group = parser.add_argument_group("HIVE KERBEROS Authentication")
        kerberos_group.add_argument("--principal", type=check_non_empty_string, nargs=1, required=True, default=SUPPRESS, help="Specify the Kerberos principal.")
        kerberos_group.add_argument("--keytab", type=check_non_empty_string, nargs=1, required=True, default=SUPPRESS, help="Specify the Keytab file path.")

    elif secret_type == "HIVE BASIC":
        hive_group = parser.add_argument_group("HIVE BASIC Authentication")
        hive_group.add_argument("--username", type=check_non_empty_string, nargs=1, required=True, default=SUPPRESS, help="Specify Hive username.")
        hive_group.add_argument("--password", type=check_non_empty_string, nargs=1, required=True, default=SUPPRESS, help="Specify Hive password.")

    elif secret_type == "DATABRICKS UNITY TOKEN":
        db_group = parser.add_argument_group("Databricks Unity")
        db_group.add_argument("--token", type=check_non_empty_string, nargs=1, required=True, default=SUPPRESS, help="Specify the Databricks Unity token.")

    elif secret_type == "ENVIRONMENT VARIABLE":
        env_group = parser.add_argument_group("Environment Variable")
        env_group.add_argument("--value", type=check_non_empty_string, nargs=1, required=True, default=SUPPRESS, help="Specify the environment variable value.")

    elif secret_type == "AWS ACCESS SECRET KEY PAIR":
        aws_group = parser.add_argument_group("AWS ACCESS SECRET KEY PAIR Credentials")
        aws_group.add_argument("--aws_access_key_id", type=check_non_empty_string, nargs=1, required=True, default=SUPPRESS, help="AWS Access Key ID")
        aws_group.add_argument("--aws_secret_access_key", type=check_non_empty_string, nargs=1, required=True, default=SUPPRESS, help="AWS Secret Access Key")
        aws_group.add_argument("--aws_default_region", type=check_non_empty_string, nargs=1, required=True, default=SUPPRESS, help="AWS Default Region")

    elif secret_type == "AZURE SERVICE PRINCIPAL":
        azure_group = parser.add_argument_group("Azure Service Principal")
        azure_group.add_argument("--tenant_id", type=check_non_empty_string, nargs=1, required=True, default=SUPPRESS, help="Azure Tenant ID")
        azure_group.add_argument("--subscription_id", type=check_non_empty_string, nargs=1, required=True, default=SUPPRESS, help="Azure Subscription ID")
        azure_group.add_argument("--client_id", type=check_non_empty_string, nargs=1, required=True, default=SUPPRESS, help="Azure Client ID")
        azure_group.add_argument("--client_secret", type=check_non_empty_string, nargs=1, required=True, default=SUPPRESS, help="Azure Client Secret")
        azure_group.add_argument("--storage_account_name", type=check_non_empty_string, nargs=1, required=True, default=SUPPRESS, help="Azure Storage Account")
        azure_group.add_argument("--container_name", type=check_non_empty_string, nargs=1, required=True, default=SUPPRESS, help="Azure Container Name")

    elif secret_type == "GOOGLE SERVICE ACCOUNT":
        gcp_group = parser.add_argument_group("Google Service Account")
        gcp_group.add_argument("--type", type=check_non_empty_string, nargs=1, required=True, default=SUPPRESS, help="Specify the type of Google Service Account")
        gcp_group.add_argument("--project_id", type=check_non_empty_string, nargs=1, required=True, default=SUPPRESS, help="Specify the Google Project ID")
        gcp_group.add_argument("--private_key_id", type=check_non_empty_string, nargs=1, required=True, default=SUPPRESS, help="Specify the Google Private Key ID")
        gcp_group.add_argument("--private_key", type=check_non_empty_string, nargs=1, required=True, default=SUPPRESS, help="Specify the Google Private Key")
        gcp_group.add_argument("--client_email", type=check_non_empty_string, nargs=1, required=True, default=SUPPRESS, help="Specify the Google Client Email")
        gcp_group.add_argument("--client_id", type=check_non_empty_string, nargs=1, required=True, default=SUPPRESS, help="Specify the Google Client ID")
        gcp_group.add_argument("--auth_uri", type=check_non_empty_string, nargs=1, required=True, default=SUPPRESS, help="Specify the Google Auth URI")
        gcp_group.add_argument("--token_uri", type=check_non_empty_string, nargs=1, required=True, default=SUPPRESS, help="Specify the Google Token URI")
        gcp_group.add_argument("--auth_provider_x509_cert_url", type=check_non_empty_string, nargs=1, required=True, default=SUPPRESS, help="Specify the Google Auth Provider X509 Cert URL")
        gcp_group.add_argument("--client_x509_cert_url", type=check_non_empty_string, nargs=1, required=True, default=SUPPRESS, help="Specify the Google Client X509 Cert URL")
        gcp_group.add_argument("--access_key", type=check_non_empty_string, nargs=1, required=True, default=SUPPRESS, help="Specify the Access Key")
        gcp_group.add_argument("--secret_key", type=check_non_empty_string, nargs=1, required=True, default=SUPPRESS, help="Specify the Access Key")

def add_secret_type_specific_args_edit(parser, secret_type):
    """Adds secret-type specific arguments for edit (all optional with default=SUPPRESS)."""

    if secret_type == "HIVE KERBEROS":
        kerberos_group = parser.add_argument_group("HIVE KERBEROS Authentication")
        kerberos_group.add_argument("--principal", type=check_non_empty_string, nargs=1, required=False, default=SUPPRESS, help="Specify the Kerberos principal.")
        kerberos_group.add_argument("--keytab", type=check_non_empty_string, nargs=1, required=False, default=SUPPRESS, help="Specify the Keytab file path.")

    elif secret_type == "HIVE BASIC":
        hive_group = parser.add_argument_group("HIVE BASIC Authentication")
        hive_group.add_argument("--username", type=check_non_empty_string, nargs=1, required=False, default=SUPPRESS, help="Specify Hive username.")
        hive_group.add_argument("--password", type=check_non_empty_string, nargs=1, required=False, default=SUPPRESS, help="Specify Hive password.")

    elif secret_type == "DATABRICKS UNITY TOKEN":
        db_group = parser.add_argument_group("Databricks Unity")
        db_group.add_argument("--token", type=check_non_empty_string, nargs=1, required=False, default=SUPPRESS, help="Specify the Databricks Unity token.")

    elif secret_type == "ENVIRONMENT VARIABLE":
        env_group = parser.add_argument_group("Environment Variable")
        env_group.add_argument("--value", type=check_non_empty_string, nargs=1, required=False, default=SUPPRESS, help="Specify the environment variable value.")

    elif secret_type == "AWS ACCESS SECRET KEY PAIR":
        aws_group = parser.add_argument_group("AWS ACCESS SECRET KEY PAIR Credentials")
        aws_group.add_argument("--aws_access_key_id", type=check_non_empty_string, nargs=1, required=False, default=SUPPRESS, help="AWS Access Key ID")
        aws_group.add_argument("--aws_secret_access_key", type=check_non_empty_string, nargs=1, required=False, default=SUPPRESS, help="AWS Secret Access Key")
        aws_group.add_argument("--aws_default_region", type=check_non_empty_string, nargs=1, required=False, default=SUPPRESS, help="AWS Default Region")

    elif secret_type == "AZURE SERVICE PRINCIPAL":
        azure_group = parser.add_argument_group("Azure Service Principal")
        azure_group.add_argument("--tenant_id", type=check_non_empty_string, nargs=1, required=False, default=SUPPRESS, help="Azure Tenant ID")
        azure_group.add_argument("--subscription_id", type=check_non_empty_string, nargs=1, required=False, default=SUPPRESS, help="Azure Subscription ID")
        azure_group.add_argument("--client_id", type=check_non_empty_string, nargs=1, required=False, default=SUPPRESS, help="Azure Client ID")
        azure_group.add_argument("--client_secret", type=check_non_empty_string, nargs=1, required=False, default=SUPPRESS, help="Azure Client Secret")
        azure_group.add_argument("--storage_account_name", type=check_non_empty_string, nargs=1, required=False, default=SUPPRESS, help="Azure Storage Account")
        azure_group.add_argument("--container_name", type=check_non_empty_string, nargs=1, required=False, default=SUPPRESS, help="Azure Container Name")

    elif secret_type == "GOOGLE SERVICE ACCOUNT":
        gcp_group = parser.add_argument_group("Google Service Account")
        gcp_group.add_argument("--type", type=check_non_empty_string, nargs=1, required=False, default=SUPPRESS, help="Specify the type of Google Service Account")
        gcp_group.add_argument("--project_id", type=check_non_empty_string, nargs=1, required=False, default=SUPPRESS, help="Specify the Google Project ID")
        gcp_group.add_argument("--private_key_id", type=check_non_empty_string, nargs=1, required=False, default=SUPPRESS, help="Specify the Google Private Key ID")
        gcp_group.add_argument("--private_key", type=check_non_empty_string, nargs=1, required=False, default=SUPPRESS, help="Specify the Google Private Key")
        gcp_group.add_argument("--client_email", type=check_non_empty_string, nargs=1, required=False, default=SUPPRESS, help="Specify the Google Client Email")
        gcp_group.add_argument("--client_id", type=check_non_empty_string, nargs=1, required=False, default=SUPPRESS, help="Specify the Google Client ID")
        gcp_group.add_argument("--auth_uri", type=check_non_empty_string, nargs=1, required=False, default=SUPPRESS, help="Specify the Google Auth URI")
        gcp_group.add_argument("--token_uri", type=check_non_empty_string, nargs=1, required=False, default=SUPPRESS, help="Specify the Google Token URI")
        gcp_group.add_argument("--auth_provider_x509_cert_url", type=check_non_empty_string, nargs=1, required=False, default=SUPPRESS, help="Specify the Google Auth Provider X509 Cert URL")
        gcp_group.add_argument("--client_x509_cert_url", type=check_non_empty_string, nargs=1, required=False, default=SUPPRESS, help="Specify the Google Client X509 Cert URL")
        gcp_group.add_argument("--access_key", type=check_non_empty_string, nargs=1, default=SUPPRESS, help="Specify the Access Key")
        gcp_group.add_argument("--secret_key", type=check_non_empty_string, nargs=1, default=SUPPRESS, help="Specify the Access Key")
