#!/bin/bash
# Quick start script for Project Atlas
# Usage: ./project-atlas.sh start|stop|status|lan-setup

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PORTS_PID_FILE="/tmp/project-atlas-ports.pid"
LAN_IP=$(ip addr show | grep "inet " | grep -v "127.0" | head -1 | awk '{print $2}' | cut -d/ -f1)

start() {
  echo "🚀 Starting Project Atlas..."
  
  # Check if already running
  if [ -f "$PORTS_PID_FILE" ] && kill -0 "$(cat $PORTS_PID_FILE)" 2>/dev/null; then
    echo "⚠️  Port-forwards already running (PID: $(cat $PORTS_PID_FILE))"
    status
    return 0
  fi
  
  # Check for --lan flag
  if [ "$2" = "--lan" ]; then
    echo "🌐 Starting with LAN access (listening on all interfaces)"
    # Listen on all interfaces (0.0.0.0) for LAN access
    kubectl -n ingress-nginx port-forward --address 0.0.0.0 svc/ingress-nginx-controller 8080:80 &>/dev/null &
  else
    # Listen only on localhost
    kubectl -n ingress-nginx port-forward svc/ingress-nginx-controller 8080:80 &>/dev/null &
  fi
  
  INGRESS_PID=$!
  echo "$INGRESS_PID" > "$PORTS_PID_FILE"
  
  # Wait for connection
  echo "⏳ Waiting for ingress to be ready..."
  for i in {1..30}; do
    if curl -s http://atlas.local:8080/ >/dev/null 2>&1; then
      echo "✅ Ingress ready!"
      break
    fi
    sleep 0.5
  done
  
  echo ""
  echo "✅ Project Atlas is running!"
  echo ""
  
  if [ "$2" = "--lan" ]; then
    echo "📍 Access from this computer:"
    echo "   http://atlas.local:8080/"
    echo ""
    echo "📍 Access from another computer on LAN:"
    echo "   http://10.0.0.145:8080/"
    echo ""
    echo "📍 To use atlas.local from other computers, add to their /etc/hosts:"
    echo "   10.0.0.145 atlas.local api.atlas.local"
    echo ""
    echo "⚠️  After adding to /etc/hosts on other computer, restart browser"
  else
    echo "📍 Access the application:"
    echo "   http://atlas.local:8080/"
  fi
  
  echo "   Login: admin / change-me"
  echo ""
  echo "📊 View Kubernetes Dashboard:"
  echo "   kubectl -n kubernetes-dashboard port-forward svc/kubernetes-dashboard 8443:443"
  echo "   Then: https://localhost:8443/"
  echo ""
  echo "To stop: ./project-atlas.sh stop"
}

stop() {
  if [ -f "$PORTS_PID_FILE" ]; then
    PID=$(cat "$PORTS_PID_FILE")
    if kill -0 "$PID" 2>/dev/null; then
      kill "$PID" 2>/dev/null || true
      rm "$PORTS_PID_FILE"
      echo "✅ Project Atlas stopped"
    else
      rm "$PORTS_PID_FILE"
      echo "⚠️  No running port-forwards found"
    fi
  else
    echo "⚠️  Project Atlas not running"
  fi
}

status() {
  if [ -f "$PORTS_PID_FILE" ] && kill -0 "$(cat $PORTS_PID_FILE)" 2>/dev/null; then
    echo "✅ Project Atlas is RUNNING"
    echo ""
    echo "Access:"
    echo "   http://atlas.local:8080/"
    echo ""
    echo "Login: admin / change-me"
  else
    echo "❌ Project Atlas is NOT running"
    echo ""
    echo "Start with: ./project-atlas.sh start"
  fi
}

case "${1:-start}" in
  start)
    start "$@"
    ;;
  stop)
    stop
    ;;
  status)
    status
    ;;
  restart)
    stop
    sleep 1
    start "$@"
    ;;
  lan-setup)
    echo "📋 To access Project Atlas from another computer on your LAN:"
    echo ""
    echo "1️⃣  On this computer (10.0.0.145), start with LAN access:"
    echo "   ./project-atlas.sh start --lan"
    echo ""
    echo "2️⃣  On the other computer, add to /etc/hosts:"
    echo "   10.0.0.145 atlas.local api.atlas.local"
    echo ""
    echo "3️⃣  Access from the other computer:"
    echo "   http://atlas.local:8080/"
    echo "   OR"
    echo "   http://10.0.0.145:8080/"
    echo ""
    ;;
  *)
    echo "Usage: $0 {start|stop|status|restart|lan-setup} [--lan]"
    echo ""
    echo "Examples:"
    echo "  ./project-atlas.sh start        # Start (localhost only)"
    echo "  ./project-atlas.sh start --lan  # Start (LAN accessible)"
    echo "  ./project-atlas.sh status       # Check status"
    echo "  ./project-atlas.sh lan-setup    # Show LAN setup instructions"
    exit 1
    ;;
esac
