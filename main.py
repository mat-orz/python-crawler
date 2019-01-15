import sys
import python_crawler

# TODO: Add some control logic
url = sys.argv[1]
output_filename = "./output/" + sys.argv[2]

crawler = python_crawler.PythonCrawler(url, output_filename)

crawler.execute()