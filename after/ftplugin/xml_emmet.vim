let g:emmet_docbk_default_attributes = get(g:, 'emmet_docbk_default_attributes', {
	\ })
call extend(g:emmet_docbk_default_attributes, get(g:, 'emmet_docbk_default_attributes_extension', {}))
