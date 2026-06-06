from fastapi import APIRouter, Request, Form, Depends, HTTPException, status, Response, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from admin_backend.models.blog_model import BlogModel
import os
import re

def format_rich_text(text: str) -> str:
    html_parts = []
    # Split by double newline to get paragraphs
    blocks = text.strip().split('\r\n\r\n')
    if len(blocks) == 1:
        blocks = text.strip().split('\n\n')
        
    for block in blocks:
        block = block.strip()
        if not block: continue
        
        # Replace **bold** with <strong>bold</strong>
        block = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', block)
        
        # Replace *italic* or _italic_ with <em>italic</em>
        block = re.sub(r'\*(.*?)\*', r'<em>\1</em>', block)
        block = re.sub(r'_(.*?)_', r'<em>\1</em>', block)
        
        # Replace [text](url) with <a href="url" target="_blank">text</a>
        block = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2" target="_blank">\1</a>', block)
        
        # If it's a short block without punctuation at the end, treat it as a title
        if len(block) < 100 and not block.endswith('.') and '\n' not in block:
            html_parts.append(f'<h3 class="font-outfit font-bold text-white text-xl md:text-2xl pt-4">{block}</h3>')
        else:
            block = block.replace('\r\n', '<br>').replace('\n', '<br>')
            html_parts.append(f'<p>{block}</p>')
            
    return '\n'.join(html_parts)

router = APIRouter()

# Setup templates
VIEWS_DIR = os.path.join(os.path.dirname(__file__), '..', 'views')
templates = Jinja2Templates(directory=VIEWS_DIR)

blog_model = BlogModel()

# --- Authentication Helpers ---
ADMIN_USER = "admin"
ADMIN_PASS = "SpacePoint2026!"
AUTH_COOKIE = "admin_auth_token"
AUTH_SECRET = "super_secret_auth_token_for_spacepoint"

def get_current_user(request: Request):
    token = request.cookies.get(AUTH_COOKIE)
    if token == AUTH_SECRET:
        return True
    return False

# --- Routes ---

@router.get("/login", response_class=HTMLResponse)
async def login_get(request: Request):
    if get_current_user(request):
        return RedirectResponse(url="/admin", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse(request=request, name="login.html", context={"request": request})

@router.post("/login")
async def login_post(request: Request, response: Response, username: str = Form(...), password: str = Form(...)):
    if username == ADMIN_USER and password == ADMIN_PASS:
        # Successful login, set cookie
        redirect = RedirectResponse(url="/admin", status_code=status.HTTP_302_FOUND)
        redirect.set_cookie(key=AUTH_COOKIE, value=AUTH_SECRET, httponly=True)
        return redirect
    
    return templates.TemplateResponse(request=request, name="login.html", context={"request": request, "error": "Invalid username or password"})

@router.get("/logout")
async def logout(response: Response):
    redirect = RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    redirect.delete_cookie(AUTH_COOKIE)
    return redirect

@router.get("/admin", response_class=HTMLResponse)
async def admin_panel(request: Request):
    if not get_current_user(request):
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    success = request.query_params.get("success")
    articles = blog_model.load_registry()
    return templates.TemplateResponse(
        request=request, 
        name="admin_panel.html", 
        context={"request": request, "success": success, "articles": articles}
    )

@router.post("/publish")
async def publish_article(
    request: Request,
    article_id: str = Form(None),
    title: str = Form(...),
    description: str = Form(...),
    author: str = Form(...),
    initials: str = Form(...),
    role: str = Form(...),
    date: str = Form(...),
    category: str = Form(...),
    content: str = Form(...),
    image_file: UploadFile = File(None),
    image_url: str = Form(None)
):
    if not get_current_user(request):
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
        
    is_edit = False
    final_article_id = None
    existing_image_path = ""
    
    if article_id and article_id.strip():
        try:
            final_article_id = int(article_id)
            is_edit = True
            # Find existing image path
            articles = blog_model.load_registry()
            for a in articles:
                if a['id'] == final_article_id:
                    existing_image_path = a.get('image_path', '')
                    break
        except ValueError:
            pass
            
    final_image_path = ""
    if image_file and image_file.filename:
        # Save the uploaded file
        upload_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'img')
        os.makedirs(upload_dir, exist_ok=True)
        # Sanitize filename to avoid space issues
        safe_filename = image_file.filename.replace(' ', '_')
        file_path = os.path.join(upload_dir, safe_filename)
        
        content_bytes = await image_file.read()
        with open(file_path, "wb") as buffer:
            buffer.write(content_bytes)
            
        final_image_path = safe_filename
    elif image_url and image_url.strip():
        final_image_path = image_url
    elif is_edit and existing_image_path:
        final_image_path = existing_image_path
    else:
        final_image_path = "The Mission.jpg" # Fallback
    
    data = {
        "title": title,
        "description": description,
        "author": author,
        "initials": initials,
        "role": role,
        "date": date,
        "category": category,
        "image_path": final_image_path,
        "content": format_rich_text(content)
    }
    
    articles = blog_model.load_registry()
    
    if is_edit:
        # Update existing entry in JSON registry
        for i, a in enumerate(articles):
            if a['id'] == final_article_id:
                articles[i] = {
                    "id": final_article_id,
                    "title": title,
                    "description": description,
                    "author": author,
                    "initials": initials,
                    "role": role,
                    "date": date,
                    "category": category,
                    "image_path": final_image_path,
                    "content": content  # Keep raw text content
                }
                break
        blog_model.save_registry(articles)
        # Rewrite the physical HTML file
        blog_model.create_article_file(final_article_id, {**data, "content": format_rich_text(content)})
        # Rebuild blog landing page
        blog_model.rebuild_blog_page()
        
        return RedirectResponse(url="/admin?success=edit", status_code=status.HTTP_302_FOUND)
    else:
        # Generate new article ID
        final_article_id = blog_model.get_next_article_id()
        # Create HTML file
        blog_model.create_article_file(final_article_id, {**data, "content": format_rich_text(content)})
        # Append to JSON registry
        articles.append({
            "id": final_article_id,
            "title": title,
            "description": description,
            "author": author,
            "initials": initials,
            "role": role,
            "date": date,
            "category": category,
            "image_path": final_image_path,
            "content": content  # Keep raw text content
        })
        blog_model.save_registry(articles)
        # Rebuild blog landing page
        blog_model.rebuild_blog_page()
        
        return RedirectResponse(url="/admin?success=1", status_code=status.HTTP_302_FOUND)

@router.get("/delete")
async def delete_article(request: Request, id: int):
    if not get_current_user(request):
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
        
    blog_model.delete_article(id)
    return RedirectResponse(url="/admin?success=delete", status_code=status.HTTP_302_FOUND)

@router.get("/reorder")
async def reorder_articles(request: Request, id: int, direction: str):
    if not get_current_user(request):
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
        
    blog_model.reorder_articles(id, direction)
    return RedirectResponse(url="/admin?success=reorder", status_code=status.HTTP_302_FOUND)
