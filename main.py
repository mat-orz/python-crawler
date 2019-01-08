from lxml import html, etree
from urllib.parse import urlparse
import requests



def get_protocol_and_domain(url):
    # Returns protocol and domain values of url

    result = {'protocol': '', 'domain': ''}
    if url:
        url_parsed = urlparse(url)
        result.update(protocol = url_parsed.scheme, domain = url_parsed.netloc)

    return result


def external_link(url, domain_main_site):
    # Checks if url is local or external

    prot_domain =  get_protocol_and_domain(url)
    url_domain = prot_domain['domain']
    protocol_url = prot_domain['protocol']

    if url_domain == domain_main_site:
        # Same domain, url is local
        return False
    elif protocol_url:
        # Different domain and has protocol, url is external
        return True
    else:
        # No protocol, url is relative local
        return False

def get_page_content(url):
    #Return page source code given url
    response = requests.get(url)
    return html.fromstring(response.content)

def clean_url(url):
    #Sanitize url
    print('pre: ' + url)
    if url:
        if url[0] == '#':
            url = '/'

        elif '#' in url:
            url = url.split('#')[0]

        if url[-1] == '/':
            url = url[0:-1]
    print('post: ' + url)
    return url

def get_unique_list_of_urls(urls):
    #Cleans and adds links to a set to remove any duplicate value
    unique_urls = set()
    
    for url in urls:
        url = clean_url(url)
        if url and url != '/' and url != '':
            unique_urls.add(url)

    return unique_urls



xpaths_list = {'urls': '//a/@href', 
          'images': '//img/@src',
          'css': ''}

# TODO: Add as parameter
url = 'https://wiprodigital.com'
protocol_domain_main_url = get_protocol_and_domain(url)


page_content = get_page_content(url)


links = page_content.xpath(xpaths_list['urls'])
images = page_content.xpath(xpaths_list['images'])

clean_unique_links = get_unique_list_of_urls(links)

for link in clean_unique_links:
    protocol_domain = get_protocol_and_domain(link) 
    print('url: ' + link)
    print('protocol: ' + protocol_domain['protocol'] + ' domain: ' + protocol_domain['domain'] + ' external?: ' + str(external_link(link, protocol_domain_main_url['domain'])))
    



