# Tested on Python 3.7.3

# For 2-Step authenticated Gmail accounts
# Follow steps mentioned in below link to generate App Password
# https://support.google.com/accounts/answer/185833

import smtplib
import imaplib
import email
import traceback

FROM_EMAIL = ""
FROM_PASSWORD = ""
IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
TO_EMAIL = ""


def read_and_forward_email():
	try:
		imap4_session = imaplib.IMAP4_SSL(IMAP_SERVER)
		imap4_session.login(FROM_EMAIL, FROM_PASSWORD)
		imap4_session.select('inbox')

		inbox_search_result = imap4_session.search(None, 'ALL')

		mail_ids = inbox_search_result[1]
		id_list = mail_ids[0].split()
		first_email_id = int(id_list[0])
		latest_email_id = int(id_list[-1])

		smtp_session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
		smtp_session.starttls()
		smtp_session.login(FROM_EMAIL, FROM_PASSWORD)

		for i in range(latest_email_id, first_email_id, -1):
			inbox_email = imap4_session.fetch(str(i), '(RFC822)')
			for response_part in inbox_email:
				arr = response_part[0]
				if isinstance(arr, tuple):
					message = email.message_from_string(str(arr[1], 'utf-8'))

					email_subject = message['subject']
					email_from = message['from']
					print('From : ' + email_from + '\n')
					print('Subject : ' + email_subject + '\n')

					message.replace_header("From", FROM_EMAIL)
					message.replace_header("To", TO_EMAIL)

					text = message.as_string()
					smtp_session.sendmail(FROM_EMAIL, TO_EMAIL, text)
					print('Mail Sent\n')

		smtp_session.quit()
	except Exception as e:
		traceback.print_exc()
		print(str(e))
	else:
		print("")


read_and_forward_email()
