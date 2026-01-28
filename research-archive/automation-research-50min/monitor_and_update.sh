#!/bin/bash
# Monitor research progress and update memory every 30 minutes

WORKSPACE="/root/clawd"
RESEARCH_DIR="/root/automation_research"
MEMORY_FILE="$WORKSPACE/memory/$(date +%Y-%m-%d).md"
BEST_PATH_FILE="$RESEARCH_DIR/best_path.json"

while true; do
    if [ -f "$BEST_PATH_FILE" ]; then
        echo "## 🤖 Automation Research Update - $(date)" >> "$MEMORY_FILE"
        echo "" >> "$MEMORY_FILE"
        
        # Extract and log best path
        top_strategy=$(jq -r '.top_strategy // "No strategy yet"' "$BEST_PATH_FILE")
        iteration=$(jq -r '.iteration // "0"' "$BEST_PATH_FILE")
        total=$(jq -r '.total_strategies_evaluated // "0"' "$BEST_PATH_FILE")
        
        echo "**Iteration:** $iteration" >> "$MEMORY_FILE"
        echo "**Top Strategy:** $top_strategy" >> "$MEMORY_FILE"
        echo "**Strategies Evaluated:** $total" >> "$MEMORY_FILE"
        
        # Runner-ups
        echo "" >> "$MEMORY_FILE"
        echo "**Runner-ups:**" >> "$MEMORY_FILE"
        jq -r '.runner_ups[]? // empty' "$BEST_PATH_FILE" | while read -r runner; do
            echo "- $runner" >> "$MEMORY_FILE"
        done
        
        echo "" >> "$MEMORY_FILE"
        echo "---" >> "$MEMORY_FILE"
        echo "" >> "$MEMORY_FILE"
        
        echo "[$(date)] Updated memory with iteration $iteration - Top: $top_strategy"
    fi
    
    # Wait 30 minutes
    sleep 1800
done
