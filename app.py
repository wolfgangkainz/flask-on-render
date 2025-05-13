import os
import smtplib
from email.mime.text import MIMEText
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    customer_email = request.form['email']
    product = request.form['product']
    quantity = int(request.form['quantity'])

    # Extract price from product string
    product_name, price_str = product.rsplit(" - $", 1)
    price = float(price_str)
    total = price * quantity

    # Compose email content
    body = f"""\
New Order from Kasi's Bio Fertili

Customer Name: {name}
Customer Email: {customer_email}

Order:
{quantity} bags of {product_name}
Unit Price: ${price:.2f}
Total Amount: ${total:.2f}
"""

    msg = MIMEText(body)
    msg['Subject'] = f"Fertilizer Order from {name}"
    msg['From'] = os.environ["EMAIL_USER"]
    msg['To'] = "wkainzat@gmail.com"  # 🔁 Updated recipient address here

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(os.environ["EMAIL_USER"], os.environ["EMAIL_PASS"])
        server.send_message(msg)
        server.quit()
        return "<h1>Order submitted! Thank you.</h1>"
    except Exception as e:
        return f"<h1>Error sending email: {str(e)}</h1>"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
