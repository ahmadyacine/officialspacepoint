import os
import re

# ════════════════ CONFIGURATION ════════════════
# Update these strings whenever you want to change the navigation menu site-wide.

NAV_LINKS_HTML = """        <a href="index.html" class="nav-link hover:text-white transition-colors">Home</a>
        <a href="about.html" class="nav-link hover:text-white transition-colors">About</a>
        <a href="programs.html" class="nav-link hover:text-white transition-colors">Programs</a>
        <a href="use_cases.html" class="nav-link hover:text-white transition-colors">Use Cases</a>
        
        <!-- Discover dropdown -->
        <div class="relative">
          <button id="discoverBtn" class="nav-link flex items-center gap-1 hover:text-white transition-colors focus:outline-none">
            Discover
            <svg class="w-3.5 h-3.5 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M19 9l-7 7-7-7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg>
          </button>
          <div id="discoverMenu" class="absolute top-8 left-1/2 -translate-x-1/2 w-[320px] opacity-0 pointer-events-none translate-y-2 z-50 transition-all duration-300">
            <div class="glass rounded-xl p-4 mt-2 border border-space-purple/20 shadow-2xl">
              <div class="grid grid-cols-2 gap-x-4 gap-y-1 text-xs text-space-light">
                <a href="journey.html" class="px-3 py-2 rounded-lg hover:bg-space-purple/30 hover:text-white transition-colors">Our Journey</a>
                <a href="team.html" class="px-3 py-2 rounded-lg hover:bg-space-purple/30 hover:text-white transition-colors">Team</a>
                <a href="alumni.html" class="px-3 py-2 rounded-lg hover:bg-space-purple/30 hover:text-white transition-colors">Alumni</a>
                <a href="ambassadors.html" class="px-3 py-2 rounded-lg hover:bg-space-purple/30 hover:text-white transition-colors">Ambassadors</a>
                <a href="shop.html" class="px-3 py-2 rounded-lg hover:bg-space-purple/30 hover:text-white transition-colors">Shop</a>
                <a href="student_mission.html" class="px-3 py-2 rounded-lg hover:bg-space-purple/30 hover:text-white transition-colors">Student Missions</a>
                <a href="media_coverage.html" class="px-3 py-2 rounded-lg hover:bg-space-purple/30 hover:text-white transition-colors">Media Coverage</a>
                <a href="our_platforms.html" class="px-3 py-2 rounded-lg hover:bg-space-purple/30 hover:text-white transition-colors">Our Platforms</a>
                <a href="resources.html" class="px-3 py-2 rounded-lg hover:bg-space-purple/30 hover:text-white transition-colors">Resources</a>
                <a href="index.html#events" class="px-3 py-2 rounded-lg hover:bg-space-purple/30 hover:text-white transition-colors">Events</a>
              </div>
            </div>
          </div>
        </div>

        <a href="index.html#blog" class="nav-link hover:text-white transition-colors">Blog</a>
        <a href="index.html#contact" class="nav-link hover:text-white transition-colors">Contact</a>"""

MOBILE_NAV_LINKS_HTML = """        <a href="index.html" class="px-3 py-3 rounded-xl hover:bg-space-purple/20 transition-colors text-space-light hover:text-white">Home</a>
        <a href="about.html" class="px-3 py-3 rounded-xl hover:bg-space-purple/20 transition-colors text-space-light hover:text-white">About</a>
        <a href="programs.html" class="px-3 py-3 rounded-xl hover:bg-space-purple/20 transition-colors text-space-light hover:text-white">Programs</a>
        <a href="use_cases.html" class="px-3 py-3 rounded-xl hover:bg-space-purple/20 transition-colors text-space-light hover:text-white">Use Cases</a>
        <a href="index.html#blog" class="px-3 py-3 rounded-xl hover:bg-space-purple/20 transition-colors text-space-light hover:text-white">Blog</a>
        <a href="index.html#contact" class="px-3 py-3 rounded-xl hover:bg-space-purple/20 transition-colors text-space-light hover:text-white">Contact</a>
        
        <div class="flex flex-col gap-2">
          <button id="mobileDiscoverBtn" class="flex items-center justify-between px-3 py-3 rounded-xl hover:bg-space-purple/20 transition-colors text-space-light hover:text-white w-full text-left font-outfit text-lg font-semibold">
            Discover
            <svg id="mobileDiscoverIcon" class="w-4 h-4 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M19 9l-7 7-7-7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg>
          </button>
          <div id="mobileDiscoverList" class="hidden flex flex-col gap-1 pl-4 border-l border-space-purple/10">
            <a href="journey.html" class="px-3 py-2 text-sm text-space-light hover:text-space-accent transition-colors rounded-lg">Our Journey</a>
            <a href="team.html" class="px-3 py-2 text-sm text-space-light hover:text-space-accent transition-colors rounded-lg">Team</a>
            <a href="alumni.html" class="px-3 py-2 text-sm text-space-light hover:text-space-accent transition-colors rounded-lg">Alumni</a>
            <a href="ambassadors.html" class="px-3 py-2 text-sm text-space-light hover:text-space-accent transition-colors rounded-lg">Ambassadors</a>
            <a href="shop.html" class="px-3 py-2 text-sm text-space-light hover:text-space-accent transition-colors rounded-lg">Shop</a>
            <a href="student_mission.html" class="px-3 py-2 text-sm text-space-light hover:text-space-accent transition-colors rounded-lg">Student Missions</a>
            <a href="media_coverage.html" class="px-3 py-2 text-sm text-space-light hover:text-space-accent transition-colors rounded-lg">Media Coverage</a>
            <a href="our_platforms.html" class="px-3 py-2 text-sm text-space-light hover:text-space-accent transition-colors rounded-lg">Our Platforms</a>
            <a href="resources.html" class="px-3 py-2 text-sm text-space-light hover:text-space-accent transition-colors rounded-lg">Resources</a>
            <a href="index.html#events" class="px-3 py-2 text-sm text-space-light hover:text-space-accent transition-colors rounded-lg">Events</a>
          </div>
        </div>"""

# ════════════════ PROCESSING LOGIC ════════════════

def update_page_navigation(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace Desktop Nav
    desktop_pattern = r'(<nav[^>]*class="hidden lg:flex items-center gap-7 font-inter text-sm font-medium text-space-light"[^>]*>)(.*?)(</nav>)'
    new_desktop_nav = f'\\1\n{NAV_LINKS_HTML}\n      \\3'
    content = re.sub(desktop_pattern, new_desktop_nav, content, flags=re.DOTALL)

    # 2. Replace Mobile Nav
    mobile_pattern = r'(<nav[^>]*class="flex flex-col gap-1 font-outfit text-lg font-semibold"[^>]*>)(.*?)(</nav>)'
    new_mobile_nav = f'\\1\n{MOBILE_NAV_LINKS_HTML}\n      \\3'
    content = re.sub(mobile_pattern, new_mobile_nav, content, flags=re.DOTALL)

    # 3. Replace direct index.html#programs with programs.html globally (for mobile nav and any other references)
    content = content.replace('href="index.html#programs"', 'href="programs.html"')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    files_processed = 0

    for filename in os.listdir(root_dir):
        if filename.endswith('.html'):
            file_path = os.path.join(root_dir, filename)
            print(f"Updating navigation in: {filename}")
            update_page_navigation(file_path)
            files_processed += 1

    print(f"\n[SUCCESS] Done! Updated navigation in {files_processed} pages.")

if __name__ == "__main__":
    main()
