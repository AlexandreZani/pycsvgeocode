#!/usr/bin/python

import urllib2
import urllib
import time
import re
import csv


address = "1600 Amphitheatre Parkway, Mountain View, CA, USA"

class GeoCodingClass:
	url = "http://maps.google.com/maps/geo?"
	APIKey = ""
	waitTime = 1
	countryCode = "us" # Australia country code is "au"

	GeoStatusCodes = {
			200 : "G_GEO_SUCCESS",
			500 : "G_GEO_SERVER_ERROR",
			601 : "G_GEO_MISSING_QUERY",
			602 : "G_GEO_UNKNOWN_ADDRESS",
			603 : "G_GEO_UNAVAILABLE_ADDRESS",
			610 : "G_GEO_BAD_KEY",
			620 : "G_GEO_TOO_MANY_QUERIES"
			}

	def GeoCodeCSV(self, inputFile, outputFile):

		badStatCode = 0
		inCSV = csv.DictReader(inputFile, delimiter=',', quotechar='"')
		outCSV = None

		for data in inCSV:
			if not('address' in data):
				return -1

			if outCSV == None:
				k = data.keys() + ['lat', 'long']
				outCSV = csv.DictWriter(outputFile, k)


			res = self.GeoCodeAddress(data['address'])

			print res[0], res[1]


			if type(res) is int:
				badStatCode += 1
				data['lat'] = res
				data['long'] = res
			else:
				data['lat'] = res[0]
				data['long'] = res[1]

			outCSV.writerow(data)

		return badStatCode

	def GeoCodeAddress(self, address):

		values = {
				"q" : address,
				"key" : self.APIKey,
				"output" : "csv",
				"oe" : "utf8",
				"gl" : self.countryCode
				}

		data = urllib.urlencode(values)
		req = self.url + data

		lat = 0
		long = 0
		statusCode = 620
		accuracy = 0

		while statusCode == 620:
			time.sleep(self.waitTime)

			response = urllib2.urlopen(req)
			csvLn = response.read()
			csvVals = re.split(",", csvLn)

			statusCode = int(csvVals[0])
			accuracy = int(csvVals[1])
			lat = float(csvVals[2])
			long = float(csvVals[3])

			if statusCode == 620:
				print "Too fast at:", self.waitTime
				self.waitTime += 0.1
		
		if statusCode == 200:
			return (lat, long)
		else:
			return statusCode

GeoCoding = GeoCodingClass()

print GeoCoding.GeoCodeCSV(open("addresses.csv"), open("geocoded.csv", "w"))
