#!/bin/bash
set -e

# Deploy Project Atlas to kind cluster
# Prerequisites: kind cluster running, docker, kubectl, helm

CLUSTER_NAME="${1:-atlas}"
NAMESPACE="project-atlas"
CHART_DIR="k8s/helm/project-atlas"

echo "🚀 Building images..."
docker build -t project-atlas-backend:latest -f backend/Dockerfile backend
docker build -t project-atlas-frontend:latest -f frontend/Dockerfile frontend

echo "📦 Loading images into kind cluster '$CLUSTER_NAME'..."
kind load docker-image project-atlas-backend:latest --name "$CLUSTER_NAME"
kind load docker-image project-atlas-frontend:latest --name "$CLUSTER_NAME"

echo "🔧 Creating namespace and deploying with Helm..."
kubectl create namespace "$NAMESPACE" --dry-run=client -o yaml | kubectl apply -f -

# Deploy with Helm (optionally pass backend secrets, etc.)
helm upgrade --install project-atlas "$CHART_DIR" \
  -n "$NAMESPACE" \
  --set backend.image.repository=project-atlas-backend \
  --set backend.image.tag=latest \
  --set frontend.image.repository=project-atlas-frontend \
  --set frontend.image.tag=latest

echo "✅ Deployment complete!"
echo ""
echo "🌐 To access frontend (after ingress/port-forward):"
echo "   kubectl port-forward -n $NAMESPACE svc/frontend 8080:80"
echo "   Then visit http://localhost:8080"
echo ""
echo "📡 To access backend API:"
echo "   kubectl port-forward -n $NAMESPACE svc/backend 8000:8000"
echo "   Then visit http://localhost:8000/api"
echo ""
echo "📊 View logs:"
echo "   kubectl logs -n $NAMESPACE -l app=backend -f"
echo "   kubectl logs -n $NAMESPACE -l app=frontend -f"
