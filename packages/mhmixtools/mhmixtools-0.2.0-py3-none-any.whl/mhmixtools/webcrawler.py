import requests, bs4, logging, json, csv
from urllib.parse import urljoin, urlparse

# Scope: Web crawling and link extraction utilities.
# Get internal links from a page	get_internal_links(url)
# Get external links	get_external_links(url)
# Get image URLs	get_image_links(url)
# Crawl and map all reachable internal URLs	crawl_site(url, depth=2)
# Check which pages return errors	check_broken_pages(url_list)
# Build a summary report	generate_site_report(url, depth=2)

# seltup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_internal_links(url):
    """Extract internal links from a given URL."""
    # check if the URL is valid and accessible
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
    except requests.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return []
    # Parse the page content
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    internal_links = set()
    base_domain = urlparse(url).netloc
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        full_url = urljoin(url, href)
        # Check if the link is internal (same domain)
        if urlparse(full_url).netloc == base_domain:
            internal_links.add(full_url)
    return list(internal_links)


def get_external_links(url):
    """Extract external links from a given URL."""
    # check if the URL is valid and accessible
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
    except requests.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return []
    # Parse the page content
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    external_links = set()
    base_domain = urlparse(url).netloc
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        full_url = urljoin(url, href)
        # Check if the link is external (different domain)
        if urlparse(full_url).netloc != base_domain:
            external_links.add(full_url)
    return list(external_links)

def get_image_links(url):
    """Extract image URLs from a given URL."""
    # check if the URL is valid and accessible
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
    except requests.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return []
    # Parse the page content
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    image_links = set()
    for img_tag in soup.find_all('img', src=True):
        src = img_tag['src']
        full_url = urljoin(url, src)
        image_links.add(full_url)
    return list(image_links)

def crawl_site(url, depth=2):
    """Crawl a website and map all reachable internal URLs."""
    logging.info(f"Starting crawl at {url} with depth {depth}")
    visited = set()
    to_visit = [(url, 0)]  # (URL, current depth)
    internal_links = []

    while to_visit:
        current_url, current_depth = to_visit.pop(0)
        if current_url in visited or current_depth > depth:
            continue
        logging.info(f"Crawling: {current_url} (depth {current_depth})")
        visited.add(current_url)

        # Get internal links from the current URL
        links = get_internal_links(current_url)
        logging.info(f"Found {len(links)} internal links on {current_url}")
        internal_links.extend(links)

        # Add new links to the queue for further crawling
        for link in links:
            if link not in visited:
                to_visit.append((link, current_depth + 1))

    logging.info(f"Crawling finished. Total unique internal links found: {len(set(internal_links))}")
    return list(set(internal_links))  # Return unique internal links


def check_broken_pages(url_list):
    """Check which pages in a list return errors."""
    broken_pages = []
    for url in url_list:
        try:
            response = requests.get(url)
            if response.status_code != 200:
                logging.warning(f"Broken page found: {url} (Status code: {response.status_code})")
                broken_pages.append((url, response.status_code))
        except requests.RequestException as e:
            logging.error(f"Error accessing {url}: {e}")
            broken_pages.append((url, str(e)))
    return broken_pages

def generate_site_report(url, depth=2):
    """Generate a summary report of the site, including internal links, external links, images, and broken pages."""
    logging.info(f"Generating site report for {url} with depth {depth}")
    internal_links = crawl_site(url, depth)
    external_links = []
    image_links = []
    broken_pages = []

    # Collect external links and images from each internal link
    for link in internal_links:
        external_links.extend(get_external_links(link))
        image_links.extend(get_image_links(link))

    # Check for broken pages
    broken_pages = check_broken_pages(internal_links)

    report = {
        'internal_links': list(set(internal_links)),
        'external_links': list(set(external_links)),
        'image_links': list(set(image_links)),
        'broken_pages': broken_pages
    }

    logging.info("Site report generated successfully.")
    return report

def print_site_report(report):
    """Pretty-print the site report."""
    print("\n📄 Site Report")
    print("=" * 40)
    print(f"🧭 Internal Links ({len(report['internal_links'])}):")
    for link in report['internal_links']:
        print(f"  - {link}")

    print(f"\n🌐 External Links ({len(report['external_links'])}):")
    for link in report['external_links']:
        print(f"  - {link}")

    print(f"\n🖼️ Image Links ({len(report['image_links'])}):")
    for link in report['image_links']:
        print(f"  - {link}")

    print(f"\n🚨 Broken Pages ({len(report['broken_pages'])}):")
    for url, reason in report['broken_pages']:
        print(f"  - {url} ({reason})")
    print("=" * 40)

def save_site_report(report, filename='site_report.json', format='json'):
    """Save the site report to a file (json or csv)."""
    if format == 'json':
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=4)
        logging.info(f"Report saved to {filename}")
    elif format == 'csv':
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Type', 'URL', 'Extra'])
            for link in report['internal_links']:
                writer.writerow(['Internal', link, ''])
            for link in report['external_links']:
                writer.writerow(['External', link, ''])
            for link in report['image_links']:
                writer.writerow(['Image', link, ''])
            for url, reason in report['broken_pages']:
                writer.writerow(['Broken', url, reason])
        logging.info(f"Report saved to {filename}")
    else:
        logging.error("Unsupported format. Use 'json' or 'csv'.")

