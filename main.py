import requests
from bs4 import BeautifulSoup


def getRulesURL():
  url = 'https://magic.wizards.com/en/rules'

  response = requests.get(url)

  soup = BeautifulSoup(response.content, 'html.parser')

  link = soup.find('a', string='TXT')

  rules_url = link['href']

  return rules_url


def downloadRulesText(url):
  response = requests.get(url)

  return response.content


def parseRulesTextIntoMarkdown():
  return "TBC"


def createHTMLFromMarkdown():
  return "TBC"


if __name__ == '__main__':
  """
    1. Scrape the rules page to get a link to the text version of the rulebook
    2. Download the text version of the rulebook
    3. Parse the text version of the rulebook into markdown
    4. Convert the markdown into html
    5. Write the html to a file
    """

  rules_text_url = getRulesURL()

  rules_text = downloadRulesText(rules_text_url)

  with open('rules.txt', 'wb') as f:
    f.write(rules_text)
