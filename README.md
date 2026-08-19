# DevSecOps Pipeline

A secure delivery pipeline that treats security checks as required CI stages rather than post-deployment tasks.

## Pipeline stages

1. Unit tests
2. Semgrep SAST
3. Gitleaks secret detection
4. Checkov Kubernetes manifest scan
5. Docker image build and publish to GHCR
6. Keyless Cosign image signing
7. Trivy vulnerability scan with SARIF upload to GitHub Security

The Kubernetes manifest also demonstrates non-root execution, dropped Linux capabilities, a read-only filesystem and resource limits.

## Run locally

```bash
python -m unittest discover -s tests -v
docker build -t secure-demo-api .
docker run --rm -p 8000:8000 secure-demo-api
```

Use branch protection to require `unit-tests` and `static-analysis` before merging. For production, sign the image with Cosign and deploy by immutable digest instead of a mutable tag.

## Pipeline stages

```
Checkout -> unit tests -> Semgrep (SAST) -> Gitleaks (secrets) -> Checkov (IaC) -> build -> Trivy -> Cosign -> SARIF
```

## Key files

- `app/app.py` — the secured service; `tests/` — unit tests.
- `Dockerfile` — non-root, read-only where possible.
- `.github/workflows/pipeline.yml` — gates: `unit-tests`, `static-analysis`, `image-security`, `signing`.
- `k8s/deployment.yaml` — dropped capabilities, read-only rootfs, resource limits.

## What I learned

Security shifts left when it blocks the merge, not the release: Gitleaks catches a committed secret the same way Semgrep catches a logic bug, and Checkov makes IaC misconfigurations a first-class review item. Signing the image with Cosign and deploying an immutable digest closes the loop — you can trust what shipped because it is verifiably what you built and scanned.

## Merge gates

| Stage | Tool | Blocks merge? |
|---|---|---|
| Unit tests | `python -m unittest` | yes |
| Static analysis | Semgrep | yes (configurable) |
| Secret scanning | Gitleaks | yes |
| IaC scanning | Checkov | yes |
| Image vulnerability | Trivy -> SARIF | yes |
| Image signing | Cosign | production deploy |
