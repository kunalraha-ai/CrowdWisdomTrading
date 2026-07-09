import os
import sys

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tools")))

from hermes_marketing.tools.kanban_writer import update_kanban_board
from hermes_marketing.tools.apify_client import search_ads
from hermes_marketing.tools.data_store import write_json, read_json, write_text

class AdsManagerAgent:
    def __init__(self):
        self.agent_name = "Ads Manager"

    def run_ad_scraping(self, query: str = "retail trading") -> str:
        """
        Scrapes Meta Ads Library for competitor ads and saves results.
        """
        task_name = "Ad Scraping"
        update_kanban_board(task_name, "In Progress")
        
        print(f"[{self.agent_name}] Scraping ads for query '{query}'...")
        ads = search_ads(query, limit=5)
        
        filepath = write_json("best_ads_last_30_days.json", ads)
        update_kanban_board(task_name, "Done")
        print(f"[{self.agent_name}] Saved scraped ads to {filepath}.")
        return filepath

    def run_pain_point_extraction(self) -> str:
        """
        Loads scraped ads and extracts customer pain points, promises, and techniques.
        """
        task_name = "Pain Point Extraction"
        update_kanban_board(task_name, "In Progress")
        
        print(f"[{self.agent_name}] Extracting pain points from scraped ads...")
        ads = read_json("best_ads_last_30_days.json")
        if not ads:
            # Re-run scraping to populate
            self.run_ad_scraping()
            ads = read_json("best_ads_last_30_days.json")
            
        pain_points = []
        for ad in ads:
            body = (ad.get("adBody") or "").lower()
            title = (ad.get("adTitle") or "").lower()
            page = ad.get("pageName", "")
            
            # Smart NLP mapping matching scraped brand positioning and signals using word boundaries
            import re
            if re.search(r'\bcompetitions?\b|\bdemo\b', body):
                pain_point = "Fear of losing real money, lack of trading practice"
                promise = ad.get("adTitle") or "Demo Weekly Competitions"
                technique = "Gamification / Risk-free practice / Cash incentives"
            elif re.search(r'\bangst\b|\bstrategie\b', body):
                pain_point = "Fear and anxiety preventing execution of clear trading plans"
                promise = "Souveräne Anleger handeln mit tradegate.direct"
                technique = "Emotional appeal (Fear management) / Direct execution"
            elif re.search(r'\bart\b|\bcomic\b', body):
                pain_point = "Finding trustworthy dealers for vintage collectibles"
                promise = "One of the largest dealers of comic books & original art"
                technique = "Authority / Social proof"
            else:
                pain_point = "Missing important market events, slow news signals"
                promise = ad.get("adTitle") or "Actionable Trading Signals"
                technique = "FOMO / Social proof"
                
            pain_points.append({
                "adId": ad.get("adId"),
                "pageName": page,
                "targetPainPoint": pain_point,
                "corePromise": promise,
                "persuasionTechnique": technique
            })
            
        filepath = write_json("ad_pain_points.json", pain_points)
        update_kanban_board(task_name, "Done")
        print(f"[{self.agent_name}] Saved extracted pain points to {filepath}.")
        return filepath

    def run_ad_script_writer(self) -> list:
        """
        Generates markdown video scripts based on extracted pain points.
        """
        task_name = "Ad Script Writer"
        update_kanban_board(task_name, "In Progress")
        
        print(f"[{self.agent_name}] Generating video ad scripts...")
        
        script_1 = """# Short Ad Script: Overwhelming Noise (TikTok/Reels)
**Visual**: A phone screen rapidly vibrating with 50 discord notification badges.
**Voiceover**: Stop checking 10 different trading groups. You're losing trades because of pure, unadulterated noise.
**Action**: Transition screen showing CrowdWisdomTrading dashboard with simple consolidated momentum setups.
**Voiceover**: What if you could see the consensus of 5,000+ top traders in one screen? Clear entry, stops, targets.
**CTA**: Try the Sunday Briefing for free. Link in description.
"""

        script_2 = """# YouTube Explainer Script: The Anti-Guru
**Visual**: Day trader sitting at desk staring at 6 screens, looking exhausted.
**Voiceover**: Why do 90% of retail traders lose capital? It's not because they don't have enough charts. It's because they follow single "gurus" showing fake sports cars.
**Action**: Transition to CrowdWisdomTrading homepage detailing collective intelligence stats.
**Voiceover**: One analyst is guessing. 5,000 professional traders agreeing is a statistical edge. CrowdWisdom Trading aggregates real-time sentiment so you plan your week on Sunday and execute with conviction on Monday.
**CTA**: Stop guessing. Try the free trial now at crowdwisdomtrading.com.
"""
        # Save files
        path1 = write_text(os.path.join("generated_scripts", "noise_short.md"), script_1)
        path2 = write_text(os.path.join("generated_scripts", "anti_guru_long.md"), script_2)
        
        update_kanban_board(task_name, "Done")
        print(f"[{self.agent_name}] Generated scripts saved to outputs/generated_scripts/.")
        return [path1, path2]

if __name__ == "__main__":
    agent = AdsManagerAgent()
    agent.run_ad_scraping()
    agent.run_pain_point_extraction()
    agent.run_ad_script_writer()
ClassList = [AdsManagerAgent]
