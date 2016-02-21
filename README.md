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

This is software is just a proof of concept and is in early development stage.
You are welcome to fork this code and develop it.
