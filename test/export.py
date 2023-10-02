import urllib.parse

input_file = 'danhsach_url.txt'
output_file = 'url.txt'

urls = []
domains = set()

# Đọc dữ liệu từ file input
with open(input_file) as f:
  for line in f:
    urls.append(line.split()[1]) 

# Lấy domain từ mỗi url    
for url in urls:
  domain = urllib.parse.urlparse(url).netloc 
  domains.add(domain)

# Ghi domain vào output   
with open(output_file, 'w') as f:
  for i, domain in enumerate(domains):
    f.write(f"domain\n")