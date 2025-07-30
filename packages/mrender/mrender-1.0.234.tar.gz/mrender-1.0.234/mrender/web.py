import re
import traceback
import urllib.parse

import requests
from bs4 import BeautifulSoup
from bs4.builder import HTMLTreeBuilder
from rich.console import Console
from rich.markdown import Markdown as RichMarkdown
from rich.panel import Panel
from rich.text import Text




def is_valid_url(url):  # noqa: ANN201
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

def expand_and_view_webpage(url):
    if not is_valid_url(url):
        return "Invalid URL. Please enter a valid URL including the protocol (e.g., http:// or https://)."
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        content = response.text
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Extract and append links
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            if not href.startswith(('http://', 'https://')):
                href = urllib.parse.urljoin(url, href)
            links.append(f"[{a.text.strip()}]({href})")
        plain_text = '\n\n## Links found on the page:\n\n' + '\n'.join(links) if links else ''
        
        # Extract text content
        text_content = soup.get_text(separator='\n', strip=True)
        
        # Get the prettified HTML content
        prettified_content = soup.prettify()
        
        return f"# Webpage Content\n\n{text_content}\n\n{plain_text}\n\n## Raw HTML:\n\n```html\n{prettified_content}\n```"
    except requests.exceptions.RequestException as e:
        error_message = f"Error fetching the webpage: {str(e)}"
        display_webpage_content(url, error_message)
        return error_message
    except Exception as e:
        error_message = f"Error parsing the webpage: {str(e)}\n\nTraceback:\n{traceback.format_exc()}"
        display_webpage_content(url, error_message)
        return error_message

def display_webpage_content(url, content):
    console = Console()
    title = Text(f"Webpage: {url}", style="bold magenta")
    
    # Clean up the content
    cleaned_content = re.sub(r'\n{3,}', '\n\n', content)  # Remove excessive newlines
    cleaned_content = re.sub(r'\s+', ' ', cleaned_content)  # Replace multiple spaces with single space
    
    # Try to parse content as Markdown
    try:
        md_content = RichMarkdown(cleaned_content)
        panel = Panel(md_content, title=title, expand=True, border_style="cyan", style="magenta on cyan1")
    except:
        # If parsing as Markdown fails, use plain text
        panel = expand_and_view_webpage(url)
    
    console.print(panel)




