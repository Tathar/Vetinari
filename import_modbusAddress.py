#!usr/bin/python3 -e

import requests
from requests.auth import HTTPDigestAuth
import json

import csv


VARTYPE_CHOICES = ((0, 'bits'),
                   (1, '8bit_int'),
                   (2, '8bit_uint'),
                   (3, '16bit_int'),
                   (4, '16bit_uint'),
                   (5, '32bit_float'),
                   (6, '32bit_int'),
                   (7, '32bit_uint'),
                   (12, '48bit_float'),
                   (13, '48bit_int'),
                   (14, '48bit_uint'),
                   (8, '64bit_float'),
                   (9, '64bit_int'),
                   (10, '64bit_uint'),
                   (11, 'string'))




url = "http://10.165.2.1/api/v1.0/"
user = "api"
password = "1motdePasse"
result = requests.get(url,auth=(user,password))

if(result.ok):
    url_api = result.json()
else :
  # If response code is not ok (200), print the resulting http error code with description
    result.raise_for_status()
    
def vartype2int(vartype) :
    for key,value in dict(VARTYPE_CHOICES).items() :
        if value == vartype :
            return key
              
def connection2url(connection) :
    return (url_api["modbusconnection"] + str(int(connection)) + "/")


with open('modbusaddress.csv', newline='') as csvfile:
    file = csv.DictReader(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    for row in file:
        data = dict(row)
        data["connection"] = connection2url(data["connection"])
        data["address"] = int(data["address"])
        data["count"] = int(data["count"])
        data["vartype"] = vartype2int(row["vartype"])
        data["delay"] = int(data["delay"])
        print(data)
        
        myResponse = requests.post(url_api["modbusaddress"],auth=(user,password), data = data)
        if(myResponse.ok):
            pass
        else :
            # If response code is not ok (200), print the resulting http error code with description
            print(myResponse.text)
            myResponse.raise_for_status()
      

