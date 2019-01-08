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



url =  'https://buildit.wiprodigital.com/'
protocol_domain_main_url = get_protocol_and_domain(url)
response = requests.get(url)

tree = html.fromstring(response.content)
links = tree.xpath('//a/@href')

uniqueLocalURLs = set()

for link in links:
    protocol_domain = get_protocol_and_domain(link) 
    
    print(link )
    print('protocol: ' + protocol_domain['protocol'] + ' domain: ' + protocol_domain['domain'] + ' external?: ' + str(external_link(link, protocol_domain_main_url['domain'])))
    



