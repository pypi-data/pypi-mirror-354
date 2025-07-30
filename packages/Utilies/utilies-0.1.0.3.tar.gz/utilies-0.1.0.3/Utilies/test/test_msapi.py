import os

from Utilies.Client import Client
from Utilies.GraphApi import GraphApi
from Utilies.msapi_bot import SharePointManager, Sharepoint_List
import pandas as pd

print("Main Started")
clt = Client(
    name='*@hpe.com'
    , client_id=''
    , client_secret=''
    , email_id=''
    , token_file_path=''
)

gpi = GraphApi(clt)

spm = SharePointManager(clt)
#
# spm.download_filtered_files(site_name='Developedcodes' ,root_folder_path='BSR Automation\\Scripts',local_download_path= r'C:\Users\skrishna\Documents\Python_Projects\2023\Pricing Data for Heightened Review_455\Output', filters={'starts_with': 'bsr'})
# spm.download_specific_file(site_name='Developedcodes' ,file_path_on_sharepoint='BSR Automation\\Scripts\\BSR_Cash_re_extraction.py',local_download_folder= r'C:\Users\skrishna\Documents\Python_Projects\2023\Pricing Data for Heightened Review_455\Output')

# filters = {
#     # 'ends_with': '.csv;.xlsx',
#     'contains': 'screenshot_1747939333',
#     # 'size_greater_than': 1024  # > 1KB
# }
#
# spm.upload_filtered_files(
#     site_name='Developedcodes',
#     library_name='Documents',
#     sharepoint_target_path='Krishna_Test_folder/test_sub_folder',
#     local_folder_path=r'C:\Users\skrishna\Documents\Python_Projects\2023\Pricing Data for Heightened Review_455\venv\test_output',
#     filters=filters
# )

share_point = Sharepoint_List(clt)
# list_schema = share_point.get_list_schema(
#     sharepoint_name='Developedcodes',
#     list_name='filtered_data',
# )
# overall_list = share_point.download_all_site_lists(
#     sharepoint_name='Developedcodes',
#     export_need=True,
#     save_details={
#         "save_dir": r'C:\Users\skrishna\Documents\Python_Projects\2023\Pricing Data for Heightened Review_455\Output',
#         'save_type': 'excel'
#     }
# )
#
# data = share_point.get_list_details(
#     sharepoint_name='Developedcodes',
#     list_name='filtered_data',
#     # filters={'ID': '5'},
#     # filters={'Title': 'EMEA'},
#     limit=2000,
#     export_need=True,
#     save_details={
#         "save_dir": r'C:\Users\skrishna\Documents\Python_Projects\2023\Pricing Data for Heightened Review_455\Output',
#         'save_type': 'excel'
#     }
#
# )
# df  = pd.DataFrame(data)
# print(len(df))
# print(list_schema)
# share_point.update_list_item(sharepoint_name='Developedcodes',list_name='filtered_data',item_id=2, updated_data={'Title': 'Updated Krishna '})
# share_point.delete_list_item(
#     sharepoint_name='Developedcodes',
#     list_name='filtered_data',
#     item_id=2
# )
#
# share_point.create_list_item(
#         sharepoint_name='Developedcodes',
#         list_name='filtered_data',
#         item_data={'Title': 'Krishna'}
# )


def send_mail_test():
    # Define email parameters
    receivers = ["krishnamurthy.s@hpe.com", "krishnamurthy.s@hpe.com"]  # List of recipients
    receivers_cc = None
    subject = "Test Subject"
    message = "This is a test email message. {image1}"
    file_names = [
        r"C:\Users\skrishna\Downloads\Automated_IL10_Credit_Note_Creation.zip"]  # List of file paths for attachments (optional)
    template = "<html><body>{{ message }}</body></html>"
    importance = "high"  # Can be "normal", "high", etc.
    inline_items = {"image1": r"C:\Users\skrishna\Pictures\Datatable.PNG"}  # Inline image attachments (optional)

    # Call the send_mail function
    result = gpi.send_mail(
        receivers=receivers,
        receivers_cc=receivers_cc,
        subject=subject,
        message=message,
        file_names=file_names,
        template=template,
        importance=importance,
        inline_items=inline_items,
        shared_mailbox=None
    )

    # Print the result
    print(result)

# send_mail_test()
search_criteria = {
    # "from": "krishnamurthy.s@hpe.com",
    "subject_and": ["Concur"]
}

output = gpi.read_mail(
    whichmail=search_criteria,
    attchdir=r"C:\Users\skrishna\Documents\Python_Projects\2023\Pricing Data for Heightened Review_455\Output\Tes 13131",
    mail_limit=5,
    move_read_mail=None,
    search_folder="Inbox",
    mark_read=True,
    get_body_chars=r"attached\s*:\s*",
    subfolder="",
    attachment_types=["pdf", "xlsx"],
    full_body=True,
    unread_only=False,
    order_by=["receivedDateTime desc"],
    # select_fields=["subject", "from", "receivedDateTime", "hasAttachments"],
    expand_entities=["attachments"],
    # search_text="Order"
)
# output = gpi.read_mail(
#     whichmail={
#         # "subject":"Spain RTR - XML missing in Deloitte FTP",
#         "from": 'bot.fin-rtr-001@hpe.com',
#         "has_attachments": True,
#         'is_read': False
#     },
#     attchdir=r"C:\Users\skrishna\Documents\Python_Projects\2023\Pricing Data for Heightened Review_455\Output\Tes 13131\output",
#     mail_limit=10,
#     move_read_mail=None,
#     search_folder="Inbox",
#     mark_read=True,
#     get_body_chars=r"Below \s*:\s*",
#     subfolder="TAX Well Project",
#     attachment_types=["pdf", 'xlsx'],
#     full_body=True,
#     unread_only=False,
#     order_by=["receivedDateTime desc"],
#     expand_entities=["attachments"],
#     search_text=None
# )
# # Unpacking the result
messages_data, last_message, account = output

for idx, (subject, headers, body, attachments, regex_match) in enumerate(messages_data):
    print(f"\n--- Email {idx + 1} ---")
    print(f"Subject: {subject}")
    print(f"Attachments: {attachments}")
    print(f"Regex Match: {regex_match}")
    print(f"Body Preview:\n{body[:300]}...\n")

