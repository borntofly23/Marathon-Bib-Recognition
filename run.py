from flask import Flask, request, jsonify
from PIL import Image
import pytesseract
import base64
from io import BytesIO
from pymongo import MongoClient
import pytesseract
from PIL import Image
from flask import render_template, request, redirect, url_for, session
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['marathon_database']
users_collection = db['users']
images_collection = db['images']
login_collection = db['login']

# Path to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def clean_extracted_text(text):
    numbers = []
    for word in text.split():
        if word.isdigit():
            number = int(word)
            if 1000 <= number <= 999999:
                numbers.append(number)
    return numbers

# @app.route('/')
# def register():
#     return render_template('registration.html') 

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/authenticate', methods=['GET','POST'])
def authenticate():
    bib_number = request.form['bib_number']
    password = request.form['password']

    # Log the login attempt in the login collection
    login_attempt = {'bib_number': bib_number, 'password': password}
    login_collection.insert_one(login_attempt)

    # Check if the provided bib number and password exist in both users_collection and login_collection
    user = users_collection.find_one({'bib_number': bib_number, 'password': password})
    login_attempt = login_collection.find_one({'bib_number': bib_number, 'password': password})

    if user and login_attempt:
        # Authentication successful, redirect to home page
        return redirect(url_for('home'))
    else:
        # Authentication failed, show error message
        error_message = "Invalid bib number or password"
        return render_template('login.html', error_message=error_message)
    
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        bib_number = request.form['bib_number']
        password = request.form['password']

        # Check if bib number already exists in the database
        if users_collection.find_one({'bib_number': bib_number}):
            error_message = "Bib number already exists"
            return render_template('registration.html', error_message=error_message)

        # Insert user data into MongoDB
        user_data = {'name': name, 'email': email, 'phone': phone, 'bib_number': bib_number, 'password': password}
        users_collection.insert_one(user_data)

        return redirect(url_for('login'))

    return render_template('registration.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/fetch')
def fetch():
    return render_template('fetch_images.html')

@app.route('/fetch_images', methods=['POST'])
def fetch_images():
    bib_number = int(request.form['bib_number'])
    images = []
    cursor = images_collection.find({"bib_number": bib_number})
    for image in cursor:
        images.append(image["image"])
    return render_template('fetch_images.html', images=images, bib_number=bib_number)


from flask import render_template, request

@app.route('/upload', methods=["GET", "POST"])
def upload():
    error = None
    success = None

    if request.method == "POST":
        if 'file' not in request.files:
            error = 'No file part'
        else:
            file = request.files['file']
            if file.filename == '':
                error = 'No selected file'
            else:
                img = Image.open(file)

                # Check if the uploaded file is an image (JPEG, JPG, or PNG)
                allowed_formats = ['JPEG', 'JPG', 'PNG']
                if img.format not in allowed_formats:
                    error = 'Unsupported file format. Please upload an image in JPEG, JPG, or PNG format.'
                else:
                    result = pytesseract.image_to_string(img, config='--psm 6 outputbase digits')
                    
                    # Clean the extracted text to get numbers
                    numbers = clean_extracted_text(result)
                    
                    if not numbers:
                        error = 'No valid number found in the image'
                    else:
                        # Convert image to base64 string
                        buffered = BytesIO()
                        img.save(buffered, format="JPEG")
                        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
                        
                        # Create dictionary to store number and image data
                        data = {
                            "bib_number": numbers[0],  # Assuming there is only one valid number,
                            "file_name": file.filename, # Assuming there is only one valid
                            "image": f"data:image/jpeg;base64,{img_str}"
                        }
                        
                        # Insert data into MongoDB collection
                        images_collection.insert_one(data)
                        
                        success = 'Image uploaded successfully.'

    return render_template('upload.html', error=error, success=success)


if __name__ == '__main__':
    app.run(debug=True)