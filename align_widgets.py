import os
import re

dir_path = r"c:\Users\ahmad yacine\Desktop\SpacePoint\systems-SE\SpacePoint-LandingPage"

rocket_pattern = r'w-14 h-14'
rocket_replacement = r'w-[60px] h-[60px]'

intercom_h_pattern = r'horizontal_padding:\s*\d+'
intercom_h_replacement = r'horizontal_padding: 108'

intercom_v_pattern = r'vertical_padding:\s*\d+'
intercom_v_replacement = r'vertical_padding: 32'

count = 0
for filename in os.listdir(dir_path):
    if filename.endswith(".html"):
        file_path = os.path.join(dir_path, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        new_content = content
        
        # We only want to replace w-14 h-14 in the rocketNav div, but it's safe to just replace it if it's part of rocketNav.
        # Actually, let's just replace w-14 h-14 anywhere if it's next to rounded-full bg-space-dark/80
        # Better yet, regex replace specifically in the rocketNav string.
        
        rocketNav_pattern = r'(id="rocketNav"[^>]*class="[^"]*)w-14 h-14([^"]*")'
        # Since id="rocketNav" is at the end of the tag in the HTML, the pattern needs to handle id at the end.
        rocketNav_pattern = r'(class="[^"]*)w-14 h-14([^"]*"[^>]*id="rocketNav")'
        new_content = re.sub(rocketNav_pattern, r'\1w-[60px] h-[60px]\2', new_content)
        
        new_content = re.sub(intercom_h_pattern, intercom_h_replacement, new_content)
        new_content = re.sub(intercom_v_pattern, intercom_v_replacement, new_content)
        
        if content != new_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            count += 1
            print(f"Updated {filename}")

print(f"Total files updated: {count}")
