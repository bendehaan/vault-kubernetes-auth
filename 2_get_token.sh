kubectl get secret $(kubectl get serviceaccount vault-reviewer -o json | jq -r '.secrets[0].name') -o json | jq -r '.data .token' | base64 -d - > token.txt
