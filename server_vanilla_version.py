from http.server import BaseHTTPRequestHandler, HTTPServer
import sys, os

class ServerException(Exception):
   ''' Internal errors in the server'''
   pass

# class RequestHandler inherits the class BaseHTTPRequestHandler
class RequestHandler(BaseHTTPRequestHandler):
   Page = '''\
   <html>
   <body>
   <table>
   <tr>  <td>Header</td>         <td>Value</td>          </tr>
   <tr>  <td>Date and time</td>  <td>{date_time}</td>    </tr>
   <tr>  <td>Client host</td>    <td>{client_host}</td>  </tr>
   <tr>  <td>Client port</td>    <td>{client_port}</td> </tr>
   <tr>  <td>Command</td>        <td>{command}</td>      </tr>
   <tr>  <td>Path</td>           <td>{path}</td>         </tr>
   </table>
   </body>
   </html>'''

   Error_Page = """\
    <html>
    <body>
    <h1>Error accessing {path}</h1>
    <p>{msg}</p>
    </body>
    </html>
    """


   # rewrite the method
   def do_GET(self):
      # self.send_response(200)
      # self.send_header("Content-Type", "text/html")
      # self.send_header("Content-Length", str(len(self.Page)))
      # self.end_headers()
      # self.wfile.write(self.Page.encode('utf-8'))
      try:
         # full path of the file
         # os.getcwd() : current working directory
         # self.path : requested relative path
         full_path = os.getcwd() + self.path
         # if the path doesn't exist
         if not os.path.exists(full_path):
            raise ServerException("'{0}' not found".format(self.path))
         elif os.path.isfile(full_path):
            self.handle_file(full_path)
         else:
            raise ServerException("Unknown object '{0}'".format(self.path))
      except Exception as msg:
         self.handle_error(msg)


   def handle_error(self, msg):
      content = self.Error_Page.format(path=self.path, msg=msg)
      self.send_content(content.encode('utf-8'),404)

   def create_page(self):    
      values = {
      'date_time'   : self.date_time_string(),
      'client_host' : self.client_address[0],
      'client_port' : self.client_address[1],
      'command'     : self.command,
      'path'        : self.path
      }
      page = self.Page.format(**values)
      return page

      
   def send_content(self, content, status=200):
      self.send_response(status)
      self.send_header("Content-type","text/html")
      self.send_header("Content-Length",str(len(content)))
      self.end_headers()
      #self.wfile.write(page.encode('utf-8'))
      # cancel the binary coding
      self.wfile.write(content)
   
   def handle_file(self, full_path):
      try:
         with open(full_path, 'rb') as reader:
            content = reader.read()
         self.send_content(content)
      except IOError as msg:
         msg = "'{0}' cannot be read: {1}".format(self.path, msg)
         self.handle_error(msg)
   
if __name__ == '__main__':
   serverAddress = ('',8080)
   server = HTTPServer(serverAddress, RequestHandler)
   server.serve_forever()

