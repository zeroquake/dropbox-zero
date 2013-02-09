import cli_client
import encrypt as krypto
from settings import APP_KEY,APP_SECRET,ACCESS_TYPE
print 'Getting the files from dropbox server'
term = cli_client.DropboxTerm(APP_KEY, APP_SECRET)
try:
	term.do_login()
except:
	print 'login error'
filename=raw_input('enter the name of file to be searched')
# getting files from dropbox
try:
	term.do_search(filename)
except:
	print 'search error'
# getting name of file to be downloaded
filedown=raw_input('enter file name to be downloaded')
# downloading the file
try:
	term.do_get(filedown,'.\\..download\\'+filedown)
	term.do_logout()
except:
	print 'Download Error'
encrypt=krypto.Encrypt()
try:
	encrypt.decryptFile('.\\..\\download\\'+filedown)
	print 'Decrypting and Saving File'
	os.rm('.\\..\\download\\'+filedown)
	print 'Removing temporary files'
except:
	print 'Failed to decrypt'
