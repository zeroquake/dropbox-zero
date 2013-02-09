import os
from settings import APP_KEY,APP_SECRET,ACCESS_TYPE
import win32file
import win32con
import cli_client
import encrypt as krypto
import webbrowser
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
  # ReadDirectoryChangesW takes a previously-created
  # handle to a directory, a buffer size for results,
  # a flag to indicate whether to watch subtrees and
  # a filter of what changes to notify.
  #
  # NB Tim Juchcinski reports that he needed to up
  # the buffer size to be sure of picking up all
  # events when a large number of files were
  # deleted at once.
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
    if ACTIONS.get(action, "Unknown")=='Created' or ACTIONS.get(action, "Unknown")=='Updated':
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
		fname=full_filename.split('.')[0]+'.enc'
		# putting file to dropbox
		try:
			term.do_put(fname,file)
			print 'Uploading to dropbox'
		except:
			print 'unable to put files'
		# rmoving file from local server
		
		term.do_logout()
