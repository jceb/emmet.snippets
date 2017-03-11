# emmet.snippets

emmet.snippets provides an [UltiSnips](https://github.com/SirVer/ultisnips)
snippet that interprets [emmet's syntax](http://docs.emmet.io/abbreviations/syntax/)
for quickly generating HTML and XML tags and attributes.

# Features

* Live generation of tags and id and class attributes
* Fully supported syntax elements: `>`, `+`, `^`, `#`, `*`, `$`, `{..}`, `[..]`
* Proper indentation
* Dynamic jumps to tags without children and attributes without values
* First line of text is deleted automatically after the first jump
* Reasonable amount of tests implemented
* Default attributes that are added to tags automatically
* Default settings and configuration for inline tags, non-block tags and
  abbreviations for tag names

# Usage

* Open a HTML or XML file in vim
* Type `e` on an empty line
* Press `<Tab>` to expand the snippet
* Start typing something that matches [emmet's
  syntax](http://docs.emmet.io/abbreviations/syntax/), e.g.
  `html>head>title^body>h1#title+p.myclass`

[![asciicast](https://asciinema.org/a/81977.png)](https://asciinema.org/a/81977)

# Installation

* Make sure [UltiSnips](https://github.com/SirVer/ultisnips) is installed
* Clone [emmet.snippets repository](https://github.com/jceb/emmet.snippets)
* Make sure it's present in your path variable
  * I recommend using [pathogen](https://github.com/tpope/vim-pathogen).  It's
    enough to clone the repository in `~/.vim/bundle`
* Test the functionality by opening a new buffer in vim `:vs`.  Change
  `filetype` to html `setf html`.  Write `et` and press `<Tab>` to expand the
  snippet and perform a self test
  * All tests should pass

# Configuration

## Abbreviations

Abbreviations are expanded into longer tags automatically.  You can overwrite the
default configuration by assinging to the variable
`g:emmet_FILETYPE_abbreviations` or extend the configuration by assigning
to the variable `g:emmet_FILETYPE_abbreviations_extension`.  `FILETYPE` has
to be replaced by the actual file type.  Currently the following file types are
supported: `html`, `xml`, `xsl`, `xslt` and `docbk`.

Example, overwrite configuration:
```
let g:emmet_html_default_attributes = {
	\ 'bq': 'blockquote',
	\ })
```

Example, extend configuration:
```
let g:emmet_html_default_attributes_extension = {
	\ 'bq': 'blockquote',
	\ })
```

## Default attributes

Default attributes are added to tags automatically.  You can overwrite the
default configuration by assinging to the variable
`g:emmet_FILETYPE_default_attributes` or extend the configuration by assigning
to the variable `g:emmet_FILETYPE_default_attributes_extension`.  `FILETYPE` has
to be replaced by the actual file type.  Currently the following file types are
supported: `html`, `xml`, `xsl`, `xslt` and `docbk`.

Example, overwrite configuration:
```
let g:emmet_html_default_attributes = {
	\ 'a': {'href': '', 'id': 'ID'},
	\ })
```

Example, extend configuration:
```
let g:emmet_html_default_attributes_extension = {
	\ 'a': {'href': '', 'id': 'ID'},
	\ })
```

This will lead to the following tag and attributes when you type `a` in emmet:
```
# a
<a href="" id="ID"></a>
```

## Inline tags

Inline tags show child tags without creating a new line.  You can overwrite the
inline tags configuration by assinging to the variable
`g:emmet_FILETYPE_inline_tags` or extend the configuration by assigning to the
variable `g:emmet_FILETYPE_inline_tags_extension`.  `FILETYPE` has to be
replaced by the actual file type.  Currently the following file types are
supported: `html`, `xml`, `xsl`, `xslt` and `docbk`.

Example, overwrite configuration:
```
let g:emmet_html_inline_tags = [
	\ 'a',
	\ ])
```

Example, extend configuration:
```
let g:emmet_html_inline_tags_extension = [
	\ 'a',
	\ ])
```

Example inline vs. block tag:
```
Inline tag span:
<span><a href=""></a></span>

Block tag p:
<p>
    <a href=""></a>
</p>
```

## Self closing tags

Self closing tags are abbreviated by avoiding the closing tag.  You can
overwrite the self closing tags configuration by assinging to the variable
`g:emmet_FILETYPE_self_closing_tags` or extend the configuration by assigning to
the variable `g:emmet_FILETYPE_self_closing_tags_extension`.  `FILETYPE` has to
be replaced by the actual file type.  Currently the following file types are
supported: `html`, `xml`, `xsl`, `xslt` and `docbk`.

Example, overwrite configuration:
```
let g:emmet_html_self_closing_tags = [
	\ 'br',
	\ ])
```

Example, extend configuration:
```
let g:emmet_html_self_closing_tags_extension = [
	\ 'br',
	\ ])
```

Example inline vs. block tag:
```
Self closing tag br:
<br />

Non-self closing tag p:
<p>
</p>
```

## Item Numbering

Item numbering, `$`, can behave in two ways when combined with multiplication,
`*`.  Stacked multiplication combines all previous modifiers while non-stacked
multiplication just takes the tags direct multiplier into account.  The variable
`g:emmet_stacked_multiplication` controls the behavior.

To enable non-stacked multiplication execute `let
g:emmet_stacked_multiplication=0` (default).
```
# ul.list$*3>li.item$$*3
<ul class="list1">
    <li class="item01"></li>
    <li class="item02"></li>
    <li class="item03"></li>
</ul>
<ul class="list2">
    <li class="item01"></li>
    <li class="item02"></li>
    <li class="item03"></li>
</ul>
<ul class="list3">
    <li class="item01"></li>
    <li class="item02"></li>
    <li class="item03"></li>
</ul>
```

To enable stacked multiplication execute `let g:emmet_stacked_multiplication=1`.
```
# ul.list$*3>li.item$$*3
<ul class="list1">
    <li class="item01"></li>
    <li class="item02"></li>
    <li class="item03"></li>
</ul>
<ul class="list2">
    <li class="item04"></li>
    <li class="item05"></li>
    <li class="item06"></li>
</ul>
<ul class="list3">
    <li class="item07"></li>
    <li class="item08"></li>
    <li class="item09"></li>
</ul>
```

# Known Issues

* Not all syntax elements are supported yet.  The following are missing:
  * Grouping: `(..)`
  * Changing numbering base and direction: `@-` and `@N`
* Almost no error handling implemented
* Python 3 only
* No support for CSS, SASS and other syntaxes

# Related Works

* [Emmet](http://emmet.io/) project - the essential toolkit for web-developers
* [emmet-vim](https://github.com/mattn/emmet-vim)
* [Sparkup](https://github.com/rstacruz/sparkup)
