# SIM CARD PURCHASE 
# You have to purchase sim like jio,vodaphone,airtel etc . for that take needed input from user like --(name ,address ,adhar no etc.), then store in db and automatically generate 10 dg phn no and mail that no to that particular person. (note: do it function based and if poosible use oops concept)

import random
import smtplib
import mysql.connector
from email.message import EmailMessage

class Database:
    """Handles all database operations for SIM card purchases."""
    
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",          
            password="*******",  
            database="SIMCardDB"
        )
        self.cursor = self.connection.cursor()

    def insert_customer(self, name, address, aadhar, email, provider, phone_number):
        """Inserts SIM purchase details into the database."""
        query = "INSERT INTO Customers (name, address, aadhar, email, provider, phone_number) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (name, address, aadhar, email, provider, phone_number)
        self.cursor.execute(query, values)
        self.connection.commit()
        print("✅ SIM card purchase details saved in the database!")

    def close_connection(self):
        """Closes the database connection."""
        self.cursor.close()
        self.connection.close()

class EmailService:
    """Handles sending email confirmations for SIM purchases."""
    
    def __init__(self):
        self.sender_email = "*******@gmail.com"  
        self.sender_password = "****************"  

    def send_email(self, name, email, provider, phone_number):
        """Sends SIM purchase confirmation email to the user."""
        subject = f"Your New SIM Card Details - {provider}"
        body = f"""
        Hello {name},

        🎉 Your SIM Card has been successfully activated!

        📲 Mobile Number: {phone_number}
        📡 Provider: {provider}

        Thank you for choosing our service. Enjoy your new connection!

        Regards,
        SIM Card Service Team
        """

        msg = EmailMessage()
        msg.set_content(body)
        msg["Subject"] = subject
        msg["From"] = self.sender_email
        msg["To"] = email

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            print(f"📩 Confirmation email sent to {email} successfully!")
        except Exception as e:
            print(f"⚠ Error sending email: {e}")

class SIMCardPurchase:
    """Handles the entire SIM card purchase process."""
    
    providers = {
        1: "Jio",
        2: "Vodafone",
        3: "Airtel",
        4: "BSNL"
    }

    def __init__(self):
        self.database = Database()
        self.email_service = EmailService()

    def get_user_details(self):
        """Takes user details as input."""
        name = input("Enter your full name: ")
        address = input("Enter your address: ")
        aadhar = input("Enter your Aadhar number: ")
        email = input("Enter your Email ID: ")
        
        print("\nAvailable SIM Providers:")
        for key, value in self.providers.items():
            print(f"{key}. {value}")

        provider_choice = int(input("Select your preferred provider (1/2/3/4): "))
        provider = self.providers.get(provider_choice, "Unknown")

        if provider == "Unknown":
            print("⚠ Invalid choice! Please select a valid provider.")
            return
        
        phone_number = self.generate_phone_number()

        print("\n✅ SIM Card Purchase Successful!")
        print(f"📲 Your New Phone Number: {phone_number} ({provider})")

        # Save details in the database
        self.database.insert_customer(name, address, aadhar, email, provider, phone_number)

        # Send email confirmation
        self.email_service.send_email(name, email, provider, phone_number)

    def generate_phone_number(self):
        """Generates a random 10-digit phone number."""
        return "9" + "".join([str(random.randint(0, 9)) for _ in range(9)])

    def close_resources(self):
        """Closes database connection when the purchase process is finished."""
        self.database.close_connection()

# Running the SIM card purchase system
if __name__ == "__main__":
    sim_system = SIMCardPurchase()
    sim_system.get_user_details()
    sim_system.close_resources()
