#!/bin/bash
# AskFiles Real-Time Monitor
# Usage: ./monitor.sh

clear
echo "🔍 AskFiles Real-Time Monitor"
echo "================================"
echo ""

while true; do
    clear
    echo "🔍 AskFiles Real-Time Monitor - $(date '+%Y-%m-%d %H:%M:%S')"
    echo "================================"
    echo ""
    
    # Check if services are running
    echo "📊 Services Status:"
    echo "-------------------"
    
    # Frontend
    if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo "✅ Frontend (port 3000): Running"
    else
        echo "❌ Frontend (port 3000): Stopped"
    fi
    
    # Backend
    if lsof -Pi :3001 -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo "✅ Backend (port 3001): Running"
    else
        echo "❌ Backend (port 3001): Stopped"
    fi
    
    # PostgreSQL
    if docker ps | grep -q askfiles-postgres; then
        echo "✅ PostgreSQL (port 5432): Running"
    else
        echo "❌ PostgreSQL (port 5432): Stopped"
    fi
    
    # Qdrant
    if docker ps | grep -q askfiles-qdrant; then
        echo "✅ Qdrant (port 6333): Running"
    else
        echo "❌ Qdrant (port 6333): Stopped"
    fi
    
    echo ""
    echo "📈 System Resources:"
    echo "-------------------"
    
    # CPU and Memory
    top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print "CPU Usage: " 100 - $1"%"}'
    free -h | awk 'NR==2{printf "Memory Usage: %s / %s (%.2f%%)\n", $3, $2, $3*100/$2}'
    df -h / | awk 'NR==2{printf "Disk Usage: %s / %s (%s)\n", $3, $2, $5}'
    
    echo ""
    echo "📝 Recent Backend Logs:"
    echo "----------------------"
    
    if [ -f /tmp/backend.log ]; then
        tail -n 5 /tmp/backend.log | sed 's/^/  /'
    else
        echo "  No logs yet"
    fi
    
    echo ""
    echo "🎨 Recent Frontend Logs:"
    echo "-----------------------"
    
    if [ -f /tmp/frontend.log ]; then
        tail -n 5 /tmp/frontend.log | sed 's/^/  /'
    else
        echo "  No logs yet"
    fi
    
    echo ""
    echo "🔄 Press Ctrl+C to exit, refreshing every 2 seconds..."
    sleep 2
done
