import mraa
import time
import codecs

u=mraa.Uart(1)
u.setBaudRate(115200)
u.setMode(8, mraa.UART_PARITY_NONE, 1)
u.setFlowcontrol(False, False)

alarm = mraa.Gpio(1)
alarm.dir(mraa.DIR_OUT)  

wake_up = bytearray(b'x55\x55\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\x03\xfd\xd4\x14\x01\x17\x00')
inlistpassive_target = bytearray(b'x00\x00\xff\x04\xfc\xd4\x4a\x01\x00\xe1\x00')
indataexchange= bytearray(b'x00\x00\xff\x0d\xf3\xd4\x40\x01\x00\xa4\x04\x00\x05\xf2\xff\xff\xff\xff\x50\x00')

card_uid=bytearray(4)
mac=bytearray(12)
while 1:
    u.write(wake_up)
    u.flush()
    if u.dataAvailable(3000):
        data_wakeup = u.read(15)
        hex_data_wakeup=codecs.getencoder('hex')(data_wakeup)
        str_data_wakeup=str(hex_data_wakeup)
        print(str_data_wakeup)
        check_wakeup = str_data_wakeup.find("d51516")
        if(check_wakeup is not -1): #if didn't find, check = -1
            print('wake up success')
            break
    else:
        print('wake up fail')

str_data_exchange= str(0)
str_data_card= str(0)        

while 1 :
    u.write(inlistpassive_target)
    if u.dataAvailable(3000):
        data_card = u.read(30)
        hex_data_card=codecs.getencoder('hex')(data_card)
        str_data_card=str(hex_data_card)
        print(str_data_card)
        time.sleep(1)
        check_card = str_data_card.find("00ff00")
        if(check_card is not -1): #if didn't find, check = -1
            print('already')
    else:
        print('no uid response')
        
    check_phone = str_data_card.find('d54100')
    if (check_phone is not -1):
        print('get phone')
        break
    else:
        check_uid = str_data_exchange.find("d54b01")
        if(check_uid is not -1):
            print('get card')
            break

    u.write(indataexchange) 
    if u.dataAvailable(3000):
        data_exchange = u.read(30)
        hex_data_exchange=codecs.getencoder('hex')(data_exchange)
        str_data_exchange=str(hex_data_exchange)
        print('aid:')
        print(str_data_exchange)
        time.sleep(1)
    else:
        print('check aid no response')

        
if (check_phone is not -1):
    mac[0]=data_card[14]
    mac[1]=data_card[15]
    mac[2]=data_card[16]
    mac[3]=data_card[17]
    mac[4]=data_card[18]
    mac[5]=data_card[19]
    mac[6]=data_card[20]
    mac[7]=data_card[21]
    mac[8]=data_card[22]
    mac[9]=data_card[23]
    mac[10]=data_card[24]
    mac[11]=data_card[25]
    hex_mac=codecs.getencoder('hex')(mac)
    mac_str=str(hex_mac)
    print(mac_str)
else:
    if (check_uid is not -1):
        card_uid[0]=data_exchange[19]
        card_uid[1]=data_exchange[20]
        card_uid[2]=data_exchange[21]
        card_uid[3]=data_exchange[22]
        card_uid_hex=codecs.getencoder('hex')(card_uid)
        card_uid_str=str(card_uid_hex)
        print(card_uid_str)

alarm.write(1)
time.sleep(1)
alarm.write(0)
print('all done')
