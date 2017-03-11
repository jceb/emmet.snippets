let g:emmet_xslt_default_attributes = get(g:, 'emmet_xslt_default_attributes', {
	\ })
call extend(g:emmet_xslt_default_attributes, get(g:, 'emmet_xslt_default_attributes_extension', {}))

let g:emmet_xslt_inline_tags = get(g:, 'emmet_xslt_inline_tags', [
	\ ])
call extend(g:emmet_xslt_inline_tags, get(g:, 'emmet_xslt_inline_tags_extension', []))

let g:emmet_xslt_self_closing_tags = get(g:, 'emmet_xslt_self_closing_tags', [
	\ ])
call extend(g:emmet_xslt_self_closing_tags, get(g:, 'emmet_xslt_self_closing_tags_extension', []))

let g:emmet_xslt_abbreviations = get(g:, 'emmet_xslt_abbreviations', {
			\ })
call extend(g:emmet_xslt_abbreviations, get(g:, 'emmet_xslt_abbreviations_extensions', {}))
