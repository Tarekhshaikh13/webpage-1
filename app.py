
from flask import Flask, render_template, request, redirect, flash, jsonify
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = 'some_secret_key'  # For flash messages

# Setup MongoDB connection
client = MongoClient("mongodb://localhost:27017/")  # This connects to a local MongoDB instance
db = client["AdmitVerify"]  # Here "user_database" is the name of the database you want to connect to
collection = db["Admitverify_documentdata"]  # Here "user_data" is the name of the collection within the database
collection.insert_one({"hi":1})

@app.route('/', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        # Get the data from the form
        file = request.files['fileInput']
        doc_number = request.form['docNumber']
        full_name = request.form['fullName']
        fathers_name = request.form['fathersName']
        gender = request.form['gender']
        dob_year = request.form['dobYear']
        address = request.form['address']

        # Insert data into MongoDB
        user_entry = {
            "document": file.filename,  # You might want to handle the file storage differently
            "document_number": doc_number,
            "full_name": full_name,
            "fathers_name": fathers_name,
            "gender": gender,
            "dob_year": dob_year,
            "address": address
        }
        collection.insert_one(user_entry)
 
        

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)