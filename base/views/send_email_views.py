from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from base.entry_data import email_sender, gmail_password

from urllib.parse import unquote

from email.message import EmailMessage
import ssl
import smtplib
import os




def generate_subject(company_name, order_id, rout, payment_type):
    if payment_type == "Scanned":
        return f"{company_name} - order {order_id} - rout {rout} - documents for payment"
    elif payment_type == "Original":
        return f"Отправка документов на {company_name} - заявка {order_id} - маршрут {rout}"
    else:
        return "No Subject"
    

def generate_body(company_name, customer_manager, order_id, order_price, invoice_num, invoice_date, cmr_number, payment_type):
    if payment_type == "Scanned":
        return f"""
Dear {customer_manager}!

Please find in attachment all documents for payment.

Company: DELTA LOGISTICS SRO
Order: {order_id}
Total price: {order_price} EUR
Invoice number: {invoice_num}
Invoice date: {invoice_date}

Best regards,
Ivan Kubrak
Managing Director
Delta Logistics S.R.O.
TIMOCOM ID: 460496
Cell.: +380 67 443 43 16
Mobile.: +380 50 418 64 84 (Viber, WhatsApp, Telegram)
Email: ivan.kubrak.eu@gmail.com
"""
    elif payment_type == "Original":
        return f"""
Добрый день!

Прошу отправить по почте инвойс {invoice_num} от {invoice_date} на сумму {order_price}EUR
и оригиналы транспортных документов (CMR, invoices и т.д.).

CMR: {cmr_number}

Адрес отправки:
{customer_manager}  # Assuming this is the post address, adjust as needed

Документы во вложении письма!

Best regards,
Ivan Kubrak
Managing Director
Delta Logistics S.R.O.
TIMOCOM ID: 460496
Cell.: +380 67 443 43 16
Mobile.: +380 50 418 64 84 (Viber, WhatsApp, Telegram)
Email: ivan.kubrak.eu@gmail.com
"""
    else:
        return "No Body Content"


# EMAIL VIEWS

@api_view(["POST"])
def sendEmail(request):
    data = request.data
    print("Received Data:", data)

    order_number = data.get("order_number")
    customer_manager = data.get("customer_manager")
    customer_email = data.get("customer_email")
    file_name = data.get("file_name")
    price = data.get("price")
    email_receiver = customer_email
    documents = data.get("documents", [])

    subject = "Hello from DELTA APP"
    body = f"Привіт, {customer_manager}!\n\n" \
           f"Номер замовлення {order_number}.\n\n" \
           f"Будь ласка оплатіть суму {price} EUR.\n\n" \
           f"Гарного дня!\n"

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    # Debug output for MEDIA_ROOT
    print("MEDIA_ROOT:", settings.MEDIA_ROOT)

    # Attach the documents
    for document_path in documents:
        # Print the raw document path as received from the request
        print(f"Raw document path: {document_path}")

        # Decode the URL-encoded document path to get the actual file name
        decoded_path = unquote(document_path)
        print(f"Decoded document path: {decoded_path}")

        # Remove the leading '/media/' if it is part of the path
        if decoded_path.startswith('/media/'):
            decoded_path = decoded_path[len('/media/'):]
            print(f"Trimmed decoded path (after removing '/media/'): {decoded_path}")

        # Construct the full path
        full_path = os.path.join(str(settings.MEDIA_ROOT), decoded_path)
        # Normalize the file path
        normalized_path = os.path.normpath(full_path)
        print(f"Attempting to attach: {normalized_path}")

        # Check if the file exists
        if os.path.exists(normalized_path):
            with open(normalized_path, "rb") as attachment_file:
                attachment_data = attachment_file.read()
                em.add_attachment(attachment_data, maintype="application", subtype="octet-stream", filename=os.path.basename(normalized_path))
                print(f"File attached: {normalized_path}")
        else:
            print(f"File does not exist: {normalized_path}")   
            
    # Send the email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, gmail_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

    return Response({"message": "Email sent successfully"}, status=status.HTTP_200_OK)