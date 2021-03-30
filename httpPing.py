import requests
import argparse
import time
import re

version = "0.1"

def getCurrentMillisec():
	return round(time.time() * 1000)

parser = argparse.ArgumentParser()
parser.add_argument("url", help="URL to be pinged (HTTP request HEAD/GET)")
parser.add_argument("-n","--number",type=int, default=5, help="Number of pings to be made. Defaults to 5.")
parser.add_argument("-t","--timeout",type=int, default=4, help="Request timeout in seconds. Defaults to 4 seconds.")
parser.add_argument("-s","--sleep",type=int, default=1, help="Time between pings in seconds. Defaults to 1 second.")
parser.add_argument("-v","--verbose", help="Verbose mode.", action="store_true")
parser.add_argument("-a","--average", help="Print average time.", action="store_true")
parser.add_argument("-g","--getdata", help="Get data.", action="store_true")
parser.add_argument("-V","--version", action='version', help="Print version.", version="Version : "+version)
args = parser.parse_args()

if re.match("^https?://.*/?$", args.url, re.IGNORECASE | re.MULTILINE) == None:
	print("Invalid URL.")
	exit(-1)

if args.verbose:
	print("HTTP(s) pinging host "+args.url+" "+str(args.number)+" times with a timeout of "+str(args.timeout)+".")

sum = 0
for i in range(args.number):
	if i > 0: time.sleep(args.sleep)
	try:
		startTime = getCurrentMillisec()
		if args.getdata:
			r = requests.get(args.url, timeout=args.timeout)
		else:
			r = requests.head(args.url, timeout=args.timeout)
	except requests.exceptions.Timeout:
		print("Timeout")
	except requests.exceptions.SSLError as e:
		print("SSL Error : "+str(e))
	except e:
		print("Error : "+str(e))
	else:	
		timeTaken = getCurrentMillisec()-startTime
		sum += timeTaken
		if args.verbose:
			print(args.url+" : "+str(timeTaken)+"ms")
		else:
			print(str(timeTaken)+"ms")
		
if args.verbose or args.average:
	print("Avg : "+str(round(sum / args.number))+"ms")