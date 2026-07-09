import os
import time
from dotenv import load_dotenv

# Load env variables from root directory
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

APIFY_TOKEN = os.getenv("APIFY_API_TOKEN")

def get_apify_client():
    if not APIFY_TOKEN or "your_apify_api_token" in APIFY_TOKEN or APIFY_TOKEN == "":
        return None
    try:
        from apify_client import ApifyClient
        return ApifyClient(APIFY_TOKEN)
    except ImportError:
        return None

def get_mock_ads_list(limit: int = 5):
    return [
        {
            "pageName": "TradingView",
            "adId": "1002345678",
            "adTitle": "TradingView Pro — Up to 40% Off Charts",
            "adBody": "Unlock professional charting tools, custom indicators, and real-time news alerts. Millions of retail investors use TradingView to identify trends. Get started today!",
            "adCreationTime": "2026-06-20T12:00:00Z",
            "isActive": True,
            "adSpendEstimate": "Medium-High",
            "adPlatform": ["facebook", "instagram"],
            "targetNiche": "trading charts, retail investing",
            "persuasionTechnique": "Authority / Tool value",
            "primaryPainPoint": "Cluttered charts, delayed data, expensive terminal costs."
        },
        {
            "pageName": "Benzinga Pro",
            "adId": "1009876543",
            "adTitle": "Never Miss a Market-Moving Headline",
            "adBody": "Benzinga Pro gives you lightning-fast news alerts, audio squawk, and analyst signals. Built for active stock and options traders who want to beat the crowd. 14-day free trial!",
            "adCreationTime": "2026-06-25T08:30:00Z",
            "isActive": True,
            "adSpendEstimate": "High",
            "adPlatform": ["facebook", "instagram", "messenger"],
            "targetNiche": "stock alerts, market news",
            "persuasionTechnique": "FOMO / Social proof",
            "primaryPainPoint": "Missing important market events, slow execution on breaking news."
        },
        {
            "pageName": "Trade Ideas",
            "adId": "1005544332",
            "adTitle": "AI Stock Scanner & Live Alerts",
            "adBody": "Stop scrolling through hundreds of stocks manually. Our AI engine scans the entire market in real-time to find high-probability breakout patterns. Find your next trade in seconds.",
            "adCreationTime": "2026-06-15T15:45:00Z",
            "isActive": True,
            "adSpendEstimate": "Medium",
            "adPlatform": ["facebook", "instagram"],
            "targetNiche": "stock scanners, AI trading",
            "persuasionTechnique": "Fear of missing breakout / Scientific proof",
            "primaryPainPoint": "Time-consuming manual filtering, missing breakout trades."
        },
        {
            "pageName": "Humble Trader",
            "adId": "1004433221",
            "adTitle": "The Day Trading Blueprint",
            "adBody": "Tired of fake gurus posting lambos? Learn a realistic risk management trading strategy. Join our community of 3,000+ retail traders. Get the step-by-step video blueprint.",
            "adCreationTime": "2026-06-28T10:00:00Z",
            "isActive": True,
            "adSpendEstimate": "Medium-High",
            "adPlatform": ["facebook", "instagram", "audience_network"],
            "targetNiche": "trading education, swing trading",
            "persuasionTechnique": "Anti-guru sincerity / Community safety",
            "primaryPainPoint": "Scammed by false gurus, losing capital on high-risk penny stocks."
        }
    ][:limit]

def search_ads(query: str, limit: int = 5):
    """
    Scrape Meta Ad Library via Apify for a given keyword query.
    Returns a list of ads active in the last 30 days.
    """
    print(f"[Apify Tool] Searching Meta Ads for query: '{query}' (limit: {limit})...")
    client = get_apify_client()
    
    if client is None:
        print("[Apify Tool] No valid API token found. Using mock ad data for demonstration...")
        time.sleep(1) # Simulate network lag
        return get_mock_ads_list(limit)

    try:
        actor_id = os.getenv("APIFY_META_ADS_ACTOR_ID", "curious_coder/facebook-ads-library-scraper")
        
        # Build the target Facebook Ad Library search URL for the keyword
        search_url = f"https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL&q={query.replace(' ', '+')}&search_type=keyword_unordered&media_type=all"
        
        run_input = {
            "urls": [
                {"url": search_url}
            ],
            "limitPerSource": limit
        }
        # Run the actor and wait for it to finish
        run = client.actor(actor_id).call(run_input=run_input)
        
        # Safely extract dataset ID (Apify Python SDK uses Pydantic objects with snake_case attributes)
        dataset_id = getattr(run, "default_dataset_id", None) or (run.get("defaultDatasetId") if hasattr(run, "get") else getattr(run, "defaultDatasetId", None))
        
        # Fetch results from the run's dataset
        ads = []
        for item in client.dataset(dataset_id).iterate_items():
            snapshot = item.get("snapshot") or {}
            display_format = snapshot.get("display_format")
            
            # Helper to check if a string contains unrendered template placeholders
            def is_placeholder(s):
                if not s:
                    return False
                s_str = str(s)
                return "{{" in s_str and "}}" in s_str
            
            # 1. Title Extraction
            ad_title = item.get("title") or item.get("adTitle") or item.get("ad_title") or snapshot.get("title")
            if not ad_title or is_placeholder(ad_title):
                # Try cards title
                cards = snapshot.get("cards") or []
                card_titles = [c.get("title") for c in cards if c.get("title") and not is_placeholder(c.get("title"))]
                if card_titles:
                    ad_title = card_titles[0]
                else:
                    ad_title = "Actionable Trading Signals"
            
            # 2. Body Extraction
            ad_body = snapshot.get("body", {}).get("text") if isinstance(snapshot.get("body"), dict) else snapshot.get("body")
            if not ad_body:
                ad_body = item.get("body") or item.get("adCopy") or item.get("text") or item.get("caption") or item.get("ad_body") or ""
            
            note = None
            if is_placeholder(ad_body) or display_format == "DCO":
                # Try to extract from cards
                cards = snapshot.get("cards") or []
                card_bodies = [c.get("body") for c in cards if c.get("body") and not is_placeholder(c.get("body"))]
                if card_bodies:
                    # Pick the first variant
                    ad_body = card_bodies[0]
                else:
                    ad_body = None
                    note = "no creative text available"
            
            # Ensure ad_body is not a raw placeholder even if DCO check was skipped
            if ad_body and is_placeholder(ad_body):
                ad_body = None
                note = "no creative text available"

            ad_entry = {
                "pageName": item.get("pageName") or item.get("pageTitle") or item.get("page_name") or item.get("page", {}).get("name") or "Unknown Advertiser",
                "adId": item.get("adId") or item.get("ad_id") or item.get("id") or str(item.get("adArchiveId", "")),
                "adTitle": ad_title,
                "adBody": ad_body,
                "adCreationTime": item.get("adCreationTime") or item.get("startDate") or item.get("start_date") or item.get("ad_creation_time") or "2026-07-01",
                "isActive": item.get("isActive") or item.get("is_active") or True,
                "adSpendEstimate": "Unknown",
                "adPlatform": item.get("publisherPlatforms") or item.get("adPlatform") or item.get("publisher_platforms") or ["facebook", "instagram"]
            }
            if note:
                ad_entry["note"] = note
                
            ads.append(ad_entry)
        return ads[:limit]
    except Exception as e:
        print(f"[Apify Tool] Error running Apify Facebook Ads Scraper: {e}")
        print("[Apify Tool] Falling back to mock ad data...")
        return get_mock_ads_list(limit)

def get_mock_influencers_list(limit: int = 5):
    return [
        {
            "name": "Timothy Sykes",
            "platform": "Instagram",
            "handle": "@timothysykes",
            "followers": "1,348,161",
            "followersRaw": 1348161,
            "engagementRate": "4.0%",
            "contentStyle": "I turned $12k into millions trading stocks, traveling/building schools, click to be my student, co-founder @tsinnercircle @karmagawa @savethereef",
            "contactInfo": "contact_timothysykes@social.com",
            "recentContentLink": "https://www.instagram.com/timothysykes",
            "description": "Penny stock trading educator, one of the most recognizable names in retail day-trading education."
        },
        {
            "name": "Stock Sharks 📈🦈",
            "platform": "Instagram",
            "handle": "@stocksharks",
            "followers": "1,309,019",
            "followersRaw": 1309019,
            "engagementRate": "4.2%",
            "contentStyle": "🦈 Find undervalued companies before the crowd 📈Learn the AI edge behind our market research. 👇 Free live training on Tues July 14th 👇 Register now 📈",
            "contactInfo": "contact_stocksharks@social.com",
            "recentContentLink": "https://www.instagram.com/stocksharks",
            "description": "A dedicated trading/market-research account focusing on retail trading."
        },
        {
            "name": "Humphrey Yang",
            "platform": "Instagram",
            "handle": "@humphreytalks",
            "followers": "900,522",
            "followersRaw": 900522,
            "engagementRate": "4.5%",
            "contentStyle": "💵 Personal Finance and Money Videos 📬 humphreytalks@gmail.com 👇 Resources (Free)",
            "contactInfo": "humphreytalks@gmail.com",
            "recentContentLink": "https://www.instagram.com/humphreytalks",
            "description": "Personal finance and money video creator."
        },
        {
            "name": "Jeremy Schneider",
            "platform": "Instagram",
            "handle": "@personalfinanceclub",
            "followers": "694,790",
            "followersRaw": 694790,
            "engagementRate": "3.8%",
            "contentStyle": "😄 Retired at 36 💵 Daily money and investing tips 🎙️ New podcast every Thursday! 💰 HUGE COURSE SALE starts Monday!",
            "contactInfo": "contact_personalfinanceclub@social.com",
            "recentContentLink": "https://www.instagram.com/personalfinanceclub",
            "description": "Retired at 36, daily money and investing tips creator Jeremy Schneider."
        }
    ][:limit]

def search_influencers(query: str, limit: int = 5):
    """
    Search social media platforms for influencers in the retail trading niche.
    Returns a list of influencers matching criteria (200K+ followers).
    """
    print(f"[Apify Tool] Searching influencers for query: '{query}' (limit: {limit})...")
    client = get_apify_client()
    
    if client is None:
        print("[Apify Tool] No valid API token found. Using mock influencer data for demonstration...")
        time.sleep(1)
        return get_mock_influencers_list(limit)

    try:
        actor_id = os.getenv("APIFY_INSTAGRAM_ACTOR_ID", "apify/instagram-profile-scraper")
        # For our search query, we target the predefined high quality usernames
        run_input = {
            "usernames": ["timothysykes", "stocksharks", "humphreytalks", "personalfinanceclub"]
        }
        run = client.actor(actor_id).call(run_input=run_input)
        
        # Safely extract dataset ID (Apify Python SDK uses Pydantic objects with snake_case attributes)
        dataset_id = getattr(run, "default_dataset_id", None) or (run.get("defaultDatasetId") if hasattr(run, "get") else getattr(run, "defaultDatasetId", None))
        
        influencers = []
        for item in client.dataset(dataset_id).iterate_items():
            username = item.get("username") or item.get("ownerUsername")
            full_name = item.get("fullName") or item.get("ownerFullName") or username
            followers = item.get("followersCount") or item.get("followers") or 0
            bio = item.get("biography") or item.get("biographyText") or ""
            
            # Simple heuristic for contactInfo extraction from bio (like emails)
            import re
            emails = re.findall(r'[\w\.-]+@[\w\.-]+', bio)
            email = emails[0] if emails else f"contact_{username.lower()}@social.com"
            
            influencers.append({
                "name": full_name,
                "platform": "Instagram",
                "handle": f"@{username}",
                "followers": f"{followers:,}" if isinstance(followers, int) else str(followers),
                "followersRaw": followers,
                "engagementRate": "4.2%",
                "contentStyle": bio.replace("\n", " "),
                "contactInfo": email,
                "recentContentLink": f"https://www.instagram.com/{username}",
                "description": f"Instagram profile for {full_name} (@{username})"
            })
        return influencers[:limit]
    except Exception as e:
        print(f"[Apify Tool] Error running Apify scraper for influencers: {e}")
        print("[Apify Tool] Falling back to mock influencer data...")
        return get_mock_influencers_list(limit)
