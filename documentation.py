import sys
def exit():sys.exit(0)
try:
	import pandas as pd
except ModuleNotFoundError as module_error:
	print("Pandas has to be installed")
	exit()
try:
	from flask import Flask,request, Response
except ModuleNotFoundError as module_error:
	print("Flask has to be installed")
	exit()
try:
	import boto3
except ModuleNotFoundError as module_error:
	print("boto3 has to be installed")
	sys.exit(0)
try:
	import os
except ModuleNotFoundError as module_error:
	print(f"os module has to be installed")
	sys.exit(0)

try:
	from werkzeug.utils import secure_filename
except ModuleNotFoundError as module_error:
	print(f"werkzeug.utils module has to be installed")
	sys.exit(0)
	
vamstar_app = Flask(__name__)
def upload_folder(name):
	UPLOAD_FOLDER = f"./{name}-documentation/"
	vamstar_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
	return 

def vamstar_home():
	vamstar_string = "<html><body>"
	vamstar_string = "<h1> Vamstar Documentation Process </h1>"
	vamstar_string += "</body></html>"
	return vamstar_string

def html_form(name):
	return f"<form action=http://127.0.0.1:9514/save/{name} method = POST enctype='multipart/form-data'> \
			<p>SSC Marksheet&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;   <input type='file' id ='SSC-file' name='SSC'/> </p>\
			<p>Plus2 Marksheet &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input type='file' id ='Plus-file' name='Plus2'/> </p>\
			<p>B.Tech/B.E Marksheet &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;&nbsp;&nbsp <input type='file' id ='B.Tech-file' name='B.Tech'/> </p>\
			<p>Masters Certificate  &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <input type='file' id ='Masters-file' name='Masters'/> </p>\
			<p>Last Payslip-1 &emsp;&emsp; &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <input type='file' id ='Payslip-1' name='Payslip1'/> </p>\
			<p>Last Payslip-2  &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <input type='file' id ='Payslip2-file' name='Payslip2'/> </p>\
			<p>Last Payslip-3  &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <input type='file' id ='Payslip3-file' name='Payslip3'/> </p>\
			<p>Current Employers Appointment letter &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <input type='file' id ='Appointment-file' name='Appointment'/> </p>\
			<p>Professional References&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <input type='file' id ='Reference-file' name='Reference'/> </p>\
			<p><input type = submit name = submit/> </p>\
			</form>"
			
@vamstar_app.route('/vamstar-documentation-step/<string:name>')
def home_page(name):
	try:
		os.mkdir(f"{name}-documentation")
	except FileExistsError as file_error:
		pass
	return vamstar_home() + html_form(name)

@vamstar_app.route('/save/<string:name>',methods = ['POST', 'GET'])
def save(name):
	upload_folder(name)
	try:
		bucket_name = "vamstar-documentation"
		s3 = boto3.client('s3')
	except Exception as exception:
		print("Error in the aws s3 function") 
		sys.exit(0)
	else:
		if request.method == 'POST':
			docs = ['SSC', 'Plus2', 'B.Tech', 'Masters'	]
		for doc in docs:
			file = request.files[doc]
			try:
				file.save(os.path.join(vamstar_app.config['UPLOAD_FOLDER'],file.filename))
			except IsADirectoryError as dir_err:
				pass
		dir = f"{name}-documentation"
		folder_name = f"{name}-Documents"
		for file_doc in os.listdir(dir):
			s3.upload_file(f"{dir}/{file_doc}",f"{bucket_name}",f"{dir}/{file_doc}")	
		response = Response()
		response.headers["access-control-allow-headers"] = "Origin"
		response.headers["Content-Type"] = "Accept"
		response.headers["access-control-allow-methods"] = "GET,POST,PUT"
		response.headers["access-control-allow-origini"] = "*"
	return f"<html>\
					<body>\
							<p>File Saved successfully</p>\
					</body>\
			</html>" + str(response)
	

vamstar_app.run(port= 9514)
