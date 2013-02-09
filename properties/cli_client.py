import cmd
import locale
import os
import pprint
import shlex
import webbrowser
from dropbox import client, rest, session

from settings import APP_KEY,APP_SECRET,ACCESS_TYPE
def command(login_required=True):
    """a decorator for handling authentication and exceptions"""
    def decorate(f):
        def wrapper(self, args):
            if login_required and not self.sess.is_linked():
                self.stdout.write("Please 'login' to execute this command\n")
                return

            try:
                return f(self, *args)
            except TypeError, e:
                self.stdout.write(str(e) + '\n')
            except rest.ErrorResponse, e:
                msg = e.user_error_msg or str(e)
                self.stdout.write('Error: %s\n' % msg)

        wrapper.__doc__ = f.__doc__
        return wrapper
    return decorate

class DropboxTerm():
    def __init__(self, app_key, app_secret):
        self.sess = StoredSession(app_key, app_secret, access_type=ACCESS_TYPE)
        self.api_client = client.DropboxClient(self.sess)
        self.current_path = ''
        #self.prompt = "Dropbox> "

        self.sess.load_creds()
	
    def do_login(self):
        """log in to a Dropbox account"""
        try:
            self.sess.link()
        except rest.ErrorResponse, e:
            self.stdout.write('Error: %s\n' % str(e))

    def do_logout(self):
        """log out of the current Dropbox account"""
        self.sess.unlink()
        self.current_path = ''

    def do_cat(self, path):
        """display the contents of a file"""
        f, metadata = self.api_client.get_file_and_metadata(self.current_path + "\\" + path)
        self.stdout.write(f.read())
        self.stdout.write("\n")

    def do_mkdir(self, path):
        """create a new directory"""
        self.api_client.file_create_folder(self.current_path + "\\" + path)

    def do_rm(self, path):
        """delete a file or directory"""
        self.api_client.file_delete(self.current_path + "\\" + path)

    def do_get(self, from_path, to_path):
        """
        Copy file from Dropbox to local file and print out out the metadata.

        Examples:
        Dropbox> get file.txt ~/dropbox-file.txt
        """
        to_file = open(os.path.expanduser(to_path), "wb")

        f, metadata = self.api_client.get_file_and_metadata(self.current_path + "\\" + from_path)
        print 'Metadata:', metadata
        to_file.write(f.read())

    def do_put(self, from_path, to_path):
        """
        Copy local file to Dropbox

        Examples:
        Dropbox> put ~/test.txt dropbox-copy-test.txt
        """
        from_file = open(os.path.expanduser(from_path), "rb")

        self.api_client.put_file(self.current_path + "\\" + to_path, from_file)

    def do_search(self, string):
        """Search Dropbox for filenames containing the given string."""
        results = self.api_client.search(self.current_path, string)
        for r in results:
            self.stdout.write("%s\n" % r['path'])

			
class StoredSession(session.DropboxSession):
    """a wrapper around DropboxSession that stores a token to a file on disk"""
    TOKEN_FILE = "token_store.txt"

    def load_creds(self):
        try:
            stored_creds = open(self.TOKEN_FILE).read()
            self.set_token(*stored_creds.split('|'))
            print "[loaded access token]"
        except IOError:
            pass # don't worry if it's not there

    def write_creds(self, token):
        f = open(self.TOKEN_FILE, 'w')
        f.write("|".join([token.key, token.secret]))
        f.close()

    def delete_creds(self):
        os.unlink(self.TOKEN_FILE)

    def link(self):
        request_token = self.obtain_request_token()
        url = self.build_authorize_url(request_token)
        print "url:", url
        print "Please authorize in the browser. After you're done, press enter."
	browser = webbrowser.get()
	browser.open_new_tab(url)
	raw_input()
        self.obtain_access_token(request_token)
        self.write_creds(self.token)

    def unlink(self):
        self.delete_creds()
        session.DropboxSession.unlink(self)

