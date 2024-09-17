import os
import smtplib
import imghdr
from email.message import EmailMessage
import os

password = os.getenv('webemaildet')
SENDER = 'alanshenjc@gmail.com'
RECEIVER = 'alanshenjc@gmail.com'

# Define the send_email function with the image_path argument
def send_email(image_path):
    print('Send email function started')
    # Create an instance of EmailMessage
    email_message = EmailMessage()
    email_message['Subject'] = 'Intruder alert!'
    email_message.set_content("Attached image of the intruder")
    # Open and read the image file
    with open(image_path, 'rb') as file:
        content = file.read()
    print('Send email function ended')

    # Attach the image to the email
    email_message.add_attachment(content, maintype = 'image', subtype = imghdr.what(None, content))
    # Connect to Gmail's SMTP server
    gmail = smtplib.SMTP('smtp.gmail.com', 587)# host,port
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER, password)

    # Send the email
    gmail.sendmail(SENDER,RECEIVER, email_message.as_string())
    gmail.quit()

if __name__ == '__main__':
    # Call the send_email function with the image path
    send_email(image_path = 'images/19.png')