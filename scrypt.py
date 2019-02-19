#!usr/bin/python3 -e

import requests
from requests.auth import HTTPDigestAuth
import json

from pymodbus.client.sync import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder


base_url = "http://10.165.0.91:8000/api/v1.0/"

url = base_url + "modbusresult/"

# It is a good practice not to hardcode the credentials. So ask the user to enter credentials at runtime
#myResponse = requests.get(url,auth=HTTPDigestAuth(raw_input("username: "), raw_input("Password: ")), verify=True)
myResponse = requests.get(url,auth=("post","postadmin"))
#myResponse = requests.get(url)


# For successful API call, response code will be 200 (OK)
if(myResponse.ok):

    # Loading the response data into a dict variable
    # json.loads takes in only binary or string variables so using content to fetch binary content
    # Loads (Load String) takes a Json file and converts into python data structure (dict or list, depending on JSON)
#    jDatas = json.loads(myResponse.content)

    jDatas = myResponse.json()

    print("The response contains {0} properties".format(len(jDatas)))
    print("\n")
    for jData in jDatas:
        for key in jData:
            print(str(key) + " : " + str(jData[key]))
else:
  # If response code is not ok (200), print the resulting http error code with description
    myResponse.raise_for_status()

client = ModbusTcpClient('10.165.2.40')
client.connect()
result = client.read_holding_registers(0,2, unit=1)

decoder = BinaryPayloadDecoder.fromRegisters(result.registers,
                                                 byteorder=Endian.Big,
                                                 wordorder=Endian.Big)

print(decoder.decode_32bit_int())
client.close()
