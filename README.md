# Vault Kubernetes Authentication demo

Made to work with Minikube and an existing Vault deployment (in default namespace).

Run as numbered, executing shell files and applying yaml files, or follow the walkthrough below. 
Optionally deploy the test pod with `kubectl apply -f test_pod.yaml` to see if works as designed.

**NB: Requires Vault to be running, unsealed, and the Vault client to be authenticated.**

## 0. Vault Kubernetes backend

Enable the kubernetes backend.

```
vault auth enable kubernetes
```


## 1. Add required namespaces, service accounts, and ClusterRoleBinding

```
kubectl apply -f 1_vault_integration.yaml
```

This will create the following resources: 
* An `application` namespace.
* A `vault-reviewer` service account in the `default` namespace (where Vault resides).
* A `vault-auth` service account in the `application` namespace (where the app resides).
* A Cluster Role Binding, giving the `vault-reviewer` rights to auth delegation.

## 2. Retrieve the vault-reviewer token (needed by Vault)

```
kubectl get secret $(kubectl get serviceaccount vault-reviewer -o json | jq -r '.secrets[0].name') -o json | jq -r '.data .token' | base64 -d - > token.txt
```

## 3. Configure the Kubernetes backend with the acquired token and minikube cert.
```
vault write auth/kubernetes/config \
    token_reviewer_jwt=@token.txt  \
    kubernetes_host=https://192.168.99.100:8443 \
    kubernetes_ca_cert=@$HOME/.minikube/ca.crt
```

## 4. Configure Vault policy and role


### 4.1 Policy
```
vault policy write application-kube-auth application-kube-auth.hcl
```

This configures the following policy:
```
path "secret/application/*" {
  capabilities = ["read"]
}

path "secret/vault_test" {
  capabilities = ["create", "read", "update", "delete", "list"]
}
```

### 4.2 Role
Using the previously created policy and service accounts, we can now create a `demo` role which we can use in the application.

```
vault write auth/kubernetes/role/demo \
    bound_service_account_names=vault-auth \
    bound_service_account_namespaces=application \
    policies=application-kube-auth \
    period=60s
```

Check if  it's configured correctly:
```
vault read auth/kubernetes/role/demo
```

## 5. Deploy a test application
This application is configured to authenticate to Vault using its kubernetes token, write a secret, read it, and delete it (see `vault_test.py`). It currently adheres to the policy defined in 4.1, but can of course do some unauthorized things as well :).

```
kubectl apply -f test_pod.yaml
```