from lxml import html, etree
from urllib.parse import urlparse
import requests
import pprint



def get_protocol_and_domain(url):
    # Returns protocol and domain values of url

    result = {'protocol': '', 'domain': ''}
    if url:
        url_parsed = urlparse(url)
        result.update(protocol = url_parsed.scheme, domain = url_parsed.netloc)

    return result


def is_local_link(url, domain_main_site):
    # Checks if url is local or external

    prot_domain =  get_protocol_and_domain(url)
    url_domain = prot_domain['domain']
    protocol_url = prot_domain['protocol']

    if url_domain == domain_main_site:
        # Same domain, url is local
        return True
    elif protocol_url:
        # Different domain and has protocol, url is external
        return False
    else:
        # No protocol, url is relative local
        return True

def get_page_content(url):
    # Return page source code given url
    response = requests.get(url)
    return html.fromstring(response.content)

def clean_url(url):
    # Sanitize url
    if len(url) > 0:
        if url[0] == '#':
            url = '/'

        elif '#' in url:
            url = url.split('#')[0]

        if url[-1] == '/':
            url = url[0:-1]
    return url

def get_unique_list_of_urls(urls):
    # Cleans and adds links to a set to remove any duplicate value
    unique_urls = set()
    
    for url in urls:
        url = clean_url(url)
        if len(url) > 0 and url != '/' and url != '':
            unique_urls.add(url)

    return unique_urls

def get_elements_by_xpath(page_content, xpaths_list, xpath_name):
    # Executes xpath expression based on name provided on page content. After getting all urls calls function to remove duplicates.
    return get_unique_list_of_urls(page_content.xpath(xpaths_list[xpath_name]))

def get_site_information(url):
    # Returns prepared object with all urls and their type

    # Grabbing domain name and protocol from the url and executing connection to get source code
    page_content = get_page_content(url)

    # Getting all unique urls from page_content based on xpath TODO: could be done better, calling the same function in the same way - leaving for clarity
    links = get_elements_by_xpath(page_content, xpaths_list, 'links')
    images = get_elements_by_xpath(page_content, xpaths_list, 'images')
    css = get_elements_by_xpath(page_content, xpaths_list, 'css')
    js = get_elements_by_xpath(page_content, xpaths_list, 'js')

    #Grabbing protocol and domain info.
    protocol_domain =  get_protocol_and_domain(url)

    return {'url': url, 
            'links': links, 
            'images': images, 
            'css': css, 
            'js': js,
            'protocol': protocol_domain['protocol'],
            'domain': protocol_domain['domain']}




# TODO: Could be stored in a config file instead
xpaths_list = {'links': '//a/@href', 
          'images': '//img/@src',
          'css': "//link[@type='text/css']/@href",
          'js': "//script[@type='text/javascript']/@src"}

# TODO: Add as parameter
url = 'https://wiprodigital.com'

# Grabbing main site protocol and domain
protocol_domain_main_url = get_protocol_and_domain(url)

local_urls_to_crawl = [url]
external_urls = {}
visited_sites = {}

while len(local_urls_to_crawl) > 0:
    for to_crawl in local_urls_to_crawl:
        if to_crawl in visited_sites:
            # Seen this site, remove from to crawl
            local_urls_to_crawl.remove(to_crawl)
        else:
            # Grab all info from this site
            site_data = get_site_information(url)

            pprint.pprint(site_data)
            local_urls_to_crawl.remove(to_crawl)


