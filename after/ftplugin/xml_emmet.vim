let g:emmet_xml_default_attributes = get(g:, 'emmet_xml_default_attributes', {
	\ })
call extend(g:emmet_xml_default_attributes, get(g:, 'emmet_xml_default_attributes_extension', {}))

let g:emmet_xml_inline_tags = get(g:, 'emmet_xml_inline_tags', [
	\ ])
call extend(g:emmet_xml_inline_tags, get(g:, 'emmet_xml_inline_tags_extension', []))

let g:emmet_xml_self_closing_tags = get(g:, 'emmet_xml_self_closing_tags', [
	\ ])
call extend(g:emmet_xml_self_closing_tags, get(g:, 'emmet_xml_self_closing_tags_extension', []))

let g:emmet_xml_abbreviations = get(g:, 'emmet_xml_abbreviations', {
			\ })
call extend(g:emmet_xml_abbreviations, get(g:, 'emmet_xml_abbreviations_extensions', {}))
