import sys
import python_crawler
import pytest
import requests
import pprint


@pytest.fixture
def crawler():
    # Returns crawler instance as fixture for pytest
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


