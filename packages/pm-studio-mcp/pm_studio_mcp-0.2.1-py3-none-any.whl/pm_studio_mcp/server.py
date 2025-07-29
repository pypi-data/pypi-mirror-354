from mcp.server.fastmcp import FastMCP
import asyncio
import os
from typing import List, Dict, Optional
from datetime import datetime
from pm_studio_mcp.utils.file_utils import FileUtils
from pm_studio_mcp.utils.search_utils import SearchUtils
from pm_studio_mcp.utils.data_visualization_utils import DataVisualizationUtils
from pm_studio_mcp.utils.graph.auth import AuthUtils
from pm_studio_mcp.utils.graph.chat import ChatUtils
from pm_studio_mcp.utils.graph.calendar import CalendarUtils
from pm_studio_mcp.skills.greeting import GreetingUtils
from pm_studio_mcp.utils.titan_metadata_utils import TitanMetadataUtils
from pm_studio_mcp.constant import *
from pm_studio_mcp.utils.crawl_utils import CrawlerUtils
from pm_studio_mcp.utils.titan_query_utils import TitanQuery
from pm_studio_mcp.config import config
import logging

# Create MCP server instance with uppercase log level
logging.basicConfig(level=logging.INFO)
mcp = FastMCP("pm-studio-mcp", settings={"log_level": "INFO"})

# All business logic and tool functions below, use config.XXX directly for configuration.
# For example: config.WORKING_PATH, config.REDDIT_CLIENT_ID, config.DATA_AI_API_KEY, etc.

@mcp.tool()
async def greeting_with_pm_studio(name: str):  # this is the one of the tool of my MCP server
    """
    Respond to a greeting message with a formatted template.
    """
    return GreetingUtils.greeting_with_pm_studio(name)

@mcp.tool()
async def google_web_tool(keywords: List[str], num_results: int = 10):
    """
    Perform a Google web search with the given keywords and return search result URLs.

    Args:
        keywords: List of search keywords
        num_results: Number of search results to return (default: 10)

    Returns:
        List of search result URLs
    """
    return SearchUtils.search_google(keywords, num_results)


@mcp.tool()
async def convert_to_markdown_tool(file_path: str):
    """
    Convert a document (doc/excel/ppt/pdf/images/csv/json/xml) to markdown format using MarkItDown.

    Args:
        file_path (str): Path to the input document file

    Returns:
        str: Path to the generated markdown file or error message
    """
    return FileUtils.convert_to_markdown_tool(file_path, config.WORKING_PATH)

@mcp.tool()
async def scrape_reddit_tool(
    subreddit_name: str,
    keywords: List[str],
    post_limit: int = 100,
    time_filter: str = "month"
):
    """
    Scrape posts from a Reddit subreddit and filter by keywords.
    
    Args:
        subreddit_name: Name of the subreddit to scrape
        keywords: List of keywords to filter posts by
        post_limit: Maximum number of posts to retrieve (default: 100)
        time_filter: Time filter for posts (default: "month")
        
    Returns:
        Dictionary with status and results including path to CSV file with scraped posts
    """
    return SearchUtils.scrape_reddit(
        subreddit_name,
        keywords,
        post_limit,
        time_filter,
        config.WORKING_PATH
    )

@mcp.tool()
async def crawl_website_tool(
    url: str, 
    max_pages: int = 5, 
    timeout: int = 30, 
    selectors: Optional[List[str]] = None,
    deep_crawl: Optional[str] = None, 
    question: Optional[str] = None
):
    """
    Crawl web page content from given URLs and output as markdown file.

    Args:
        url (str): URL to crawl
        max_pages (int): Maximum number of pages to crawl (default: 5)
        timeout (int): Timeout in seconds for each request (default: 30)
        selectors (List[str], optional): CSS selectors to extract specific content
        deep_crawl (str, optional): Strategy for deep crawling ('bfs' or 'dfs')
        question (str, optional): Specific question for LLM extraction

    Returns:
        dict: Dictionary with crawl results and status including path to output files
    """
    try:
        result = await CrawlerUtils.crawl_website(
            url=url,
            timeout=timeout,
            working_dir=config.WORKING_PATH
        )
        return result
    except Exception as e:
        import time
        error_file = os.path.join(config.WORKING_PATH, f"error_{int(time.time())}.md")
        with open(error_file, 'w') as f:
            f.write(f"# Error crawling {url}\n\n{str(e)}")
            
        return {
            "status": "error",
            "message": f"Failed to crawl website: {str(e)}",
            "url": url,
            "output_file": error_file,
            "markdown_path": error_file
        }

#@mcp.tool()
#async def login():
#   """
#    start authentication process against MSAL.
#
#    Returns:
#        bool: True if authentication is not needed, False otherwise
#    """
#    return AuthUtils().login()

@mcp.tool()
async def scrape_app_reviews_tool(
    product_id: str = None,
    market: str = "google-play",
    start_date: str = None,
    end_date: str = None,
    countries: List[str] = None,
    rating: List[int] = None,
    version: str = "all"
):
    """
    Fetch app reviews from data.ai API and save them to a CSV file.
       Args: 
        product_id: App ID of the product (optional, uses DATA_AI_GOOGLE_PLAY_ID or DATA_AI_APP_STORE_ID if not provided)
        market: Market - one of 'ios', 'mac', or 'google-play' (default: 'google-play')
        start_date: Start date in format YYYY-MM-DD (default: 30 days ago)
        end_date: End date in format YYYY-MM-DD (default: today)
        countries: List of country codes (iOS only)
        rating: List of ratings to filter by (1-5)
        version: App version or 'all' (default: 'all')

    Returns:
        Dictionary with status and results including path to CSV file with scraped app reviews
    """
    return SearchUtils.scrape_app_reviews(
        product_id,
        market,
        start_date,
        end_date,
        countries,
        rating,
        version,
        config.WORKING_PATH
    )

@mcp.tool()
async def send_message_to_chat_tool(type: str, topic: str, message: str):
    """
    Send a note to a group chat in Microsoft Teams using MS Graph API.

    Args:
        type (str): The type of chat to send the message to. Can be "myself" or "group".
        topic (str): The topic of the group chat. Only used if type is "group".
        message (str): The message to send.  

    Returns:
        dict: Dictionary containing status and response data
    """
    return ChatUtils.send_message_to_chat(type, topic, message)

@mcp.tool()
async def get_calendar_events(start_date: str, end_date: str):
    """
    get the calendar events from Microsoft Graph API.
    Args:
        start_date: Start date in ISO format withh Beijing timezone, e.g. 2023-10-01T00:00:00+08:00
        end_date: End date in ISO format withh Beijing timezone, e.g. 2023-10-31T23:59:59+08:00
    Returns:
        dict: Dictionary containing status and response data
    """
    return CalendarUtils.get_calendar_events(start_date, end_date)

@mcp.tool()
async def generate_data_visualization(visualization_type: str, data_source: str, chart_options: Dict):
    """
    Generate data visualizations using the DataVisualizationUtils unified chart generation interface.
    
    Args:
        visualization_type: Type of visualization to generate ('bar', 'line', 'pie', 'scatter')
        data_source: Path to the data source file (.csv or .xlsx), or a dictionary of data
        chart_options: Dictionary containing options for the chart:
            - title: Chart title (optional, defaults to a suitable title based on chart type)
            - filename: Name for the output file (optional, defaults to a suitable name based on chart type)
            - figsize: Figure size as a tuple of (width, height) in inches (optional)
            - dpi: Resolution in dots per inch (optional)
            - Various chart-specific parameters:
                - For pie charts: category_column, value_column, autopct, startangle, etc.
                - For bar charts: x_column, y_column, orientation, etc.
                - For line charts: x_column, y_columns, markers, etc.
                - For scatter plots: x_column, y_column, hue_column, size_column, etc.
            
    Returns:
        dict: Dictionary containing:
            - success (bool): Whether the chart was generated successfully
            - output_path (str): Path to the generated chart file
            - message (str): Success or error message
            - data: The extracted data used to generate the chart
            - chart_type: The type of chart generated
            - timestamp: ISO format timestamp when the chart was generated
    """
    try:
        # Use the unified chart generation interface
        # Note: convert_visualization_type is now called automatically in generate_chart
        return DataVisualizationUtils.generate_chart(
            chart_type=visualization_type,
            data_source=data_source,
            **chart_options
        )
    
    except Exception as e:
        return {"success": False, "message": f"Error generating visualization: {str(e)}"}

@mcp.tool()
async def titan_query_data_tool(query_str: str, table: str):
    """
    Query data from Titan API and save results to a CSV file.
    """
    try:
        titan_query = TitanQuery(
            titan_client_id=config.TITAN_CLIENT_ID,
            microsoft_tenant_id=config.MICROSOFT_TENANT_ID,
            titan_endpoint=config.TITAN_ENDPOINT,
            titan_scope=config.TITAN_SCOPE
        )
        result = titan_query.query_data_from_titan_tool(
            query_str=query_str,
            table=table,
            output_dir=config.WORKING_PATH
        )
        return result
    except Exception as e:
        return {
            "error": str(e)
        }

@mcp.tool()
async def titan_search_table_metadata_tool(table_name: str):
    """
    Search for SQL templates based on template name or description keyword.
    This tool performs exact and fuzzy matching on SQL templates.

    Args:
        table_name (str): Template name or keyword (e.g., "mac_dau", "retention by browser")

    Returns:
        dict: Dictionary containing search results
            - status: Search status ("success" or "error")
            - message: Status message with summary of found templates
            - template_matches: List of matching templates with their table info:
                - table: Table name containing the template
                - template: Template name
                - description: Template description
                - table_description: Table description
                - filter_columns: Filter configurations
            - result_path: Path to the saved JSON file (if templates found)
    """
    return TitanMetadataUtils.find_templates_tool(table_name, config.WORKING_PATH)

@mcp.tool()
async def titan_generate_sql_from_template_tool(template_name: str, filter_values: dict = None):
    """
    Generate SQL query from a template with provided filter values.
    This tool generates executable SQL by replacing placeholders in the template with provided filter values.

    Args:
        template_name (str): Name of the SQL template to use (obtained from search_table_metadata_tool)
        filter_values (dict, optional): Dictionary of filter values to apply to the template.
            Keys should match the filter column names in the template.
            If not provided, default values will be used where available.

    Returns:
        dict: Dictionary containing:
            - status: "success", "error", or "warning"
            - message: Status message
            - sql: Generated SQL query (if successful)
            - template_info: Original template information
            - filter_values: Applied filter values (including default values)
            - used_default_values: Dictionary of values that used defaults (if any)
            - remaining_filters: List of optional filters that were not provided (if warning)
    """
    return TitanMetadataUtils.generate_sql_from_template(
        template_name=template_name,
        filter_values=filter_values
    )

def serve():
    mcp.run(transport='stdio')
