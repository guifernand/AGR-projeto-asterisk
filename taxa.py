#!/usr/bin/python3

#ativar premissões de execução
#sudo pip install beautifulsoup4
#sudo pip install lxml
#sudo pip install requets -->acho que ja esta por default
#sudo pip install --upgrade requests

import sys
import re
from bs4 import BeautifulSoup 
import requests

def checkresult (params):
   params = params.rstrip()
   if re.search('^200',params):
      result = re.search('result=(\d+)',params)
      if (not result):
         sys.stderr.write("FAIL ('%s')\n" % params)
         sys.stderr.flush()
         return -1
      else:
         result = result.group(1)
         #debug("Result:%s Params:%s" % (result, params))
         sys.stderr.write("PASS (%s)\n" % result)
         sys.stderr.flush()
         return result
   else:
      sys.stderr.write("FAIL (unexpected result '%s')\n" % params)
      sys.stderr.flush()
      return -2

def setvariable (name,value):
   sys.stderr.write('SET VARIABLE %s "%s" \n' % (name, value))
   sys.stderr.flush()
   sys.stdout.write('SET VARIABLE %s "%s" \n' % (name, value))
   sys.stdout.flush()
   result = sys.stdin.readline().strip()
   checkresult(result)


def saynumber (params):
   sys.stderr.write("SAY NUMBER %s \"\"\n" % params)
   sys.stderr.flush()
   sys.stdout.write("SAY NUMBER %s \"\"\n" % params)
   sys.stdout.flush()
   result = sys.stdin.readline().strip()
   checkresult(result)


def sayit (params):
   sys.stderr.write("STREAM FILE %s \"\"\n" % str(params))
   sys.stderr.flush()
   sys.stdout.write("STREAM FILE %s \"\"\n" % str(params))
   sys.stdout.flush()
   result = sys.stdin.readline().strip()
   checkresult(result)

# Read and ignore AGI environment (read until blank line)

env = {}
tests = 0;

while 1:
   line = sys.stdin.readline().strip()

   if line == '':
      break
   key,data = line.split(':')
   if key[:4] != 'agi_':
      #skip input that doesn't begin with agi_
      sys.stderr.write("Did not work!\n");
      sys.stderr.flush()
      continue
   key = key.strip()
   data = data.strip()
   if key != '':
      env[key] = data

sys.stderr.write("AGI Environment Dump:\n");
sys.stderr.flush()
for key in env.keys():
   sys.stderr.write(" -- %s = %s\n" % (key, env[key]))
   sys.stderr.flush()

html_text=requests.get('https://www.bportugal.pt/taxas-cambio').text
soup= BeautifulSoup(html_text, 'lxml')

conj_rates=soup.find('div', id = 'rates-principal')
front=conj_rates.find('div', id = 'rates-front')
rows=front.find_all('div', class_ = 'rates-row')
for row in rows:
    pais=row.find_all('div', class_ = 'rates-country-name')
    country=pais[0].text.replace(' ','')
    if country == "EstadosUnidos":
        taxa=row.find_all('div', class_ = 'rates-rate')
        rate=taxa[0].text.replace(' ','')
        rate=rate.replace(',','.')
        break

speech="speech"
setvariable(speech,str(rate))
