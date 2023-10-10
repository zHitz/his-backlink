import datetime
import requests

# Read the content of domain.txt file and set it as the caption
with open('domain_results.txt', 'r') as file:
    domain_content = file.read()

# Replace 'YOUR_API_TOKEN' with your actual Telegram Bot API token
api_token = 'APi-Key'
# Use your channel chat ID
chat_id = 'Chat-ID'  
# Use your channel thread ID
message_thread_id = 'Thread-ID'
message = f'<b> Domain chứa Backlink: </b>\n{domain_content}'

# Lấy ngày hiện tại dưới định dạng yyyy-mm-dd
current_date = datetime.datetime.now().strftime('%Y-%m-%d')

# Lưu DataFrame chung vào tệp Excel chung với mã hóa UTF-8
excel_chung_file = f'results_backlink_{current_date}.xlsx'

# Create the message data
data = {
    'chat_id': chat_id,
    'text': message,
    'message_thread_id': message_thread_id,
    'parse_mode': 'HTML'
}

data_doc = {
    'caption': 'cap',
    'message_thread_id': message_thread_id,
}

files = {
    'document': open(f'{excel_chung_file}', 'rb'),
}

# Send the message using the Telegram Bot API
url_chat = f'https://api.telegram.org/bot{api_token}/sendMessage'
response_chat = requests.post(url_chat, data=data)

url_doc = f'https://api.telegram.org/bot{api_token}/sendDocument?chat_id={chat_id}'
response_doc = requests.post(url_doc, data=data, files=files)
