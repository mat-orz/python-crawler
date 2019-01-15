from urllib.parse import urlparse
import requests
import pprint
import json
from operator import itemgetter
import sys
from lxml import html


class PythonCrawler(object):

    def __init__(self, url, output_filename):
        self.url = url
        self.output_filename = output_filename

        # TODO: visited_sites and visited_sites_urls could be merged together.
        self.local_urls_to_crawl = [url]
        self.visited_sites = []
        self.visited_sites_urls = []
        self.external_sites = []

        # TODO: Could be stored in a config file instead
        self.xpaths_list = {'links': '//a/@href', 
                'images': '//img/@src',
                'css': "//link[@type='text/css']/@href",
                'js': "//script[@type='text/javascript']/@src"}
                
        # Debug TODO: Add as parameters
        self.execs = 0
        self.execs_limit = 2
        self.debug_flag = False

    def get_protocol_and_domain(self, url):
        # Returns protocol and domain values of url

        result = {'protocol': '', 'domain': ''}
        if url:
            url_parsed = urlparse(url)
            result.update(protocol = url_parsed.scheme, domain = url_parsed.netloc)

        return result

    def is_local_link(self, url, domain_main_site):
        # Checks if url is local or external

        prot_domain =  self.get_protocol_and_domain(url)
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

    def get_page_content(self, url):
        # Return page source code given url
        response = requests.get(url)
        return html.fromstring(response.content)

    def clean_url(self, url):
        # Sanitize url: remove urls that start with #, get only part up to # and remove trailing /
        if len(url) > 0:
            if url[0] == '#':
                url = '/'

            elif '#' in url:
                url = url.split('#')[0]

            if url[-1] == '/':
                url = url[0:-1]

        return url.strip()

    def get_unique_list_of_urls(self, urls):
        # Cleans and adds links to a set to remove any duplicate value
        unique_urls = set()
        
        for url in urls:
            url = self.clean_url(url)

            # Adding only if it's not empty and not root url
            if len(url) > 0 and url != '/' and url != '':
                unique_urls.add(url)

        # Converting back to list so it can be serializied to json
        if unique_urls:
            return sorted(list(unique_urls))
        else:
            return []

    def get_elements_by_xpath(self, page_content, xpaths_list, xpath_name):
        # Executes xpath expression based on name provided on page content. After getting all urls calls function to remove duplicates.
        return self.get_unique_list_of_urls(page_content.xpath(xpaths_list[xpath_name]))

    def get_site_information(self, url):
        # Returns prepared object with all urls and their type

        # Grabbing domain name and protocol from the url and executing connection to get source code
        page_content = self.get_page_content(url)

        # Getting all unique urls from page_content based on xpath TODO: could be done better, calling the same function in the same way - leaving for clarity
        child_links = self.get_elements_by_xpath(page_content, self.xpaths_list, 'links')
        images = self.get_elements_by_xpath(page_content, self.xpaths_list, 'images')
        css = self.get_elements_by_xpath(page_content, self.xpaths_list, 'css')
        js = self.get_elements_by_xpath(page_content, self.xpaths_list, 'js')

        # Grabbing protocol and domain info.
        protocol_domain = self.get_protocol_and_domain(url)

        # Checking domain of all child links and setting is_local
        child_urls = []

        for child_link in child_links:
            child_urls.append({'url' : child_link, 
                            'is_local': self.is_local_link(child_link, protocol_domain['domain'])})

        return {'url': url, 
                'child_urls': child_urls, 
                'images': images, 
                'css': css, 
                'js': js,
                'protocol': protocol_domain['protocol'],
                'domain': protocol_domain['domain'],
                'is_local': True}


    def local_get(self, url):
        p_url = urlparse(url)
        filename = url2pathname(p_url.path)
        return open(filename, 'rb')

    # TODO: Split into smaller pieced to test each part individually
    def execute(self):

        print('Using following xpath expressions:')
        pprint.pprint(self.xpaths_list)

        # Grabbing main site protocol and domain
        protocol_domain_main_url = self.get_protocol_and_domain(self.url)

        # TODO: Could be done as a recursive function
        while len(self.local_urls_to_crawl) > 0:
            for to_crawl in self.local_urls_to_crawl:
                if to_crawl not in self.visited_sites_urls:

                    # Grab all info from this site
                    print('Gathering data from: ' + to_crawl)
                    site_data = self.get_site_information(to_crawl)

                    # Add to visited site to avoid child elements to be iterated infinitely
                    self.visited_sites_urls.append(to_crawl)

                    # Iterate through all links found on the page and add them to the queue
                    for child_to_crawl in site_data['child_urls']:
                        child_url = child_to_crawl['url']

                        if not child_to_crawl['is_local'] and child_url not in self.external_sites:
                            # Child is external adding just to external sites
                            self.external_sites.append(child_url)

                        elif child_to_crawl['is_local'] and child_url not in self.local_urls_to_crawl and child_url not in self.visited_sites_urls:
                            # Adding to to_crawl because it's local
                            self.local_urls_to_crawl.append(child_url)
                    
                    # Debug
                    if self.debug_flag:
                        pprint.pprint(site_data)
                        self.execs = self.execs + 1
                    # Appending all info to visited_sites, removing child urls so it's more readable in the final form
                    del site_data['child_urls']
                    self.visited_sites.append(site_data)
                            
                # Finished setting up all the childs, can remove from the queue
                self.local_urls_to_crawl.remove(to_crawl)

                # Debug
                if self.execs >= self.execs_limit:
                    self.local_urls_to_crawl = []
                    break

        # Sorting to make a pseudo json sitemap
        visited_sites = sorted(self.visited_sites, key=itemgetter('url'))
        external_sites = sorted(self.external_sites)

        # Preparing final object
        final_result = {'local_sites': visited_sites, 'external_sites': external_sites}

        with open(self.output_filename, 'w') as outfile:
            json.dump(final_result, outfile, sort_keys=True, indent=4)

        print('Crawled over ' + str(len(visited_sites)) + ' local sites and detected ' + str(len(external_sites)) + ' external links')
        print('Full results with other static resources listed are stored as json file: ' + self.output_filename)

