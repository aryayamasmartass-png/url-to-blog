import sys
import asyncio

# CRITICAL: Set Windows event loop policy BEFORE importing crawl4ai
# This is needed because uvicorn --reload spawns a new process
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

from typing import Optional
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

class CrawlerService:
    def __init__(self):
        self.browser_config = BrowserConfig(
            headless=True,
            viewport_width=1920,
            viewport_height=1080,
            verbose=True
        )
        
        # Pruning filter to remove ads/nav/footer
        md_generator = DefaultMarkdownGenerator(
            content_filter=PruningContentFilter(
                threshold=0.4, 
                threshold_type="fixed",
                min_word_threshold=10
            )
        )
        
        self.crawler_config = CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            # remove_overlay_elements=True, # Note: some versions use different config names, double check if error persists
            wait_for_images=True,
            markdown_generator=md_generator,
            word_count_threshold=10
        )

    async def crawl(self, url: str) -> Optional[str]:
        async with AsyncWebCrawler(config=self.browser_config) as crawler:
            result = await crawler.arun(
                url=url,
                config=self.crawler_config
            )

            if not result.success:
                print(f"Error crawling {url}: {result.error_message}")
                return None

            print(f"Successfully crawled {url}")

            # Safe access for fit_markdown (handles v0.4+ structure)
            # Check if markdown_v2 (object) exists, otherwise fallback
            if hasattr(result, 'markdown_v2') and result.markdown_v2:
                # Prioritize fit_markdown, fall back to raw_markdown
                return result.markdown_v2.fit_markdown or result.markdown_v2.raw_markdown
            
            # Fallback for older versions or if object structure differs
            if hasattr(result, 'markdown') and hasattr(result.markdown, 'fit_markdown'):
                return result.markdown.fit_markdown
            
            # Final fallback to raw string
            return str(result.markdown) if result.markdown else ""
