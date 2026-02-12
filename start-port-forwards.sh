#!/bin/bash
# Start persistent port-forwards with auto-restart

# Kill any existing port-forwards
pkill -f "port-forward svc/ingress-nginx-controller" 2>/dev/null || true
pkill -f "port-forward svc/kubernetes-dashboard" 2>/dev/null || true

echo "Starting port-forwards..."

# Ingress controller (frontend + backend routing)
kubectl -n ingress-nginx port-forward svc/ingress-nginx-controller 8080:80 &
INGRESS_PID=$!

# Kubernetes Dashboard
kubectl -n kubernetes-dashboard port-forward svc/kubernetes-dashboard 8443:443 &
DASHBOARD_PID=$!

echo "Port-forwards started:"
echo "  - Ingress: localhost:8080 (atlas.local)"
echo "  - Dashboard: https://localhost:8443"
echo ""
echo "Access URLs:"
echo "  - Frontend: http://atlas.local:8080/"
echo "  - Dashboard: https://localhost:8443/"
echo ""
echo "Press Ctrl+C to stop"

# Keep script running and restart port-forwards if they crash
while true; do
  sleep 30
  
  if ! kill -0 $INGRESS_PID 2>/dev/null; then
    echo "Restarting ingress port-forward..."
    kubectl -n ingress-nginx port-forward svc/ingress-nginx-controller 8080:80 &
    INGRESS_PID=$!
  fi
  
  if ! kill -0 $DASHBOARD_PID 2>/dev/null; then
    echo "Restarting dashboard port-forward..."
    kubectl -n kubernetes-dashboard port-forward svc/kubernetes-dashboard 8443:443 &
    DASHBOARD_PID=$!
  fi
done
