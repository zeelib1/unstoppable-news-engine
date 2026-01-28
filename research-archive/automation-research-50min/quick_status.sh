#!/bin/bash
# Quick status check for research loop

echo "🤖 RALPH WIGGUM RESEARCH LOOP - STATUS"
echo "========================================"
echo ""

# Time info
START_TIME="2026-01-28 02:49:00"
END_TIME="2026-01-28 07:49:00"
CURRENT_TIME=$(date "+%Y-%m-%d %H:%M:%S")

echo "⏰ Timeline:"
echo "   Start: $START_TIME"
echo "   Current: $CURRENT_TIME"
echo "   Target End: $END_TIME"
echo ""

# Process status
echo "🔄 Process Status:"
LOOP_PID=$(pgrep -f "python3.*loop.py")
EXECUTOR_PID=$(pgrep -f "python3.*research_executor.py")
MONITOR_PID=$(pgrep -f "monitor_and_update.sh")
SCHEDULER_PID=$(pgrep -f "schedule_report.sh")

if [ -n "$LOOP_PID" ]; then
    echo "   ✅ Main Loop: Running (PID $LOOP_PID)"
else
    echo "   ❌ Main Loop: Not running"
fi

if [ -n "$EXECUTOR_PID" ]; then
    echo "   ✅ Research Executor: Running (PID $EXECUTOR_PID)"
else
    echo "   ❌ Research Executor: Not running"
fi

if [ -n "$MONITOR_PID" ]; then
    echo "   ✅ Memory Monitor: Running (PID $MONITOR_PID)"
else
    echo "   ❌ Memory Monitor: Not running"
fi

if [ -n "$SCHEDULER_PID" ]; then
    echo "   ✅ Report Scheduler: Running (PID $SCHEDULER_PID)"
else
    echo "   ❌ Report Scheduler: Not running"
fi

echo ""

# Best path
echo "🎯 Current Best Strategy:"
if [ -f "/root/automation_research/best_path.json" ]; then
    ITERATION=$(jq -r '.iteration // "?"' /root/automation_research/best_path.json)
    TOP_STRATEGY=$(jq -r '.top_strategy // "None yet"' /root/automation_research/best_path.json)
    TOTAL=$(jq -r '.total_strategies_evaluated // "0"' /root/automation_research/best_path.json)
    
    echo "   Iteration: $ITERATION"
    echo "   Strategies Evaluated: $TOTAL"
    echo "   Top: $TOP_STRATEGY"
else
    echo "   (Best path not yet determined)"
fi

echo ""

# Latest log entries
echo "📝 Latest Activity:"
if [ -f "/root/automation_research/research_log.md" ]; then
    tail -5 /root/automation_research/research_log.md | sed 's/^/   /'
else
    echo "   (No activity yet)"
fi

echo ""
echo "========================================"
echo "For full status: cat ~/automation_research/STATUS.md"
echo "For live logs: tail -f ~/automation_research/research_log.md"
