import sys
import python_crawler
import pytest


@pytest.fixture
def crawler():
    # Returns crawler instance as fixture for pytest
    # TODO: Add some control logic & add as parameters
    url = "https://wiprodigital.com/"
    output_filename = "output/sitemap-test.json"

    return python_crawler.PythonCrawler(url, output_filename)

def test_url_validity(crawler):
    assert "http" in crawler.url




