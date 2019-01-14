vault write auth/kubernetes/config \
    token_reviewer_jwt=@token.txt  \
    kubernetes_host=https://192.168.99.100:8443 \
    kubernetes_ca_cert=@$HOME/.minikube/ca.crt

