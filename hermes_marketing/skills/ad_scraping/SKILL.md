---
name: ad_scraping
description: "Scrapes Meta Ad Library via Apify for trading and investing ads"
---

# Ad Scraping Skill

This skill directs the agent to execute the competitor ad scraping, pain point extraction, and ad copywriting processes by running the Ads Manager Agent.

## Execution Steps

1. Run the Ads Manager Agent script by executing the following command in the terminal:
   `python -m hermes_marketing.agents.ads_manager`

2. Verify from the command output that the Obsidian Kanban board was updated (moved to "In Progress" and then to "Done" for "Ad Scraping", "Pain Point Extraction", and "Ad Script Writer") and that `best_ads_last_30_days.json`, `ad_pain_points.json`, and `noise_short.md` outputs were written to their respective folders.

3. Send a confirmation message to the user summarizing the scraped ads and the copy hooks.
