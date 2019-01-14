vault policy write application-kube-auth application-kube-auth.hcl

vault write auth/kubernetes/role/demo \
    bound_service_account_names=vault-auth \
    bound_service_account_namespaces=application \
    policies=application-kube-auth \
    period=60s

vault read auth/kubernetes/role/demo
