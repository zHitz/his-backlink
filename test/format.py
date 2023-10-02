with open("/data/his-door-alert/data.txt", "r", encoding= "utf-8'") as file:
     input_string = file.read()

# Split the input string based on the header and footer
header = input_string.split("User: ")[0]

# Print the header
print(header)

# Extract user, portal, method, and time sections as before
user_section = input_string.split("\nUser: ")[1].split(",\n")[0]
user_list = user_section.split(", ")

portal_section = input_string.split("\nVào cổng: ")[1].split(",\n")[0]
portal_list = portal_section.split(", ")

method_section = input_string.split("\nPhương thức nhận diện: ")[1].split(",\n")[0]
method_list = method_section.split(", ")

time_section = input_string.split("\nThời gian: ")[1].split(",\n")[0]
time_list = time_section.split(", ")

# Remove any empty elements
# user_list = [user.strip() for user in user_list if user.strip()]

# Iterate over the lists and print the information
for i in range(len(user_list)):
    print(f"🌟<strong>User: {user_list[i]}</strong>🌟")
    print("       <strong>Thông tin:</strong>")
    print(f"          <strong>Phương thức nhận diện:</strong> {method_list[i]}")
    print(f"          <strong>Thời gian:</strong> {time_list[i]}")
    print(f"          <strong>Vào cổng:</strong> {portal_list[i]}")
    print()
