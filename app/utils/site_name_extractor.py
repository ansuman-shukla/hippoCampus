from urllib.parse import urlparse

async def extract_site_name(url: str) -> str:
    # If the URL doesn't start with a scheme, add "http://"
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    
    # Parse the URL
    parsed = urlparse(url)
    domain = parsed.netloc  # e.g., "www.something.com"
    
    # Remove any leading "www."
    if domain.startswith("www."):
        domain = domain[4:]
    
    # Split the domain by '.' and take the first part as the site name
    # (this will work for "something.com", "something.ai", etc.)
    site_name = domain.split('.')[0]
    return site_name
