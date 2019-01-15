import sys
import python_crawler
import pytest
import test_crawler

# TODO: Add some control logic
url = sys.argv[1]
output_filename = "./output/" + sys.argv[2]

# Running tests before executing main crawler if 3rd argument is present
if len(sys.argv) > 2:
   pytest.main(['-x', '--verbose'])

# Running main class
crawler = python_crawler.PythonCrawler(url, output_filename)
crawler.execute()