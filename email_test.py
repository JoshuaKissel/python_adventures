# Import smtplib for the actual sending function
import smtplib

subject = 'Grab dinner this weekend?'
body = 'How about dinner at 6pm this saturday?'

msg = f'Subject: {subject}\n\n{body}'

smtp.sendmail(msg)