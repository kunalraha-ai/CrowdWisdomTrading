import os
import sys
import pytest

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from hermes_marketing.agents.marketing_manager import MarketingManagerAgent
from hermes_marketing.agents.ads_manager import AdsManagerAgent
from hermes_marketing.agents.influencer_outreach import InfluencerOutreachAgent
from hermes_marketing.tools.kanban_writer import read_kanban

def test_marketing_manager_agent():
    agent = MarketingManagerAgent()
    
    # Run competitor research
    report_path = agent.run_competitor_research()
    assert os.path.exists(report_path)
    
    # Check that competitor research is now Done on Kanban board
    content = read_kanban()
    assert "## Done" in content
    assert "- [x] Competitor Research" in content
    
    # Run post repurposer
    posts_path = agent.run_social_post_repurposer()
    assert os.path.exists(posts_path)
    content = read_kanban()
    assert "- [x] Social Post Repurposer" in content

def test_ads_manager_agent():
    agent = AdsManagerAgent()
    
    # Run ad scraping, extraction, and script writing
    ads_path = agent.run_ad_scraping()
    assert os.path.exists(ads_path)
    
    pe_path = agent.run_pain_point_extraction()
    assert os.path.exists(pe_path)
    
    script_paths = agent.run_ad_script_writer()
    for p in script_paths:
        assert os.path.exists(p)
        
    content = read_kanban()
    assert "- [x] Ad Scraping" in content
    assert "- [x] Pain Point Extraction" in content
    assert "- [x] Ad Script Writer" in content

def test_influencer_outreach_agent():
    agent = InfluencerOutreachAgent()
    
    # Run influencer discovery and outreach
    disc_path = agent.run_influencer_discovery()
    assert os.path.exists(disc_path)
    
    outreach_paths = agent.run_cold_outreach_drafting()
    for p in outreach_paths:
        assert os.path.exists(p)
        
    content = read_kanban()
    assert "- [x] Influencer Discovery" in content
    assert "- [x] Cold Outreach Drafting" in content
