#!usr/bin/python3 -e

import requests
from requests.auth import HTTPDigestAuth
from json import  JSONEncoder

from pymodbus.client.sync import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.exceptions import ConnectionException

import time

SLEEP = 60

def ModbusAddress(client, address, word = 1, unit_ID = 0, byteorder = True, wordorder = True, vartype = 1):
        
    if byteorder:
        byteorder_endian = Endian.Big
    else :
        byteorder_endian = Endian.Little
        
    if wordorder:
        wordorder_endian = Endian.Big
    else :
        wordorder_endian = Endian.Little
    
    if address < 20000 :
        pass
    elif address < 30000 :
        pass
    elif address < 40000 :
        pass
    elif address < 50000 :
        result = client.read_holding_registers(address-40000, word, unit=unit_ID)
        decoder = BinaryPayloadDecoder.fromRegisters(result.registers,
                                                     byteorder=byteorder_endian,
                                                     wordorder=wordorder_endian)
    
    if vartype == 0 :
        return decoder.decode_32bit_int()


base_url = "http://10.165.0.235:8000/api/v1.0/"
user = "post"
password = "postadmin"

url = base_url + "host/"

# It is a good practice not to hardcode the credentials. So ask the user to enter credentials at runtime
#myResponse = requests.get(url,auth=HTTPDigestAuth(raw_input("username: "), raw_input("Password: ")), verify=True)
myResponse = requests.get(url,auth=(user,password))
#myResponse = requests.get(url)


# For successful API call, response code will be 200 (OK)
if(myResponse.ok):

    # Loading the response data into a dict variable
    # json.loads takes in only binary or string variables so using content to fetch binary content
    # Loads (Load String) takes a Json file and converts into python data structure (dict or list, depending on JSON)
#    jDatas = json.loads(myResponse.content)

    hosts = myResponse.json()["results"]

    print("The response contains {0} properties".format(len(hosts)))
    print("\n")

    for host in hosts:
        url = base_url + "modbuswatcher/?host=" + str(host["id"])
        reponse_modbus = requests.get(url,auth=(user,password))
        host["modbuswatcher"] = reponse_modbus.json()["results"]
        host["client"] = ModbusTcpClient(host["ip_address"])
else:
  # If response code is not ok (200), print the resulting http error code with description
    myResponse.raise_for_status()

while True :
    mytime = time.time()
    for host in hosts:
#        client = ModbusTcpClient(host["ip_address"])
#        client.connect()
        

        for modbuswatcher in host["modbuswatcher"] :
#            print(modbuswatcher["address"])
            try :
                result = ModbusAddress(host["client"], modbuswatcher["address"],modbuswatcher["word"] ,modbuswatcher["unit_ID"] , vartype = modbuswatcher["vartype"] )
            except ConnectionException:
                print("connection error")
            else:
#                print(result)
                url = base_url + "modbusresult/"
                data = {}
                data["modbus_watcher"] = modbuswatcher["url"]
                data["data"] = result
                json = JSONEncoder().encode(data)
#                print(json)
                reponse_modbus = requests.post(url,auth=(user,password),json = data)
    
#        client.close()
    sleep =  (mytime + SLEEP ) - time.time()
    print("sleep " + str(sleep))
    if sleep > 0 :      
        time.sleep(sleep)

