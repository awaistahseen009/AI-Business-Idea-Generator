import os
from typing import Optional, List, Dict
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper

class WebSearchService:
    def __init__(self):
        self.api_key = os.getenv('TAVILY_API_KEY')
        try:
            # LangChain community wrapper reads TAVILY_API_KEY from env
            self.wrapper = TavilySearchAPIWrapper()
        except Exception as e:
            print(f"Failed to initialize Tavily wrapper: {e}")
            self.wrapper = None

    def search(self, query: str, max_results: int = 5) -> Optional[Dict[str, object]]:
        """
        Perform web search using Tavily (LangChain Community wrapper)
        Returns dict with keys:
          - text: formatted string for prompting
          - sources: list[{title, url}]
        """
        if not self.api_key or not self.wrapper:
            print("Warning: TAVILY_API_KEY not found or Tavily wrapper not initialized. Web search disabled.")
            return None

        try:
            # Get structured results (list of dicts with title, content, url)
            results: List[Dict[str, str]] = self.wrapper.results(query=query, max_results=max_results)

            sources: List[Dict[str, str]] = []
            # Build a pseudo 'data' compatible with previous formatter
            formatted_sections = []
            for i, res in enumerate(results[:3], 1):
                title = res.get('title', '').strip()
                content = (res.get('content', '') or '').strip()
                url = res.get('url', '').strip()
                if not title and not content:
                    continue
                if len(content) > 300:
                    content = content[:300] + '...'
                section = f"{i}. {title}\n{content}\n"
                if url:
                    section += f"Source: {url}\n"
                    sources.append({"title": title or url, "url": url})
                formatted_sections.append(section)

            formatted_text = "Recent Market Insights:\n" + ("\n".join(formatted_sections) if formatted_sections else "No relevant market data found.")
            return {"text": formatted_text.strip(), "sources": sources}

        except Exception as e:
            print(f"Web search error: {e}")
            return None
    
    # Deprecated: kept for reference only; formatting now handled inline
    def _format_results(self, data: dict) -> str:
        return ""
