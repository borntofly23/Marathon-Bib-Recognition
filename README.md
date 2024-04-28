# Marathon Bib Recognition Project

## Introduction:
The Marathon Bib Recognition Project is a Python Flask application designed to facilitate the registration, authentication, and management of marathon participants' bib numbers and images. The project utilizes optical character recognition (OCR) techniques to extract bib numbers from uploaded images, storing them along with the corresponding images in a MongoDB database. Additionally, the project includes features for user registration, login, and image fetching.

## Requirements:
To run the Marathon Bib Recognition Project, ensure that you have the following installed:

1. **Python 3:** The project is written in Python, so ensure that you have Python 3 installed on your system. You can download Python from the official website: www.Python.org.
2. **Flask:** Flask is a web development framework for Python. Install Flask using pip, the Python package installer:
   ```bash
   pip install Flask
   ```
3. **pymongo:** pymongo is a Python driver for MongoDB. Install pymongo using pip:
   ```bash
   pip install pymongo
   ```
4. **pytesseract:** pytesseract is a Python wrapper for Google's Tesseract-OCR Engine. Install pytesseract using pip:
    ```bash
    pip install pytesseract
    ```
5. **Pillow (PIL):** Pillow is a Python Imaging Library (fork of the original PIL). Install Pillow using pip:
    ```bash
    pip install Pillow
    ```
6. **werkzeug:** The project uses werkzeug for hashing passwords. Install it using pip:
    ```bash
    pip install Werkzeug
    ```

## MongoDB Database:

- The project uses MongoDB to store user data, login attempts, and uploaded images.
- Make sure MongoDB is installed and running on your system.
- The connection to the MongoDB database is established in `run.py` using the MongoClient from the pymongo library.
- By default, the application connects to MongoDB running on `localhost` at port `27017`.
- You can customize the MongoDB connection URL in `run.py` if your MongoDB server is running on a different host or port.
  
## Project Structure:

- **run.py:** This file contains the main Flask application code, including routes for registration, login, authentication, image uploading, and image fetching.
- **templates/:** This directory contains HTML templates used by the Flask application for rendering web pages.
   - **login.html:** HTML template for the login page.
   - **registration.html:** HTML template for the registration page.
   - **home.html:** HTML template for the home page.
   - **upload.html:** HTML template for the image uploading page.
   - **fetch_images.html:** HTML template for displaying fetched images.
- **static/:** This directory contains static files such as CSS stylesheets and images used by the HTML templates.
- **uploads/:** This directory is used to store uploaded images.

## Running the Application:

1. Clone the repository or download the project files to your local machine.
2. Navigate to the project directory in your terminal.
3. Install the required dependencies.
4. Start the Flask application by running:
   ```bash
   python run.py
   ```
5. Open a web browser and navigate to `http://localhost:5000` to access the application.

## Usage:

- **Registration:** Users can register by providing their name, email, phone number, bib number, and password.
- **Login:** Registered users can log in using their bib number and password.
- **Image Upload:** Users can upload images containing bib numbers. The application extracts bib numbers from the images using OCR and stores them in the database.
- **Image Fetching:** Users can fetch images associated with a specific bib number.

## Hashed Password Implementation:
Passwords are hashed before storing in the database and compared during login using hashed values to enhance security.

## Contributing:
Contributions to the Marathon Bib Recognition Project are welcome. If you encounter any issues or have suggestions for improvement, please feel free to submit a pull request or open an issue on the project's GitHub repository.

## License:
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgments:
-Special thanks to the developers of Flask, pymongo, pytesseract, and Pillow for their excellent libraries.

## Contact:
For any inquiries or support, please contact Rushikesh Jadhav (https://github.com/borntofly23).
