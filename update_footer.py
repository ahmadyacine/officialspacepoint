import os
import re

dir_path = r"c:\Users\ahmad yacine\Desktop\SpacePoint\systems-SE\SpacePoint-LandingPage"

# We'll use regex to find and replace the email block and the phone block

# Email replace
email_pattern = r'href="mailto:info@spacepoint\.com">info@spacepoint\.com</a>'
email_replacement = r'href="mailto:info@spacepoint.ae">info@spacepoint.ae</a>'

# Phone replace
# We want to replace the two phone lines with just one
phone_pattern = r'<a class="hover:text-space-accent transition-colors" href="tel:\+971501234567">\+971 50 123 4567</a>[\s\S]*?<a class="hover:text-space-accent transition-colors" href="tel:\+97141234567">\+971 4 123 4567</a>'
phone_replacement = r'<a class="hover:text-space-accent transition-colors" href="tel:+971562987005">+971 56 298 7005</a>'

count = 0
for filename in os.listdir(dir_path):
    if filename.endswith(".html"):
        file_path = os.path.join(dir_path, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        new_content = re.sub(email_pattern, email_replacement, content)
        new_content = re.sub(phone_pattern, phone_replacement, new_content)
        
        if content != new_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            count += 1
            print(f"Updated {filename}")

print(f"Total files updated: {count}")
