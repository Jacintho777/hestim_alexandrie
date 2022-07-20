##########################
import convert
from pdf2image import convert_from_path
import os
##########################


# from flask import Flask, render_template, Response, request, redirect, url_for

import random

try :
	from flask import Flask

	from flask import redirect,url_for,request,render_template,send_file,send_from_directory, Response
	from io import BytesIO

	from flask_wtf.file import FileField
	from wtforms import SubmitField
	from flask_wtf import FlaskForm
	import sqlite3
	print("All modules imported")
except :
	print("Some modules weren't imported")

app = Flask(__name__, template_folder='template')
app.config["SECRET_KEY"] = 'secret'
#Lancement des pages

@app.route("/index")

def index():

	return render_template('index.html',title = "Hestim Scholar - Accueil")

@app.route("/espace_didactique")

def espace_didactique():

	return render_template("espace_didactique.html")

@app.route("/espace_informatif")

def espace_informatif():

	return render_template("espace_informatif.html")

#######################################################

@app.route("/rapports", methods = ['GET', 'POST'])

def rapports():

	form = UploadForm()

	if request.method == 'POST':

		if form.validate_on_submit():

			file_name = form.file.data

			# Store the documents in the uploads folder

			save_path = 'C:\\Users\\mpete\\OneDrive\\Bureau\\Projets HESTIM\\2eme annee\\Innovation_Créativité\\test\\uploads'
			filenoun = file_name.filename

			completeName = os.path.join(save_path, filenoun)
			print(completeName)
			file1 = open(completeName, "wb")
			file1.write(file_name.read())
			file1.close()

			#Storing the first pages as images
			convert.pdf_to_png(filenoun,filenoun[:-3]+'png')
			doc_names = open('doc_names.txt','a')
			doc_names.write(filenoun[:-3]+'png\n')
			doc_names.close()

			#############################################################
			database(name = file_name.filename, data = file_name.read())

			return print_files()
			# return render_template("home.html", form = form)

	return print_files()
	# return render_template("home.html", form = form)


	# return render_template("rapports.html")

@app.route('/rapports/download/<int:id>',methods=['GET','POST'])

def download(id):

	form = UploadForm()
	content = []

	if request.method == 'GET':

		conn = sqlite3.connect("files.db")
		cursor = conn.cursor()
		c = cursor.execute("""SELECT * FROM my_table """)
		for x in c.fetchall():
			content.append(x)
		return get_it(content[id][0],content[id][1])
		conn.commit()
		cursor.close()
		conn.close()

	return render_template("rapports.html", form = form)

def get_it(name,data):

	return send_file(BytesIO(data), attachment_filename = name, as_attachment = True)

@app.route("/rapports")

def print_files():

#fontion to print the list of titles of the documents

	try:
		
		#get files name from the database

		form = UploadForm()

		files_name = []
		images_names = []
		conn = sqlite3.connect("files.db")
		cursor = conn.cursor()
		c = cursor.execute("""SELECT * FROM my_table """)
		for x in c.fetchall():
			files_name.append(x)
			images_names.append(x[0][:-3]+'png')
			print(x[0][:-3]+'png')
		conn.commit()
		cursor.close()
		conn.close()

		#liste de nombres d'étoiles à afficher

		stars = []
		for i in range(len(files_name)):
			stars.append(random.randrange(1,6))

		return render_template("rapports.html", form = form ,reports = files_name, names = images_names, stars = stars)

	except :

		conn = sqlite3.connect("files.db")
		cursor = conn.cursor()

		cursor.execute(""" CREATE TABLE IF NOT EXISTS my_table (name TEXT, data BLOP) """)
		conn.commit()
		cursor.close()
		conn.close()

		return "initialisation"


@app.route("/rapports/<image_name>")

def send_image(image_name):

	return send_from_directory('C:\\Users\\mpete\\OneDrive\\Bureau\\Projets HESTIM\\2eme annee\\Innovation_Créativité\\test\\uploads',image_name)

@app.route("/rapports/<string:d_file>")

def display(d_file):

	return """<html>
	<embed src = '/uploads'"""+d_file+"""type = "application/pdf" width = "100%" height = "600px"/></embed>
	</html>
	"""

class UploadForm(FlaskForm):

	file = FileField()
	submit = SubmitField("submit")
	download = SubmitField("download")

def database(name, data):

	# Storing files to database after uploading

	conn = sqlite3.connect("files.db")
	cursor = conn.cursor()

	cursor.execute(""" CREATE TABLE IF NOT EXISTS my_table (name TEXT, data BLOP) """)

	if cursor.execute("""SELECT EXISTS (SELECT 1 FROM my_table WHERE name = ?)""",(name,)).fetchone() != (1,):

		cursor.execute("""INSERT INTO my_table (name, data) VALUES (?,?) """,(name, data))

	else:

		print("This file was already uploaded")

	conn.commit()
	cursor.close()
	conn.close()

#########################################################

@app.route("/nouveautes")

def nouveautes():

	return render_template("nouveautes.html")

#Pour faire la recherche dans l'espace d'upload des rapports

@app.route("/") 

def rechercher():

	word = request.args.get("research")
	print(word)
	mot = "%"+str(word)+"%"
	print(mot)

	files_name = []
	images_names = []

	conn = sqlite3.connect("files.db")
	cursor = conn.cursor()

	c = cursor.execute("""SELECT * FROM my_table WHERE name like ? """,(mot,))

	for x in c.fetchall():

		files_name.append(x)
		images_names.append(x[0][:-3]+'png')
		
	conn.commit()
	cursor.close()
	conn.close()

	stars = []
	for i in range(len(files_name)):
		stars.append(random.randrange(1,6))

	return render_template("searching.html",reports = files_name, names = images_names, stars = stars)

#Récupération des avis

@app.route("/form", methods=["POST"])

def printing():

	# msg = Message('Hello', sender = "mpeteyemawuli@gmail.com", recipients = ['mpeteyemawuli@gmail.com'])
	# mail.send(msg)
	return render_template('hello.html')

if __name__ == '__main__' :

	app.run(debug = True, port = 8001)

# Faire apparaître le message à base du click.
