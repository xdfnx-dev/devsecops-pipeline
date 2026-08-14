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
