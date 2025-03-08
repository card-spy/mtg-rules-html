#!/usr/bin/env python3

import requests
import markdown
import re
from markdown.extensions.toc import TocExtension
from markdown.extensions.attr_list import AttrListExtension
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

def getIdAndRule(line):
  (id, rule) = re.split(r'\s', line, maxsplit=1)
  return (id, rule)

def isRuleSection(line):
  (id, rule) = getIdAndRule(line)
  return re.match(r'^\d{1,2}[.]$', id) != None

def isRuleSubsection(line):
  (id, rule) = getIdAndRule(line)
  return re.match(r'^\d{3,}[.]$', id) != None

def isIndividualRule(line):
  (id, rule) = getIdAndRule(line)
  return re.match(r'^\d{3,}[.]\d{1,}([a-z]+|[.])$', id) != None

def formatIndividualRule(line):
  """
  This functions takes a rule entry like:
  - 104.3a A player can concede the game at any time.
  And parses it into this markdown format:
  - [104.3a A player can concede the game at any time.](#104.3a) {{: id="104.3a" }}
  """
  (id, rule) = getIdAndRule(line)
  return f'[{id}](#{id}) {rule}\n {{: #{id} }}\n'

def isExampleForRule(line):
  return line.lower().startswith('example')

def parseRulesEntry(rules_entry):
  if isRuleSection(rules_entry):
    (id, rule) = getIdAndRule(rules_entry)
    return '## ' + rule + '\n'
  elif isRuleSubsection(rules_entry):
    (id, rule) = getIdAndRule(rules_entry)
    return '### ' + rule + '\n'
  elif isIndividualRule(rules_entry):
    return formatIndividualRule(rules_entry)
  elif isExampleForRule(rules_entry):
    return '\n_' + rules_entry + '_\n'
  else:
    return rules_entry + '\n'

def parseLineFromRules(line):
  if line in TOP_LEVEL_HEADINGS:
    return '# ' + line + '\n'
  elif line in SUB_LEVEL_HEADINGS:
    return '## ' + line + '\n'
  else:
    return line + '\n'

def parseRulesTextIntoMarkdown(rules_text):
  markdown_rules = ""
  current_section = None

  for line in rules_text.splitlines():
    if line.strip() == 'Introduction':
      current_section = 'Introduction'

    if current_section == 'Introduction':
      if (line.strip() == "Contents"):
        current_section = 'Contents'

        markdown_rules += parseLineFromRules(line.strip())
        markdown_rules += "[TOC]\n"

        continue

      markdown_rules += parseLineFromRules(line.strip())
    elif current_section == 'Contents':
      if (line.strip() == "Credits"):
        current_section = 'Rules'

      continue
    elif current_section == 'Rules':
      if (line.strip() == "Glossary"):
        current_section = 'Glossary'
        markdown_rules += parseLineFromRules(line.strip())
        continue

      if (len(line.strip()) > 0):
        markdown_rules += parseRulesEntry(line.strip())
      else:
        markdown_rules += '\n\n'
    elif current_section == 'Glossary':
      if (line.strip() == "Credits"):
        current_section = 'Credits'
        markdown_rules += parseLineFromRules(line.strip())
        continue

      markdown_rules += line + '\n\n'
    elif current_section == 'Credits':
      markdown_rules += line + '\n\n'
    else:
      markdown_rules += parseLineFromRules(line.strip())

  return markdown_rules.strip()

def createHTMLFromMarkdown(markdown_rules):
  return markdown.markdown(markdown_rules,
                           extensions=[
                             TocExtension(anchorlink=True, toc_depth=('2-3')),
                             AttrListExtension()
                           ])

def createHTMLRulesPage(html_rules):
  return f"""
  <!DOCTYPE html>
  <html>
    <head>
      <title>Magic: The Gathering Comprehensive Rules</title>
      <meta charset="utf-8">
      <link rel="stylesheet" href="rules.css">
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
