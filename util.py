def get_readable_username_from_html_fragment(html):
    nick_spans = html.a.span.contents
    username_fragments = [f.string for f in nick_spans if f.string]
    return ''.join(username_fragments)