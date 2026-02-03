This folder contains a backup of the Helm chart `project-atlas` that was
disabled by the operator on 2026-02-02. The chart files were moved here to
stop Helm-based deployments while switching to a vanilla Kubernetes workflow.

To restore the chart, move the files back to `k8s/helm/project-atlas/`.

Files backed up:
- Chart.yaml
- values.yaml
- NOTES.txt
- templates/*

Reason: user requested to stop using Helm and use plain Kubernetes manifests.
