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

#Stripe variables
stripe.api_key='sk_test_51KWojhGG70SVIjLMD7fZWNAJ2oB1fkFuYQdxJXHS7Ip5Q8V8V88Z0UTu8otd2FRmyxG2agE5tcma7ZOE1oAJ82hB00fUMGJuTo'

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
  clientsecret = None

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

  # initiate stripe PaymentIntent
  intent = stripe.PaymentIntent.create(
    amount = amount,
    currency = "usd",
    automatic_payment_methods = {"enabled": True},
  )

  print('payment initiated ' +intent.client_secret, file=sys.stdout) 

  #retrieve payment for logging

  return render_template('checkout.html', title=title, amount=amount, error=error, client_secret=intent.client_secret)

# Success route
@app.route('/success', methods=['GET'])
def success():
  return render_template('success.html')


if __name__ == '__main__':
  app.run(port=5000, host='0.0.0.0', debug=True)