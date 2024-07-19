from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
import os
import smtplib
import codecs

import azure.functions as func
import psycopg2
import psycopg2.extras
from datetime import datetime


def main(msg: func.ServiceBusMessage):
    # notification_id = int(msg.get_body().decode('uft-8'))
    # logging.info('Python ServiceBus queue trigger processed message: %s', notification_id)
    
    try:
        data_body = msg.get_body()
        notification_id = int(data_body.decode('utf-8'))
        logging.info('Python ServiceBus queue trigger processed message: %s', notification_id)
        
        logging.info("Connecting to Postgres Server")
        connection = psycopg2.connect(
            host= "anlt16server.postgres.database.azure.com",
            database= "postgres",
            user= "azureuser",
            password= "123!@#qweQWE",
            port= "5432")
        cursor = connection.cursor()
        
        logging.info(f"Get notification {notification_id}")
        postgresql_query = "SELECT subject, message FROM notification where id = {};"
        cursor.execute(postgresql_query.format(notification_id))
        
        notification_db = cursor.fetchone()
        subject = notification_db[0]
        message = notification_db[1]        
        
        logging.info(f"Get all attendee")
        cursor.execute("SELECT email, first_name FROM attendee")
        attendees = cursor.fetchall()
        
        logging.info(f"Loop through each attendee to send an email")
        for attendee in attendees:
            email = attendee[0]
            first_name = attendee[1]
            custom_subject = '{}: {}'.format(first_name, subject)
            send_email(email, custom_subject, message)
        
        status = "Notified {} attendees".format(len(attendees))        
        cursor.execute("UPDATE notification SET status = '{}', completed_date = '{}' WHERE id = {};".format(status, datetime.utcnow(), notification_id))
        connection.commit()
        logging.info(f"Send out emails and updated data to postgres database")
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
        connection.rollback()
    finally:
        logging.info("Closing connection to Postgres Server")
        if connection:
            cursor.close()
            connection.close()
            logging.info("Postgres Server is closed connection")   
        
# def send_email(email, subject, body):
    
#     msg = MIMEMultipart()
#     msg['From'] = sender_email
#     msg['To'] = email
#     msg['Subject'] = subject
    
#     msg.attach(MIMEText(body, 'plain'))
    
#     try:
#         server = smtplib.SMTP(smtp_server, smtp_port)
#         server.starttls()
        
#         server.login(sender_email, app_password)
        
#         server.sendmail(sender_email, email, msg.as_string())
        
#         server.quit()
        
#         print("Email sent successfullt.")
#     except Exception as e:
#         print(f"failed to send mail: {e}")    
