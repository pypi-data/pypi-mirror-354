import os
from duckduckgo_search import DDGS
from serpapi import SerpApiClient

def web_search(max_results: int = 10, **kwargs) -> str:
    """
    Performs a DuckDuckGo web search based on your query (think a Google search) then returns the top search results.
    If DuckDuckGo search fails, it falls back to SerpAPI.

    Args:
        query (str): The search query to perform.
        max_results (int, optional): Maximum number of results to return. Defaults to 10.
        **kwargs: Additional keyword arguments to pass to DDGS.

    Returns:
        str: Formatted string containing search results.

    Raises:
        ImportError: If the duckduckgo_search or serpapi package is not installed.
        Exception: If no results are found for the given query via both DuckDuckGo and SerpAPI, or if the SerpAPI key is not found.

    Note:
        For SerpAPI fallback, the SERPAPI_API_KEY environment variable must be set.
    """
    try:
        ddgs_instance = DDGS()
    except ImportError as e:
        raise ImportError("You must install package `duckduckgo_search` to run this function: for instance run `pip install duckduckgo-search`.") from e

    try:
        query = kwargs['query']
        results = ddgs_instance.text(query, max_results=max_results)
        if len(results) == 0:
            raise Exception("No results found via DuckDuckGo.")

        postprocessed_results = [f"[{result['title']}]({result['href']})\n{result['body']}" for result in results]
        
        return "## Search Results (via DuckDuckGo)\n\n" + "\n\n".join(postprocessed_results)
        
    except Exception as e:
        # print(f"DuckDuckGo search failed: {e}. Falling back to SerpAPI.")
        # If the exception was the specific DDGS ImportError, we re-raise it directly if it wasn't caught above.
        # However, the structure above should prevent it from reaching here.
        # The primary purpose of this block is to catch runtime errors from ddgs.text or the "No results" exception.

        api_key = os.environ.get("SERPAPI_API_KEY")
        if not api_key:
            raise Exception("SerpAPI key not found. Please set the SERPAPI_API_KEY environment variable.")

        try:
            client = SerpApiClient({"api_key": api_key})
        except ImportError as serp_e:
            raise ImportError("You must install package `serpapi` to run this function: for instance run `pip install google-search-results`.") from serp_e
        
        search_params = {
            "engine": "google",
            "q": query,
            "num": max_results  # SerpAPI uses 'num' for number of results
        }
        serp_results = client.search(search_params)

        if "organic_results" in serp_results and serp_results["organic_results"]:
            organic_results = serp_results["organic_results"]
            postprocessed_results = [f"[{result['title']}]({result['link']})\n{result.get('snippet', '')}" for result in organic_results]
            return "## Search Results (via SerpAPI)\n\n" + "\n\n".join(postprocessed_results)
        else:
            raise Exception(f"No results found via DuckDuckGo or SerpAPI! Original error: {e}")