import bleach

bleach_tags = [
    'img', 'em', 'strong', 'span', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'pre', 'br', 'a', 'embed', 'ul', 'li', 'ol', 'hr', 
    'i', 's', 'table', 'tbody', 'td', 'tr', 'blockquote', 'code', 'caption', 'big', 'small', 'q', 'div', 'cite'
]

bleach_attrs = {
    'div': ['style'],
    'span': ['class', 'style', 'dir'],
    'table': ['border', 'cellpadding', 'style', 'cellspacing'],
    'a': ['href', 'title', 'rel'],
    'img': ['alt', 'style', 'src'],
    'embed': ['type', 'class', 'src', 'width', 'height', 'allowfullscreen', 'loop', 'menu', 'play', 'src', 'style', 'wmode']
}

bleach_styles = [
    'font-size', 'color', 'font-weigth', 'float', 'text-align', 'background', 'font-family', 'border', 'padding'
]

def bleach_clean(string):
	return bleach.clean(string, tags=bleach_tags, attributes=bleach_attrs,styles=bleach_styles)