import requests
import markdown
from markdown.extensions.toc import TocExtension
from bs4 import BeautifulSoup

TOP_LEVEL_HEADINGS = [
  "Magic: The Gathering Comprehensive Rules",
]

SUB_LEVEL_HEADINGS = [
  "Introduction",
  "Contents",
  "Glossary",
  "Credits",
]

def getRulesURL():
  url = 'https://magic.wizards.com/en/rules'

  response = requests.get(url)

  soup = BeautifulSoup(response.content, 'html.parser')

  link = soup.find('a', string='TXT')

  rules_url = link['href']

  return rules_url

def downloadRulesText(url):
  response = requests.get(url)

  return response.content.decode('utf-8-sig')

def parseLineFromRules(line):
  if line in TOP_LEVEL_HEADINGS:
    return '# ' + line + '\n'
  elif line in SUB_LEVEL_HEADINGS:
    return '## ' + line + '\n'
  else:
    return line + '\n'

def parseRulesTextIntoMarkdown(rules_text):
  markdown_rules = ""
  skip_contents_list = False

  for line in rules_text.splitlines():
    if (skip_contents_list):
      if (line.strip() == "Credits"):
        skip_contents_list = False
      continue

    markdown_rules += parseLineFromRules(line.strip())

    if (line.strip() == "Contents"):
      skip_contents_list = True
      markdown_rules += "[TOC]\n"

  return markdown_rules.strip()

def createHTMLFromMarkdown(markdown_rules):
  return markdown.markdown(
    markdown_rules,
    extensions=[TocExtension(anchorlink=True, toc_depth=('2-3'))])

def createHTMLRulesPage(html_rules):

  styles = """
  <style>
    body {
      margin: 0 10px 0 10px;
    }
    .toclink {
      color:white;
      text-decoration: none;
    }
    a {
      text-decoration: none;
      margin-left: 0;
    }
    a:hover, .toclink:hover {
      text-decoration: underline;
    }
    ul {
      padding-left: 20px
    }
    h2 {
      margin: 10px 0 10px 0;
    }
  </style>
  """

  return f"""
  <!DOCTYPE html>
  <html>
    <head>
      <title>Magic: The Gathering Comprehensive Rules</title>
      <meta charset="utf-8">
      {styles}
    </head>
    <body>
      {html_rules}
    </body>
  </html>
  """

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

  markdown_rules = parseRulesTextIntoMarkdown(rules_text)

  html_rules = createHTMLFromMarkdown(markdown_rules)

  rules_page = createHTMLRulesPage(html_rules)

  with open('rules.html', 'w') as f:
    f.write(rules_page)
