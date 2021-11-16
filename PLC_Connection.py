import snap7

IP = '192.168.0.1' # ip adress opgegeven voor de PLc
RACK = 0  # prop plc welk rack, zie foto van PLc links
SLOT = 1  # Zie divce overvieuw

DB_NUMBER = 100  # aanspreken van datablock adress
start_adress = 1  # start adress van het data pakket
size = 259  # + 1 grootste data adress

plc = snap7.client.Client()  # verbinding server van siemens
plc.connect(IP, RACK, SLOT)  # verbindiing leggen met PLC

plc.get_connected()
print(plc.get_connected())

#  plc_info = plc.get_cpu_info()
#  print(plc_info)

state = plc.get_cpu_state()
print(state)

db = plc.db_read(DB_NUMBER, start_adress, size)

plc.db_write(DB_NUMBER, start_adress, b'snap7 app to plc!')
product_name = db[0:255].decode('UTF-8').strip('\x00')
print(product_name)

product_value = int.from_bytes(db[255:257], byteorder='big')
print(product_value)

product_status = bool(db[258])
print(product_status)

product_test = bool(db[258])
print(product_test)

plc.db_write(DB_NUMBER, 260, b'  this is suppossed to happen')