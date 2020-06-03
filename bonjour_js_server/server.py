#multithreading
import threading
#server
import flask
from flask import request, jsonify
from bonjour_discovery import BonjourDiscovery
import json
#from time import sleep

#sleep(10)

#create flask server
app = flask.Flask(__name__, static_url_path='', static_folder='')
app.config["DEBUG"] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 #IMPORTANT disables cacheing of our javascript on requesting computer so printer list will update every time it is requested

#creates ip_discovery object
BD = BonjourDiscovery()

#A route used for trusting the database
@app.route('/', methods=['GET'])
def home():
    return '''<p>Printer server now trusted. Return to wiki for printer information.</p>'''

# A route that returns json list of printers. (Does not work on wiki)
@app.route('/api', methods=['GET'])
def api_json():
    BD.checkPrinterStatus()
    return jsonify(BD.printers)
    
# A route that returns json list of printers. (Does not work on wiki)
@app.route('/api/flush', methods=['GET'])
def api_flush():
    BD.removePrinters()
    return "Printers flushed"
    
# A route that returns javascript table of printers. (for wiki)
@app.route('/api/data.js')
def api_js():
    BD.checkPrinterStatus()
    BD.checkDeviceStatus()
    #create new js file with current data
    with open('data.js', 'w') as outfile:
        #write header
        outfile.write("printers = ")
        #write json data
        outfile.write(json.dumps(BD.printers))
        outfile.write("\r\n")
        #write header
        outfile.write("devices = ")
        #write json data
        outfile.write(json.dumps(BD.devices))
        outfile.write("\r\n")
        #write the rest of the functions
        with open('data_functions.js') as infile:
            outfile.write(infile.read())
    return app.send_static_file('data.js')
    
#start printer discovery
service_thread = threading.Thread(target=BD.loop)
service_thread.daemon = True
service_thread.start()

#app.run(host='0.0.0.0', port=5000) #http server

app.run(host='0.0.0.0', port=5000, ssl_context='adhoc') #https with blank certificate

#app.run('0.0.0.0', port=5000, ssl_context=('/home/pi/Bonjour_3D_printer_discovery/bonjour_js_server/cert.crt', '/home/pi/Bonjour_3D_printer_discovery/bonjour_js_server/key.key')) # https with full certificate (requires password on startup)

