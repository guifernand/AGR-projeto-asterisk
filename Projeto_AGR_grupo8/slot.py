#!/usr/bin/python3

#ativar execution permissions
import sys
import re
import random

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

def getnumber (prompt, timelimit, digcount):
 sys.stderr.write("GET DATA %s %d %d\n" % (prompt, timelimit, digcount))
 sys.stderr.flush()
 sys.stdout.write("GET DATA %s %d %d\n" % (prompt, timelimit, digcount))
 sys.stdout.flush()
 result = sys.stdin.readline().strip()
 result = checkresult(result)
 sys.stderr.write("digits are %s\n" % result)
 sys.stderr.flush()
 if result:
    return result
 else:
    result = -1

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

def slot():
    credits=10
    timeout=5000
    digitcount=1
    values=["projeto/Strawberry","projeto/Orange","projeto/Lemon","projeto/Plum","projeto/Cherry","projeto/Grapes"]
    while(credits>0):
        sayit("projeto/bet")
        bet=getnumber("silence/5",timeout,digitcount)    #obter extesion do asterisk
        bet = int(bet)
        if bet!=0:
            if bet>0 and bet<10 and bet<=credits:
                credits=credits-bet
                x=random.randint(0,5)

                y=random.randint(0,5)

                z=random.randint(0,5)
				
				sayit("projeto/sequence")
                sayit(values[x])
                sayit(values[y])
                sayit(values[z])

                 if x==y==z and x!=0:
                    bet=bet*10
                    sayit("projeto/Multiplier")
                elif x==0 and y==0 and z==0:
                    bet=bet*25
                    sayit("projeto/Jackpot!")
                elif x==y or x==z or y==z:
                    bet=bet
                    sayit("projeto/Cashback")
                else:
                    bet=0
					
                sayit("projeto/You-won")
                saynumber(bet)
                sayit("projeto/credits")
                credits=credits+bet
                sayit("projeto/You-have")
                saynumber(credits)
                sayit("projeto/credits")
            else:
                sayit("projeto/Invalid-bet")
        else:

            return()

slot()

