---
name: pain_point_extraction
description: "Extracts customer pain points and persuasion techniques from competitor ads"
---

# Pain Point Extraction Skill

This skill directs the Ads Manager Agent to analyze scraped competitor ads to map out marketing angles and trading psychological triggers.

## Execution Steps

1. **Update Kanban Board:**
   Call the `update_kanban` tool to move the task "Pain Point Extraction" from "Backlog" to "In Progress".

2. **Load Scraped Ads:**
   Read the contents of the `best_ads_last_30_days.json` file in the outputs directory.

3. **Analyze Copy & Creative:**
   For each ad in the list, extract:
   - **Target Pain Point**: The specific frustration or fear being triggered (e.g., losing money, too much noise, missing trade breakouts, lack of discipline, expensive tools).
   - **Core Promise**: What value or solution the ad guarantees (e.g., higher win rate, real-time news, automated scans, expert community, clear trading setups).
   - **Persuasion Technique**: The psychological driver used (e.g., Fear Of Missing Out (FOMO), authority, social proof, risk reversal, anti-guru authenticity).

4. **Write Outputs:**
   Save the structured analysis list in JSON format to `ad_pain_points.json` in the outputs folder.

5. **Complete Kanban Task:**
   Call the `update_kanban` tool to move the task "Pain Point Extraction" to "Done".
