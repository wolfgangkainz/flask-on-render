import os
import smtplib
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get("name")
    email = request.form.get("email")
    products = request.form.getlist("products")
    quantity = request.form.get("quantity")

    message = f"""\ 
Subject: New Fertilizer Order from {name}

Name: {name}
Email: {email}
Selected Products: {', '.join(products)}
Quantity: {quantity} bag(s)
"""

    # Send the email
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(os.environ["EMAIL_USER"], os.environ["EMAIL_PASS"])
        server.sendmail(os.environ["EMAIL_USER"], "wkainz@gmail.com", message)
        server.quit()
    except Exception as e:
        return f"<h1>Error sending email: {str(e)}</h1>"

    return "<h1>Order submitted! You will receive a confirmation email soon.</h1>"

# 🔥 THIS IS ESSENTIAL FOR RENDER
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
