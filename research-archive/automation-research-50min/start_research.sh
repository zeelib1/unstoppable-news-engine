#!/bin/bash
# Start both research processes for autonomous operation

RESEARCH_DIR="/root/automation_research"
cd "$RESEARCH_DIR"

# Clean up old files
rm -f loop.log executor.log research_log.md results.json query_queue.json best_path.json RESEARCH_NEEDED.txt final_knowledge.json FINAL_REPORT.md

# Kill any existing processes
pkill -f research_executor.py 2>/dev/null
pkill -f "loop.py" 2>/dev/null
sleep 2

DURATION=${1:-5}  # Default to 5 minutes if not specified

echo "🚀 Starting Ralph Wiggum Research Loop..."
echo "Duration: $DURATION minutes"
echo ""

# Start research executor first
nohup python3 research_executor.py > executor.log 2>&1 &
EXECUTOR_PID=$!
echo "✅ Research Executor started (PID: $EXECUTOR_PID)"

# Give it a moment to initialize
sleep 2

# Start main loop with duration parameter
nohup python3 loop.py $DURATION > loop.log 2>&1 &
LOOP_PID=$!
echo "✅ Main Loop started (PID: $LOOP_PID)"

echo ""
echo "📊 Monitoring:"
echo "   tail -f $RESEARCH_DIR/loop.log"
echo "   tail -f $RESEARCH_DIR/executor.log"
echo "   tail -f $RESEARCH_DIR/research_log.md"
echo ""
echo "🛑 To stop:"
echo "   pkill -f research_executor.py && pkill -f loop.py"
echo ""

# Verify both are running
sleep 3
ps aux | grep -E "(loop\.py|research_executor\.py)" | grep -v grep

echo ""
echo "✅ All systems operational!"
