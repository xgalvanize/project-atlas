Required repository secrets and best-practices

Required GitHub Secrets
- `DOCKERHUB_USERNAME` — your Docker Hub username or org (e.g. `xgalvanize`).
- `DOCKERHUB_TOKEN` — Docker Hub access token or password (use a token when possible).

Best practices
- Never commit credentials, API keys, or DB passwords to source. Use GitHub Secrets for CI and Kubernetes Secrets (or external secret managers) for runtime.
- For Helm installs, pass secrets at deploy time instead of writing them to `values.yaml`. Example:

  helm upgrade --install project-atlas ./project-atlas -n project-atlas --create-namespace \
    --set backend.image.repository=docker.io/${{ secrets.DOCKERHUB_USERNAME }}/project-atlas-backend \
    --set backend.image.tag=latest \
    --set-string backend.secrets.DJANGO_SECRET_KEY="$(echo $DJANGO_SECRET_KEY)"

- Consider using `sops`, `sealed-secrets`, or cloud provider secret managers for production.
