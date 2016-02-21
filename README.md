# chitti
Chitti is an open domain QA chat server which understands natural language

System requirements:
Python(3.4)
mongodb(>=2.4)

Additional python libraries required:
cherrypy
nltk

To start the server, run
python qa_server.py

modify the ip address and port number to listen in the qa_server.conf configuration file.
server.socket_host="0.0.0.0"
server.socket_port=9000

Currently it is set to listen on all ip addresses, to make it available only on local machine change the socket_host to "127.0.0.1"

To use chitti, go to your web browser and start chatting with the server in the format below:
http://localhost:9000/q/?q=<your questions>

Sample question and answer:
http://localhost:9000/q/?q=Who is Richard Stallman?
<START of server response>
Category : president of the free software foundation

Image
Info :
Born : March 16, 1953, New York City
Nationality : American
Other names : RMS, rms
Alma mater : Harvard University, Massachusetts Institute of Technology
Occupation : President of the Free Software Foundation
Known for : Free software movement, GNU, Emacs, GCC
Awards : MacArthur Fellowship, EFF Pioneer Award,... see Honors and awards
Description :
Richard Matthew Stallman, often known by his initials, rms, is a software freedom activist and computer programmer. He campaigns for software to be distributed in a manner such that its users receive the freedoms to use, study, distribute and modify that software. Software that ensures these freedoms is termed free software. Stallman launched the GNU Project, founded the Free Software Foundation, developed the GNU Compiler Collection and GNU Emacs, and wrote the GNU General Public License.

Data source : Wikipedia 
<END of server response>

This application currenlty presents only the API and does not have any UI as it is meant to be integrated into a wide variety of applications such as a chat bot in whatsapp, XMPP or IRC networks, as a standalone mobile/desktop application etc.

This software is just a proof of concept and is in early development stage.
You are welcome to fork this code and develop it.
