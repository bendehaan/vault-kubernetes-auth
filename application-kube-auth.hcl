path "secret/application/*" {
  capabilities = ["read"]
}

path "secret/vault_test" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

