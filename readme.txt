#Name : Paruchuri Chaitanya
#course : CSE 6331   Cloud Computing
#NO: 1000790255

The Following libraries are necessary in python

crypto
gntp.notifier
dropbox
win32


python backup.py
The windows service polls continously for changes, When a file is dropped into upload folder, it is encrypted and stored in "tempenc" folder and is uploaded to dropbox 


python download.py
The file can be downloaded by giving its name,metadata is also shown,and the downloaded encrypted file is deleted after being decrypted.Download folder will contain this folder 

Environment : Windows
Python 2.7.3