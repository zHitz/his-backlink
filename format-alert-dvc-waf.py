import json

# Read the JSON file
with open('/data/dvc/alert-waf.json', 'r') as file:
    data = file.read()

# Modify the contents
modified_data = '[' + data.rstrip() + ']'

# Write the modified contents back to the file
with open('/data/dvc/alert-waf.json', 'w') as file:
    file.write(modified_data)


# Đọc dữ liệu từ tệp JSON
with open('/data/dvc/alert-waf.json') as json_file:
    json_data = json.load(json_file)

# Xử lý và định dạng kết quả

print("🚨<strong>HISSC - Cảnh báo tấn công Dịch vụ công</strong>")
print()
for item in json_data:
    buckets = item['aggregations']['0']['buckets']
    
    for i, bucket in enumerate(buckets):
        ip = bucket['key']
        count = bucket['doc_count']
        aggregations = bucket['1']['buckets']
        
        print(f"🌟<strong>Đối tượng {i+1}:</strong>🌟")
        print(f"<strong>Source IP: {ip}</strong>")
        print(f"<strong>Destination IP: 120.72.116.18</strong>")
        print(f"<strong>Số lần tấn công: </strong>{count}")
        print("<strong>Dạng tấn công:</strong>")
        for j, aggregation in enumerate(aggregations):
            aggregation_key = aggregation['key']
            aggregation_count = aggregation['doc_count']
            
            print(f'<i>  {aggregation_key} : {aggregation_count} lần </i>')     
        print()
print('-----------')
totalcount = item['hits']['total']['value']
print(f'<strong>Tổng cộng:</strong> {totalcount} cuộc tấn công')
