import stripe

stripe.api_key = "sk_test_51RNXtICjhDk9lyme0J33xIEz51cePudiTtJRwSuEFck6SxlxmrWckhb2sqhkBU1Ek2jVxwsUGoqU0XBCvupfK0V700acDRBlqr"

customer = stripe.Customer.create(
    name="John Doe",
    email="john.doe@example.com",
    phone="+254712345678",
    address={
        "line1": "123 Main St",
        "city": "Nairobi",
        "postal_code": "12345",
        "country": "KENYA",
    },
)

print(customer)

# create a payment intent
# https://docs.stripe.com/testing?testing-method=payment-methods#visa
payment_intent = stripe.PaymentIntent.create(
    amount=500,
    currency="usd",
    payment_method="pm_card_visa",
    payment_method_types=["card"],
)

print(payment_intent)

# checkout session
checkout_session = stripe.checkout.Session.create(
    payment_method_types=["card"],
    line_items=[
        {
            "price_data": {
                "product_data": {"name": "Test Product"},
                "unit_amount": 500,
                "currency": "usd",
            },
            "quantity": 1,
        }
    ],
    mode="payment",
    success_url="https://example.com/success",
    cancel_url="https://example.com/cancel",
)

print({"id": checkout_session.id})
