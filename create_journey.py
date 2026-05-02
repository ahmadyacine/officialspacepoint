import io
import re

# Read template.html
with io.open('template.html', 'r', encoding='utf-8') as f:
    template = f.read()

# Extract header and footer
# The structure has <!-- ════════════════ PAGE CONTENT ════════════════ -->
parts = template.split('<!-- ════════════════ PAGE CONTENT ════════════════ -->')
header = parts[0]
footer = '<!-- ════════════════ FOOTER & CONTACT ════════════════ -->' + parts[1].split('<!-- ════════════════ FOOTER & CONTACT ════════════════ -->')[1]

# We need to replace the "Our Journey" link in the header so it points to journey.html
# The discover dropdown links look like:
# <a href="index.html" class="px-3 py-2 rounded-lg hover:bg-space-purple/30 hover:text-white transition-colors">Our Journey</a>
# I'll just use regex or a simple replace for that specific link.
header = header.replace(
    '<a href="index.html" class="px-3 py-2 rounded-lg hover:bg-space-purple/30 hover:text-white transition-colors">Our\n                  Journey</a>',
    '<a href="journey.html" class="px-3 py-2 rounded-lg hover:bg-space-purple/30 hover:text-white transition-colors">Our\n                  Journey</a>'
)
header = header.replace(
    '<a href="index.html"\n            class="px-3 py-2 text-sm text-space-light hover:text-space-accent transition-colors rounded-lg">Our\n            Journey</a>',
    '<a href="journey.html"\n            class="px-3 py-2 text-sm text-space-light hover:text-space-accent transition-colors rounded-lg">Our\n            Journey</a>'
)


journey_content = '''
  <!-- ════════════════ OUR JOURNEY ════════════════ -->
  <main class="relative z-10 pt-32 pb-24 min-h-screen">
    <div class="max-w-7xl mx-auto px-6 lg:px-8">
      
      <!-- Page Title -->
      <div class="text-center mb-20 fade-in">
        <h1 class="font-outfit font-extrabold text-5xl md:text-6xl text-white mb-4">Our <span class="text-space-accent">Journey</span></h1>
        <p class="text-space-light text-lg md:text-xl max-w-2xl mx-auto">From a single question to an ecosystem of space innovation.</p>
        <div class="w-24 h-1.5 bg-space-accent rounded-full mx-auto mt-6"></div>
      </div>

      <div class="flex flex-col gap-24 lg:gap-32">
        
        <!-- Section 1 -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div class="order-2 lg:order-1 flex flex-col gap-5 text-space-light font-inter leading-relaxed fade-in">
            <h2 class="text-3xl font-outfit font-bold text-white mb-2">Every mission starts with a question.</h2>
            <p>For Abdullah, it was a simple yet defining one: <strong>“What should I do next?”</strong></p>
            <p>As a school graduate, he stood at a crossroads, torn between engineering, business, medicine, and more. Like many students, the path wasn’t clear. With guidance from his family, he stepped into engineering, only to realize it wasn’t the right fit. That moment of uncertainty led him to shift into electrical engineering, a decision that would shape everything that followed.</p>
            <p>Yet even then, the question remained.</p>
            <p>After graduation, Abdullah faced another crossroad: pursue a job, continue studying, or take a completely different path. A recommendation changed everything, he joined a Master’s in Space Science at UAE University. At the same time, he began working at the National Space Science and Technology Center (NSSTC).</p>
            <div class="p-6 mt-4 glass border border-space-accent/30 rounded-2xl relative overflow-hidden">
                <div class="absolute top-0 left-0 w-1 h-full bg-space-accent"></div>
                <p class="text-white italic">"That’s when everything clicked. In the mornings, he was building real satellites, working on systems, integration, and real missions. At night, he was studying the theory behind them."</p>
            </div>
            <p>But something didn’t add up. There was a clear gap between what students learn… and what engineers actually do.</p>
            <p>Space technology, one of the most exciting and impactful fields, was simply out of reach for most students. Not because of lack of interest, but because of lack of access. The tools were expensive. The experience was limited. The learning was disconnected.</p>
            <p class="font-bold text-space-accent">That realization became the turning point.</p>
          </div>
          <div class="order-1 lg:order-2 relative fade-in glass p-2 rounded-[2rem] border border-space-purple/30 shadow-[0_0_30px_rgba(167,125,255,0.15)]">
            <div class="relative rounded-[1.5rem] overflow-hidden aspect-[4/3] group">
              <img src="assets/img/Story Photos/PHOTO 1.jpg" alt="Abdullah starting the journey" class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105" />
            </div>
          </div>
        </div>

        <!-- Section 2 -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div class="relative fade-in glass p-2 rounded-[2rem] border border-space-purple/30 shadow-[0_0_30px_rgba(167,125,255,0.15)]">
            <div class="relative rounded-[1.5rem] overflow-hidden aspect-[4/3] group">
              <img src="assets/img/Story Photos/PHOTO 2.jpg" alt="The Birth of SatKit" class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105" />
            </div>
          </div>
          <div class="flex flex-col gap-5 text-space-light font-inter leading-relaxed fade-in">
            <div class="inline-flex items-center justify-center w-12 h-12 rounded-full bg-space-purple/20 text-2xl mb-2 border border-space-purple/40">🛰️</div>
            <h2 class="text-3xl font-outfit font-bold text-white">The Birth of SatKit</h2>
            <p>Determined to bridge this gap, Abdullah began working on a concept: <br><strong>What if students could actually build and understand satellites, hands-on, from day one?</strong></p>
            <p>This idea first took shape as a virtual concept, which later gained recognition and awards. But the real breakthrough came when the Abdulla Al Ghurair Foundation saw its potential. Through the support and belief of Nesma Farhat, a simple yet powerful question was asked:</p>
            <p class="text-white font-semibold">“Can this be adapted for 12-year-old students?”</p>
            <p>What seemed ambitious became a challenge worth taking. Within just three months, the first prototype of SatKit was developed, a physical, hands-on educational kit that transforms satellite learning into a real, interactive experience.</p>
            <p>But building the kit was only the beginning. It took over a year and a half of development, from March 2023 to June 2024, to fully design the program, curriculum, and experience around it. Every detail was refined to ensure students don’t just learn… but truly experience satellite development.</p>
            <p>During that time, the journey was far from public. A small, focused effort was quietly taking shape, supported by a few who believed in the vision early on. Alongside Nesma’s early support, Mohammed Almehrzi contributed with his technical perspective, while Shahera Al Ameemi supported from a business development angle. At that stage, almost no one knew about SatKit beyond this small circle.</p>
            <p>Even after Abubaker joined, the team remained just four people, working relentlessly behind the scenes to bring the vision to life. That quiet effort soon turned into a defining moment.</p>
            <div class="glass px-5 py-4 rounded-xl border border-space-purple/40 bg-space-purple/10 mt-2">
                <p class="text-white font-medium text-sm">🏆 The project went on to win 1st Place in the AI & Advanced Technology Category at the Graduates Fund’s Entrepreneurship Challenge, marking the first major validation of what SpacePoint was building.</p>
            </div>
          </div>
        </div>

        <!-- Section 3 -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div class="order-2 lg:order-1 flex flex-col gap-5 text-space-light font-inter leading-relaxed fade-in">
            <div class="inline-flex items-center justify-center w-12 h-12 rounded-full bg-space-purple/20 text-2xl mb-2 border border-space-purple/40">🎤</div>
            <h2 class="text-3xl font-outfit font-bold text-white">From Idea to Launch</h2>
            <p>In June 2024, Abdullah stood in front of a panel during a major pitch at Shark Tank Dubai.</p>
            <p>He was asked: <strong>“When are you launching?”</strong></p>
            <p>His answer: <strong>“Tomorrow.”</strong></p>
            <p>And that’s exactly what happened. The journey officially began.</p>
            <ul class="space-y-4 mt-4">
              <li class="flex items-start gap-3">
                <div class="w-2 h-2 mt-2 rounded-full bg-space-accent flex-shrink-0"></div>
                <div><span class="text-white font-semibold">July 2024:</span> First pilot launched at the NASA Space Apps Challenge</div>
              </li>
              <li class="flex items-start gap-3">
                <div class="w-2 h-2 mt-2 rounded-full bg-space-accent flex-shrink-0"></div>
                <div><span class="text-white font-semibold">October 2024:</span> First major contract signed with Space42 (formerly Yahsat/Bayanat)</div>
              </li>
            </ul>
            <p class="mt-4 italic">That moment marked more than just traction, it was validation from the industry itself.</p>
          </div>
          <div class="order-1 lg:order-2 grid grid-cols-1 sm:grid-cols-2 gap-6 fade-in">
             <div class="relative glass p-2 rounded-[1.5rem] border border-space-purple/30 aspect-[4/5] overflow-hidden">
                <img src="assets/img/Story Photos/Shark Tank 1_.jpg" alt="Shark Tank Dubai Pitch" class="w-full h-full object-cover rounded-xl" />
             </div>
             <div class="relative glass p-2 rounded-[1.5rem] border border-space-purple/30 aspect-[4/5] overflow-hidden sm:mt-10">
                <img src="assets/img/Story Photos/WhatsApp Image 2024-11-05 at 2.08.29 AM (1).jpeg" alt="Major Contract Signing" class="w-full h-full object-cover rounded-xl" />
             </div>
          </div>
        </div>

        <!-- Section 4 -->
        <div class="max-w-4xl mx-auto glass p-8 md:p-12 rounded-[2rem] border border-space-purple/30 fade-in relative overflow-hidden">
            <div class="absolute top-0 right-0 w-64 h-64 bg-space-accent/10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/3"></div>
            <div class="inline-flex items-center justify-center w-12 h-12 rounded-full bg-space-purple/20 text-2xl mb-6 border border-space-purple/40">🤝</div>
            <h2 class="text-3xl font-outfit font-bold text-white mb-6">A Shared Mission</h2>
            <div class="text-space-light font-inter leading-relaxed space-y-5">
              <p>In January 2024, before the official launch, another key piece of the puzzle came together.</p>
              <p><strong>Abubaker joined the journey.</strong></p>
              <p>Having experienced a similar path of uncertainty in his own academic journey, eventually finding his place in mechanical engineering, he deeply connected with the mission. He didn’t just join a startup. He joined a purpose.</p>
              
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-6 py-6">
                 <div class="bg-space-dark/50 border border-space-purple/20 rounded-2xl p-5">
                    <h4 class="text-white font-bold mb-2">Abdullah</h4>
                    <p class="text-sm">Leads the electrical and systems development vision</p>
                 </div>
                 <div class="bg-space-dark/50 border border-space-purple/20 rounded-2xl p-5">
                    <h4 class="text-white font-bold mb-2">Abubaker</h4>
                    <p class="text-sm">Leads the mechanical and product experience aspects</p>
                 </div>
              </div>

              <p>Together, they built SpacePoint as co-founders, combining complementary expertise with a shared belief: <strong>students deserve access to real, hands-on space technology.</strong></p>
              <p>Supporting them is a board of advisors, industry experts who believed in the mission early on and contributed their time, knowledge, and trust without expecting anything in return.</p>
            </div>
        </div>

        <!-- Section 5 -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div class="relative fade-in glass p-2 rounded-[2rem] border border-space-purple/30 shadow-[0_0_30px_rgba(167,125,255,0.15)]">
            <div class="relative rounded-[1.5rem] overflow-hidden aspect-[4/3] group">
              <img src="assets/img/Story Photos/PHOTO 3.jpg" alt="Expanding Beyond Borders" class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105" />
            </div>
          </div>
          <div class="flex flex-col gap-5 text-space-light font-inter leading-relaxed fade-in">
            <div class="inline-flex items-center justify-center w-12 h-12 rounded-full bg-space-purple/20 text-2xl mb-2 border border-space-purple/40">🌍</div>
            <h2 class="text-3xl font-outfit font-bold text-white">Expanding Beyond Borders</h2>
            <p>What started as a single idea quickly grew into a regional movement.</p>
            <p>SpacePoint entered leading incubators and programs, including:</p>
            <ul class="space-y-3 mb-2">
              <li class="flex items-center gap-3">
                <div class="w-1.5 h-1.5 rounded-full bg-space-accent"></div>
                UAE-based incubators and innovation platforms
              </li>
              <li class="flex items-center gap-3">
                <div class="w-1.5 h-1.5 rounded-full bg-space-accent"></div>
                SEA SpaceTech Tech (Saudi Arabia)
              </li>
            </ul>
            <p class="font-semibold text-white">Soon after:</p>
            <ul class="space-y-3">
              <li class="flex items-start gap-3">
                <div class="w-1.5 h-1.5 mt-2 rounded-full bg-space-accent flex-shrink-0"></div>
                <span>KAUST (Saudi Arabia) became a key partner through their KAUST Enrichment for Youth (KEY) Program</span>
              </li>
              <li class="flex items-start gap-3">
                <div class="w-1.5 h-1.5 mt-2 rounded-full bg-space-accent flex-shrink-0"></div>
                <span>Expansion began into Oman through collaborations like Etlaq Spaceport</span>
              </li>
              <li class="flex items-start gap-3">
                <div class="w-1.5 h-1.5 mt-2 rounded-full bg-space-accent flex-shrink-0"></div>
                <span>Entry into Egypt through Maker Faire Cairo as a technical partner</span>
              </li>
            </ul>
            <p class="mt-2 text-space-accent font-medium">Egypt, in particular, became a major focus, marking a strategic step toward scaling impact across the region.</p>
          </div>
        </div>

        <!-- Section 6 -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div class="order-2 lg:order-1 flex flex-col gap-5 text-space-light font-inter leading-relaxed fade-in">
            <div class="inline-flex items-center justify-center w-12 h-12 rounded-full bg-space-purple/20 text-2xl mb-2 border border-space-purple/40">📈</div>
            <h2 class="text-3xl font-outfit font-bold text-white">From One Student to Thousands</h2>
            <p>What began as one student’s question has now impacted hundreds, soon thousands, of students across the region.</p>
            <p>SpacePoint continues to grow rapidly:</p>
            <ul class="space-y-4">
              <li class="flex items-center gap-4 bg-space-purple/5 border border-space-purple/20 p-4 rounded-xl">
                <div class="w-8 h-8 rounded-full bg-space-accent/20 flex items-center justify-center text-space-accent shrink-0">🚀</div>
                <span class="text-white font-medium">Expanding programs across multiple countries</span>
              </li>
              <li class="flex items-center gap-4 bg-space-purple/5 border border-space-purple/20 p-4 rounded-xl">
                <div class="w-8 h-8 rounded-full bg-space-accent/20 flex items-center justify-center text-space-accent shrink-0">🤝</div>
                <span class="text-white font-medium">Building partnerships with leading institutions</span>
              </li>
              <li class="flex items-center gap-4 bg-space-purple/5 border border-space-purple/20 p-4 rounded-xl">
                <div class="w-8 h-8 rounded-full bg-space-accent/20 flex items-center justify-center text-space-accent shrink-0">🛰️</div>
                <span class="text-white font-medium">Empowering students with real satellite development experiences</span>
              </li>
            </ul>
          </div>
          <div class="order-1 lg:order-2 relative fade-in glass p-2 rounded-[2rem] border border-space-purple/30 shadow-[0_0_30px_rgba(167,125,255,0.15)]">
            <div class="relative rounded-[1.5rem] overflow-hidden aspect-[4/3] group">
              <img src="assets/img/Story Photos/PHOTO 4.jpg" alt="Impacting Thousands" class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105" />
            </div>
          </div>
        </div>

        <!-- Section 7 -->
        <div class="text-center py-16 fade-in relative">
          <div class="absolute inset-0 bg-space-purple/5 blur-3xl rounded-[100%] pointer-events-none"></div>
          <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-space-purple/20 text-3xl mb-8 border border-space-purple/40">🌌</div>
          <h2 class="text-4xl md:text-5xl font-outfit font-extrabold text-white mb-8">This Is Just the Beginning</h2>
          <div class="text-space-light font-inter text-xl leading-relaxed max-w-3xl mx-auto space-y-4">
            <p>Our journey is not just about building satellites. It’s about building confidence, curiosity, and capability in the next generation.</p>
            <div class="flex flex-col sm:flex-row items-center justify-center gap-4 sm:gap-8 py-6 font-medium text-white">
               <span>From confusion to clarity.</span>
               <span class="hidden sm:inline text-space-accent">•</span>
               <span>From theory to hands-on impact.</span>
               <span class="hidden sm:inline text-space-accent">•</span>
               <span>From one idea to a growing ecosystem.</span>
            </div>
            <p class="text-2xl font-bold text-space-accent pt-4">And we’re just getting started.</p>
          </div>
        </div>

      </div>
    </div>
  </main>
'''

full_html = header + journey_content + footer

with io.open('journey.html', 'w', encoding='utf-8') as f:
    f.write(full_html)
