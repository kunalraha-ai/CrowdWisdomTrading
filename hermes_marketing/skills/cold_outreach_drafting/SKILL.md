---
name: cold_outreach_drafting
description: "Drafts personalized, soft-pitch outreach emails/DMs for discovered influencers"
---

# Cold Outreach Drafting Skill

This skill directs the Influencer Outreach Agent to draft high-converting, personalized messaging templates for the discovered influencer list.

## Execution Steps

1. **Update Kanban Board:**
   Call the `update_kanban` tool to move the task "Cold Outreach Drafting" from "Backlog" to "In Progress".

2. **Load Influencers:**
   Read the `influencers.json` database from the outputs folder.

3. **Draft Personalized outreach:**
   For each influencer:
   - Reference their specific platform and style.
   - Craft a soft-touch pitch (e.g. "Hey [Name], loved your recent video on price action. We've built a dashboard aggregating consensus from 5,000+ traders. We'd love your honest, brutal feedback on it — no string attached, here is a free pro account...").
   - Maintain a respectful, peer-to-peer tone (no corporate jargon or hard sales pitch).
   - Tailor the communication channel (e.g., email format for YouTube creators, short DM format for X/Twitter creators).

4. **Write Outputs:**
   Save each outreach draft inside the `outreach_drafts/` directory as individual markdown files (e.g. `rayner_teo_email.md`, `ricky_gutierrez_email.md`).

5. **Complete Kanban Task:**
   Call the `update_kanban` tool to move the task "Cold Outreach Drafting" to "Done".
