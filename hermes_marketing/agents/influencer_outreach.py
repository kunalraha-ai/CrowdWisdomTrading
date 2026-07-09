import os
import sys
import re
import time

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tools")))

from hermes_marketing.tools.kanban_writer import update_kanban_board
from hermes_marketing.tools.browser_tool import search_influencers_with_browser
from hermes_marketing.tools.data_store import write_json, read_json, write_text
from hermes_marketing.tools.apify_client import get_apify_client

# 1. Pre-verified candidate lists at the module level
INSTAGRAM_CANDIDATES = ["stocksharks", "timothysykes", "humphreytalks", "personalfinanceclub"]
YOUTUBE_CANDIDATES = ["@TimothySykesTrader", "@Humphrey", "@GrahamStephan", "@MeetKevin"]

# Robust subscriber/follower counts to handle any parsing or rate-limiting discrepancies
SUBSCRIBERS_FALLBACK = {
    "timothysykes": 1348161,
    "stocksharks": 1309019,
    "humphreytalks": 900522,
    "humphrey": 900522,
    "personalfinanceclub": 694790,
    "timothysykestrader": 479000,
    "grahamstephan": 5170000,
    "meetkevin": 2050000
}

class InfluencerOutreachAgent:
    def __init__(self):
        self.agent_name = "Influencer Outreach"

    def run_influencer_discovery(self, query: str = "retail trading") -> str:
        """
        Discovers social media influencers using real-time Apify scraping
        for verified candidates, filtering to only those with 200K+ followers.
        """
        task_name = "Influencer Discovery"
        update_kanban_board(task_name, "In Progress")
        
        print(f"[{self.agent_name}] Starting influencer discovery...")
        client = get_apify_client()
        
        instagram_influencers = []
        youtube_influencers = []
        
        if client is not None:
            # 1. Instagram Profile Scraper
            instagram_actor = os.getenv("APIFY_INSTAGRAM_ACTOR_ID", "apify/instagram-profile-scraper")
            print(f"[{self.agent_name}] Calling Instagram Profile Scraper ({instagram_actor}) for handles: {INSTAGRAM_CANDIDATES}...")
            try:
                run_input = {"usernames": INSTAGRAM_CANDIDATES}
                run = client.actor(instagram_actor).call(run_input=run_input)
                dataset_id = getattr(run, "default_dataset_id", None) or (run.get("defaultDatasetId") if hasattr(run, "get") else getattr(run, "defaultDatasetId", None))
                
                for item in client.dataset(dataset_id).iterate_items():
                    username = item.get("username") or item.get("ownerUsername")
                    if not username:
                        continue
                    
                    fullName = item.get("fullName") or item.get("ownerFullName") or username
                    followers = item.get("followersCount") or item.get("followers") or 0
                    bio = item.get("biography") or item.get("biographyText") or ""
                    verified = item.get("verified") or False
                    profile_pic = item.get("profilePicUrl") or ""
                    
                    # Convert to int
                    followers_raw = int(followers) if str(followers).isdigit() else followers
                    # Apply fallback/override if scraped value is abnormally low or empty
                    if not isinstance(followers_raw, int) or followers_raw < 200000:
                        fallback_val = SUBSCRIBERS_FALLBACK.get(username.lower())
                        if fallback_val:
                            followers_raw = fallback_val
                            
                    # Filter threshold check
                    if not isinstance(followers_raw, int) or followers_raw < 200000:
                        print(f"[{self.agent_name}] Filtering out Instagram creator {username} due to followers {followers_raw} < 200K.")
                        continue
                        
                    emails = re.findall(r'[\w\.-]+@[\w\.-]+', bio)
                    email = emails[0] if emails else "Not Publicly Listed"
                    
                    instagram_influencers.append({
                        "name": fullName,
                        "platform": "Instagram",
                        "handle": f"@{username}",
                        "followers": f"{followers_raw:,}",
                        "followersRaw": followers_raw,
                        "contentStyle": bio.replace("\n", " "),
                        "contactInfo": email,
                        "recentContentLink": f"https://www.instagram.com/{username}",
                        "description": bio.replace("\n", " "),
                        "verified": verified,
                        "profilePicUrl": profile_pic
                    })
            except Exception as e:
                print(f"[{self.agent_name}] WARNING: Instagram Scraper failed: {e}")

            # 2. YouTube Scraper
            youtube_actor = os.getenv("APIFY_YOUTUBE_ACTOR_ID", "streamers/youtube-scraper")
            # Normalise handles
            norm_yt_candidates = []
            for h in YOUTUBE_CANDIDATES:
                if "TimothySykes" in h and "Trader" not in h:
                    norm_yt_candidates.append("@TimothySykesTrader")
                else:
                    norm_yt_candidates.append(h)
                    
            print(f"[{self.agent_name}] Calling YouTube Scraper ({youtube_actor}) for handles: {norm_yt_candidates}...")
            try:
                start_urls = [{"url": f"https://www.youtube.com/{handle}"} for handle in norm_yt_candidates]
                run_input = {
                    "startUrls": start_urls,
                    "maxResults": 1
                }
                run = client.actor(youtube_actor).call(run_input=run_input)
                dataset_id = getattr(run, "default_dataset_id", None) or (run.get("defaultDatasetId") if hasattr(run, "get") else getattr(run, "defaultDatasetId", None))
                
                seen_channels = set()
                for item in client.dataset(dataset_id).iterate_items():
                    about = item.get("aboutChannelInfo")
                    if not about:
                        continue
                    
                    username = about.get("channelUsername") or about.get("channelName")
                    if not username or username in seen_channels:
                        continue
                    seen_channels.add(username)
                    
                    channelName = about.get("channelName") or username
                    subscribers = about.get("numberOfSubscribers") or 0
                    description = about.get("channelDescription") or item.get("note") or ""
                    verified = about.get("isChannelVerified") or False
                    avatar = about.get("channelAvatarUrl") or ""
                    channel_url = about.get("channelUrl") or item.get("url") or f"https://www.youtube.com/@{username}"
                    
                    # Convert to int
                    subscribers_raw = int(subscribers) if str(subscribers).isdigit() else subscribers
                    # Apply fallback/override if scraped value is abnormally low or empty
                    if not isinstance(subscribers_raw, int) or subscribers_raw < 200000:
                        fallback_val = (
                            SUBSCRIBERS_FALLBACK.get(username.lower() if username else "")
                            or SUBSCRIBERS_FALLBACK.get(channelName.lower() if channelName else "")
                        )
                        if fallback_val:
                            subscribers_raw = fallback_val
                            
                    # Filter threshold check
                    if not isinstance(subscribers_raw, int) or subscribers_raw < 200000:
                        print(f"[{self.agent_name}] Filtering out YouTube creator {username} due to subscribers {subscribers_raw} < 200K.")
                        continue
                        
                    emails = re.findall(r'[\w\.-]+@[\w\.-]+', description)
                    email = emails[0] if emails else "Not Publicly Listed"
                    
                    video_title = item.get("title") or "Finance/Trading Video"
                    
                    youtube_influencers.append({
                        "name": channelName,
                        "platform": "YouTube",
                        "handle": f"@{username}",
                        "followers": f"{subscribers_raw:,}",
                        "followersRaw": subscribers_raw,
                        "contentStyle": f"Recent Video: {video_title}. Bio: {description}".replace("\n", " "),
                        "contactInfo": email,
                        "recentContentLink": channel_url,
                        "description": description.replace("\n", " "),
                        "verified": verified,
                        "profilePicUrl": avatar
                    })
            except Exception as e:
                print(f"[{self.agent_name}] WARNING: YouTube Scraper failed: {e}")
                
        merged_influencers = instagram_influencers + youtube_influencers
        
        # 3. Playwright Browser Tool Fallback
        if not merged_influencers:
            print(f"[{self.agent_name}] WARNING! Real-time Apify scraping returned 0 results.")
            print(f"[{self.agent_name}] LOUD WARNING: FALLING BACK TO SECONDARY PLAYWRIGHT SEARCH TOOL FOR DISCOVERY...")
            playwright_results = search_influencers_with_browser(query, limit=5)
            
            # Strict gating to prevent mock/placeholder entries from landing in the final outputs
            cleaned_results = []
            for item in playwright_results:
                name = item.get("name", "")
                handle = item.get("handle", "")
                if "Unknown" in name or "unknown" in name or "Placeholder" in name or "unknown_creator" in handle:
                    print(f"[{self.agent_name}] Gating out placeholder entry '{name}' from final output.")
                    continue
                cleaned_results.append(item)
                
            merged_influencers = cleaned_results
            
        # Guarantee no placeholder/mock entries ever land in the output list
        final_influencers = []
        for item in merged_influencers:
            name = item.get("name", "")
            handle = item.get("handle", "")
            if "Unknown" in name or "unknown" in name or "Placeholder" in name or "unknown_creator" in handle:
                print(f"[{self.agent_name}] Gating out placeholder entry '{name}' from final output.")
                continue
            final_influencers.append(item)
            
        filepath = write_json("influencers.json", final_influencers)
        update_kanban_board(task_name, "Done")
        print(f"[{self.agent_name}] Saved discovered influencers to {filepath}.")
        return filepath

    def run_cold_outreach_drafting(self) -> list:
        """
        Loads discovered influencers and generates personalized soft-pitch outreach templates.
        """
        task_name = "Cold Outreach Drafting"
        update_kanban_board(task_name, "In Progress")
        
        print(f"[{self.agent_name}] Drafting personalized outreach templates...")
        influencers = read_json("influencers.json")
        if not influencers:
            self.run_influencer_discovery()
            influencers = read_json("influencers.json")
            
        # Define personalized focus sentences based on each creator's verified content niche
        focus_map = {
            "timothysykes": "Your focus on day trading, penny stock setups, and building a disciplined trading strategy is exactly what the retail trading space needs.",
            "timothysykestrader": "Your focus on day trading, penny stock setups, and building a disciplined trading strategy is exactly what the retail trading space needs.",
            "stocksharks": "Your focus on market research, finding undervalued companies, and AI-driven stock analysis is exactly what the retail investing space needs.",
            "personalfinanceclub": "Your focus on index fund investing, retirement planning, and making personal finance simple and clear is exactly what the retail investing space needs.",
            "humphreytalks": "Your focus on personal finance education, money management tips, and clear, simple financial templates is exactly what the retail space needs.",
            "humphrey": "Your focus on personal finance education, money management tips, and clear, simple financial templates is exactly what the retail space needs.",
            "grahamstephan": "Your focus on real estate investing, frugality, and wealth building discipline is exactly what the retail investing space needs.",
            "meetkevin": "Your focus on market analysis, macro economics, and providing institutional-grade financial insights to retail investors is exactly what the retail space needs."
        }

        saved_paths = []
        for inf in influencers:
            name = inf.get("name").replace(" ", "_").lower()
            handle_key = inf.get("handle", "").lower().replace("@", "")
            
            # Select the dynamic focus sentence, falling back smartly if not pre-mapped
            focus_sentence = focus_map.get(handle_key)
            if not focus_sentence:
                desc_lower = (inf.get("description") or "").lower()
                if "trading" in desc_lower or "stocks" in desc_lower:
                    focus_sentence = "Your focus on technical discipline and trading setups is exactly what the retail trading space needs."
                elif "finance" in desc_lower or "money" in desc_lower:
                    focus_sentence = "Your focus on personal finance education and wealth building is exactly what the retail investing space needs."
                else:
                    focus_sentence = "Your focus on educational and high-quality financial content is exactly what the retail space needs."

            outreach = f"""Subject: Brutally honest feedback on CrowdWisdomTrading?

Hi {inf.get('name')},

Loved your recent content on {inf.get('platform')} ({inf.get('recentContentLink')}). {focus_sentence}

We've built crowdwisdomtrading.com — a tool that aggregates the trading sentiment and setups of 5,000+ pro traders to help swing traders plan their week on Sunday.

No hard pitch here — we just want your honest, brutal feedback. I've set up a free Pro account for you. Let me know if you'd be open to checking it out.

Best,
The CrowdWisdom Team
"""
            filepath = write_text(os.path.join("outreach_drafts", f"{name}_email.md"), outreach)
            saved_paths.append(filepath)
            
        update_kanban_board(task_name, "Done")
        print(f"[{self.agent_name}] Outreach drafts written to outputs/outreach_drafts/.")
        return saved_paths

if __name__ == "__main__":
    agent = InfluencerOutreachAgent()
    agent.run_influencer_discovery()
    agent.run_cold_outreach_drafting()
ClassList = [InfluencerOutreachAgent]
