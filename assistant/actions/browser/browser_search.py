from assistant.actions.base_tool import BaseTool, ToolType
from assistant.actions.browser.browser import Browser
from assistant.config.settings import SEARCH_ENGINE

from pathlib import Path

LOG_DIR = Path("logs") / "test"
LOG_DIR.mkdir(parents=True, exist_ok=True)

class BrowserSearchTool(BaseTool):
    name = "browser_search"

    description = "Search the web and return structured search results."

    tool_type = ToolType.REASONING

    parameters = {
        "query": "string"
    }

    examples = [
        "Search latest AI news",
        "Search Python tutorials",
        "Find OpenAI website",
        "Search weather in Chennai",
        "Look up machine learning"
    ]

    def execute(self, query: str, **kwargs):

        browser = Browser()
        page = browser.launch()

        page.goto(
            SEARCH_ENGINE.format(query=query.replace(" ", "+"))
        )

        page.wait_for_load_state("networkidle")


        page.screenshot(
            path=str(LOG_DIR / "duckduckgo.png")
        )

        results = []

        search_results = page.locator("article").all()

        for result in search_results[:5]:

            try:
                title = result.locator("h2").inner_text()

                link = result.locator("a").first.get_attribute("href")

                snippet = ""

                try:
                    snippet = result.locator("[data-result='snippet']").inner_text()
                except:
                    pass

                results.append({
                    "title": title,
                    "url": link,
                    "snippet": snippet
                })

            except:
                continue

        browser.close()

        return {
            "success": True,
            "response": None,
            "data": {
                "query": query,
                "results": results
            },
            "llm": True
        }