import sys
import python_crawler
import pytest
import requests
import pprint
from unittest.mock import Mock
from requests.models import Response
from lxml import html

## Creates crawler instance as fixture for pytest

@pytest.fixture
def crawler():
    # TODO: Add some control logic & add as parameters
    url = 'https://wiprodigital.com/'
    output_filename = 'output/sitemap-test.json'
    print('Creating crawler instance. url: ' + url + ' output: '+ output_filename)
    return python_crawler.PythonCrawler(url, output_filename)


## Testing get_protocol_and_domain and is_local_link functions

def test_domain_protocol_local_external_logic(crawler):
    
    # All cases scenarios
    domain_main_site = 'wiprodigital.com'
    mock_url_local_1 = crawler.url
    mock_url_local_2 = '#something'
    mock_url_local_3 = 'https://wiprodigital.com/test/page'
    mock_url_ext_1 = 'https://www.google.com'
   
    # Assume protocol ok, domain ok, is local
    prot_domain = crawler.get_protocol_and_domain(mock_url_local_1)
    is_local = crawler.is_local_link(mock_url_local_1, domain_main_site)
    assertion1 = len(prot_domain['protocol']) > 0 and len(prot_domain['domain']) > 0 and is_local

    # Assume protocol ko, domain ko, is local
    prot_domain = crawler.get_protocol_and_domain(mock_url_local_2)
    is_local = crawler.is_local_link(mock_url_local_2, domain_main_site)
    assertion2 = len(prot_domain['protocol']) == 0 and len(prot_domain['domain']) == 0 and is_local

    # Assume protocol ok, domain ok, is local
    prot_domain = crawler.get_protocol_and_domain(mock_url_local_3)
    is_local = crawler.is_local_link(mock_url_local_3, domain_main_site)
    assertion3 = len(prot_domain['protocol']) > 0 and len(prot_domain['domain']) > 0 and is_local

    # Assume protocol ok, domain ok, is external
    prot_domain = crawler.get_protocol_and_domain(mock_url_ext_1)
    is_local = crawler.is_local_link(mock_url_ext_1, domain_main_site)
    assertion4 = len(prot_domain['protocol']) > 0 and len(prot_domain['domain']) > 0 and not is_local

    assert assertion1 and assertion2 and assertion3 and assertion4

## Testing url sanitizer

def test_url_sanitizer(crawler):
    
    # TODO: Add more tests with spaces
    trailing_slash = 'test/'
    contains_hash = 'test#page'
    starts_with_hash = '#test'
    with_spaces = '  ' + trailing_slash

    assertion1 = crawler.clean_url(trailing_slash) == 'test'
    assertion2 = crawler.clean_url(contains_hash) == 'test'
    assertion3 = crawler.clean_url(starts_with_hash) == ''
    assertion4 = crawler.clean_url(with_spaces) == 'test'

    assert assertion1 and assertion2 and assertion3 and assertion4

## Testing unique lists

def test_unique_list(crawler):
    
    # Adding all cases
    mock_urls = {
        'test.com',     # Assume added as first
        '#test',        # Assume ignored
        'test.com/1',   # Assume added as second
        '',             # Assume ignored
        '/'             # Assume ignored
    }

    # Expected result
    to_compare = ['test.com', 'test.com/1']

    # Creating unique list
    cleaned_list = crawler.get_unique_list_of_urls(mock_urls)
    pprint.pprint(cleaned_list)

    # Checking if values are the same
    same_values = True
    for index, value in enumerate(cleaned_list):
        if value != to_compare[index]:
            same_values = False  
    
    assert len(cleaned_list) == len(to_compare) and same_values

## Testing xpaths TODO: Make a local mock site

def test_xpaths(crawler):

    # Running xpath on js objects
    js_mock = '<script type="text/javascript" src="x.js"></script><s><script type="text/javascript" src="xy.js"></s>'
    list_js = crawler.get_elements_by_xpath(html.fromstring(js_mock), crawler.xpaths_list, 'js')
    pprint.pprint(list_js)

    # Assuming x.js and xy.js got pulled
    assertion1 = len(list_js) == 2 and list_js[0] == 'x.js' and list_js[1] == 'xy.js'

    # Running xpath on css objects
    css_mock = '<link rel="stylesheet" id="wipro-style-css"  href="https://x.css" type="text/css" media="all" /><link rel="stylesheet" id="wipro-style-css"  href="y.css" type="text/css" media="all" />'
    list_css = crawler.get_elements_by_xpath(html.fromstring(css_mock), crawler.xpaths_list, 'css')
    pprint.pprint(list_css)

    # Assuming https://x.css and y.css got pulled
    assertion2 = len(list_css) == 2 and list_css[0] == 'https://x.css' and list_css[1] == 'y.css'

    # Running xpath on url objects
    url_mock = '<a id="allcaItem4" class="caItem allcaItem allcaItem4 CAStandard" href="https://x.com"> <a id="allcaItem4" class="caItem allcaItem allcaItem4 CAStandard" href="https://y.com">'
    list_links = crawler.get_elements_by_xpath(html.fromstring(url_mock), crawler.xpaths_list, 'links')
    pprint.pprint(list_links)

    # Assuming https://x.com and https://y.com got pulled
    assertion3 = len(list_links) == 2 and list_links[0] == 'https://x.com' and list_links[1] == 'https://y.com'

    # Running xpath on images objects
    images_mock = '<img class="wd-navlogo-digital" src="https://x.com/logo.png" alt="wipro digital"><img class="wd-navlogo-digital" src="https://y.com/logo.png" alt="wipro digital">'
    list_images = crawler.get_elements_by_xpath(html.fromstring(images_mock), crawler.xpaths_list, 'images')
    pprint.pprint(list_images)

    # Assuming https://x.com/logo.png and https://y.com/logo.png got pulled
    assertion4 = len(list_links) == 2 and list_images[0] == 'https://x.com/logo.png' and list_images[1] == 'https://y.com/logo.png'

    assert assertion1 and assertion2 and assertion3 and assertion4


## Testing get_page_content

def test_local_url_connection(crawler):
    # Checking google connection TODO: Test on internal website
    local_url = 'https://www.google.com'
    print('Running local connection check on: ' + local_url + ' expecting 200 status code' )
    try:
        crawler.get_page_content(local_url)
        assert True
    except:
        assert False

def test_chosen_url_connection(crawler):
    # Checking chosen url connection
    print('Running connection check on: ' + crawler.url + ' expecting 200 status code' )
    try:
        crawler.get_page_content(crawler.url)
        assert True
    except:
        assert False

## Testing final execute

## TODO: Refactor execute(self) and test granulary all cases


