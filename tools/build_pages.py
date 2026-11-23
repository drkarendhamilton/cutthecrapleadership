"""Builds the inner pages of the site from index.html's head/nav/footer.
Run: python3 tools/build_pages.py   (from the repo root)

Form + booking settings live in site-config.js (edit there, not here).
"""
import re, html

ROOT = '.'
idx = open(f'{ROOT}/index.html').read()

HEAD = idx[:idx.index('</head>')]
FOOTER = re.search(r'<footer class="grand-footer">.*?</footer>', idx, re.S).group(0)
REVEAL_JS = idx[idx.index('<script>\n(function(){\n  var reduce'):]
REVEAL_JS = REVEAL_JS[:REVEAL_JS.index('</script>') + 9]

NAV_LINKS = [('speaking.html', 'Speaking'), ('workshops.html', 'Workshops'),
             ('coaching.html', 'Coaching'), ('book-clubs.html', 'Book Clubs')]


def nav(current, home='index.html'):
    items = ''.join(
        f'<li><a href="{h}"{" aria-current=\"page\" class=\"is-current\"" if h == current else ""}>{t}</a></li>'
        for h, t in NAV_LINKS)
    return f'''<nav>
  <div class="wrap">
    <a href="{home}" class="logo" aria-label="Cut the Crap Leadership home"><img class="logo-img" src="logo-flat.png" alt="Cut the Crap Leadership" width="640" height="167"></a>
    <button class="menu-btn" type="button" aria-label="Open menu" onclick="this.closest(\'nav\').classList.toggle(\'open\')"><span></span><span></span><span></span></button>
    <ul>
      <li><a href="index.html#book">The Book</a></li>
      {items}
      <li><a href="book-now.html" class="nav-cta">Book Now</a></li>
    </ul>
  </div>
</nav>'''


PAGE_CSS = '''<style>
  /* ===== inner pages ===== */
  .page-hero { background: linear-gradient(180deg, var(--champagne), var(--satin)); padding: 96px 0 84px; position: relative; overflow: hidden; }
  .page-hero .wrap { display: grid; grid-template-columns: 1.3fr .9fr; gap: 64px; align-items: center; }
  .page-hero h1 { font-size: clamp(46px, 6.4vw, 84px); margin: 14px 0 22px; }
  .page-hero h1 em { color: var(--camel); }
  .page-hero .lede { font-family: 'Cormorant Garamond', serif; font-style: italic; font-size: 25px; line-height: 1.45; color: var(--text); max-width: 600px; margin-bottom: 34px; }
  .page-hero .ctas { display: flex; gap: 14px; flex-wrap: wrap; }
  .page-hero .side { background: rgba(255,255,255,.6); border-top: 2px solid var(--gold); padding: 34px 32px; }
  .page-hero .side h3 { font-family: 'Jost', sans-serif; font-size: 12px; font-weight: 500; letter-spacing: .3em; text-transform: uppercase; color: var(--camel); margin-bottom: 14px; }
  .page-hero .side ul { list-style: none; }
  .page-hero .side li { padding: 10px 0; border-bottom: 1px solid var(--line); font-size: 16px; }
  .page-hero .side li:last-child { border-bottom: 0; }
  .page-hero .side li strong { font-weight: 500; color: var(--espresso); }
  .block { padding: 96px 0; }
  .block.alt { background: var(--satin); }
  .cards { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; }
  .cards.two { grid-template-columns: repeat(2, 1fr); }
  .card-x { background: #fff; border-top: 2px solid var(--camel); padding: 36px 32px; transition: transform .5s cubic-bezier(.2,.7,.2,1), box-shadow .5s; }
  .card-x:hover { transform: translateY(-6px); box-shadow: 0 26px 50px rgba(74,48,26,.12); }
  .card-x .k { font-family: 'Cormorant Garamond', serif; font-style: italic; font-size: 20px; color: var(--gold); }
  .card-x h3 { font-family: 'Cormorant Garamond', serif; font-weight: 500; font-size: 29px; color: var(--espresso); margin: 6px 0 10px; line-height: 1.15; }
  .card-x p { color: var(--muted); font-size: 16px; }
  .card-x ul { margin: 14px 0 0 18px; color: var(--muted); font-size: 15px; }
  .steps { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0; counter-reset: s; border-top: 1px solid var(--line); }
  .steps > div { padding: 34px 30px 10px 0; counter-increment: s; }
  .steps > div::before { content: '0' counter(s); display: block; font-family: 'Cormorant Garamond', serif; font-size: 44px; color: var(--gold); line-height: 1; margin-bottom: 12px; }
  .steps h3 { font-family: 'Cormorant Garamond', serif; font-weight: 500; font-size: 26px; color: var(--espresso); margin-bottom: 6px; }
  .steps p { color: var(--muted); font-size: 16px; }
  .chips { display: flex; flex-wrap: wrap; gap: 10px; }
  .chips span { border: 1px solid var(--sand); background: rgba(255,255,255,.6); padding: 9px 16px; font-size: 14px; letter-spacing: .04em; }
  /* forms */
  .form-wrap { display: grid; grid-template-columns: .9fr 1.1fr; gap: 64px; align-items: start; }
  .form-wrap .intro h2 { font-size: clamp(36px, 4.4vw, 54px); margin: 12px 0 16px; }
  .form-wrap .intro p { color: var(--muted); font-size: 17px; margin-bottom: 14px; }
  form.lead-form { background: #fff; padding: 40px; border-top: 2px solid var(--gold); box-shadow: 0 30px 60px rgba(74,48,26,.08); }
  .lead-form .row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
  .lead-form label { display: block; font-size: 11px; font-weight: 500; letter-spacing: .24em; text-transform: uppercase; color: var(--camel-dark); margin: 0 0 7px; }
  .lead-form .f { margin-bottom: 18px; }
  .lead-form input, .lead-form select, .lead-form textarea { width: 100%; font: inherit; font-size: 16px; color: var(--text); background: var(--ivory); border: 1px solid var(--sand); padding: 13px 14px; outline: none; transition: border-color .2s, background .2s; border-radius: 0; }
  .lead-form input:focus, .lead-form select:focus, .lead-form textarea:focus { border-color: var(--camel); background: #fff; }
  .lead-form textarea { min-height: 120px; resize: vertical; }
  .lead-form label.check { text-transform: none; letter-spacing: 0; font-weight: 400; font-size: 14px; color: var(--muted); }
  .lead-form .check { display: flex; gap: 10px; align-items: flex-start; font-size: 14px; color: var(--muted); margin: 4px 0 20px; }
  .lead-form .check input { width: auto; margin-top: 4px; }
  .lead-form button { width: 100%; border: 0; cursor: pointer; }
  .lead-form .fine { font-size: 12px; color: var(--muted); margin-top: 14px; text-align: center; }
  .lead-form .fine a { color: var(--camel-dark); }
  .form-done { display: none; text-align: center; padding: 30px 10px; }
  .form-done h3 { font-family: 'Cormorant Garamond', serif; font-weight: 500; font-size: 34px; color: var(--espresso); margin-bottom: 8px; }
  .form-done p { color: var(--muted); }
  form.lead-form.sent .fields { display: none; }
  form.lead-form.sent .form-done { display: block; }
  .booking-embed { background: #fff; border-top: 2px solid var(--gold); min-height: 200px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 40px; gap: 14px; }
  .booking-embed iframe { width: 100%; min-height: 700px; border: 0; }
  .booking-embed .note { color: var(--muted); font-size: 15px; max-width: 420px; }
  .type-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 40px; }
  .type-grid a { display: block; text-decoration: none; background: #fff; padding: 24px 22px; border: 1px solid var(--line); transition: border-color .25s, transform .25s; }
  .type-grid a:hover { border-color: var(--camel); transform: translateY(-3px); }
  .type-grid a strong { display: block; font-family: 'Cormorant Garamond', serif; font-weight: 500; font-size: 24px; color: var(--espresso); }
  .type-grid a span { font-size: 14px; color: var(--muted); }
  nav ul a.is-current { color: var(--camel); }
  nav ul { gap: 26px; }
  @media (max-width: 1080px) { nav ul { gap: 18px; } nav ul a { letter-spacing: .14em; } }
  @media (max-width: 900px) {
    .page-hero .wrap, .form-wrap { grid-template-columns: 1fr; gap: 40px; }
    .cards, .cards.two, .steps, .type-grid { grid-template-columns: 1fr; }
    .lead-form .row { grid-template-columns: 1fr; gap: 0; }
    form.lead-form { padding: 28px 22px; }
    .block { padding: 72px 0; }
  }
</style>'''


def esc(s):
    return html.escape(s, quote=True)


def form(form_id, kind, title, intro_html, fields, button, done_msg, list_group):
    """fields: list of (name, label, type, extra) where type in text/email/tel/date/number/select/textarea/row"""
    out = []
    for fld in fields:
        if fld[0] == 'ROW':
            out.append('<div class="row">' + ''.join(field_html(f) for f in fld[1]) + '</div>')
        else:
            out.append(field_html(fld))
    return f'''<div class="form-wrap">
      <div class="intro reveal">{intro_html}</div>
      <form class="lead-form reveal" id="{form_id}" data-kind="{esc(kind)}" data-group="{esc(list_group)}" novalidate>
        <div class="fields">
          {''.join(out)}
          <label class="check"><input type="checkbox" name="newsletter" value="yes" checked> <span>Also send me Karen&rsquo;s monthly leadership notes and launch news. Unsubscribe anytime.</span></label>
          <button type="submit" class="btn">{button}</button>
          <p class="fine">We respect your privacy. See our <a href="privacy.html">Privacy Policy</a>.</p>
        </div>
        <div class="form-done" role="status" aria-live="polite"><h3>Thank you.</h3><p>{done_msg}</p></div>
      </form>
    </div>'''


def field_html(f):
    name, label, typ = f[0], f[1], f[2]
    extra = f[3] if len(f) > 3 else {}
    req = ' required' if extra.get('required') else ''
    star = ' *' if extra.get('required') else ''
    ph = f' placeholder="{esc(extra["ph"])}"' if extra.get('ph') else ''
    fid = f'f-{name}-{abs(hash(label)) % 9999}'
    if typ == 'select':
        opts = ''.join(f'<option{" selected" if o == extra.get("default") else ""}>{esc(o)}</option>' for o in extra['options'])
        ctl = f'<select id="{fid}" name="{name}"{req}><option value="">Select…</option>{opts}</select>'
    elif typ == 'textarea':
        ctl = f'<textarea id="{fid}" name="{name}"{ph}{req}></textarea>'
    else:
        ctl = f'<input id="{fid}" type="{typ}" name="{name}"{ph}{req}>'
    return f'<div class="f"><label for="{fid}">{esc(label)}{star}</label>{ctl}</div>'


def page(fname, title, desc, current, body):
    head = HEAD
    head = re.sub(r'<title>.*?</title>', f'<title>{esc(title)} | Cut the Crap Leadership</title>', head)
    head = re.sub(r'<meta name="description"[^>]*>', f'<meta name="description" content="{esc(desc)}">', head)
    head = re.sub(r'<meta property="og:title"[^>]*>', f'<meta property="og:title" content="{esc(title)} | Cut the Crap Leadership">', head)
    head = re.sub(r'<meta property="og:description"[^>]*>', f'<meta property="og:description" content="{esc(desc)}">', head)
    doc = (head + PAGE_CSS + '\n<script src="site-config.js"></script>\n</head>\n<body>\n\n<div class="progress" aria-hidden="true"></div>\n'
           + nav(current) + '\n' + body + '\n' + FOOTER.replace('href="#', 'href="index.html#') + '\n'
           + REVEAL_JS + '\n<script src="forms.js"></script>\n</body>\n</html>\n')
    open(f'{ROOT}/{fname}', 'w').write(doc)
    print('built', fname)


BOOK_CTA = '<a href="book-now.html" class="btn">Book Now</a>'
EMAIL_FIELDS = [('ROW', [('name', 'Full name', 'text', {'required': True}), ('email', 'Email', 'email', {'required': True})])]

# ---------------------------------------------------------------- SPEAKING
speaking = f'''
<header class="page-hero">
  <div class="wrap">
    <div>
      <div class="eyebrow">Keynotes &amp; Speaking</div>
      <h1 class="display">Leadership talks that <em>cut the noise.</em></h1>
      <p class="lede">Straight talk, real stories, and one clear framework your audience can use on Monday morning.</p>
      <div class="ctas">{BOOK_CTA}<a href="#topics" class="btn ghost" style="color:var(--espresso)">See the Topics</a></div>
    </div>
    <aside class="side reveal">
      <h3>At a glance</h3>
      <ul>
        <li><strong>Formats:</strong> keynote, breakout, workshop-style session, panel or fireside chat</li>
        <li><strong>Delivery:</strong> in person or virtual</li>
        <li><strong>Audiences:</strong> leadership teams, conferences, universities, churches &amp; ministries, nonprofits</li>
        <li><strong>Speaker:</strong> Dr. Karen Hamilton, DSL &middot; Doctor of Global Strategic Leadership</li>
      </ul>
    </aside>
  </div>
</header>

<section class="block" id="topics">
  <div class="wrap">
    <div class="section-head reveal"><div class="eyebrow"><span class="sec-num">01</span><span class="sec-line"></span>Signature Topics</div>
      <h2 class="display" style="margin-top:12px;">Every talk is tailored to your audience.</h2></div>
    <div class="cards stagger">
      <div class="card-x"><div class="k">Signature keynote</div><h3>Cut the Crap: Then Lead With Clarity</h3><p>The four things that stand between every leader and their results, and how to cut them without cutting corners.</p></div>
      <div class="card-x"><div class="k">C &middot; Complacency</div><h3>Complacency Is a Choice</h3><p>How to spot quiet decline long before it shows up on a report, and how to restart momentum.</p></div>
      <div class="card-x"><div class="k">R &middot; Red Tape</div><h3>Busy Isn&rsquo;t Better</h3><p>Removing the busywork and meetings that teach your best people that looking busy matters more than results.</p></div>
      <div class="card-x"><div class="k">A &middot; Assumptions</div><h3>Assumptions Cost You People</h3><p>Testing what &ldquo;everyone knows&rdquo; before it costs you good decisions and good people.</p></div>
      <div class="card-x"><div class="k">P &middot; Politics</div><h3>Integrity Over Politics</h3><p>Leading with principle when the room rewards whoever manages it best.</p></div>
      <div class="card-x"><div class="k">For educators</div><h3>Leading Change in Higher Education</h3><p>Lessons from building programs, raising retention, and leading academic teams through change.</p></div>
    </div>
  </div>
</section>

<section class="block alt">
  <div class="wrap">
    <div class="section-head reveal"><div class="eyebrow"><span class="sec-num">02</span><span class="sec-line"></span>How It Works</div>
      <h2 class="display" style="margin-top:12px;">Simple from first call to final applause.</h2></div>
    <div class="steps stagger">
      <div><h3>Discovery call</h3><p>A short call to learn about your event, audience, and goals.</p></div>
      <div><h3>Tailored message</h3><p>Karen shapes the talk around your people and the challenges they face.</p></div>
      <div><h3>Deliver &amp; follow through</h3><p>An engaging session, with optional workshops or book copies to keep the momentum going.</p></div>
    </div>
  </div>
</section>

<section class="block" id="inquire">
  <div class="wrap">
    {form('form-speaking', 'Speaking Inquiry', 'Request Karen to speak',
      '<div class="eyebrow">Request Karen</div><h2 class="display">Bring Karen to your event.</h2><p>Share a few details and we&rsquo;ll follow up within two business days.</p><p>Prefer to talk first? <a href="book-now.html" style="color:var(--camel-dark)">Schedule a call</a>.</p>',
      EMAIL_FIELDS + [('ROW', [('organization', 'Organization', 'text', {}), ('phone', 'Phone', 'tel', {})]),
                      ('ROW', [('event_date', 'Event date', 'date', {}), ('audience', 'Audience size', 'number', {'ph': 'e.g. 150'})]),
                      ('format', 'Format', 'select', {'options': ['Keynote', 'Breakout session', 'Workshop-style session', 'Panel / fireside chat', 'Virtual event', 'Not sure yet']}),
                      ('message', 'Tell us about your event', 'textarea', {'ph': 'Theme, audience, location, budget range…'})],
      'Send Speaking Request', 'Your request is on its way. Karen&rsquo;s team will follow up within two business days.', 'Speaking Inquiries')}
  </div>
</section>'''

# ---------------------------------------------------------------- WORKSHOPS
workshops = f'''
<header class="page-hero">
  <div class="wrap">
    <div>
      <div class="eyebrow">Team Workshops</div>
      <h1 class="display">Find your team&rsquo;s CRAP. <em>Then cut it.</em></h1>
      <p class="lede">Hands-on sessions that turn the book into decisions your team actually makes.</p>
      <div class="ctas">{BOOK_CTA}<a href="#formats" class="btn ghost" style="color:var(--espresso)">Workshop Formats</a></div>
    </div>
    <aside class="side reveal">
      <h3>Your team leaves with</h3>
      <ul>
        <li>A shared language for what slows you down</li>
        <li>A prioritized list of what to cut first</li>
        <li>Clear owners and next steps</li>
        <li>A plan to keep the clutter from coming back</li>
      </ul>
    </aside>
  </div>
</header>

<section class="block" id="formats">
  <div class="wrap">
    <div class="section-head reveal"><div class="eyebrow"><span class="sec-num">01</span><span class="sec-line"></span>Workshop Formats</div>
      <h2 class="display" style="margin-top:12px;">Built around your team.</h2></div>
    <div class="cards stagger">
      <div class="card-x"><div class="k">Focused</div><h3>The CRAP Audit</h3><p>A working session where your team names its complacency, red tape, assumptions, and politics, and decides what to cut first.</p></div>
      <div class="card-x"><div class="k">Deep dive</div><h3>Leadership Team Retreat</h3><p>An in-depth session for senior teams to reset priorities, decision-making, and how they work together.</p></div>
      <div class="card-x"><div class="k">Ongoing</div><h3>Multi-Session Series</h3><p>One letter at a time over several sessions, with practice and accountability between each.</p></div>
    </div>
    <div class="reveal" style="margin-top:44px"><div class="eyebrow" style="margin-bottom:14px">Great for</div>
      <div class="chips"><span>Executive teams</span><span>Department heads</span><span>Faculty &amp; academic leaders</span><span>Church &amp; ministry staff</span><span>Nonprofit boards</span><span>New managers</span></div></div>
  </div>
</section>

<section class="block alt">
  <div class="wrap">
    <div class="section-head reveal"><div class="eyebrow"><span class="sec-num">02</span><span class="sec-line"></span>How It Works</div>
      <h2 class="display" style="margin-top:12px;">From conversation to clarity.</h2></div>
    <div class="steps stagger">
      <div><h3>Listen</h3><p>A discovery call to understand your team, goals, and what&rsquo;s getting in the way.</p></div>
      <div><h3>Design</h3><p>Karen tailors the agenda, exercises, and examples to your organization.</p></div>
      <div><h3>Cut &amp; commit</h3><p>Your team leaves with decisions, owners, and a plan, plus optional copies of the book.</p></div>
    </div>
  </div>
</section>

<section class="block" id="inquire">
  <div class="wrap">
    {form('form-workshops', 'Workshop Inquiry', 'Plan a workshop',
      '<div class="eyebrow">Plan a Workshop</div><h2 class="display">Let&rsquo;s design your session.</h2><p>Tell us about your team and we&rsquo;ll follow up within two business days.</p>',
      EMAIL_FIELDS + [('ROW', [('organization', 'Organization', 'text', {}), ('team_size', 'Team size', 'number', {'ph': 'e.g. 25'})]),
                      ('ROW', [('format', 'Format', 'select', {'options': ['The CRAP Audit', 'Leadership team retreat', 'Multi-session series', 'Not sure yet']}),
                               ('delivery', 'Delivery', 'select', {'options': ['In person', 'Virtual', 'Either']})]),
                      ('message', 'What would you like to change?', 'textarea', {'ph': 'Challenges, goals, timing…'})],
      'Send Workshop Request', 'Thank you. Karen&rsquo;s team will follow up within two business days.', 'Workshop Inquiries')}
  </div>
</section>'''

# ---------------------------------------------------------------- COACHING
coaching = f'''
<header class="page-hero">
  <div class="wrap">
    <div>
      <div class="eyebrow">Leadership Coaching</div>
      <h1 class="display">Lead with <em>clarity,</em> not clutter.</h1>
      <p class="lede">Personal coaching for leaders who are ready to stop managing the noise and start leading the work.</p>
      <div class="ctas">{BOOK_CTA}<a href="#options" class="btn ghost" style="color:var(--espresso)">Coaching Options</a></div>
    </div>
    <aside class="side reveal">
      <h3>Coaching is for you if</h3>
      <ul>
        <li>You&rsquo;re busy but not moving the needle</li>
        <li>You&rsquo;ve stepped into a bigger role</li>
        <li>Politics or red tape are wearing you down</li>
        <li>You want a trusted, candid thinking partner</li>
      </ul>
    </aside>
  </div>
</header>

<section class="block" id="options">
  <div class="wrap">
    <div class="section-head reveal"><div class="eyebrow"><span class="sec-num">01</span><span class="sec-line"></span>Coaching Options</div>
      <h2 class="display" style="margin-top:12px;">Choose the support that fits.</h2></div>
    <div class="cards stagger">
      <div class="card-x"><div class="k">One-on-one</div><h3>Executive Coaching</h3><p>Private coaching focused on your goals, your decisions, and the specific CRAP in your way.</p></div>
      <div class="card-x"><div class="k">Small group</div><h3>Leadership Cohorts</h3><p>A small group of leaders growing together, with shared learning and peer accountability.</p></div>
      <div class="card-x"><div class="k">New in role</div><h3>Emerging Leaders</h3><p>For new managers and rising leaders building confidence and clear habits from day one.</p></div>
    </div>
  </div>
</section>

<section class="block alt">
  <div class="wrap">
    <div class="section-head reveal"><div class="eyebrow"><span class="sec-num">02</span><span class="sec-line"></span>How It Works</div>
      <h2 class="display" style="margin-top:12px;">A clear path forward.</h2></div>
    <div class="steps stagger">
      <div><h3>Discovery call</h3><p>A conversation about where you are, where you want to go, and whether it&rsquo;s a fit.</p></div>
      <div><h3>Your CRAP check</h3><p>Identify the complacency, red tape, assumptions, and politics holding you back.</p></div>
      <div><h3>Coaching plan</h3><p>Regular sessions with practical actions, honest feedback, and accountability.</p></div>
    </div>
  </div>
</section>

<section class="block" id="inquire">
  <div class="wrap">
    {form('form-coaching', 'Coaching Inquiry', 'Start coaching',
      '<div class="eyebrow">Get Started</div><h2 class="display">Start with a conversation.</h2><p>Share a little about yourself and we&rsquo;ll be in touch within two business days.</p>',
      EMAIL_FIELDS + [('ROW', [('role', 'Your role / title', 'text', {}), ('organization', 'Organization', 'text', {})]),
                      ('format', 'Interested in', 'select', {'options': ['Executive coaching (one-on-one)', 'Leadership cohort (small group)', 'Emerging leaders', 'Not sure yet']}),
                      ('message', 'What would you like help with?', 'textarea', {'ph': 'Goals, challenges, timing…'})],
      'Request Coaching', 'Thank you. Karen&rsquo;s team will reach out within two business days.', 'Coaching Inquiries')}
  </div>
</section>'''

# ---------------------------------------------------------------- BOOK CLUBS
bookclubs = f'''
<header class="page-hero">
  <div class="wrap">
    <div>
      <div class="eyebrow">Book Clubs</div>
      <h1 class="display">Read it together. <em>Cut it together.</em></h1>
      <p class="lede"><em>Cut the Crap Leadership</em> was made for discussion: leadership teams, church groups, cohorts, and classrooms.</p>
      <div class="ctas"><a href="#register" class="btn">Register Your Book Club</a></div>
    </div>
    <aside class="side reveal">
      <h3>Registered clubs receive</h3>
      <ul>
        <li><strong>Discussion guide</strong> with questions for every chapter</li>
        <li><strong>Bulk-copy options</strong> for your group</li>
        <li><strong>A chance to meet Karen</strong> at a virtual session, as her schedule allows</li>
        <li><strong>Launch news</strong> and book club updates</li>
      </ul>
    </aside>
  </div>
</header>

<section class="block">
  <div class="wrap">
    <div class="section-head reveal"><div class="eyebrow"><span class="sec-num">01</span><span class="sec-line"></span>Why Read It Together</div>
      <h2 class="display" style="margin-top:12px;">Every chapter: one story, one cut, one action.</h2>
      <p>The structure makes it easy to meet weekly: read a chapter, talk about the story, name what your group needs to cut, and commit to one action before you meet again.</p></div>
    <div class="cards stagger">
      <div class="card-x"><div class="k">Workplace</div><h3>Leadership Teams</h3><p>Use it to build a shared language and actually remove what&rsquo;s slowing the team down.</p></div>
      <div class="card-x"><div class="k">Faith</div><h3>Church &amp; Ministry Groups</h3><p>Principled leadership for pastors, staff, volunteers, and boards.</p></div>
      <div class="card-x"><div class="k">Learning</div><h3>Classes &amp; Cohorts</h3><p>A practical text for leadership courses, cohorts, and professional development.</p></div>
    </div>
  </div>
</section>

<section class="block alt" id="register">
  <div class="wrap">
    {form('form-bookclub', 'Book Club Registration', 'Register your club',
      '<div class="eyebrow">Register</div><h2 class="display">Register your book club.</h2><p>Tell us about your group and we&rsquo;ll send the discussion guide and launch updates as soon as they&rsquo;re available.</p><p>Need copies for your group? Choose &ldquo;Yes&rdquo; below and we&rsquo;ll follow up about bulk orders.</p>',
      EMAIL_FIELDS + [('ROW', [('club_name', 'Book club / group name', 'text', {}), ('group_size', 'Number of readers', 'number', {'ph': 'e.g. 12'})]),
                      ('ROW', [('group_type', 'Type of group', 'select', {'options': ['Leadership team', 'Church / ministry', 'Class or cohort', 'Community book club', 'Other']}),
                               ('bulk', 'Need bulk copies?', 'select', {'options': ['Yes', 'No', 'Maybe']})]),
                      ('ROW', [('start_date', 'Planned start', 'date', {}), ('karen_visit', 'Interested in a visit from Karen?', 'select', {'options': ['Yes, virtual', 'Yes, in person', 'No']})]),
                      ('message', 'Anything else?', 'textarea', {})],
      'Register Book Club', 'Your book club is registered. Watch your inbox for the discussion guide and launch updates.', 'Book Clubs')}
  </div>
</section>'''

# ---------------------------------------------------------------- EARLY READERS
early = f'''
<header class="page-hero">
  <div class="wrap">
    <div>
      <div class="eyebrow">Early Readers &middot; Launching December 2026</div>
      <h1 class="display">Be first to <em>cut the crap.</em></h1>
      <p class="lede">Join the Early Readers list for launch-day news, early-reader offers, and no-fluff leadership notes from Karen.</p>
    </div>
    <aside class="side reveal">
      <h3>Early readers get</h3>
      <ul>
        <li>Launch-day announcement and buy links</li>
        <li>Early-reader offers</li>
        <li>Behind-the-scenes updates on the book</li>
        <li>Invitations to launch events</li>
        <li>Karen&rsquo;s monthly leadership notes</li>
      </ul>
    </aside>
  </div>
</header>

<section class="block" id="join">
  <div class="wrap">
    {form('form-early', 'Early Reader Sign-up', 'Join the Early Readers',
      '<div class="eyebrow">Join</div><h2 class="display">Join the Early Readers list.</h2><p>It&rsquo;s free. One email a month, plus launch news. Unsubscribe anytime.</p>',
      [('ROW', [('first_name', 'First name', 'text', {'required': True}), ('email', 'Email', 'email', {'required': True})]),
       ('role', 'I&rsquo;m most interested as a…', 'select', {'options': ['Leader / manager', 'Educator', 'Pastor / ministry leader', 'Book club organizer', 'Just curious']})],
      'Join the Early Readers', 'You&rsquo;re on the list. Watch your inbox for launch news.', 'Early Readers')}
  </div>
</section>'''

# ---------------------------------------------------------------- BOOK NOW
booknow = f'''
<header class="page-hero">
  <div class="wrap" style="grid-template-columns:1fr">
    <div>
      <div class="eyebrow">Book Now</div>
      <h1 class="display">Let&rsquo;s talk about <em>your</em> leaders.</h1>
      <p class="lede">Schedule a free 30-minute discovery call, or send a request and we&rsquo;ll get back to you within two business days.</p>
    </div>
  </div>
</header>

<section class="block">
  <div class="wrap">
    <div class="type-grid stagger">
      <a href="speaking.html#inquire"><strong>Keynotes &amp; Speaking</strong><span>Conferences, retreats, events</span></a>
      <a href="workshops.html#inquire"><strong>Team Workshops</strong><span>The CRAP Audit and more</span></a>
      <a href="coaching.html#inquire"><strong>Coaching</strong><span>One-on-one and cohorts</span></a>
      <a href="book-clubs.html#register"><strong>Book Clubs</strong><span>Register your group</span></a>
      <a href="#request"><strong>Bulk Book Orders</strong><span>Copies for your team</span></a>
      <a href="#request"><strong>Media &amp; Podcasts</strong><span>Interviews and features</span></a>
    </div>
    <div class="section-head reveal"><div class="eyebrow"><span class="sec-num">01</span><span class="sec-line"></span>Schedule a Call</div>
      <h2 class="display" style="margin-top:12px;">Pick a time that works for you.</h2></div>
    <div class="booking-embed reveal" id="booking">
      <p class="note">Online scheduling is coming soon. In the meantime, send a request below and we&rsquo;ll reply with available times.</p>
      <a href="#request" class="btn">Send a Request</a>
    </div>
  </div>
</section>

<section class="block alt" id="request">
  <div class="wrap">
    {form('form-booknow', 'Booking Request', 'Send a request',
      '<div class="eyebrow"><span class="sec-num">02</span><span class="sec-line"></span>Send a Request</div><h2 class="display">Tell us what you need.</h2><p>For speaking, workshops, coaching, bulk orders, or media. We&rsquo;ll follow up within two business days.</p>',
      EMAIL_FIELDS + [('ROW', [('organization', 'Organization', 'text', {}), ('phone', 'Phone', 'tel', {})]),
                      ('ROW', [('request_type', 'Request type', 'select', {'required': True, 'options': ['Keynote / speaking', 'Team workshop', 'Coaching', 'Book club', 'Bulk book order', 'Media / podcast', 'Other']}),
                               ('date', 'Preferred date', 'date', {})]),
                      ('quantity', 'Number of copies (bulk orders)', 'number', {'ph': 'e.g. 50'}),
                      ('message', 'Details', 'textarea', {'ph': 'Tell us about your event, team, or request…'})],
      'Send Request', 'Your request is on its way. We&rsquo;ll follow up within two business days.', 'Booking Requests')}
  </div>
</section>'''

page('speaking.html', 'Keynotes & Speaking', 'Book Dr. Karen Hamilton for keynotes and speaking on Cut the Crap Leadership.', 'speaking.html', speaking)
page('workshops.html', 'Team Workshops', 'Hands-on Cut the Crap leadership workshops for teams.', 'workshops.html', workshops)
page('coaching.html', 'Leadership Coaching', 'One-on-one and small-group leadership coaching with Dr. Karen Hamilton.', 'coaching.html', coaching)
page('book-clubs.html', 'Book Clubs', 'Register your book club for Cut the Crap Leadership.', 'book-clubs.html', bookclubs)
page('early-readers.html', 'Early Readers', 'Join the Early Readers list for Cut the Crap Leadership.', 'early-readers.html', early)
page('book-now.html', 'Book Now', 'Schedule a call or send a request to Dr. Karen Hamilton.', 'book-now.html', booknow)
