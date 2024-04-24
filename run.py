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

@app.route('/')
def register():
    return render_template('registration.html')

@app.route('/register', methods=['POST'])
def register_user():
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

@app.route('/login')
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
        return redirect(url_for('fetch'))
    else:
        # Authentication failed, show error message
        error_message = "Invalid bib number or password"
        return render_template('login.html', error_message=error_message)

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
    return render_template('fetch_images.html', images=images)


@app.route('/upload', methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        # Read the image file
        img = Image.open(file)

        result = pytesseract.image_to_string(img, config='--psm 6 outputbase digits')
        print("Detected Numbers:", result)
        
        # Clean the extracted text to get numbers
        numbers = clean_extracted_text(result)
        
        if not numbers:
            return jsonify({'error': 'No valid number found in the image'}), 400
        
        # Convert image to base64 string
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        # Create dictionary to store number and image data
        data = {
            "number": numbers[0],  # Assuming there is only one valid number
            "image": f"data:image/jpeg;base64,{img_str}"
        }
        
        # Insert data into MongoDB collection
        images_collection.insert_one(data)
        
        return jsonify({'message': 'Image and number successfully added to the database'}), 201
    
    # If GET request, return HTML form to upload image
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)