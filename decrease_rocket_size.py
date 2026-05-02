import os
import re

dir_path = r"c:\Users\ahmad yacine\Desktop\SpacePoint\systems-SE\SpacePoint-LandingPage"

rocket_replacement = r'w-12 h-12'
intercom_h_pattern = r'horizontal_padding:\s*108'
intercom_h_replacement = r'horizontal_padding: 96'

count = 0
for filename in os.listdir(dir_path):
    if filename.endswith(".html"):
        file_path = os.path.join(dir_path, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        new_content = content
        
        rocketNav_pattern = r'(class="[^"]*)w-\[60px\] h-\[60px\]([^"]*"[^>]*id="rocketNav")'
        new_content = re.sub(rocketNav_pattern, r'\1w-12 h-12\2', new_content)
        
        new_content = re.sub(intercom_h_pattern, intercom_h_replacement, new_content)
        
        if content != new_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            count += 1
            print(f"Updated {filename}")

print(f"Total files updated: {count}")
