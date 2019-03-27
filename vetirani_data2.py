#!usr/bin/python3 -e

import requests
from requests.auth import HTTPDigestAuth
# from json import  JSONEncoder

from pymodbus.client.sync import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.exceptions import ConnectionException, ModbusIOException

from struct import pack, unpack

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

def addresstoint(address,exclude = 1):
    if len(address) == 5 :
        return int(address[exclude:],16)
    else :
        return int(address,16)
    
def modbus_get_buffer(client, address, count = 1, unit_ID = 0):
    
    if count == 0 :
        return None
    
    if len(address) == 5 :
        modbus_add = addresstoint(address)
        type = int(address[0])
    else :
        modbus_add = addresstoint(address)
        type = 0
        
#    print("modbus type : %s address: %i count: %i unitid: %i" % (type, modbus_add, count, unit_ID))
    
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
        print("client:%s address:%s count:%i unit_id:%i" %(client, address, count ,unit_ID))
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
    elif vartype == 12 : #24Bit float
        """ Decodes a 48 bit float(double) from the buffer
        """
        decoder._pointer += 6
        fstring = 'd'
        handle = decoder._payload[decoder._pointer - 6:decoder._pointer]
        handle = bytearray(2) + handle
        handle = decoder._unpack_words(fstring, handle)
        return unpack("!"+fstring, handle)[0]
        
    elif vartype == 13 : #24Bit int
        """ Decodes a 48 bit signed int from the buffer
        """
        decoder._pointer += 6
        fstring = 'q'
        handle = decoder._payload[decoder._pointer - 6:decoder._pointer]
        handle = bytearray(2) + handle
        handle = decoder._unpack_words(fstring, handle)
        return unpack("!"+fstring, handle)[0]
    elif vartype == 14 : #24Bit uint
        """ Decodes a 48 bit unsigned int from the buffer
        """
        decoder._pointer += 6
        fstring = 'Q'
        handle = decoder._payload[decoder._pointer - 6:decoder._pointer]
        handle = bytearray(2) + handle
        handle = decoder._unpack_words(fstring, handle)
        return unpack("!"+fstring, handle)[0]
    
    elif vartype < 1 :
        decoder.skip_bytes(vartype * -1)
        return None
    
def modbusconnectionloop(modbusconnection) :
    
    ret = []
    
    for loop in modbusconnection["loop"] :
        buffer = None
        decoder = None
        buffer = modbus_get_buffer(modbusconnection["client"], loop["firstaddress"],loop["count"] ,modbusconnection["unit_ID"])
        if buffer is None :
#            print("buffer  == None")
            continue

        
        try:
            decoder = modbus_get_decoder(buffer, modbusconnection["byte_bigEndian"], modbusconnection["word_bigEndian"])
        except ModbusIOException :  
            print("ModbusIOException")
            return ret
            
            
        for modbusaddress in loop["modbusaddress"] :
    #                 print(modbusaddress["address"])
#            try :
#                print("address: %s skip: %i" % (modbusaddress["address"], modbusaddress["skip"]))
#            except KeyError:
#                print("address: %s" % (modbusaddress["address"]))
                
            
            result = modbus_decode(decoder, modbusaddress["vartype"])
            print(result)
            
            try :
                decoder.skip_bytes(modbusaddress["skip"] * 2)
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
                    temp_modbusaddress = reponse_modbusaddress.json()["results"]
                    
                    temp_modbusaddress.sort(key=itemgetter("address"))
                    
                    connection["loop"] = []
                    
#                     for i in range(5) :
#                         connection["loop"].append({"firstaddress": "ffffff" , "lastaddress" : "00000", "count" : 0})
                    
                    last = None
#                     last_type = None
        
                    
                    for modbusaddress in temp_modbusaddress :
                        
                        
                        type = int(modbusaddress["address"][0]) if len(modbusaddress["address"]) == 5 else 0
                        
                        if last is None:
                            #Premier passage dans la boucle
                            connection["loop"].append({"firstaddress": "ffffff" , "lastaddress" : "00000", "count" : 0})
                            connection["loop"][-1]["modbusaddress"] = []
            
                        
                        if last is not None:
                            last["skip"] = addresstoint(modbusaddress["address"]) - addresstoint(last["address"]) - last["count"]
                            
                            if last["skip"] < 4 :
                                connection["loop"][-1]["modbusaddress"].append(last)
                            else :
                                last["skip"] = 0
                                connection["loop"][-1]["modbusaddress"].append(last)
                                connection["loop"].append({"firstaddress": "ffffff" , "lastaddress" : "00000", "count" : 0})
                                connection["loop"][-1]["modbusaddress"] = []
                             
                        if addresstoint(modbusaddress["address"], 0) < addresstoint(connection["loop"][-1]["firstaddress"], 0) :
                                connection["loop"][-1]["firstaddress"] = modbusaddress["address"]
                                 
                        if addresstoint(modbusaddress["address"], 0) > addresstoint(connection["loop"][-1]["lastaddress"], 0) :
                                connection["loop"][-1]["lastaddress"] = modbusaddress["address"]
                                connection["loop"][-1]["count"] = modbusaddress["count"]
                                
                        last = modbusaddress
#                         last_type = type
                        #print(modbusaddress["address"])
                       
                    if last is not None:
                        connection["loop"][-1]["modbusaddress"].append(last)

                    for loop in connection["loop"] :
                        loop["firstaddress"] = loop["firstaddress"] if loop["firstaddress"] != 100000 else 0
                        loop["count"] = addresstoint(loop["lastaddress"]) - addresstoint(loop["firstaddress"]) + loop["count"] if loop["count"] > 0 else 0
                        
                    #print(connection["loop"])
                     
                    
                    
                        
                else:
                    # If response code is not ok (200), print the resulting http error code with description
                    reponse_modbusaddress.raise_for_status()
        
                
        else:
            # If response code is not ok (200), print the resulting http error code with description
            reponse_modbusconnection.raise_for_status()
        
           
else:
  # If response code is not ok (200), print the resulting http error code with description
    myResponse.raise_for_status()

print(hosts)
print("conf OK")

while True :
    mytime = time.time()
    data = []
    for host in hosts:
        #print(host)
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

