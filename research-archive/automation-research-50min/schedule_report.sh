#!/bin/bash
# Wait 5 hours then generate the final report

echo "⏰ Scheduled report generation in 5 hours (300 minutes)..."
echo "Start time: $(date)"

# Wait 5 hours (18000 seconds)
sleep 18000

echo "🏁 5 hours elapsed. Generating final report..."
echo "End time: $(date)"

cd /root/automation_research
python3 generate_report.py

echo ""
echo "✅ RESEARCH LOOP COMPLETE"
echo "📄 Final report saved to: /root/automation_research/FINAL_REPORT.md"
echo ""
echo "Stopping background processes..."
pkill -f research_executor.py
pkill -f loop.py
pkill -f monitor_and_update.sh

echo "All processes stopped. Research complete."
