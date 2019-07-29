#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""workreport.py generates the basic structure needed for a Salt Squad work report based on the SDS prject board."""

__author__ = "Jochen Breuer"
__email__  = "jbreuer@suse.de"
__license__ = "GPLv3"

import os
import requests

query = """query {
  repository(owner: "SUSE", name: "spacewalk") {
    project(number: 38) {
      columns(first: 10) {
        nodes {
          name
          cards(first: 100) {
            edges {
              node {
                content {
                  __typename
                  ... on Issue {
                    number
                    title
                    url
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
"""

url = 'https://api.github.com/graphql'
json = { 'query' : query }
api_token = os.environ.get('GITHUB_TOKEN_GALAXY')
headers = {'Authorization': 'token %s' % api_token}

r = requests.post(url=url, json=json, headers=headers)
data = r.json()

print("# MISC")
for column in data['data']['repository']['project']['columns']['nodes']:
    name = column.get('name')
    if name not in ['Done', 'Blocked / Postponed', 'Waiting', 'In progress']:
        continue
    name_trans = {
        u'Done': u'DONE',
        u'Blocked / Postponed': u'BLOCKED',
        u'Waiting': u'NEXT',
        u'In progress': u'IN PROGRESS'
    }
    print("\n\n## {}\n".format(name_trans.get(name, '??????')))
    for card in column['cards']['edges']:
        if card['node']['content']:
            number = card['node']['content']['number']
            title = card['node']['content']['title']
            url = card['node']['content']['url']
            print("* {} #{}".format(title, number))
            print("🔗 {}\n\n".format(url))
