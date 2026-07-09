---
name: influencer_discovery
description: "Discovers retail trading influencers with large followings"
---

# Influencer Discovery Skill

This skill directs the agent to execute the influencer discovery, metrics validation, and outreach drafting processes by running the Influencer Outreach Agent.

## Execution Steps

1. Run the Influencer Outreach Agent script by executing the following command in the terminal:
   `cd "C:\Users\kunal\OneDrive\pineapple\Ma4rketing Agent" && python -m hermes_marketing.agents.influencer_outreach`

2. Verify from the command output that the Obsidian Kanban board was updated (moved to "In Progress" and then to "Done" for both "Influencer Discovery" and "Cold Outreach Drafting") and that `influencers.json` and outreach drafts in `outputs/outreach_drafts/` were written successfully.

3. Send a confirmation message to the user summarizing the discovered creators.
