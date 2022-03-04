

(async () => {
  //retreive stripe key for this environment from .env file
  const response = await fetch('/stripekey');
  const stripePublishableKey = await response.json();

  //setup Stripe
const stripe = Stripe(
  stripePublishableKey
    );

const appearance = {
    theme: 'flat'
  };
     
const options = {
    clientSecret: client_secret,
    appearance: appearance
};

const elements = stripe.elements(options);


//create payment element and associate it with a a div by id
const paymentElement = elements.create('payment');
paymentElement.mount('#payment-element');

//listen to submission of payment
const form = document.getElementById("payment-form");

//get root URL to make portable between environments
var host = location.protocol.concat('//').concat(location.hostname).concat(':').concat(location.port);

form.addEventListener('submit', async (event) => {
  event.preventDefault();

  const {error} = await stripe.confirmPayment({
    elements,
    confirmParams: {
      return_url:  host +'/success?' + client_secret
    },
  });

  if (error) {
    const messageContainer = document.querySelector('#error-message');
    messageContainer.textContent = error.message;
  } else {
    //put redirection for other payment method errors here
  }
  });
})();