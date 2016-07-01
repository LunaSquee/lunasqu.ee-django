from urllib.parse import urlparse
import bleach

embed_allow = [
    'player.vimeo.com',
    'youtube.com',
    'www.youtube.com',
    'w.soundcloud.com',
    'dailymotion.com',
    'www.dailymotion.com'
]

def filter_iframe_content(name, value):
     if name in ('alt', 'height', 'width', 'scrolling', 'frameborder', 'allowfullscreen'):
         return True
     if name == 'src':
         p = urlparse(value)
         return (not p.netloc) or p.netloc in embed_allow
     return False

def filter_divs(name, value):
    if name in ('style'):
        return True
    if name == 'class':
        if value == 'spoiler' or value == 'spoiler-title' or value == 'spoiler-toggle hide-icon' or value == 'spoiler-content':
            return True
    return False

bleach_tags = [
    'img', 'em', 'strong', 'span', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'pre', 'br', 'a', 'embed', 'ul', 'li', 'ol', 'hr', 
    'i', 's', 'table', 'tbody', 'td', 'tr', 'blockquote', 'code', 'caption', 'big', 'small', 'q', 'div', 'cite', 'iframe'
]

bleach_attrs = {
    'div': filter_divs,
    'span': ['class', 'style', 'dir'],
    'table': ['border', 'cellpadding', 'style', 'cellspacing'],
    'tr': ['style'],
    'th': ['style'],
    'a': ['href', 'title', 'rel'],
    'img': ['alt', 'style', 'src'],
    'iframe': filter_iframe_content,
    'embed': ['type', 'class', 'src', 'width', 'height', 'allowfullscreen', 'loop', 'menu', 'play', 'src', 'style', 'wmode']
}

bleach_styles = [
    'font-size', 'width', 'height', 'color', 'font-weigth', 'float', 'text-align', 'background', 'background-color', 'font-family', 'border', 'padding'
]

def bleach_clean(string):
    return bleach.clean(string, tags=bleach_tags, attributes=bleach_attrs,styles=bleach_styles, strip=True)
