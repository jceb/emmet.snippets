let g:emmet_xsl_default_attributes = get(g:, 'emmet_xsl_default_attributes', {
	\ })
call extend(g:emmet_xsl_default_attributes, get(g:, 'emmet_xsl_default_attributes_extension', {}))

let g:emmet_xsl_inline_tags = get(g:, 'emmet_xsl_inline_tags', [
	\ ])
call extend(g:emmet_xsl_inline_tags, get(g:, 'emmet_xsl_inline_tags_extension', []))

let g:emmet_xsl_self_closing_tags = get(g:, 'emmet_xsl_self_closing_tags', [
	\ ])
call extend(g:emmet_xsl_self_closing_tags, get(g:, 'emmet_xsl_self_closing_tags_extension', []))
