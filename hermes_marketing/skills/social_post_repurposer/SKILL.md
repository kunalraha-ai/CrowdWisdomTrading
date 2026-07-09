---
name: social_post_repurposer
description: "Repurposes high-converting ad scripts into engaging organic posts for X and LinkedIn"
---

# Social Post Repurposer Skill (Custom Module)

This skill directs the Marketing Agent to take the generated video ad scripts and transform them into engaging organic copy for social media distribution.

## Execution Steps

1. **Update Kanban Board:**
   Call the `update_kanban` tool to move the task "Social Post Repurposer" from "Backlog" to "In Progress".

2. **Load Generated Scripts:**
   Scan and read the generated scripts from the `generated_scripts/` directory.

3. **Repurpose for X (Twitter):**
   - Focus on an attention-grabbing hook (e.g. "Most retail traders lose money because of 1 simple trap: Noise...").
   - Use high-readability spacing and bullet points.
   - Design it as a single high-impact post or a short thread.
   - Include relevant tags and a clean CTA to sign up for predictions.

4. **Repurpose for LinkedIn:**
   - Use a story-based professional hook ("I spent years jumping from one Discord trading group to another...").
   - Contrast individual opinion with the power of aggregated consensus data (Collective Intelligence).
   - Use professional formatting (clear headings, whitespace).
   - End with a low-friction invitation to try the free Sunday briefing.

5. **Write Outputs:**
   Save the drafted posts in a file named `social_posts_drafts.md` in the outputs folder.

6. **Complete Kanban Task:**
   Call the `update_kanban` tool to move the task "Social Post Repurposer" to "Done".
