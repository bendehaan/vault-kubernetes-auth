vault write pki/config/urls \
       issuing_certificates="http://vault.default.minikube.bdh.local:8200/v1/pki/ca" \
       crl_distribution_points="http://vault.default.minikube.bdh.local:8200/v1/pki/crl"