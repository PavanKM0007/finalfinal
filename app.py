

import firebase_admin
from firebase_admin import credentials, firestore


from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)



@app.route("/closed")
def closed():
    return render_template("closed.html")


# Step 1: Initial selection form
@app.route('/', methods=['GET', 'POST'])
def index(): 
    if request.method == 'POST':
        # Get the value from the form submission
        choice = request.form.get('form_type')
        
        # Route to the appropriate form based on response
        if choice == 'corporate':
            return redirect(url_for('corporate_form'))
        elif choice == 'individual':
            return redirect(url_for('individual_form'))
        
        
    return render_template('home.html')

# Step 2: Destination form routes

   
@app.route('/form/corporate', methods=['GET', 'POST'])
def corporate_form():
    if not check_count("mixed-doubles",16):    
        if request.method == 'POST':
            # Match the name attributes in mixed.html
            player1 = request.form.get('player1', '').strip()
            player2 = request.form.get('player2', '').strip()
            phone1 = request.form.get('phone1', '').strip()
            phone2 = request.form.get('phone2', '').strip()
            email1 = request.form.get('email1', '').strip()
            email2 = request.form.get('email2', '').strip()

            # Server-side validation
            if phone1 == phone2:
                return "Player phone numbers must be different.", 400

            if not all([player1, player2, phone1, phone2, email1, email2]):
                return "Please fill in all required fields.", 400

        

            try:
                db.collection("mixed-doubles").add({
                    "name-1": player1,
                    "name-2": player2,
                    "phone-1": phone1,
                    "phone-2": phone2,
                    "email-1": email1,
                    "email-2": email2,
                    "status": "unverified"
                })

                return render_template("payment1.html"),200

            except Exception:
                app.logger.exception("Failed to save registration")
                return "Unable to save registration. Please try again.", 500

        return render_template('mixed.html')
    else:
        return render_template("closed.html")
@app.route('/form/individual', methods=['GET', 'POST'])
def individual_form():
    if not check_count("singles",24):
        if request.method == 'POST':
            # Match the name attributes in mixed.html
            player = request.form.get('name', '').strip()
        
            phone = request.form.get('phone', '').strip()
        
            email = request.form.get('email', '').strip()
        

            if not all([player, phone,email]):
                return "Please fill in all required fields.", 400

            if (
                len(phone) != 10 or not phone.isdigit()
            
            ):
                return "Phone numbers must contain exactly 10 digits.", 400

            try:
                db.collection("singles").add({
                    "name": player,
                    
                    "phone": phone,
                    
                    "email": email,
                                "status": "unverified"
                })

                return render_template("payment.html"), 200

            except Exception:
                app.logger.exception("Failed to save registration")
                return "Unable to save registration. Please try again.", 500
        
        return render_template('singles.html')
    else:
        return render_template("closed.html")



# Set FIREBASE_CREDENTIALS to the path of your service-account JSON file.
# Example (Windows): set FIREBASE_CREDENTIALS=C:\\path\\to\\serviceAccountKey.json
import os

firebase_credentials_path = os.environ.get(
    "FIREBASE_CREDENTIALS",
    "serviceAccountKey.json"
)
cred = credentials.Certificate(firebase_credentials_path)
firebase_admin.initialize_app(cred)

db = firestore.client()

def check_count(collection_name, counter):
    docs = (db.collection(collection_name).stream())
    count = 0
    for doc in docs:
        doc_data = doc.to_dict()
        if doc._data["status"].lower() == "verified":
            count+=1
    print(count)

    if count >= counter :
        return True
    else:
        return False


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
