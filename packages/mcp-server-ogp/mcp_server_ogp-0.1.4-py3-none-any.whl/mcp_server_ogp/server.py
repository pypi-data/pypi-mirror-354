import io
import re
import logging
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import httpx
from bs4 import BeautifulSoup
from fastmcp import FastMCP, Image
from PIL import Image as PILImage
from mcp.shared.exceptions import McpError
from mcp.types import ErrorData, INVALID_PARAMS, INTERNAL_ERROR
from pydantic import BaseModel, Field, ConfigDict, HttpUrl

# Configure logging
logger = logging.getLogger(__name__)

# Create an MCP server instance
mcp = FastMCP("OGP Information Server")


# Pydantic models for data validation
class OGPInfo(BaseModel):
    """Model for OGP information."""

    model_config = ConfigDict(extra="allow")

    title: Optional[str] = Field(default=None, description="Page title")
    description: Optional[str] = Field(default=None, description="Page description")
    image: Optional[str] = Field(default=None, description="OGP image URL")
    url: Optional[str] = Field(default=None, description="Page URL")
    type: Optional[str] = Field(default=None, description="Content type")
    site_name: Optional[str] = Field(default=None, description="Site name")


class OGPInfoRequest(BaseModel):
    """Model for OGP information request parameters."""

    model_config = ConfigDict(extra="forbid")

    url: HttpUrl = Field(description="The URL of the web page to extract OGP information from")


class OGPImageRequest(BaseModel):
    """Model for OGP image request parameters."""

    model_config = ConfigDict(extra="forbid")

    url: HttpUrl = Field(description="The URL of the web page to extract the OGP image from")


async def fetch_html(url: str) -> str:
    """
    Asynchronously fetch HTML content from a specified URL.

    This function sends an HTTP request to a web page and returns the HTML content
    as a string. It includes timeout handling and error management for robust operation.

    Args:
        url: The target URL to fetch content from

    Returns:
        HTML content as a string

    Raises:
        httpx.HTTPError: When HTTP-related errors occur
        Exception: For any other unexpected errors
    """
    logger.debug(f"Fetching HTML from URL: {url}")
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, follow_redirects=True)
            response.raise_for_status()
            
            logger.debug(f"Successfully fetched HTML from {url}, content length: {len(response.text)}")
            return response.text
    
    except httpx.HTTPError as e:
        logger.error(f"HTTP error fetching {url}: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error fetching {url}: {e}")
        raise


def extract_ogp_info(html: str, base_url: str) -> OGPInfo:
    """
    Extract Open Graph Protocol (OGP) information from HTML content.

    This function parses HTML content to find OGP meta tags and returns
    the information in a structured OGPInfo model. If OGP tags are not found,
    it attempts to extract alternative information from basic HTML tags.

    Args:
        html: The HTML content to parse
        base_url: Base URL for converting relative URLs to absolute URLs

    Returns:
        OGPInfo model containing the extracted OGP information
    """
    logger.debug(f"Extracting OGP info from HTML content (length: {len(html)})")
    
    soup = BeautifulSoup(html, 'html.parser')
    ogp_data = {}

    # Search for OGP meta tags and extract information
    ogp_tags = soup.find_all('meta', property=lambda x: x and x.startswith('og:'))
    
    logger.debug(f"Found {len(ogp_tags)} OGP meta tags")

    for tag in ogp_tags:
        property_name = tag.get('property')
        content = tag.get('content')

        if property_name and content:
            # Remove "og:" prefix to create clean key names
            key = property_name.replace('og:', '')
            ogp_data[key] = content.strip()

    # Fallback processing when OGP tags are not found
    if 'title' not in ogp_data:
        title_tag = soup.find('title')
        if title_tag:
            ogp_data['title'] = title_tag.get_text().strip()

    if 'description' not in ogp_data:
        desc_tag = soup.find('meta', attrs={'name': 'description'})
        if desc_tag:
            content = desc_tag.get('content', '').strip()
            if content:
                ogp_data['description'] = content

    # Convert relative image URLs to absolute URLs
    if 'image' in ogp_data:
        ogp_data['image'] = urljoin(base_url, ogp_data['image'])

    logger.debug(f"Extracted OGP data: {list(ogp_data.keys())}")
    
    return OGPInfo(**ogp_data)


async def fetch_image_data(image_url: str) -> Optional[Image]:
    """
    Fetch image data from a URL and return it as an optimized Image object.

    This function downloads an image file from the specified URL, processes it
    using PIL for optimization, and returns it as a FastMCP Image object.

    Args:
        image_url: The URL of the image to fetch

    Returns:
        FastMCP Image object containing optimized image data
        Returns None if fetching fails
    """
    logger.debug(f"Fetching image from URL: {image_url}")
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(image_url, follow_redirects=True)
            response.raise_for_status()

            logger.debug(f"Downloaded image, size: {len(response.content)} bytes")

            # Process image data with PIL for optimization
            image = PILImage.open(io.BytesIO(response.content)).convert('RGB')
            
            original_size = image.size
            logger.debug(f"Original image size: {original_size}")

            # Apply size constraints to prevent memory issues with very large images
            max_size = (1200, 1200)
            if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
                image.thumbnail(max_size, PILImage.Resampling.LANCZOS)
                logger.debug(f"Resized image to: {image.size}")

            # Optimize the image for efficient storage and transmission
            buffer = io.BytesIO()
            image.save(buffer, format="JPEG", quality=80, optimize=True)
            
            logger.debug(f"Optimized image, final size: {len(buffer.getvalue())} bytes")

            return Image(data=buffer.getvalue(), format="jpeg")

    except Exception as e:
        logger.error(f"Failed to fetch image from {image_url}: {str(e)}")
        return None


@mcp.tool()
async def ogp_info(url: str) -> Dict[str, Any]:
    """
    Extract Open Graph Protocol (OGP) information from a specified URL.

    This function retrieves OGP metadata from web pages, which is commonly used
    for social media sharing previews. It extracts information like title,
    description, image URL, site name, and other OGP properties.

    Args:
        url: The URL of the web page to extract OGP information from

    Returns:
        Dictionary containing OGP metadata:
        - title: Page title
        - description: Page description
        - image: OGP image URL
        - url: Page URL
        - type: Content type
        - site_name: Site name
        - Other OGP properties as available

    Raises:
        McpError: When URL is invalid, fetching fails, or parsing errors occur
    """
    # Validate and create request model
    try:
        request = OGPInfoRequest(url=url)
    except Exception as e:
        logger.error(f"OGP info request validation failed: {str(e)}")
        raise McpError(
            ErrorData(code=INVALID_PARAMS, message=f"Invalid URL parameter: {str(e)}")
        )

    try:
        # Fetch HTML content from the target URL
        html_content = await fetch_html(str(request.url))

        # Extract OGP information from the HTML
        ogp_data = extract_ogp_info(html_content, str(request.url))

        # Convert to dictionary and return
        result = ogp_data.model_dump(exclude_none=True)
        
        logger.info(f"Successfully extracted OGP info from {url}")
        return result

    except httpx.HTTPError as e:
        logger.error(f"HTTP error extracting OGP info from {url}: {e}")
        raise McpError(
            ErrorData(
                code=INTERNAL_ERROR,
                message=f"Failed to fetch HTML from {url}: {e!r}"
            )
        )
    except Exception as e:
        logger.error(f"Unexpected error extracting OGP info from {url}: {e}")
        raise McpError(
            ErrorData(
                code=INTERNAL_ERROR,
                message=f"Unexpected error while extracting OGP info from {url}: {e!r}"
            )
        )


@mcp.tool()
async def ogp_image(url: str) -> Optional[Image]:
    """
    Retrieve the OGP image from a specified URL and return it as an optimized Image object.

    This function first extracts OGP information to locate the image URL,
    then downloads and processes the image using PIL for optimization.
    The result is returned as a FastMCP Image object.

    Args:
        url: The URL of the web page to extract the OGP image from

    Returns:
        FastMCP Image object containing the optimized OGP image data
        Returns None if no image is found or if an error occurs

    Raises:
        McpError: When URL is invalid, fetching fails, or image processing errors occur
    """
    # Validate and create request model
    try:
        request = OGPImageRequest(url=url)
    except Exception as e:
        logger.error(f"OGP image request validation failed: {str(e)}")
        raise McpError(
            ErrorData(code=INVALID_PARAMS, message=f"Invalid URL parameter: {str(e)}")
        )

    try:
        # First, extract OGP information to find the image URL
        html_content = await fetch_html(str(request.url))
        ogp_data = extract_ogp_info(html_content, str(request.url))

        # Check if OGP image URL exists
        image_url = ogp_data.image
        if not image_url:
            logger.info(f"No OGP image found for {url}")
            return None

        # Fetch and process the image data
        image_data = await fetch_image_data(image_url)
        
        if image_data:
            logger.info(f"Successfully extracted OGP image from {url}")
        else:
            logger.warning(f"Failed to fetch OGP image from {url}")

        return image_data

    except httpx.HTTPError as e:
        logger.error(f"HTTP error extracting OGP image from {url}: {e}")
        raise McpError(
            ErrorData(
                code=INTERNAL_ERROR,
                message=f"Failed to fetch HTML from {url}: {e!r}"
            )
        )
    except Exception as e:
        logger.error(f"Unexpected error extracting OGP image from {url}: {e}")
        raise McpError(
            ErrorData(
                code=INTERNAL_ERROR,
                message=f"Unexpected error while extracting OGP image from {url}: {e!r}"
            )
        )
