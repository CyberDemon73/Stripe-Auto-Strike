import requests
import json
import random
from pprint import pprint
import pyfiglet
T = ("Stripe Killers V 4.1")
ASCII_art_1 = pyfiglet.figlet_format(T)
print(ASCII_art_1)




class StripeAPI:
    def authenticate(self, stripe_api_key):
        self.headers = {
            "Authorization": f"Bearer {stripe_api_key}"
        }

####################################
##            CreditCard          ##
####################################

class CreditCard(StripeAPI):
    def generate_card_number(self):
        choices = [4242424242424242, 4000056655665556, 5555555555554444, 2223003122003222, 5200828282828210, 4000002500001001, 
        5555552500001001, 4000007840000001]

        credit_card_number = random.choice(choices)
        return credit_card_number
    
    def generate_expiry(self):
        expiry_month = str(random.randint(1, 12)).zfill(2)
        expiry_year = str(random.randint(2022, 2027)).zfill(4)
        return expiry_month, expiry_year
    
    def generate_cvv(self):
        cvc = str(random.randint(000, 999)).zfill(3)
        return cvc
    
    def create_token(self, credit_card_number, expiry_month, expiry_year, cvc):
        token_url = "https://api.stripe.com/v1/tokens"
        data = {
          "card[number]": credit_card_number,
          "card[exp_month]": expiry_month,
          "card[exp_year]": expiry_year,
          "card[cvc]": cvc
        }
        self.headers = {
            "Authorization": f"Bearer {stripe_api_key}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        response = requests.post(token_url, data=data, headers=self.headers)
        
        if response.status_code == 200:
            T = ("Successfully created credit card token.")
            ASCII_art_1 = pyfiglet.figlet_format(T)
            print(ASCII_art_1)
            ####  Pretty Print  ####
            #print("Successfully created credit card token.")
            #print("Status Code:", response.status_code)
            #print("Response Body:", json.dumps(response.json(), indent=2))
            token = response.json()["id"]
            transaction_details = response.json()
            print("Payment Token ID:", transaction_details['id'])
            print("Card ID:", transaction_details['card']['id'])
            print("Brand:", transaction_details['card']['brand'])
            print("Country:", transaction_details['card']['country'])
            print("Fingerprint:", transaction_details['card']['fingerprint'])
            print("Funding:", transaction_details['card']['funding'])
            print("Client IP:", transaction_details['client_ip'])
            print("")
            print("")

            return token
        else:
            print("Unable to create credit card token. Check your API key and credit card details and try again.")

####################################
##            Customer            ##
####################################

class Customer(StripeAPI):
    def create_customer(self, customer_name, customer_email, customer_phone, token):
        customer_url = "https://api.stripe.com/v1/customers"
        data = {
            "source": token,
            "name": customer_name,
            "email": customer_email,
            "phone": customer_phone,
            "source": token
        }
        self.headers = {
            "Authorization": f"Bearer {stripe_api_key}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        response = requests.post(customer_url, data=data, headers=self.headers)

        if response.status_code == 200:
            customer_id = response.json()["id"]

            T = (f"Successfully created Customer ID:")
            ASCII_art_1 = pyfiglet.figlet_format(T)
            print(ASCII_art_1)
            #print("")
            #print("")
            #print(f"Customer ID: {customer_id}")
            #print("Object Type:", customer_id['object'])
            #print("Card ID:", customer_id['default_source'])
            #print("Invoice Prefix:", customer_id['invoice_prefix'])
            #print("")
            #print("")
            #print("Status Code:", response.status_code)
            #print("Response Body:", json.dumps(response.json(), indent=2))
            return customer_id
        else:
            print("Unable to create Customer ID")

####################################
##          Transaction           ##
####################################

class Transaction(StripeAPI):
                ## Create Payment ##
    def create_transaction(self, customer_id, amount, currency):
        charge_url = "https://api.stripe.com/v1/charges"
        data = {
            "customer": customer_id,
            "amount": amount,
            "currency": currency
        }
        self.headers = {
            "Authorization": f"Bearer {stripe_api_key}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        response = requests.post(charge_url, data=data, headers=self.headers)

        if response.status_code == 200:
            print("Successfully created transaction.")
            #print("Status Code:", response.status_code)
            #print("Response Body:", json.dumps(response.json(), indent=2))
            
            transaction_id = response.json()["id"]
            return transaction_id
        else:
            print("Unable to create transaction. Check your API key and customer details and try again.")
    
############################################
##          Retrive Transaction           ##
############################################

    def retrieve_transaction(self, transaction_id):
        charge_url = f"https://api.stripe.com/v1/charges/{transaction_id}"
        response = requests.get(charge_url, headers=self.headers)

        if response.status_code == 200:
            transaction_details = response.json()
            T = ("Transaction Success")
            ASCII_art_1 = pyfiglet.figlet_format(T)
            print(ASCII_art_1)
            print("Amount:", transaction_details['amount'])
            print("Transaction ID:", transaction_details['balance_transaction'])
            print("Company:", transaction_details['calculated_statement_descriptor'])
            print("Status:", transaction_details['outcome']['network_status'])
            print("Risk Level:", transaction_details['outcome']['risk_level'])
            print("Risk Score:", transaction_details['outcome']['risk_score'])
            print("Response Message:", transaction_details['outcome']['seller_message'])
            print("Reciept URL:", transaction_details['receipt_url'])
            print("")
            print("")
            #print("Successfully retrieved transaction details.")
            #print("Status Code:", response.status_code)
            #print("Response Body:", json.dumps(response.json(), indent=2))
            
            return transaction_details
        else:
            print("Unable to retrieve transaction details. Check your API key and transaction ID and try again.")


####################################
##    Begin The Main Funtion      ##
####################################


# Get Stripe API key from user
stripe_api_key = input("Enter your Stripe API key: ")

###################################################################################################

# Authenticate the requests
stripe = StripeAPI()
stripe.authenticate(stripe_api_key)

###################################################################################################

# Display Account ID
response = requests.get("https://api.stripe.com/v1/account", headers=stripe.headers)

if response.status_code == 200:
  account_id = response.json()["id"]
  pprint(f"Your Account ID: {account_id}")

###################################################################################################

# Generate Credit Card details
credit_card = CreditCard()
credit_card_number = credit_card.generate_card_number()
expiry_month, expiry_year = credit_card.generate_expiry()
cvv = credit_card.generate_cvv()

###################################################################################################33

#Print The Details
pprint(f"Generated credit card number: {credit_card_number}")
pprint(f"Expiry Month: {expiry_month}")
pprint(f"Expiry Year: {expiry_year}")
pprint(f"CVV: {cvv}")

###################################################################################################

# Create Credit Card Token using Stripe API
token = credit_card.create_token(credit_card_number, expiry_month, expiry_year, cvv)

###################################################################################################

# Request customer data from user to create Customer ID
customer_name = input("Enter Customer Name: ")
customer_email = input("Enter Customer Email: ")
customer_phone = input("Enter Customer Phone: ")

###################################################################################################

# Create Customer ID using Stripe API
customer = Customer()
customer_id = customer.create_customer(customer_name, customer_email, customer_phone, token)

###################################################################################################

# Request transaction data from user to create Transaction
amount = input("Enter transaction amount in Cents: ")
currency = input("Enter transaction currency: ")

###################################################################################################

# Create Transaction using Stripe API
transaction = Transaction()
transaction_id = transaction.create_transaction(customer_id, amount, currency)

###################################################################################################

# Retrieve Transaction details
transaction_details = transaction.retrieve_transaction(transaction_id)

###################################################################################################
