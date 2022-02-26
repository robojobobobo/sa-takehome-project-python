const stripe = Stripe(
    'pk_test_51KWojhGG70SVIjLMrwySfAASeyY6Hd7zM31Ls9RbzRHSS1vyBlaLoE02BauxWSBjYd94lZsjjkFBx8p5YtaHUPob00En8icC0m'
    );

const options = {
    clientSecret: client_secret,
    apperance:{/*TODO - mess around with this/*/},
};

const elements = stripe.elements(options);

//create payment element and associate it with a a div by id
const paymentElement = elements.create('payment');
paymentElement.mount('#payment-element');

//listen to submission of payment
const form = document.getElementById("payment-form");

form.addEventListener('submit', async (event) => {
  event.preventDefault();

  const {error} = await stripe.confirmPayment({
    elements,
    confirmParams: {
      return_url: 'http://localhost:5000/success?' + client_secret
    },
  });

  if (error) {
    const messageContainer = document.querySelector('#error-message');
    messageContainer.textContent = error.message;
  } else {
    // Your customer will be redirected to your `return_url`. For some payment
    // methods like iDEAL, your customer will be redirected to an intermediate
    // site first to authorize the payment, then redirected to the `return_url`.
  }
});