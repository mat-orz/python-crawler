from lxml import html, etree
from urllib.parse import urlparse
import requests
import pprint
import json


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
    # Sanitize url: remove urls that start with #, get only part up to # and remove trailing /
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

        # Adding only if it's not empty and not root url
        if len(url) > 0 and url != '/' and url != '':
            unique_urls.add(url)

    # Converting back to list so it can be serializied to json
    if unique_urls:
        return list(unique_urls)
    else:
        return []

def get_elements_by_xpath(page_content, xpaths_list, xpath_name):
    # Executes xpath expression based on name provided on page content. After getting all urls calls function to remove duplicates.
    return get_unique_list_of_urls(page_content.xpath(xpaths_list[xpath_name]))

def get_site_information(url):
    # Returns prepared object with all urls and their type

    # Grabbing domain name and protocol from the url and executing connection to get source code
    page_content = get_page_content(url)

    # Getting all unique urls from page_content based on xpath TODO: could be done better, calling the same function in the same way - leaving for clarity
    child_links = get_elements_by_xpath(page_content, xpaths_list, 'links')
    images = get_elements_by_xpath(page_content, xpaths_list, 'images')
    css = get_elements_by_xpath(page_content, xpaths_list, 'css')
    js = get_elements_by_xpath(page_content, xpaths_list, 'js')

    # Grabbing protocol and domain info.
    protocol_domain =  get_protocol_and_domain(url)

    # Checking domain of all child links and setting is_local
    child_urls = []

    for child_link in child_links:
        child_urls.append({'url' : child_link, 
                        'is_local': is_local_link(child_link, protocol_domain['domain'])})

    return {'url': url, 
            'child_urls': child_urls, 
            'images': images, 
            'css': css, 
            'js': js,
            'protocol': protocol_domain['protocol'],
            'domain': protocol_domain['domain'],
            'is_local': True}


# TODO: Could be stored in a config file instead
xpaths_list = {'links': '//a/@href', 
          'images': '//img/@src',
          'css': "//link[@type='text/css']/@href",
          'js': "//script[@type='text/javascript']/@src"}

print('Using following xpath expressions:')
pprint.pprint(xpaths_list)

# TODO: Add as parameters
url = 'https://wiprodigital.com'
output_filename = 'result.json'

# Grabbing main site protocol and domain
protocol_domain_main_url = get_protocol_and_domain(url)

# TODO: visited_sites and visited_sites_urls could be merged together. 
local_urls_to_crawl = [url]
visited_sites = []
visited_sites_urls = []
external_sites = []

# TODO: Could be done as a recursive function
while len(local_urls_to_crawl) > 0:
    for to_crawl in local_urls_to_crawl:
        if to_crawl not in visited_sites_urls:
            # Grab all info from this site
            
            print('Gathering data from: ' + to_crawl)
            site_data = get_site_information(to_crawl)
            visited_sites.append(site_data)

            # Add to visited site to avoid child elements to be iterated infinitely
            visited_sites_urls.append(to_crawl)

            # Iterate through all links found on the page and add them to the queue
            for child_to_crawl in site_data['child_urls']:
                child_url = child_to_crawl['url']

                if not child_to_crawl['is_local'] and child_url not in external_sites:
                    # Child is external adding just to external sites
                    external_sites.append(child_url)

                elif child_to_crawl['is_local'] and child_url not in local_urls_to_crawl and child_url not in visited_sites_urls:
                    # Adding to to_crawl because it's local
                    local_urls_to_crawl.append(child_url)
                    
        # Finished setting up all the childs, can remove from the queue
        local_urls_to_crawl.remove(to_crawl)
        
# Preparing final object
final_result = {'local_sites': visited_sites, 'external_sites': external_sites}

with open(output_filename, 'w') as outfile:
    json.dump(final_result, outfile)

print('Crawled over ' + str(len(visited_sites)) + ' local sites and detected ' + str(len(external_sites)) + ' external links')
print('Full results with other static resources listed are stored as json file: ' + output_filename)

