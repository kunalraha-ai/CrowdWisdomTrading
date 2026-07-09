import os
import sys

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tools")))

from hermes_marketing.tools.kanban_writer import update_kanban_board
from hermes_marketing.tools.data_store import write_text, read_json

class MarketingManagerAgent:
    def __init__(self):
        self.agent_name = "Marketing Manager"

    def run_competitor_research(self) -> str:
        """
        Orchestrates competitor research and positioning guides.
        """
        task_name = "Competitor Research"
        update_kanban_board(task_name, "In Progress")
        
        print(f"[{self.agent_name}] Starting competitor research and positioning analysis...")
        
        # Simulated/constructed research output (as defined in skill instructions)
        report_content = """# CrowdWisdomTrading Marketing Strategy & Competitor Report

## 1. CrowdWisdomTrading Positioning Guide

### Target Audience
*   **Retail Swing Traders**: Individual traders looking to capture medium-term market swings (holding 2-10 days) without the stress of day-trading.
*   **Crypto Investors**: Investors seeking high-conviction momentum signals on major digital assets.
*   **Part-time Traders**: Professionals with full-time day jobs who need a structured, time-efficient way to plan their weekly trades.

### Core Value Propositions
1.  **Noise Reduction**: Eliminates the cognitive overload of following hundreds of chatrooms, news feeds, and social media commentators.
2.  **Collective Intelligence**: Aggregates the real-time sentiment and conviction of over 5,000 professional traders to extract high-probability consensus ideas.
3.  **Actionable Setups**: Provides complete, structured "Pro setups" with clear Entry, Target, and Stop-Loss levels.
4.  **Time Efficiency**: Designed around a "Sunday read, Monday act" workflow, requiring minimal mid-week monitoring.

### Tone of Voice Guide
*   **Professional**: Data-backed, educational, and risk-focused.
*   **Realistic**: Open about probabilities; does not promise quick riches or 100% win rates.
*   **Direct & Clear**: Bullet points, transparent numbers, and actionable takeaways over hype.

---

## 2. Competitor Comparison Matrix

| Competitor | Product Focus | Estimated Pricing | Signals / Alerts Offered | Content Style | Social Presence |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TradingView** | Charting & Social Network | Free - $60/month | User-submitted trading ideas, custom indicator alerts. | Informational & Community-driven | Very High (Millions of users, active Twitter/X, YouTube) |
| **Benzinga Pro** | Real-Time News & Squawk | $99 - $177/month | News flashes, analyst rating upgrades/downgrades, audio squawk. | Fast-paced, news-focused, high urgency | High (Well-known financial media company) |
| **Trade Ideas** | Automated AI Scanners | $84 - $189/month | Real-time automated stock scanners, buy/sell AI signals. | Analytical, technical, tool-heavy | Medium (Highly valued by technical day traders) |
| **Stock Dads** | Community & Education | $50 - $150/month | Direct options/stock alerts, educational guides, parental community. | Warm, educational, community-centric | Medium-High (Strong presence on Twitter/X, Discord) |

---

## 3. Positioning Gap & Opportunity
Most competitors focus on providing **more information** (faster news feeds, more indicators, more chat messages). This leads to **information overload**.

**CrowdWisdomTrading's Opportunity:** Position the platform as the **filters of the noise**. We don't give traders more charts or faster headlines; we give them the **distilled consensus** of 5,000+ experts. This makes it the ultimate solution for busy retail traders seeking peace of mind and clarity.
"""
        filepath = write_text("competitor_report.md", report_content)
        update_kanban_board(task_name, "Done")
        print(f"[{self.agent_name}] Saved competitor research to {filepath}.")
        return filepath

    def run_social_post_repurposer(self) -> str:
        """
        Repurposes ad scripts into organic social media copy for X and LinkedIn.
        """
        task_name = "Social Post Repurposer"
        update_kanban_board(task_name, "In Progress")
        
        print(f"[{self.agent_name}] Repurposing generated ad scripts into organic posts...")
        
        # Check for generated script or fall back
        script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "outputs", "generated_scripts"))
        script_path = os.path.join(script_dir, "noise_short.md")
        
        script_excerpt = ""
        if os.path.exists(script_path):
            with open(script_path, "r", encoding="utf-8") as f:
                script_excerpt = f.read()
        
        social_content = """# Organic X Post (Thread Option)
1/ Most retail traders lose money because of 1 simple trap:
Cognitive Overload.

Too many feeds, too many Discord rooms, too many gurus.
It's pure noise.

Here is the antidote... 👇

2/ Instead of chasing 50 alerts, follow Collective Intelligence.
We aggregate the real-time conviction of 5,000+ professional traders.

No chatter. No hype.
Just clear entry, target, and stop loss levels.

3/ The rhythm is simple:
Sunday Read. Monday Act.

Plan your entire trading week in 15 minutes.
Try the Sunday Briefing for free: crowdwisdomtrading.com

---

# Organic LinkedIn Post
I spent years jumping from one Discord trading group to another, looking for the ultimate signal provider. 

What I found was information overload. Every "guru" had a different, conflicting opinion. 

That is why we built CrowdWisdomTrading. 

Instead of relying on a single source of advice, our platform aggregates the sentiment and conviction of over 5,000 professional traders. 

We filter the noise, giving you clean, actionable setups with clear entry, target, and stop-loss levels. 

"Sunday Read. Monday Act." 

Reduce your cognitive load. Try the free trial today at crowdwisdomtrading.com.

#TradingStrategy #CollectiveIntelligence #RiskManagement #RetailTrading
"""
        filepath = write_text("social_posts_drafts.md", social_content)
        update_kanban_board(task_name, "Done")
        print(f"[{self.agent_name}] Saved repurposed posts to {filepath}.")
        return filepath

if __name__ == "__main__":
    agent = MarketingManagerAgent()
    agent.run_competitor_research()
    agent.run_social_post_repurposer()
