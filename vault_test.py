import hvac
import os
import sys


def to_bool(bool_str):
    """Parse the string and return the boolean encoded or raise exception."""
    if bool_str.lower() in ['true', 't', '1']:
        return True
    elif bool_str.lower() in ['false', 'f', '0']:
        return False
    else:
        return bool_str  # Probably a CA path


def read_vault_token_file(filename):
    """Read k8s token file and return the JWT."""
    with open(filename, 'r') as f:
        print("Reading vault token file at: {0}".format(filename))
        jwt = f.read()
        return jwt


if __name__ == '__main__':
    """Set up a vault connection and manipulate a secret."""

    env_vars = [
            'VAULT_ADDR',
            'VAULT_TOKEN_FILE',
            'VERIFY_VAULT_CERT',
            'VAULT_ROLE'
    ]

    for env_var in env_vars:
        if env_var not in os.environ:
            print('Environment variable {0} not set'.format(env_var))
            sys.exit(1)

    verify_cert = to_bool(os.environ['VERIFY_VAULT_CERT'])
    if verify_cert:
        print("Good job! You're verifying a cert!")
    else:
        print("Oh no! Cert validation is turned off....")

    vault_token = read_vault_token_file(os.environ['VAULT_TOKEN_FILE'])
    secret = 'secret/vault_test'

    try:
        client = hvac.Client(url=os.environ['VAULT_ADDR'], verify=verify_cert)
        client.auth_kubernetes(os.environ['VAULT_ROLE'], vault_token)
        print("Client authenticated? {0}".format(client.is_authenticated()))
        print("Writing secret: {0}".format(secret))
        client.write(secret, verysecretsecret='s3cr3t', lease='1h')
        print('Reading secret: {0}'.format(secret))
        print(client.read(secret))
        print('Deleting secret: {0}'.format(secret))
        client.delete(secret)
    except hvac.VaultError() as e:
        print(e)
