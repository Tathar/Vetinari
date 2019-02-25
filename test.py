#!usr/bin/python3 -e

import requests
from requests.auth import HTTPDigestAuth
# from json import  JSONEncoder

from pymodbus.client.sync import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.exceptions import ConnectionException

import time

from operator import itemgetter

SLEEP = 60

url = "http://10.165.2.1/api/v1.0/"
user = "api"
password = "1motdePasse"
result = requests.get(url,auth=(user,password))

if(result.ok):
    url_api = result.json()
else :
  # If response code is not ok (200), print the resulting http error code with description
    result.raise_for_status()
    
VARTYPE_CHOICES = ((0, 'bits'),
                   (1, '8bit_uint'),
                   (2, '16bit_int'),
                   (3, '16bit_uint'),
                   (4, '32bit_float'),
                   (5, '32bit_int'),
                   (6, '32bit_uint'),
                   (7, '64bit_float'),  
                   (8, '64bit_int'),
                   (9, '64bit_uint'),
                   (10, '8bit_int'),
                   (11, 'string'))

def modbus_get_buffer(client, address, count = 1, unit_ID = 0):
    
    if count == 0 :
        return None
    
    if len(address) = 5 :
        modbus_add = address[1:4]
        type = address[0]
    else :
        modbus_add = address
        type = 0
        
    print("modbus type : %s address: %s" % (type, modbus_add))
    
    try :
        if type == 0 :
            return client.read_coils(modbus_add, count, unit=unit_ID)
        elif type == 1 :
            return client.read_discrete_inputs(modbus_add, count, unit=unit_ID)
        elif type == 2 :
            pass
        elif type == 3 :
            return client.read_holding_registers(modbus_add, count, unit=unit_ID)
        elif type == 4 :
            return client.read_input_registers(modbus_add, count, unit=unit_ID)
    except ConnectionException:
        print("connection error")
        print("client:%s address:%i count:%i unit_id:%i" %(client, address, count ,unit_ID))
        return None
    
        
        
def modbus_get_decoder(buffer, byteorder = True, wordorder = True):
    
    if byteorder:
        byteorder_endian = Endian.Big
    else :
        byteorder_endian = Endian.Little
        
    if wordorder:
        wordorder_endian = Endian.Big
    else :
        wordorder_endian = Endian.Little
    
    return BinaryPayloadDecoder.fromRegisters(buffer.registers,
                                              byteorder=byteorder_endian,
                                              wordorder=wordorder_endian)
    
def modbus_decode(decoder, vartype = 0):
    
    if vartype == 0 :
        return decoder.decode_bits()
    elif vartype == 1 :
        return decoder.decode_8bit_int()
    elif vartype == 2:
        return decoder.decode_8bit_uint()
    elif vartype == 3 :
        return decoder.decode_16bit_int()
    elif vartype == 4 :
        return decoder.decode_16bit_uint()
    elif vartype == 5 :
        return decoder.decode_32bit_float()
    elif vartype ==  6:
        return decoder.decode_32bit_int()
    elif vartype == 7 :
        return decoder.decode_32bit_uint()
    elif vartype == 8 :
        return decoder.decode_64bit_float()
    elif vartype == 9 :
        return decoder.decode_64bit_int()
    elif vartype == 10 :
        return decoder.decode_64bit_uint()
    elif vartype == 11 :
        return decoder.decode_string()
    elif vartype < 1 :
        decoder.skip_bytes(vartype * -1)
        return None
    
def modbusconnectionloop(modbusconnection) :
    
    ret = []
    
    for loop in modbusconnection["loop"] :
        buffer = modbus_get_buffer(modbusconnection["client"], loop["firstaddress"],loop["count"] ,modbusconnection["unit_ID"])
        if buffer is None :
            continue
        decoder = modbus_get_decoder(buffer, modbusconnection["byte_bigEndian"], modbusconnection["word_bigEndian"])
            
        for modbusaddress in modbusconnection["modbusaddress"] :
    #                 print(modbusaddress["address"])
            try :
                print("address: %s skip: %i" % (modbusaddress["address"], modbusaddress["skip"]))
            except KeyError:
                pass
            
            result = modbus_decode(decoder, modbusaddress["vartype"])
            
            try :
                decoder.skip_bytes(modbusaddress["skip"])
            except KeyError:
                pass
    
            data = {}
            data["modbus_address"] = modbusaddress["url"]
            data["data"] = result
            ret.append(data)
            
    return ret
    
    
def ModbusAddress(client, address, count = 1, unit_ID = 0, byteorder = True, wordorder = True, vartype = 0):
        
    buffer = modbus_get_buffer(client, address, count, unit_ID)
    decoder = modbus_get_decoder(buffer, byteorder, wordorder)
    return modbus_decode(decoder, vartype)



# It is a good practice not to hardcode the credentials. So ask the user to enter credentials at runtime
#myResponse = requests.get(url,auth=HTTPDigestAuth(raw_input("username: "), raw_input("Password: ")), verify=True)
myResponse = requests.get(url_api["host"],auth=(user,password))
#myResponse = requests.get(url)

# For successful API call, response code will be 200 (OK)
if(myResponse.ok):

    # Loading the response data into a dict variable
    # json.loads takes in only binary or string variables so using content to fetch binary content
    # Loads (Load String) takes a Json file and converts into python data structure (dict or list, depending on JSON)
#    jDatas = json.loads(myResponse.content)

    hosts = myResponse.json()["results"]

    for host in hosts:
        url = url_api["modbusconnection"] + "?host=" + str(host["id"])
        reponse_modbusconnection = requests.get(url,auth=(user,password))
        if(reponse_modbusconnection.ok):
            host["modbusconnection"] = reponse_modbusconnection.json()["results"]
            
            for connection in host["modbusconnection"] :
                connection["client"] = ModbusTcpClient(host["ip_address"], port=connection["port"] )
                url = url_api["modbusaddress"] + "?connection=" + str(connection["id"])
                reponse_modbusaddress = requests.get(url,auth=(user,password))
                if(reponse_modbusaddress.ok):
                    connection["modbusaddress"] = reponse_modbusaddress.json()["results"]
                    
                    connection["modbusaddress"].sort(key=itemgetter("address"))
                    
                    connection["loop"] = []
                    
                    for i in range(5) :
                        connection["loop"].append({"firstaddress": 100000 , "lastaddress" : 0, "count" : 0})
                    
                    last = None
                    last_type = None
                    
                    for modbusaddress in connection["modbusaddress"] :
                        
                        
                        type = int(modbusaddress["address"] / 10000) if modbusaddress["address"] != 0 else 0
                        
                        if last is None:
                            #Premier passage dans la boucle
                            pass
                        
                        if last is not None:
                            last["skip"] = modbusaddress["address"] - last["address"] - last["count"] if type == last_type else 0
                             
                        
                        if modbusaddress["address"] < connection["loop"][type]["firstaddress"] :
                                connection["loop"][type]["firstaddress"] = modbusaddress["address"]
                                 
                        if modbusaddress["address"] > connection["loop"][type]["lastaddress"] :
                                connection["loop"][type]["lastaddress"] = modbusaddress["address"]
                                connection["loop"][type]["count"] = modbusaddress["count"]
                                
                        last = modbusaddress
                        last_type = type
                        print(modbusaddress["address"])
                        

                    for loop in connection["loop"] :
                        loop["firstaddress"] = loop["firstaddress"] if loop["firstaddress"] != 100000 else 0
                        loop["count"] = loop["lastaddress"] - loop["firstaddress"] + loop["count"] if loop["count"] > 0 else 0
                        
                    print(connection["loop"])
                     
                    
                    
                        
                else:
                    # If response code is not ok (200), print the resulting http error code with description
                    reponse_modbusaddress.raise_for_status()
            
        else:
            # If response code is not ok (200), print the resulting http error code with description
            reponse_modbusconnection.raise_for_status()
else:
  # If response code is not ok (200), print the resulting http error code with description
    myResponse.raise_for_status()

print("conf OK")


while True :
    mytime = time.time()
    data = []
    for host in hosts:
#        client = ModbusTcpClient(host["ip_address"])
#        client.connect()
        
        for modbusconnection in host["modbusconnection"] :
            
            data += (modbusconnectionloop(modbusconnection))
#        client.close()

    reponse_modbus = requests.post(url_api["modbusresult"],auth=(user,password),json = data)
    
    sleep =  (mytime + SLEEP ) - time.time()

    print("sleep " + str(sleep))
    if sleep > 0 :      
        time.sleep(sleep)

