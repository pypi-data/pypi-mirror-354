import os
from email.policy import default

import click
from griddot.provision_keycloak import import_realm, get_user_uuid_by_username, get_access_token, delete_user
from griddot.tools import encrypt_secrets, create_new_key, decrypt_secrets, helm_template
from griddot.tools import helm_list_charts


@click.group()
def cli():
    """CLI for GridDot platform tools"""
    pass


@click.group()
def keycloak():
    """Tools for managing keycloak"""
    pass


@click.group()
def secrets():
    """Tools for managing secrets"""
    pass


@click.group()
def deploy():
    """Tools for managing deployments"""
    pass


cli.add_command(secrets)
cli.add_command(keycloak)
cli.add_command(deploy)


@keycloak.command("provision", short_help="Provision Keycloak with realms and users")
@click.option('--url', help='Keycloak server URL')
@click.option('--username', help='User name')
@click.option('--password', help='Username password')
@click.option('--realms-dir', help='Path to the directory with realm JSON files')
@click.option('--delete-user-when-provisioned', type=bool, default=True)
@click.option('--email-password', help='Email provider password')
def keycloak_provision(url, username, password, realms_dir, delete_user_when_provisioned, email_password):
    """Keycloak provisioning tool"""

    for realm_path in os.listdir(realms_dir):
        full_path = os.path.join(realms_dir, realm_path)
        print(f"Importing realm from {full_path}")
        import_realm(url, username, password, full_path, email_password, True)

    if delete_user_when_provisioned.lower() == 'yes':
        token = get_access_token(url, username, password)
        user_id = get_user_uuid_by_username(url, "master", token, username)
        delete_user(url, "master", token, user_id)
        print(f"Deleted user {username} from master realm.")


@secrets.command("decrypt", short_help="Decrypt secrets files using the private key .secrets/key.pem")
@click.option('--file', '-f', multiple=True, help='Path to the encrypted secrets file(s)')
def secrets_decrypt(file: tuple[str]):
    decrypt_secrets(list(file))


@secrets.command("create", short_help="Create a new RSA key pair: .secrets/key.pem and .secrets/key.pub")
def secrets_create():
    create_new_key()


@secrets.command("encrypt", short_help="Encrypt secrets files using the public key .secrets/key.pub")
@click.option('--file', '-f', multiple=True, help='Path to the secrets file(s) to encrypt')
def secrets_encrypt(file: tuple[str]):
    encrypt_secrets(list(file))


@deploy.command("list", short_help="List all deployments from helm repository")
def deploy_list():
    helm_charts = helm_list_charts()
    print("Possible deployments:")
    for chart in helm_charts:
        print(f"- {chart}")


@deploy.command("template", short_help="Templates a Kubernetes deployment using helm for podman kube play command")
@click.option('--deployment', '-d', required=True, help='Deployment name from the griddot helm repository (run `griddot deploy list` to see available deployments)')
@click.option('--values-path', '-v', help='Path to the values file for the helm chart')
@click.option('--output', '-o', default='pod.yaml', help='Output file to write the template to')
def deploy_list(deployment: str, values_path: str, output: str):
    templated_yaml = helm_template(deployment, values_path)
    with open(output, 'w', encoding='utf-8') as f:
        f.write(templated_yaml)

    print(f"Templated deployment {deployment} to {output}")
