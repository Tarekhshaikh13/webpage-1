
from flask import Flask, render_template, request, redirect, flash, jsonify,send_file
from pymongo import MongoClient
from io import BytesIO
from bson.objectid import ObjectId
import gridfs

app = Flask(__name__)
app.secret_key = 'some_secret_key'  # For flash messages

# Setup MongoDB connection
client = MongoClient("mongodb://localhost:27017/")  # This connects to a local MongoDB instance
db = client["AdmitVerify"]  # Here "user_database" is the name of the database you want to connect to
collection = db["Admitverify_documentdata"]  # Here "user_data" is the name of the collection within the database
fs = gridfs.GridFS(db)

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

        # Store the uploaded file in GridFS
        file_id = fs.put(file, filename=file.filename)

        # Insert data into MongoDB
        user_entry = {
            "document": file.filename, 
            "document_id": file_id, 
            "document_number": doc_number,
            "full_name": full_name,
            "fathers_name": fathers_name,
            "gender": gender,
            "dob_year": dob_year,
            "address": address
        }
        collection.insert_one(user_entry)
 
        

    return render_template('index.html')

@app.route('/admin', methods=['GET'])
def admin_page():
    # Fetch all data from the collection
    data = list(db["Admitverify_documentdata"].find({}))
    return render_template('admin.html', data=data)




MIME_TYPE_MAP = {
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'png': 'image/png',
    'gif': 'image/gif',
    'pdf': 'application/pdf'
    # ... add more as needed
}

@app.route('/file/<file_id>', methods=['GET'])
def get_file(file_id):
    try:
        # Fetch the file from GridFS
        grid_out = fs.get(ObjectId(file_id))
        
        # Check the file type to determine if it should be displayed or downloaded
        file_type = grid_out.filename.split('.')[-1]
        display_in_browser = file_type in ['jpg', 'jpeg', 'png', 'gif', 'pdf']
        
        # Determine MIME type
        mime_type = MIME_TYPE_MAP.get(file_type, 'application/octet-stream')  # Use 'application/octet-stream' as default

        response = send_file(BytesIO(grid_out.read()), mimetype=mime_type, as_attachment=not display_in_browser)
        
        # Set the Content-Disposition header for all files
        disposition_type = 'inline' if display_in_browser else 'attachment'
        response.headers['Content-Disposition'] = f'{disposition_type}; filename="{grid_out.filename}"'
        
        return response
    except gridfs.errors.NoFile:
        return "File not found in GridFS", 404
    except Exception as e:
        return f"An error occurred: {e}", 500
    

@app.route('/delete/<entry_id>', methods=['POST'])
def delete_entry(entry_id):
    try:
        # Fetch the entry from MongoDB
        entry = db["Admitverify_documentdata"].find_one({"_id": ObjectId(entry_id)})
        
        # Delete the file from GridFS
        fs.delete(entry['document_id'])
        
        # Delete the entry from MongoDB
        db["Admitverify_documentdata"].delete_one({"_id": ObjectId(entry_id)})
        
        flash('Entry deleted successfully!', 'success')
        return redirect('/admin')
    except Exception as e:
        flash(f'An error occurred: {e}', 'error')
        return redirect('/admin')


if __name__ == '__main__':
    app.run(debug=True)