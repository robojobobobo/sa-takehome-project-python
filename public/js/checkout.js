const stripe = Stripe(
    'pk_test_51KWojhGG70SVIjLMrwySfAASeyY6Hd7zM31Ls9RbzRHSS1vyBlaLoE02BauxWSBjYd94lZsjjkFBx8p5YtaHUPob00En8icC0m'
    );

const options = {
    clientSecret: '{{CLIENT_SECRET}}',
    apperance:{/*TODO - mess around with this/*/},
};

const elements = stripe.elements(options);

//create payment element and associate it with a a div by id
const paymentElement = elements.create('payment');
paymentElement.mount('#payment-element');