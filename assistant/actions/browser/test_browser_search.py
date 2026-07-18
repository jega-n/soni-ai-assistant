from pprint import pprint

from assistant.actions.browser.browser_search import BrowserSearchTool

tool = BrowserSearchTool()

result = tool.execute("latest AI news")

pprint(result)