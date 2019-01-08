from lxml import html, etree
import requests

url =  'https://buildit.wiprodigital.com/'
response = requests.get(url)

tree = html.fromstring(response.content)

links = tree.xpath('//a/@href')

for link in links:
    print(link)