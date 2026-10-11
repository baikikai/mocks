"""Origins and History of Tendokan Dojo: an editorial page. Centre column, full-bleed images, margin notes."""
import html, re
import build as B

# Margin notes: term, kanji, short definition in terms of practice.
# PLACEHOLDER COPY: written for the comp; the chief instructor should replace it. Kanji to be checked by a Japanese reader.
NOTES = [
    ('Budo', '武道', 'The martial path. Practice is a way of refining character, not only technique. Every class is meant to polish the spirit as much as the body.'),
    ('Shogaku', '初学', 'A first-stage misogi initiation. It is an intensive training where students meet their limits and go past them, the doorway into serious practice.'),
    ('Shihan', '師範', 'A senior teacher who embodies the art. A shihan carries the teaching forward and trains students until they can teach for themselves.'),
    ('Uchideshi', '内弟子', 'A live-in student. An uchideshi gives a period of life to the dojo, training and caring for it daily, to learn the way from the inside.'),
    ('Kenshushei', '研修生', 'A dedicated trainee who studies deeply while living outside the dojo. It is the path for those preparing to teach while keeping a life beyond the mat.'),
    ('Iaido', '居合道', 'The art of drawing the sword. It sharpens attention and clarity, and shows students where the movements of aikido come from.'),
    ('Samu', '作務', 'Work practice. Cleaning, cooking and repairing the dojo are training in themselves, a way to practise attention and service in ordinary tasks.'),
    ('Karma', '業', 'The pattern of action and consequence that shapes a life. It points to how each person’s history and habits show up in the way they practise.'),
    ('Zazen', '坐禅', 'Seated meditation. It steadies the mind and brings students back to the present, the ground for everything done on the mat.'),
    ('Misogi', '禊', 'Purification practice. It is demanding training meant to strip away self-defences and bring students closer to the root of their being.'),
    ('Shodan', '初段', 'First degree black belt. It marks the beginning of real study, not its end, the point from which deeper practice opens.'),
    ('Shugyo', '修行', 'Austere training. It is the heart of the dojo, a rigorous path of practice meant to loosen the grip of the self.'),
    ('Dharma', '法', 'The teaching and the way things are. It is what keeps being revealed through study, whoever comes and goes.'),
]

def note(term, kanji, text):
    return (f'<aside class="sn" data-k="{term}"><dl><dt><span lang="ja">{kanji}</span> <b>{html.escape(term)}</b></dt>'
            f'<dd>{html.escape(text)}</dd></dl></aside>')

def wrap_terms(h, seen):
    """Wrap the first occurrence of each unseen term in a paragraph's HTML (outside links) in a button-like span."""
    parts = re.split(r'(<[^>]+>)', h); depth = 0; hit = []
    for i, tok in enumerate(parts):
        if tok.startswith('<'):
            if tok.startswith('<a '): depth += 1
            elif tok == '</a>': depth -= 1
            continue
        if depth: continue
        for term, kanji, text in NOTES:
            if term in seen: continue
            m = re.search(r'\b' + term + r'\b', tok, re.I)
            if m:
                seen.add(term); hit.append((term, kanji, text))
                tok = (tok[:m.start()] + f'<span class="tm" role="button" tabindex="0" data-k="{term}" data-j="{kanji}">{m.group(0)}</span>' + tok[m.end():])
        parts[i] = tok
    return ''.join(parts), hit

def figure(label='', ratio='21/9', cls='fb'):
    cap = f'<figcaption>{html.escape(label)}</figcaption>' if label else ''
    return f'<figure class="ph {cls}" style="aspect-ratio:{ratio}">{cap}</figure>'

def pair(a, b):
    return f'<div class="fpair">{figure(a, "3/4", "fp")}{figure(b, "3/4", "fp")}</div>'

def byline(lines):
    return '<p class="by edby">' + ''.join(f'<span>{html.escape(l)}</span>' for l in lines) + '</p>'

def card():
    return ('<div id="ncard" hidden><div class="nc-in" role="dialog" aria-modal="true"><button type="button" class="nc-x" aria-label="Close note"><i></i><i></i></button>'
            '<div class="nc-body"></div></div></div>')

def build():
    items = B.pages['seed-page-history']['content']
    parts = []; cur = None
    for it in items:
        if it['type'] == 'h2': cur = {'h': it['text'], 'items': []}; parts.append(cur)
        else: cur['items'].append(it)
    seen = set()
    out = ''
    for pi, pt in enumerate(p for p in parts if p['h'] != 'History of Aikido'):
        txt = [i for i in pt['items'] if i['type'] != 'img']
        imgs = [i['alt'] for i in pt['items'] if i['type'] == 'img']
        bylines = [t['text'] for t in txt if t['text'].startswith(('by ', 'from '))]
        body = [t['text'] for t in txt if not t['text'].startswith(('by ', 'from '))]
        if pi == 0:
            out += byline(bylines)
            # four source images: landscape, a portrait pair, landscape
            figs = [figure('Photo: ' + imgs[0]), pair('Photo: ' + imgs[1], 'Photo: ' + imgs[2]), figure('Photo: ' + imgs[3])]
        else:
            out += figure() + f'<h2 class="edh">{html.escape(pt["h"].replace("Tendokan Dojo- Part II", "Tendokan Dojo, Part II"))}</h2>' + byline(bylines)
            figs = [figure('', '3/4', 'fsolo')]
        at = {round(len(body) * (k + 1) / (len(figs) + 1)): f for k, f in enumerate(figs)}
        for n, t in enumerate(body, 1):
            h, hit = wrap_terms(B.para(t), seen)
            cls = 'tp' if hit else ''
            if cls: h = h.replace('<p>', '<p class="tp">', 1)
            sn = '<div class="sns">' + ''.join(note(*x) for x in hit) + '</div>' if hit else ''
            drop = ' drop' if pi == 0 and n == 1 else ''
            out += f'<div class="pn{drop}">{h}{sn}</div>'
            if n in at: out += at[n]
    return f'<div class="ed">{out}</div>'
