import os
import re

dir_path = r"c:\Users\ahmad yacine\Desktop\SpacePoint\systems-SE\SpacePoint-LandingPage"

pattern = r'app_id: "hsw1zj8e",'
replacement = r'app_id: "hsw1zj8e",\n      action_color: "#A77DFF",\n      background_color: "#A77DFF",'

count = 0
for filename in os.listdir(dir_path):
    if filename.endswith(".html"):
        file_path = os.path.join(dir_path, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        new_content = re.sub(pattern, replacement, content)
        
        if content != new_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            count += 1
            print(f"Updated {filename}")

print(f"Total files updated: {count}")
