import os
import re
import json

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
REGISTRY_PATH = os.path.join(ROOT_DIR, 'admin_backend', 'models', 'blogs_registry.json')

def init_registry():
    articles = []
    pattern = re.compile(r'^article(\d+)\.html$')
    
    # List all articles in root
    filenames = sorted(
        [f for f in os.listdir(ROOT_DIR) if pattern.match(f)],
        key=lambda x: int(pattern.match(x).group(1))
    )
    
    for filename in filenames:
        article_id = int(pattern.match(filename).group(1))
        filepath = os.path.join(ROOT_DIR, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()
            
        # Parse fields
        title_match = re.search(r'<title>(.*?) \| SpacePoint</title>', html)
        title = title_match.group(1).strip() if title_match else ""
        
        desc_match = re.search(r'<meta content="(.*?)" name="description" />', html)
        description = desc_match.group(1).strip() if desc_match else ""
        
        # Category: find span with uppercase letters or bg-space-purple
        cat_match = re.search(r'bg-space-purple/30[^>]*>\s*([A-Z\s]+)\s*</span>', html)
        category = cat_match.group(1).strip() if cat_match else "TECHNOLOGY"
        
        # Initials
        initials_match = re.search(r'rounded-full bg-space-purple/30 flex items-center justify-center text-sm font-bold text-space-accent">\s*([A-Z]{1,3})\s*</div>', html)
        if not initials_match:
            initials_match = re.search(r'rounded-full bg-space-purple/30 flex items-center justify-center text-xs font-bold text-space-accent">\s*([A-Z]{1,3})\s*</div>', html)
        if not initials_match:
            initials_match = re.search(r'rounded-full bg-space-purple/30 flex items-center justify-center text-\[10px\] font-bold text-space-accent">\s*([A-Z]{1,3})\s*</div>', html)
        initials = initials_match.group(1).strip() if initials_match else "SA"
        
        # Author Name
        author_match = re.search(r'<p class="text-white text-sm font-semibold">\s*(.*?)\s*</p>', html)
        if not author_match:
            author_match = re.search(r'<p class="text-white text-xs font-semibold">\s*(.*?)\s*</p>', html)
        author = author_match.group(1).strip() if author_match else "Sarah Al Kaabi"
        
        # Role & Date
        role_date_match = re.search(r'<p class="text-space-light/50 text-xs">\s*(.*?) • (.*?)\s*</p>', html)
        if not role_date_match:
            role_date_match = re.search(r'<p class="text-space-light/50 text-\[10px\]">\s*(.*?) • (.*?)\s*</p>', html)
        if role_date_match:
            role = role_date_match.group(1).strip()
            date = role_date_match.group(2).strip()
        else:
            role = "Aerospace Instructor"
            date = "January 1, 2026"
            
        # Image path
        img_match = re.search(r'<!-- Article Image -->\s*<div[^>]*>\s*<img src="assets/img/(.*?)"', html)
        if not img_match:
            img_match = re.search(r'<!-- Article Image -->\s*<div[^>]*>\s*<img src="(.*?)"', html)
        image_path = img_match.group(1).strip() if img_match else "The Mission.jpg"
        
        # Content: grab everything in class="max-w-3xl mx-auto text-left ... mb-16" or similar
        content_match = re.search(r'<!-- Article Content -->\s*<div[^>]*>\s*(.*?)\s*</div>\s*<!-- Comment Section -->', html, re.DOTALL)
        content_html = content_match.group(1).strip() if content_match else ""
        
        # Convert HTML content back to basic markdown (replace <p> with nothing/newlines, <h3 ...>Title</h3> with Subheading, etc.)
        content = content_html
        content = content.replace('<p>', '').replace('</p>', '\n\n')
        content = content.replace('<br>', '\n').replace('<br />', '\n')
        content = re.sub(r'<h3[^>]*>(.*?)</h3>', r'\1\n\n', content)
        content = re.sub(r'<strong>(.*?)</strong>', r'**\1**', content)
        content = re.sub(r'<b>(.*?)</b>', r'**\1**', content)
        content = re.sub(r'<em>(.*?)</em>', r'*\1*', content)
        content = re.sub(r'<i>(.*?)</i>', r'*\1*', content)
        content = re.sub(r'<a href="(.*?)"[^>]*>(.*?)</a>', r'[\2](\1)', content)
        
        # Clean up any HTML lists
        content = content.replace('<ul class="list-disc pl-6 space-y-2 text-sm md:text-base">', '')
        content = content.replace('<ul class="list-disc pl-6 space-y-2 text-base">', '')
        content = content.replace('</ul>', '')
        content = content.replace('<li>', '- ').replace('</li>', '\n')
        
        # Clean extra spaces/newlines
        content = re.sub(r'\n{3,}', '\n\n', content).strip()
        
        articles.append({
            "id": article_id,
            "title": title,
            "description": description,
            "category": category,
            "author": author,
            "initials": initials,
            "role": role,
            "date": date,
            "image_path": image_path,
            "content": content
        })
        print(f"Parsed {filename}: {title}")
        
    with open(REGISTRY_PATH, 'w', encoding='utf-8') as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)
    print(f"Registry initialized at {REGISTRY_PATH}")

if __name__ == '__main__':
    init_registry()
