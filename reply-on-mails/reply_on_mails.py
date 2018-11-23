# Author KaliAWSfatE
from email.mime.multipart import MIMEMultipart
from email.Utils import COMMASPACE, formatdate
from email.mime.text import MIMEText
from argparse import ArgumentParser
import ipaddress
import datetime
import imaplib
import logging
import smtplib
import subprocess
import mailparser
import re
import email
import sys

# logging in to the mail box and getting latest mails.
def get_email_list(source_mail, passwd):
    try:
       # Connecting to the mail
       inbox = imaplib.IMAP4_SSL('imap-mail.outlook.com')
       #inbox.login
       inbox.login(source_mail, passwd)
       #list of "folders" aka labels in gmail.
       inbox.list()
       #connect to inbox.
       inbox.select("inbox")
       date = (datetime.date.today() - datetime.timedelta(0)).strftime('%d-%b-%Y')
       since = '(SINCE ' + '"' + str(date) + '"' + ")"
       result, data = inbox.search(None, "%s" %since)

       #data is a list of integer.
       ids = data[0]
       #ids is a space separated string
       id_list = ids.split()
       logging.info("Done - Retreiving latest mails were successfully")
       return inbox, id_list
    except Exception, e:
       logging.error("Error when connecting to the email: " + str(e))
       sys.exit(1)

# Cheking whether the IP is private or public
def is_private(ip_addr):
    try:
       private = False
       private_ip = ""
       pub_ip = ""
       for i in ip_addr:
          if ipaddress.ip_address(u'%s' %i).is_private:
             private = True
             private_ip = str(i) + " " + private_ip
          else:
            pub_ip = str(i) + " " + pub_ip
       if private:
          return private, private_ip
       else:
          return private, pub_ip
    except Exception, e:
       logging.error("Error - Could not check whether the IP(s) " + ip_addr + " are private or not: " + str(e))

# Handling how to respond to the mails.
def handle_responses(private, mail, ip_addresses, source_mail):
    dest = [mail.from_[0][1], source_mail, mail.to[0][1]]
    if private:
      # Handling the case where at least one of the IPs found in a mail is private
      body = """
Hi %s,

The following IP address(es) are Private: %s.
Leave a message to the email sender.

Regards.""" %( mail.from_[0][0].split("@",1)[0] , ip_addresses)

      send_email(body, dest , mail.subject, mail.message_id)
    if private == False:
      # Handling the case where all the IPs are public
      dt = datetime.datetime.now()
      body = """
Hi %s,
Below IPs are good %s.
Leave a custom message
%s

Thank you,""" %(mail.from_[0][0].split("@",1)[0], dt.strftime('%A'), ip_addresses)
      send_email(body, dest , mail.subject, mail.message_id)

# Working on sending the email
def send_email(body, dest, subject, msg_id, source_mail):
    smtp = "smtp.office365.com:587"
    subject_header = 'Subject: %s' % subject
    from_header = 'From: %s' % from_address
    # Establishing the SMTP connection
    try:
        smtp_server = smtplib.SMTP(smtp)
        smtp_server.starttls()
        smtp_server.login(source_mail, passwd)
    except Exception, e:
        logging.error("SMTP login error: " + str(e))
        sys.exit(1)

    # Sending the email
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = source_mail
        msg['To'] = COMMASPACE.join(dest)
        msg['Subject'] = subject
        msg.add_header("In-Reply-To", msg_id)
        msg.attach( MIMEText(body, 'plain') )
        smtp_server.sendmail(source_mail, dest, msg.as_string())
        smtp_server.quit()
        logging.info("Done - email with the subject '" + subject+ "' sent successfully")
    except Exception, e:
        logging.error("Error when sending email: " + str(e))
        smtp_server.quit()
        sys.exit(1)

# Setting the logging
# add a variable for this
log_file = log_file
logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.FileHandler(log_file)
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S")
handler.setFormatter(formatter)
logger.addHandler(handler)

# Global variable
ips_to_add = ""

# Credentials
source_mail = "sourcemail@blabla.com"
passwd = "password"
source_mail_to_be_ignored = "@something.com"
inbox, email_list = get_email_list(source_mail, passwd)

for email_id in email_list:

    # fetch the email body (RFC822) for the given ID
    result, data = inbox.fetch(email_id, "(RFC822)")

    # here's the body, which is raw text of the whole email including headers and alternate payloads
    raw_email = data[0][1]
    mail = mailparser.parse_from_string(raw_email)

    #IP extraction, Still missing IPs with /24
    if  mail.from_[0][1].split("@",1)[1] != source_mail_to_be_ignored:
        try:
            ip_range_1 = re.findall(r'(?<![.\d])\b\d{1,3}(?:\.\d{1,3}){3}\b(?![.\d]) - (?<![.\d])\b\d{1,3}(?:\.\d{1,3}){3}\b(?![.\d])', mail.text_plain[0])
            ip_range_2 = re.findall(r'(?<![.\d])\b\d{1,3}(?:\.\d{1,3}){3}\b(?![.\d])-(?<![.\d])\b\d{1,3}(?:\.\d{1,3}){3}\b(?![.\d])', mail.text_plain[0])
            #ip_network =       # regex for ips with mask /xx
            ip_range = ip_range_1 + ip_range_2
            ip_addr = []
            ip_addr_raw = re.findall(r'(?<![.\d])\b\d{1,3}(?:\.\d{1,3}){3}\b(?![\d])', mail.text_plain[0])
            for i in ip_addr_raw:
                test = False
                for j in ip_range:
                    if str(i) in str(j):
                        test = True
                    if test == False and ([0<=int(x)<256 for x in re.split('\.',re.match(r'^\d+\.\d+\.\d+\.\d+$',i).group(0))].count(True)==4) == True:
                        ip_addr.append(str(i))
        except Exception, e:
            logging.error("Error - Something went wrong when parsing the email for Ip addresses. " + str(e))
    ip_addr = list(set(ip_addr))
    if ip_addr != []:
       private, ip_addresses = is_private(ip_addr)
       handle_responses(private, mail, ip_addresses)
       if private == False:
            ips_to_add += ip_addresses
