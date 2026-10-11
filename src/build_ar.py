"""Anti-racism / DEI page, copied from brooklynaikikai.com/anti-racism, on the Tendokan editorial template."""
import html
import build_tend as T

TITLE = 'Brooklyn Aikikai’s Vow to Oppose Inequity and Injustice'
INTRO = [
 'Brooklyn Aikikai acknowledges that the systems which surround our lives – including policing, education, healthcare, housing, and government – uphold and reproduce inequity and injustice. This systemic inequity and injustice, often associated with white supremacist power, constantly adapts to seize and maintain control through interconnected forms of oppression driven by the fear of an “other”.',
 'Our dojo vows to oppose systemic inequity and injustice by confronting oppression when it manifests, as thoughts we see in ourselves or as behaviors we see in our community. We make this vow because it is core to our practice of Aikido and Zen, which guides us to unfold to our true nature that transcends the notions of “self” and “other”.',
 'To make this vow concrete, we commit to naming specific manifestations of systemic inequity and injustice in our time, which often directly impact members of our community. In that spirit, we offer this non-exhaustive list of oppressions that we are committed to intimately understanding and confronting:',
]
LIST = ['Anti-Blackness', 'Anti-Asian racism', 'Islamophobia', 'Antisemitism', 'Anti-immigrant violence', 'Erasure of Indigenous lands and cultures',
        'Economic dispossession', 'Transphobia and homophobia', 'Attacks on bodily autonomy for people assigned female at birth']
CLOSE = 'By naming these patterns of thought and behavior, we make our vow concrete and take the first step toward putting it into practice. We will continue this work by creating opportunities to discuss and grapple with the systemic inequity and injustice we face as a community. Moreover, we plan to revisit and re-affirm this vow, as a community, at regular intervals. We will continuously enact this vow with the rigor, sincerity, and constancy that defines the practice of our dojo.'
H2 = 'Diversity, Equity, and Inclusion Committee Mission Statement'
DEIC = [
 'The Brooklyn Aikikai Diversity, Equity, and Inclusion Committee acknowledges that the existence of systemic racism and implicit bias must be confronted and addressed.',
 'Our mission: With the goal of reflecting the diversity of New York City in the dojo, the DEIC is formed to expand Brooklyn Aikikai’s capacity for training, tools, and research in navigating and normalizing conversations about racism, sexism, colonial thought, and the cruelty of intolerance.',
 'How we realize the mission:',
]
STEPS = [
 'The DEIC supports Brooklyn Aikikai’s stated <a class="lk" href="#mission" data-go="mission">Mission, Vision</a>, and <a class="lk" href="#anti-racism" data-go="anti-racism">Commitment to Anti-Racism</a>. We are here to learn aikido by practicing aikido; personally, locally, and globally. We commit to supporting and growing the community of Brooklyn Aikikai.',
 'The DEIC becomes a place of inquiry and sanctuary. This process is a lens through which we attempt to make sense of disharmony and develop techniques for understanding. It is a value of our dojo and our committee to dig deeper and engage with our discomfort. This includes creating space for discussing institutional and interpersonal oppression that may play out in our practice of aikido.',
 'The DEIC explores and identifies ways to enhance accessibility to all that Brooklyn Aikikai has to offer.',
]
END = 'In this way, the Brooklyn Aikikai Diversity, Equity, and Inclusion Committee works to ensure that our dojo remains committed to education and presence in anti-oppression and care.'

def pn(t, drop=False, raw=False):
    return f'<div class="pn{" drop" if drop else ""}"><p>{t if raw else html.escape(t)}</p></div>'

def dashes(items, raw=False):
    return '<ol class="stp">' + ''.join(f'<li><span class="dash" aria-hidden="true"></span><span>{x if raw else html.escape(x)}</span></li>' for x in items) + '</ol>'

def build():
    out = pn(INTRO[0], True) + pn(INTRO[1]) + pn(INTRO[2]) + dashes(LIST) + pn(CLOSE)
    out += f'<h2 class="edh">{html.escape(H2)}</h2>'
    out += ''.join(pn(t) for t in DEIC) + dashes(STEPS, True) + pn(END)
    return f'<div class="ed">{out}</div>'
