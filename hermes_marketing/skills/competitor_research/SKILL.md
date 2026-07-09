---
name: competitor_research
description: "Generates CrowdWisdomTrading positioning guide and competitor comparison report"
---

# Competitor Research & Marketing Strategy Skill

This skill directs the agent to execute the competitor research, positioning analysis, and social post repurposing processes by running the Marketing Manager Agent.

## Execution Steps

1. Run the Marketing Manager Agent script by executing the following command in the terminal:
   `cd "C:\Users\kunal\OneDrive\pineapple\Ma4rketing Agent" && python -m hermes_marketing.agents.marketing_manager`

2. Verify from the command output that the Obsidian Kanban board was updated (moved to "In Progress" and then to "Done" for both "Competitor Research" and "Social Post Repurposer") and that `competitor_report.md` and `social_posts_drafts.md` were written to the outputs directory.

3. Send a confirmation message to the user summarizing the positioning and comparison results.
