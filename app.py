import os
import stripe
import sys

from dotenv import load_dotenv
from flask import Flask, request, render_template, jsonify

load_dotenv()

app = Flask(__name__,
  static_url_path='',
  template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "views"),
  static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "public"))

#import Stripe variables from .ENV file
stripe.api_key=os.getenv("STRIPE_SECRET_KEY")

# Home route
@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')

# Checkout route
@app.route('/checkout', methods=['GET'])
def checkout():
  # Just hardcoding amounts here to avoid using a database
  item = request.args.get('item')
  title = None
  amount = None
  error = None
  
  if item == '1':
    title = 'The Art of Doing Science and Engineering'
    amount = 2300
  elif item == '2':
    title = 'The Making of Prince of Persia: Journals 1985-1993'
    amount = 2500
  elif item == '3':
    title = 'Working in Public: The Making and Maintenance of Open Source'
    amount = 2800
  else:
    # Included in layout view, feel free to assign error
    error = 'No item selected' 

  intent = stripe.PaymentIntent.create(
    amount = amount,
    currency = "usd",
    automatic_payment_methods = {"enabled": True},
  )

  print('payment initiated ' +intent.id, file=sys.stdout)

  #establishing data convention to ease passing variables to js
  data= {'title':title, 'amount':amount, 'error':error, 'client_secret':intent.client_secret}

  return render_template('checkout.html', data=data)

# Success route
@app.route('/success', methods=['GET'])
def success():
  status = None
  amount = None

  #get client secret from Stripe appended query parameters
  payment_intent_id = request.args.get('payment_intent')
  #print('payment intent id ' + payment_intent_id)

  #retrieve the payment intent
  intent = stripe.PaymentIntent.retrieve(
    payment_intent_id
  )

  #create data to pass important parameters
  data= {'id':payment_intent_id, 'amount':intent.amount, 'status':intent.status}

  return render_template('success.html', data=data)


if __name__ == '__main__':
  app.run(port=5000, host='0.0.0.0', debug=True)