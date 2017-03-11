let g:emmet_html_default_attributes = get(g:, 'emmet_html_default_attributes', {
	\ 'a': {'href': ''},
	\ 'abbr': {'title': ''},
	\ 'acronym': {'title': ''},
	\ 'audio': {'src': ''},
	\ 'button': {'type': ''},
	\ 'form': {'action': '', 'method': ''},
	\ 'iframe': {'src': ''},
	\ 'img': {'src': '', 'alt': ''},
	\ 'input': {'type': '', 'name': '', 'id': ''},
	\ 'link': {'rel': 'stylesheet', 'href': ''},
	\ 'option': {'value': ''},
	\ 'script': {'src': ''},
	\ 'select': {'name': '', 'id': ''},
	\ 'textarea': {'name': '', 'id': ''},
	\ 'video': {'src': ''},
	\ })
call extend(g:emmet_html_default_attributes, get(g:, 'emmet_html_default_attributes_extension', {}))
