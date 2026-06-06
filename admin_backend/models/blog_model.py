import os
import re
import json
from jinja2 import Environment, FileSystemLoader

# Paths
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
MODELS_DIR = os.path.dirname(__file__)
REGISTRY_PATH = os.path.join(MODELS_DIR, 'blogs_registry.json')

class BlogModel:
    def __init__(self):
        self.env = Environment(loader=FileSystemLoader(MODELS_DIR))
        self.template = self.env.get_template('article_template.html')

    def load_registry(self):
        if not os.path.exists(REGISTRY_PATH):
            return []
        try:
            with open(REGISTRY_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []

    def save_registry(self, articles):
        with open(REGISTRY_PATH, 'w', encoding='utf-8') as f:
            json.dump(articles, f, indent=2, ensure_ascii=False)

    def get_next_article_id(self):
        articles = self.load_registry()
        if not articles:
            return 1
        return max(a['id'] for a in articles) + 1

    def create_article_file(self, article_id, data):
        img_src = data.get('image_path')
        if img_src and not img_src.startswith('http'):
            if not img_src.startswith('/') and not img_src.startswith('assets/img/'):
                img_src = f"/assets/img/{img_src}"
            elif img_src.startswith('assets/img/'):
                img_src = f"/{img_src}"
            
        html_content = self.template.render(
            title=data.get('title'),
            description=data.get('description'),
            category=data.get('category'),
            author=data.get('author'),
            initials=data.get('initials'),
            role=data.get('role'),
            date=data.get('date'),
            image_src=img_src,
            content=data.get('content')
        )
        
        filepath = os.path.join(ROOT_DIR, 'articles', f'article{article_id}.html')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        return filepath

    def delete_article(self, article_id):
        # 1. Delete physical file
        filepath = os.path.join(ROOT_DIR, 'articles', f'article{article_id}.html')
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except Exception as e:
                print(f"Error removing file: {e}")
                
        # 2. Update registry
        articles = self.load_registry()
        articles = [a for a in articles if a['id'] != article_id]
        self.save_registry(articles)
        
        # 3. Rebuild blog.html
        self.rebuild_blog_page()

    def reorder_articles(self, article_id, direction):
        articles = self.load_registry()
        index = -1
        for i, a in enumerate(articles):
            if a['id'] == article_id:
                index = i
                break
                
        if index == -1:
            return False
            
        if direction == 'up' and index > 0:
            # Swap with previous
            articles[index], articles[index - 1] = articles[index - 1], articles[index]
        elif direction == 'down' and index < len(articles) - 1:
            # Swap with next
            articles[index], articles[index + 1] = articles[index + 1], articles[index]
        else:
            return False
            
        self.save_registry(articles)
        self.rebuild_blog_page()
        return True

    def rebuild_blog_page(self):
        blog_html_path = os.path.join(ROOT_DIR, 'blog.html')
        if not os.path.exists(blog_html_path):
            return False
            
        with open(blog_html_path, 'r', encoding='utf-8') as f:
            blog_content = f.read()
            
        # Generate the dynamic card list
        articles = self.load_registry()
        cards_html = []
        
        for a in articles:
            img_src = a.get('image_path')
            if not img_src.startswith('http') and not img_src.startswith('assets/img/'):
                img_src = f"assets/img/{img_src}"
                
            card = f"""
          <!-- Article Card {a['id']} -->
          <a href="articles/article{a['id']}.html" class="group cursor-pointer flex flex-col rounded-3xl overflow-hidden glass border border-space-purple/20 bg-space-purple-dark/5 hover:-translate-y-2 hover:border-space-accent/50 hover:shadow-[0_0_30px_rgba(167,125,255,0.15)] transition-all duration-300">
            <div class="relative h-56 overflow-hidden bg-space-purple-dark/20">
              <img src="{img_src}" alt="{a.get('title')}" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
              <span class="absolute top-4 left-4 bg-space-purple/80 backdrop-blur-md text-white text-[10px] font-bold uppercase tracking-wider px-3 py-1.5 rounded-full">
                {a.get('category')}
              </span>
            </div>
            <div class="p-6 flex flex-col flex-grow bg-[#0B0510]/40">
              <h3 class="font-outfit font-bold text-xl text-white group-hover:text-space-accent transition-colors leading-snug mb-3">
                {a.get('title')}
              </h3>
              <div class="flex items-center gap-2 text-space-light/60 text-xs mb-6">
                <span>{a.get('date')}</span>
              </div>
              <div class="mt-auto flex items-center justify-between">
                <div class="flex items-center gap-2">
                  <div class="w-6 h-6 rounded-full bg-space-purple/30 flex items-center justify-center text-[10px] font-bold text-space-accent">{a.get('initials')}</div>
                  <span class="text-white text-xs font-semibold">{a.get('author')}</span>
                </div>
                <span class="text-space-accent text-xs font-bold flex items-center gap-1 group-hover:gap-2 transition-all">
                  Read 
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
                </span>
              </div>
            </div>
          </a>
"""
            cards_html.append(card)
            
        deck_html = "\n".join(cards_html)
        
        # Replace block inside comment markers
        start_marker = "<!-- ARTICLE CARDS START -->"
        end_marker = "<!-- ARTICLE CARDS END -->"
        
        start_idx = blog_content.find(start_marker)
        end_idx = blog_content.find(end_marker)
        
        if start_idx != -1 and end_idx != -1:
            before = blog_content[:start_idx + len(start_marker)]
            after = blog_content[end_idx:]
            new_content = before + "\n" + deck_html + "\n          " + after
            
            with open(blog_html_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
            
        return False
