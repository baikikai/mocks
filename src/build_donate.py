"""Standalone donate page: one editorial scroll, the call to action always in reach.
Copy is the live site's donate copy (see build_rev16.donate); the headings and placeholders are the only additions."""
import html

def icon(name, size=24, cls='lx'):
    paths = {
        'arrow': '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
        'play': '<polygon points="6 3 20 12 6 21 6 3"/>',
        'moon': '<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>',
        'sun': '<circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/>',
    }[name]
    return (f'<svg class="{cls}" viewBox="0 0 24 24" width="{size}" height="{size}" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths}</svg>')

def words(text):
    return ''.join(f'<span class="w"><span style="--w:{i}">{html.escape(w)}</span></span> ' for i, w in enumerate(text.split())).strip()

def video(label, cls=''):
    return (f'<figure class="vid {cls}"><button type="button" class="pl" aria-label="{html.escape(label)}">{icon("play", 28)}</button>'
            f'<figcaption>{html.escape(label)}</figcaption></figure>')

MARQUEE = 'Thank you for your continued support!'

CSS = r'''
:root{
  --D:'Shippori Mincho','Hiragino Mincho ProN',serif;
  --B:'Zen Kaku Gothic New','Hiragino Sans',system-ui,sans-serif;
  --bg:#14171C;--bg2:#1B2029;--fg:#ECEDE8;--mut:#C4C8C0;--line:rgba(236,237,232,.22);--gold:#E2B53F;--gt:#E2B53F;--ink:#14171C;--glow:rgba(226,181,63,.16);
  --ease:cubic-bezier(.2,.7,.2,1);--pad:clamp(20px,5vw,60px);
  color-scheme:dark;
}
@media (prefers-color-scheme: light){:root:not([data-site="dark"]){--bg:#ECEDE8;--bg2:#E1E3DB;--fg:#14171C;--mut:#4B5058;--line:rgba(20,23,28,.28);--gt:#8A5E00;--glow:rgba(138,94,0,.14);color-scheme:light}}
:root[data-site="light"]{--bg:#ECEDE8;--bg2:#E1E3DB;--fg:#14171C;--mut:#4B5058;--line:rgba(20,23,28,.28);--gt:#8A5E00;--glow:rgba(138,94,0,.14);color-scheme:light}
:root[data-site="dark"]{--bg:#14171C;--bg2:#1B2029;--fg:#ECEDE8;--mut:#C4C8C0;--line:rgba(236,237,232,.22);--gt:#E2B53F;--glow:rgba(226,181,63,.16);color-scheme:dark}
*{box-sizing:border-box}
html{scroll-behavior:auto}
body{margin:0;background:var(--bg);color:var(--fg);font-family:var(--B);font-size:19px;line-height:1.6;transition:background .3s,color .3s;overflow-x:clip}
a{color:inherit;text-decoration:none}
button{font:inherit;color:inherit;background:none;border:0;padding:0;cursor:pointer;text-align:left}
:focus-visible{outline:2px solid var(--gt);outline-offset:3px}
p{margin:0}
.lx{display:block;flex:none}
.wrap{padding-inline:var(--pad);max-width:1280px;margin-inline:auto}

/* reading progress: a bar that slides in from the left */
.pg{position:fixed;left:0;right:0;top:0;height:3px;z-index:90;overflow:hidden;pointer-events:none}
.pg i{display:block;height:100%;background:var(--gold);transform:translateX(-100%)}

/* header */
.dh{position:fixed;top:0;left:0;right:0;z-index:80;display:flex;align-items:center;justify-content:space-between;gap:20px;height:70px;padding:3px var(--pad) 0;transition:background .3s,transform .5s var(--ease)}
.dh.bar{background:color-mix(in srgb,var(--bg) 92%,transparent);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.dh .logo{font-family:var(--D);font-size:22px;letter-spacing:-.01em}
.dh .r{display:flex;align-items:center;gap:20px}
.tg{width:44px;height:44px;display:flex;align-items:center;justify-content:center;transition:color .2s}
.tg:hover{color:var(--gt)}
.tg .sun{display:none}
:root[data-site="light"] .tg .sun,:root:not([data-site="dark"]) .tg.sys .sun{display:none}
.dn{display:inline-flex;align-items:center;gap:10px;height:44px;padding:0 20px;border:1px solid var(--gold);color:var(--gt);font-size:16px;letter-spacing:.02em;opacity:0;transform:translateY(-10px);pointer-events:none;transition:opacity .4s var(--ease),transform .4s var(--ease),background .25s,color .25s}
.dn.on{opacity:1;transform:none;pointer-events:auto}
.dn:hover{background:var(--gold);color:var(--ink)}

/* the call to action */
.cta{position:relative;display:inline-flex;align-items:center;justify-content:center;gap:20px;min-height:80px;padding:0 50px;background:var(--gold);color:var(--ink);font-family:var(--D);font-size:30px;letter-spacing:-.005em;overflow:hidden;isolation:isolate;transition:transform .4s var(--ease)}
.cta::before{content:"";position:absolute;inset:0;background:var(--fg);transform:translateX(-101%);transition:transform .5s var(--ease);z-index:-1}
.cta:hover::before,.cta:focus-visible::before{transform:none}
.cta .lx{transition:transform .4s var(--ease)}
.cta:hover .lx{transform:translateX(8px)}
.cta:active{transform:translateY(2px)}

/* hero */
.hero{position:relative;min-height:100svh;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:130px var(--pad) 90px;overflow:hidden}
.hero::before{content:"";position:absolute;left:50%;top:50%;width:min(1100px,150vw);aspect-ratio:1;margin:calc(min(1100px,150vw)/-2) 0 0 calc(min(1100px,150vw)/-2);background:radial-gradient(closest-side,var(--glow),transparent 70%);transform:translateY(var(--py,0px));pointer-events:none}
.num{position:absolute;left:50%;top:50%;display:flex;gap:.02em;font-family:var(--D);font-weight:400;font-size:clamp(300px,52vw,760px);line-height:.8;letter-spacing:-.04em;color:transparent;-webkit-text-stroke:2px color-mix(in srgb,var(--gold) 32%,transparent);transform:translate(-50%,calc(-50% + var(--py,0px)));user-select:none;pointer-events:none;white-space:nowrap}
.num span{display:block;overflow:hidden;padding-block:.06em}
.num b{display:block;font-weight:400;transform:translateY(105%);transition:transform 1.3s var(--ease)}
.ld .num b{transform:none}
.num span:nth-child(2) b{transition-delay:.15s}
.ring{position:absolute;left:50%;top:50%;width:min(980px,140vw);aspect-ratio:1;margin:calc(min(980px,140vw)/-2) 0 0 calc(min(980px,140vw)/-2);color:var(--gold);opacity:.7;clip-path:inset(0 100% 0 0);transition:clip-path 2s var(--ease) .3s;pointer-events:none}
.ld .ring{clip-path:inset(0 0 0 0)}
.hero .hi{position:relative;display:flex;flex-direction:column;align-items:center;gap:30px;max-width:900px}
.ey{font-size:15px;letter-spacing:.14em;text-transform:uppercase;color:var(--mut)}
.hero h1{margin:0;font-family:var(--D);font-weight:400;font-size:clamp(60px,9vw,140px);line-height:1;letter-spacing:-.02em}
.hero .msg{font-family:var(--D);font-size:clamp(26px,3.4vw,44px);line-height:1.2;letter-spacing:-.01em;max-width:18em;text-wrap:balance}
.hero .fine{max-width:30em;color:var(--mut);font-size:17px;line-height:1.5;text-wrap:balance}
.rv{opacity:0;transform:translateY(26px);transition:opacity .9s var(--ease),transform .9s var(--ease);transition-delay:calc(var(--d,0)*90ms)}
.rv.in,.ld .hero .rv{opacity:1;transform:none}
.hero .rv{transition-delay:calc(.5s + var(--d,0)*120ms)}
.hint{position:absolute;left:50%;bottom:30px;width:1px;height:50px;background:var(--line);overflow:hidden;opacity:0;transition:opacity 1s 1.8s}
.ld .hint{opacity:1}
.hint::after{content:"";position:absolute;inset:0;background:var(--gold);transform:translateY(-100%);animation:drip 2.2s var(--ease) infinite}
@keyframes drip{0%{transform:translateY(-100%)}60%,100%{transform:translateY(100%)}}

/* marquee */
.mq{border-block:1px solid var(--line);overflow:hidden;padding-block:25px;background:var(--bg)}
.mq .tr{display:flex;width:max-content;animation:mq 42s linear infinite}
.mq.rev .tr{animation-direction:reverse;animation-duration:55s}
.mq span{display:flex;align-items:center;gap:40px;padding-right:40px;font-family:var(--D);font-size:clamp(30px,5vw,64px);line-height:1.1;white-space:nowrap}
.mq span::after{content:"";width:12px;height:12px;border-radius:50%;background:var(--gold);flex:none}
.mq.rev span{color:transparent;-webkit-text-stroke:1px var(--fg)}
@keyframes mq{to{transform:translateX(-50%)}}

/* editorial */
.sec{padding-block:clamp(80px,12vw,160px)}
.lead{font-family:var(--D);font-size:clamp(32px,5vw,70px);line-height:1.18;letter-spacing:-.015em;max-width:18em;text-wrap:balance}
.w{display:inline-block;overflow:hidden;vertical-align:top;padding-bottom:.12em;margin-bottom:-.12em}
.w>span{display:inline-block;transform:translateY(110%);transition:transform 1s var(--ease);transition-delay:calc(var(--w)*45ms)}
.in .w>span,.wr.in .w>span{transform:none}
.cols{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:30px;margin-top:clamp(50px,7vw,100px);align-items:start}
.cols .a{grid-column:1/span 5}
.cols .b{grid-column:7/span 6;display:flex;flex-direction:column;gap:30px}
.cols p{font-size:21px;line-height:1.6}
.cols .a p{color:var(--mut)}
.pledge{position:relative;margin-top:clamp(60px,9vw,130px);padding-top:30px;border-top:1px solid var(--line);display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:30px;align-items:end}
.pledge p{grid-column:1/span 8;font-family:var(--D);font-size:clamp(26px,3.4vw,46px);line-height:1.22;letter-spacing:-.01em;text-wrap:balance}
.pledge .cta{grid-column:9/span 4;justify-self:end}
.thanks{margin-top:clamp(40px,6vw,80px);font-family:var(--D);font-size:clamp(50px,9vw,140px);line-height:1;letter-spacing:-.02em;color:var(--gt)}

/* videos */
.vid{position:relative;margin:0;aspect-ratio:16/9;background:var(--bg2);border:1px solid var(--line);display:flex;align-items:flex-end;overflow:hidden;clip-path:inset(0 0 100% 0);transition:clip-path 1.2s var(--ease)}
.vid.in{clip-path:inset(0)}
.vid::before{content:"";position:absolute;inset:0;background:linear-gradient(135deg,color-mix(in srgb,var(--gold) 14%,transparent),transparent 60%);transform:translateX(-100%);transition:transform 1.4s var(--ease) .2s}
.vid.in::before{transform:none}
.vid figcaption{position:relative;padding:20px 25px;font-size:15px;color:var(--mut)}
.pl{position:absolute;left:50%;top:50%;width:90px;height:90px;margin:-45px 0 0 -45px;display:flex;align-items:center;justify-content:center;border:1px solid var(--fg);border-radius:50%;transition:background .3s,color .3s,transform .4s var(--ease)}
.pl .lx{margin-left:4px}
.vid:hover .pl,.pl:focus-visible{background:var(--gold);border-color:var(--gold);color:var(--ink);transform:translateY(-4px)}
.feat{margin-top:0}
h2{margin:0 0 clamp(30px,4vw,60px);font-family:var(--D);font-weight:400;font-size:clamp(40px,6vw,88px);line-height:1.05;letter-spacing:-.02em}
.sub{padding-top:clamp(60px,9vw,120px);border-top:1px solid var(--line)}

/* shirts */
.shirts{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:30px;align-items:start}
.shirts .t{grid-column:1/span 4;position:sticky;top:110px}
.shirts .t p{margin-top:20px;font-size:21px;color:var(--mut)}
.shirts .g{grid-column:5/span 8;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}
.shirts .g figure{margin:0;aspect-ratio:3/4;background:var(--bg2);border:1px solid var(--line);opacity:0;transform:translateY(30px);transition:opacity .8s var(--ease),transform .8s var(--ease),border-color .25s;transition-delay:calc(var(--d,0)*60ms)}
.shirts .g figure.big{grid-column:span 2;grid-row:span 2;aspect-ratio:auto}
.shirts .g figure.in{opacity:1;transform:none}
.shirts .g figure:hover{border-color:var(--gold)}

/* check and mail */
.two{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:30px;padding-block:clamp(60px,8vw,110px);border-top:1px solid var(--line)}
.two>div:first-child{grid-column:1/span 5}
.two>div:last-child{grid-column:7/span 6}
.two h3{margin:0 0 20px;font-family:var(--D);font-weight:400;font-size:clamp(30px,3.6vw,48px);line-height:1.1}
.two p{font-size:21px;color:var(--mut);max-width:26em}
form{display:flex;flex-direction:column;gap:20px;align-items:flex-start}
label{font-size:15px;color:var(--mut)}
.f{display:flex;flex-direction:column;gap:10px;width:100%;max-width:520px}
input[type=email]{height:60px;padding:0 20px;background:var(--bg2);border:1px solid var(--line);color:var(--fg);font:inherit;border-radius:0;transition:border-color .2s}
input[type=email]:focus{outline:none;border-color:var(--gold)}
.opt{display:flex;align-items:center;gap:15px;font-size:17px;color:var(--fg)}
.opt input{width:22px;height:22px;accent-color:var(--gold)}
.sb{height:60px;padding:0 40px;border:1px solid var(--fg);font-size:17px;letter-spacing:.02em;transition:background .25s,color .25s,border-color .25s}
.sb:hover{background:var(--gold);border-color:var(--gold);color:var(--ink)}

/* past videos */
.vids{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:30px}
.vids .vid:nth-child(even){transition-delay:.15s}

/* closing call */
.end{display:flex;flex-direction:column;align-items:center;text-align:center;gap:40px;padding-block:clamp(90px,14vw,200px);border-top:1px solid var(--line);position:relative;overflow:hidden}
.end::before{content:"";position:absolute;left:50%;top:50%;width:min(1000px,140vw);aspect-ratio:1;margin:calc(min(1000px,140vw)/-2) 0 0 calc(min(1000px,140vw)/-2);background:radial-gradient(closest-side,var(--glow),transparent 70%);pointer-events:none}
.end p{position:relative;font-family:var(--D);font-size:clamp(34px,5.4vw,80px);line-height:1.1;letter-spacing:-.02em;max-width:14em;text-wrap:balance}
.end .cta{position:relative}

/* footer */
.ft{display:flex;justify-content:space-between;align-items:flex-start;gap:20px 30px;flex-wrap:wrap;padding:30px var(--pad) 40px;border-top:1px solid var(--line);font-size:15px;color:var(--mut)}
.ft nav,.ft .lg{display:flex;gap:10px 25px;flex-wrap:wrap}
.ft a{text-decoration:underline;text-decoration-color:transparent;text-underline-offset:5px;text-decoration-thickness:2px;transition:color .2s,text-decoration-color .2s}
.ft a:hover{color:var(--gt);text-decoration-color:var(--gt)}
.ft .lg>span:last-child{text-align:right;text-wrap:balance}

/* a donate bar that rides the bottom edge on phones once the hero's own button has gone */
.stk{position:fixed;left:0;right:0;bottom:0;z-index:70;padding:10px var(--pad) calc(10px + env(safe-area-inset-bottom,0px));background:color-mix(in srgb,var(--bg) 94%,transparent);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);border-top:1px solid var(--line);transform:translateY(110%);transition:transform .5s var(--ease);display:none}
.stk.on{transform:none}
.stk .cta{width:100%;min-height:60px;font-size:24px}

@media (max-width:900px){
  body{font-size:17px}
  .dh{height:60px}
  .dh .logo{font-size:20px}
  .dn{display:none}
  .stk{display:block}
  .cta{min-height:70px;padding:0 40px;font-size:26px}
  .hero{padding-top:110px;justify-content:center}
  .hero .fine{font-size:15px}
  .cols,.pledge,.shirts,.two{grid-template-columns:minmax(0,1fr);gap:30px}
  .cols .a,.cols .b,.pledge p,.pledge .cta,.shirts .t,.shirts .g,.two>div:first-child,.two>div:last-child{grid-column:1/-1}
  .pledge .cta{justify-self:stretch}
  .shirts .t{position:static}
  .shirts .g{grid-template-columns:repeat(2,minmax(0,1fr))}
  .cols p,.shirts .t p,.two p{font-size:19px}
  .vids{grid-template-columns:minmax(0,1fr);gap:20px}
  .ft .lg>span:last-child{text-align:left}
  .end .cta{width:100%}
}
@media (prefers-reduced-motion:reduce){
  .rv,.w>span,.num b,.ring,.vid,.vid::before,.shirts .g figure{transition:none!important;transform:none!important;opacity:1!important;clip-path:none!important}
  .mq .tr,.hint::after{animation:none}
}
'''

JS = r'''
(function () {
  var root = document.documentElement;
  try { var s = localStorage.getItem('site-theme'); if (s === 'light' || s === 'dark') root.setAttribute('data-site', s); } catch (e) {}
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function eff() { return root.getAttribute('data-site') || (window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark'); }
  function paintTheme() { var l = eff() === 'light'; [].forEach.call(document.querySelectorAll('.tg'), function (b) { b.querySelector('.moon').style.display = l ? 'block' : 'none'; b.querySelector('.sun').style.display = l ? 'none' : 'block'; b.setAttribute('aria-label', l ? 'Switch to dark mode' : 'Switch to light mode'); }); }
  document.addEventListener('click', function (e) {
    var b = e.target.closest('.tg'); if (!b) return;
    var n = eff() === 'light' ? 'dark' : 'light'; root.setAttribute('data-site', n); try { localStorage.setItem('site-theme', n); } catch (x) {} paintTheme();
  });
  paintTheme();

  /* load-in */
  requestAnimationFrame(function () { requestAnimationFrame(function () { root.classList.add('ld'); }); });

  /* reveal on scroll */
  var pending = [].slice.call(document.querySelectorAll('.rv,.wr,.vid,.shirts .g figure'));
  var hero = document.querySelector('.hero .cta'), dn = document.querySelector('.dn'), stk = document.querySelector('.stk'), hd = document.querySelector('.dh');
  var endCta = document.querySelector('.end .cta'), bar = document.querySelector('.pg i'), tick = false;
  function frame() {
    tick = false;
    var y = window.pageYOffset, vh = window.innerHeight, h = document.documentElement.scrollHeight - vh;
    bar.style.transform = 'translateX(' + (-100 + (h > 0 ? y / h * 100 : 0)) + '%)';
    hd.classList.toggle('bar', y > 40);
    if (!reduce && y < vh * 1.4) root.style.setProperty('--py', Math.round(y * 0.22) + 'px');
    pending = pending.filter(function (el) {
      var r = el.getBoundingClientRect();
      if (reduce || (r.top < vh * 0.9 && r.bottom > 0)) { el.classList.add('in'); return false; }
      return true;
    });
    /* the header's own Donate button and the phone bar appear once the hero's button has scrolled away, and leave for the closing one */
    var on = hero.getBoundingClientRect().bottom < 0 && endCta.getBoundingClientRect().top > vh * 0.85;
    dn.classList.toggle('on', on); stk.classList.toggle('on', on);
  }
  window.addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(frame); } }, { passive: true });
  window.addEventListener('resize', frame);
  frame();
})();
'''

def build(mobile):
    donate_href = '#give'
    foot = ('<footer class="ft"><nav aria-label="Footer"><a href="#" data-dead>Contact</a><a href="#" data-dead>Accessibility</a><a href="#" data-dead>Site Credits</a>'
            '<a href="https://www.instagram.com/baikikai/" target="_blank" rel="noopener">Instagram<span style="position:absolute;left:-9999px"> (opens in a new tab)</span></a></nav>'
            '<div class="lg"><span>© 2026 Brooklyn Aikikai</span>'
            '<span>Brooklyn Aikikai is a 501(c)(3) <a href="https://www.guidestar.org/profile/26-1693436" target="_blank" rel="noopener">EIN: 26-1693436</a></span></div></footer>')
    marq = ''.join(f'<span>{MARQUEE}</span>' for _ in range(8))
    shirts = ''.join(f'<figure style="--d:{i}"></figure>' for i in range(8))
    past = ''.join(video('Video: Past Fundraiser ' + str(i + 1)) for i in range(4))
    back = '../../rev16/mobile/' if mobile else '../rev16/'
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Brooklyn Aikikai Donate</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@400;600&family=Zen+Kaku+Gothic+New:wght@400;500&display=swap">
<style>{CSS}</style>
</head>
<body>
<div class="pg" aria-hidden="true"><i></i></div>
<header class="dh"><a class="logo" href="{back}">Brooklyn Aikikai</a>
  <div class="r"><a class="dn" href="{donate_href}">Donate {icon("arrow", 18)}</a>
  <button type="button" class="tg" aria-label="Switch theme">{icon("moon", 20, "lx moon")}{icon("sun", 20, "lx sun")}</button></div></header>

<main>
<section class="hero" aria-labelledby="h1">
  <div class="num" aria-hidden="true"><span><b>2</b></span><span><b>5</b></span></div>
  <svg class="ring" viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width=".14" aria-hidden="true"><circle cx="50" cy="50" r="48"/></svg>
  <div class="hi">
    <span class="ey rv" style="--d:0">Brooklyn Aikikai</span>
    <h1 id="h1" class="rv" style="--d:1">25 Years</h1>
    <p class="msg rv" style="--d:2">Our 25th Anniversary Fundraiser is underway!</p>
    <a class="cta rv" style="--d:3" href="{donate_href}">Donate {icon("arrow", 28)}</a>
    <p class="fine rv" style="--d:4">This year, in honor of our 25th year, all donations from January 2026, to December 31st, 2026 will count towards our 2026 fundraiser.</p>
  </div>
  <span class="hint" aria-hidden="true"></span>
</section>

<div class="mq" aria-hidden="true"><div class="tr">{marq}</div></div>

<section class="sec" id="give"><div class="wrap">
  <p class="lead wr">{words("Brooklyn Aikikai is a nonprofit dedicated to rigorous training and personal transformation through aikido and other traditional Japanese arts.")}</p>
  <div class="cols">
    <div class="a rv"><p>Donations help us keep our doors open, fund need-based scholarships for adults and children, and host guest instructors who have dedicated their lives to aikido.</p></div>
    <div class="b rv" style="--d:1"><p>Through your continued support, we have been able to thrive and flourish, keeping our dojo space in New York City for over two decades! Your donations help us to cover our sliding scale for dues, the rising costs of material goods, utilities, and scholarships that enable travel year after year.</p></div>
  </div>
  <div class="pledge rv"><p>This year, in honor of our 25th year, all donations from January 2026, to December 31st, 2026 will count towards our 2026 fundraiser.</p><a class="cta" href="#">Donate {icon("arrow", 28)}</a></div>
  <p class="thanks wr">{words("Thank you for your support!")}</p>
</div></section>

<section class="wrap" style="padding-bottom:clamp(80px,12vw,160px)">
  <p class="rv" style="font-size:21px;color:var(--mut);max-width:34em;margin-bottom:40px">We’ve put together a montage film of the last 25 years to show just how lucky we are to have a community like this! Thank you for your continued support!</p>
  {video("Video: 25 years of Brooklyn Aikikai", "feat")}
</section>

<div class="mq rev" aria-hidden="true"><div class="tr">{marq}</div></div>

<section class="sec"><div class="wrap shirts">
  <div class="t rv"><h2 style="margin:0;font-size:clamp(40px,5vw,72px)">Here for Summer!</h2><p>Check out our new t-shirts! Another excellent design from dojo member Diego Medina-Rosas and Sensei. Grab one today!</p></div>
  <div class="g"><figure class="big" style="--d:0"></figure>{shirts}</div>
</div></section>

<div class="wrap"><div class="two">
  <div class="rv"><h3>Donate by Check</h3><p>Donations by check can be made payable to Brooklyn Aikikai. Our mailing address is 408 3rd Avenue, Brooklyn, NY 11215.</p></div>
  <div class="rv" style="--d:1"><form novalidate><p style="margin-bottom:10px;font-family:var(--D);font-size:clamp(30px,3.6vw,48px);line-height:1.1;color:var(--fg);max-width:12em">Join our mailing list for fundraising and incentive updates!</p>
    <div class="f"><label for="ml">Email Address</label><input id="ml" name="ml" type="email" autocomplete="email"></div>
    <label class="opt"><input type="checkbox" name="sub"><span>I want to subscribe to your mailing list.</span></label>
    <button type="submit" class="sb">Subscribe</button></form></div>
</div></div>

<section class="sec sub"><div class="wrap">
  <h2 class="rv">Past Fundraiser Videos</h2>
  <div class="vids">{past}</div>
</div></section>

<section class="end"><p class="wr">{words("Thank you for your continued support!")}</p><a class="cta rv" href="#">Donate {icon("arrow", 28)}</a></section>
</main>
{foot}
<div class="stk"><a class="cta" href="#">Donate {icon("arrow", 24)}</a></div>
<script>{JS}</script>
</body>
</html>
'''
