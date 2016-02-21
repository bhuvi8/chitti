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

![Alt text](./data/sample_response_screenshot.png?raw=true "Response")


This application currenlty presents only the API and does not have any UI as it is meant to be integrated into a wide variety of applications such as a chat bot in whatsapp, XMPP or IRC networks, as a standalone mobile/desktop application etc.

This software is just a proof of concept and is in early development stage.
You are welcome to fork this code and develop it.
