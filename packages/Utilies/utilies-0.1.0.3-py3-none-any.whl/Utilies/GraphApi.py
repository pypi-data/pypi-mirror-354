# -*- coding: utf-8 -*-
"""
Created on Mon May  19  2025

@author: Krishna Murthy S (krishnamurthy.s@hpe.com)
"""
import asyncio
import mimetypes
from datetime import timedelta

from Utilies.Client import Auth, AuthenticationError, has_matches

'''importing libraries'''
import re
import os
import logging
from os.path import exists

# Setting up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Graph API class that interacts with Office 365 services
class GraphApi(Auth):
    def __init__(self, client):
        super().__init__(client)
        self.account = self.generate_token()
        self.account_scopes = {
            "send_mail": "email_send",
            "read_mail": "email_read",
            "sharepoint_read": "sharepoint_read",
            "sharepoint_write": "sharepoint_write",
            "onedrive_read": "onedrive_read",
            "onedrive_write": "onedrive_write",
            "graph_read": "graph_read",
            "graph_write": "graph_write",
            "teams_read": "teams_read",
            "teams_write": "teams_write",
            "exchange_read": "exchange_read"
        }

    def validate_email(self, email):
        """Validate email address format."""
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(pattern, email)

    async def send_email_async(self, msg):
        """Send email asynchronously to avoid blocking."""
        try:
            msg.send()
            logging.info("Email sent successfully.")
            return "Email sent successfully"
        except Exception as e:
            logging.error(f"Error sending email: {str(e)}")
            return f"Error: {str(e)}"

    def send_mail(self, receivers=None, receivers_cc=None, subject=None, message=None, file_names=None,
                  template=None, importance='normal', inline_items=None, shared_mailbox=None, receivers_bcc=None):
        """Send an email to specified receivers."""
        try:
            if self.account.is_authenticated:
                # Check if the account has the required scope for sending mail
                if not self.check_account_scope(self.account, "send_mail"):
                    raise PermissionError("Account does not have permission to send emails.")

                # Validate email addresses
                for recipient in (receivers or []):
                    if not self.validate_email(recipient):
                        logging.warning(f"Invalid email address: {recipient}")
                for recipient in (receivers_cc or []):
                    if not self.validate_email(recipient):
                        logging.warning(f"Invalid CC email address: {recipient}")
                for recipient in (receivers_bcc or []):
                    if not self.validate_email(recipient):
                        logging.warning(f"Invalid BCC email address: {recipient}")

                # Initialize the message object
                msg = self.account.new_message()

                # Use shared mailbox if provided
                if shared_mailbox:
                    msg.sender = shared_mailbox

                # Add To, CC, and BCC recipients
                if receivers:
                    msg.to.add(receivers)
                if receivers_cc:
                    msg.cc.add(receivers_cc)
                if receivers_bcc:
                    msg.bcc.add(receivers_bcc)

                # Set subject and importance
                msg.subject = subject or "No Subject"
                msg.importance = importance
                # Handling inline images if provided
                if inline_items:
                    for key, value in inline_items.items():
                        if not exists(value):
                            logging.warning(f"File not found for inline item: {value}")
                            continue

                        mime_type, _ = mimetypes.guess_type(value)
                        if mime_type and mime_type.startswith("image"):
                            # Inline images are rendered as HTML
                            message = message.replace(f"{{{key}}}", f"<img src='{value}'>")

                        else:
                            # Non-image files are treated as regular attachments
                            msg.attachments.add(value)
                            logging.warning(
                                f"Skipping non-image file for inline: {value} and added to regular attachments")
                    msg.body = message
                else:
                    msg.body = self.render_template(template, message) if template else (
                            message or "No message body provided.")
                # Set the email body using the provided template or plain message
                # context = {"message": message}  # Add more context data if needed

                msg.body_text = "This is a plain text version of your message."  # Fallback plain text version

                # Attach additional files if provided and validate their size
                MAX_ATTACHMENT_SIZE = 25 * 1024 * 1024  # 25MB in bytes
                if file_names:
                    for att in file_names:
                        if exists(att):
                            if os.path.getsize(att) > MAX_ATTACHMENT_SIZE:
                                logging.warning(f"File too large to attach: {att}")
                                continue
                            msg.attachments.add(att)
                        else:
                            logging.warning(f"File not found: {att}")

                # Send email asynchronously
                return asyncio.run(self.send_email_async(msg))


            else:
                raise AuthenticationError("Account is not authenticated.")

        except Exception as e:
            logging.error(f"Error sending email: {str(e)}")
            return f"Error: {str(e)}"


    def query_helper(self,qry, search, value):
        re_subject, re_from, re_seen, re_datetime = ('subject', 'from', 'seen', 'created_date')
        re_attach, re_body, re_imp, re_draft, re_reply = ('has_attachment', 'body', 'importance', 'draft', 'reply')

        if has_matches(re_subject, search): return qry.on_attribute('subject').contains(value)
        if has_matches(re_from, search): return qry.on_attribute('from').contains(value)
        if has_matches(re_body, search): return qry.on_attribute('body_preview').contains(value)
        if has_matches(re_seen, search): return qry.on_attribute('is_read').equals(value)
        if has_matches(re_draft, search): return qry.on_attribute('is_draft').equals(value)
        if has_matches(re_attach, search): return qry.on_attribute('has_attachments').equals(value)
        if has_matches(re_imp, search): return qry.on_attribute('importance').equals(value)
        if has_matches(re_reply, search): return qry.on_attribute('reply_to').equals(value)
        if has_matches(re_datetime, search):
            qry = qry.on_attribute('created_date_time').greater_equal(value)
            return qry.on_attribute('created_date_time').less_equal(value + timedelta(days=1))

    def get_mail_folder(self, folder_name):
        return self.account.mailbox().get_folder(folder_name=folder_name)

    def get_query(self, which_mail, qry):
        counter = 1
        clean_cond = lambda x, cond='and': ('and', x.replace('_and', '')) if cond == 'and' else (
            'or', x.replace('_or', ''))  # Clean condition names for _and and _or keywords

        for search, value in which_mail.items():
            if counter == 1:
                if isinstance(value, list):  # Handling lists in filters
                    qry = qry.open_group()
                    icon, src = clean_cond(search, 'or' if '_or' in search else 'and')
                    for last, k in enumerate(value):
                        self.query_helper(qry, src, k)
                        if last != len(value) - 1:  # Correct logic to chain conditions
                            qry = qry.chain(icon)
                    qry = qry.close_group()
                else:
                    self.query_helper(qry, search, value)

            else:
                if isinstance(value, list):
                    qry = qry.chain('and').open_group()
                    icon, src = clean_cond(search, 'or' if '_or' in search else 'and')
                    for last, k in enumerate(value):
                        self.query_helper(qry, src, k)
                        if last != len(value) - 1:
                            qry = qry.chain(icon)
                    qry = qry.close_group()
                else:
                    qry = qry.chain('and')
                    self.query_helper(qry, search, value)
            counter += 1

        return qry

    # def query_helper(self, qry, field, value):
    #     qry.equals(field, value)  # You can expand this to support 'contains', 'startswith', etc.

    def read_mail(self, whichmail={}, attchdir='', mail_limit=1, move_read_mail=None, search_folder='Inbox',
                  mark_read=False, get_body_chars='', subfolder='', attachment_types=None, full_body=False,
                  unread_only=False, order_by=None, select_fields=None, expand_entities=None, search_text=None):
        """
        Enhanced mail reading function with filtering, ordering, search, and attachment handling.
        """
        data = []
        try:
            root_mail = self.get_mail_folder(search_folder)
            mailbox = root_mail
            movebox = None

            # Locate subfolder (if any)
            if subfolder:
                for folder in root_mail.get_folders():
                    if folder.name.lower() == subfolder.lower():
                        mailbox = folder
                        break
                else:
                    logging.warning(f"Subfolder '{subfolder}' not found under {search_folder}. Using base folder.")

            # Locate move folder (if any)
            if move_read_mail:
                for folder in root_mail.get_folders():
                    if folder.name.lower() == move_read_mail.lower():
                        movebox = folder
                        break
                else:
                    logging.warning(f"Move target folder '{move_read_mail}' not found. Skipping move.")

            # Build query
            qry = mailbox.new_query()
            # if unread_only:
            #     qry = qry.on_attribute('is_read').equals(False)
            if search_text:
                qry.search(search_text)

            qry = self.get_query(whichmail, qry)

            # Add advanced query modifiers
            if order_by is not None and len(whichmail) == 0:
                for item in order_by:
                    if " " in item:
                        field, direction = item.split()
                        ascending = direction.lower() != "desc"
                    else:
                        field = item
                        ascending = True  # default to ascending if no direction specified
                    qry.order_by(field, ascending=ascending)
            if select_fields:
                qry.select(*select_fields)
            if expand_entities:
                qry.expand(*expand_entities)

            messages = mailbox.get_messages(limit=mail_limit, query=qry, download_attachments=False)

            for message in messages:
                try:
                    sub = message.subject
                    head = message.message_headers
                    body = message.body if full_body else message.body_preview
                    match = re.search(get_body_chars, body, re.IGNORECASE | re.MULTILINE) if get_body_chars else None
                    att_data = []

                    if message.has_attachments:
                        for att in message.attachments:
                            ext = os.path.splitext(att.name)[1].lstrip('.').lower()
                            if attachment_types and ext not in attachment_types:
                                continue

                            filename = re.sub(r'[\s+]', '_', att.name)
                            filepath = os.path.join(attchdir, filename)
                            att.save(location=attchdir, custom_name=filename)
                            att_data.append(filepath)

                    data.append((sub, head, body, att_data, match.group() if match else None))

                    if movebox:
                        message.move(movebox)
                    if mark_read:
                        message.mark_as_read()

                except Exception as e:
                    logging.error(f"Error processing a message: {e}")

            return data, message, self.account

        except Exception as e:
            logging.error(f"Failed to read mail: {str(e)}")
            return [], None, self.account

    def check_account_scope(self, account, action):
        """Verify if the account has the required scope for the action."""
        required_scope = self.account_scopes.get(action)

        if not required_scope:
            raise ValueError(f"Invalid action: {action}")

        return True
        # return False

    def render_template(self, template, message):
        """Render the provided HTML template with the given message."""
        if not template:
            return message
        return template.replace("{{ message }}", message)
