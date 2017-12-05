# pn532_uart_linkit7688_python
Use PN532 (RFID , NFC) to read Mifare cards or cellphone's NFC by Uart on Linkit-7688.

This is the python code on linkit-7688.
My partner coded the android APP.
This code have 3 steps.
First at all, I will initial(wake_up) the PN532 by sending a bytearray.
And the content of bytearrays please reference the "PN532 User Manual".
Second, I will set the PN532 to read card(NFC or RFID) by sending a bytearray, and it will response the card UID .
The final step is sending a bytearray to know if the phone is the correct.
If the answer is yes, the phone will send back its MAC address to me.

Q1:How did you know the phone was the correct?
A1:We have the password "AID" in the third bytearray. 
   And checked if the phone's AID was the same.
   So we had to develop an APP on the phone, and get its AID by NFC.
   But the APP part I can't provide.
