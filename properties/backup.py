#Name : Paruchuri Chaitanya
#course : CSE 6331   Cloud Computing
#NO: 1000790255

import os
import sys
from settings import APP_KEY,APP_SECRET,ACCESS_TYPE
import win32file
import win32con
import cli_client
import encrypt as krypto
import webbrowser
import gntp.notifier
ACTIONS = {
  1 : "Created",
  2 : "Deleted",
  3 : "Updated",
  4 : "Renamed from something",
  5 : "Renamed to something"
}
FILE_LIST_DIRECTORY = 0x0001

# windows path compatible
path_to_watch = ".\\..\\upload"
hDir = win32file.CreateFile (
  path_to_watch,
  FILE_LIST_DIRECTORY,
  win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
  None,
  win32con.OPEN_EXISTING,
  win32con.FILE_FLAG_BACKUP_SEMANTICS,
  None
)
while 1:
  #

  #
  results = win32file.ReadDirectoryChangesW (
    hDir,
    1024,
    True,
    win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
     win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
     win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
     win32con.FILE_NOTIFY_CHANGE_SIZE |
     win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
     win32con.FILE_NOTIFY_CHANGE_SECURITY,
    None,
    None
  )
  for action, file in results:
	# getting the name of files changed
    full_filename = os.path.join (path_to_watch, file)
	# checking for the action of file
    if ACTIONS.get(action, "Unknown") in ('Created', 'Updated'):
		# encrypting the file
		encrypt=krypto.Encrypt()
		encrypt.encryptFile(full_filename)
		# initiating drop box connection
		term = cli_client.DropboxTerm(APP_KEY, APP_SECRET)
		# logging to server
		try:
			term.do_login()
		except:
			print 'Unable to log in to dropbox server'
			sys.exit()
		#splits file - text.txt to text
		#fname=full_filename.split('.')[0]+'.enc'
		full_newfile =full_filename.replace('upload', 'tempenc')
		fname=full_newfile +'.enc'
		print "fname :" +fname			    

		

		# putting file to dropbox
		try:
			term.do_put(fname,file)
			print 'Uploading to dropbox'
			gntp.notifier.mini("file uploaded to dropbox")

		except:
			print 'unable to put files'
		# rmoving file from local server
		
		term.do_logout()
