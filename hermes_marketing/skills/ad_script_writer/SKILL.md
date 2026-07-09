---
name: ad_script_writer
description: "Generates high-converting ad video scripts based on customer pain points"
---

# Ad Script Writer Skill

This skill directs the Ads Manager Agent to draft ad scripts based on CrowdWisdomTrading's value proposition and mapped competitor pain points.

## Execution Steps

1. **Update Kanban Board:**
   Call the `update_kanban` tool to move the task "Ad Script Writer" from "Backlog" to "In Progress".

2. **Read Inputs:**
   - Retrieve positioning details from `competitor_report.md`.
   - Retrieve mapped psychological drivers from `ad_pain_points.json`.

3. **Draft Ad Scripts:**
   Draft at least two distinct video script copies:
   
   - **Script 1 (Short-form TikTok/Reels Style — Focus: Overwhelming Noise)**
     - *Hook (0-3s)*: Visual pattern showing a phone vibrating with 50 discord notifications. "Stop checking 10 different trading groups. You're losing trades because of noise."
     - *Body (3-15s)*: Introduce CrowdWisdomTrading. "What if you could see the exact consensus of 5,000+ professional traders in one dashboard? No chatting, no noise. Just clean entry, targets, and stops."
     - *Call to Action (CTA) (15-20s)*: "Get the Sunday Briefing for free. Link in bio."
   
   - **Script 2 (YouTube Explainer Style — Focus: The Anti-Guru Angle)**
     - *Hook (0-10s)*: "Why do 90% of retail traders lose money? It's not because they don't have charts. It's because they follow single 'gurus' showing rented sports cars."
     - *Body (10-45s)*: Explain the power of Collective Intelligence. "One analyst is guessing. 5,000 professional traders agreeing is a statistical edge. CrowdWisdom Trading aggregates real-time sentiment so you plan your week on Sunday and execute with conviction on Monday."
     - *Call to Action (CTA) (45-60s)*: "Stop guessing. Try the free trial now at crowdwisdomtrading.com."

4. **Write Outputs:**
   Save each script in the `generated_scripts/` directory as markdown files (e.g. `noise_short.md`, `anti_guru_long.md`).

5. **Complete Kanban Task:**
   Call the `update_kanban` tool to move the task "Ad Script Writer" to "Done".
