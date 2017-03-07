#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Depends: vim, UltiSnips
#
# MIT License
#
# Copyright (c) 2016 Jan Christoph Ebersbach
# Homepage  http://www.e-jc.de/
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import emmet


tests = {
		# functionality tests
		# -------------------

		# simple tags
		'html': '<html></html>',

		# childen
		'html>body':   '<html>\n\t<body></body>\n</html>',
		'html>body>p': '<html>\n\t<body>\n\t\t<p></p>\n\t</body>\n</html>',

		# siblings
		'html+body': '<html></html>\n<body></body>',

		# parent
		'html>body>p^head':       '<html>\n\t<body>\n\t\t<p></p>\n\t</body>\n\t<head></head>\n</html>',
		'html>body>p^head^html2': '<html>\n\t<body>\n\t\t<p></p>\n\t</body>\n\t<head></head>\n</html>\n<html2></html2>',
		'html>body>p^^head':      '<html>\n\t<body>\n\t\t<p></p>\n\t</body>\n</html>\n<head></head>',
		'html>body>p>p^^^head':   '<html>\n\t<body>\n\t\t<p>\n\t\t\t<p></p>\n\t\t</p>\n\t</body>\n</html>\n<head></head>',

		# id
		'html#html':            '<html id="html"></html>',
		'html#top>body#bottom': '<html id="top">\n\t<body id="bottom"></body>\n</html>',

		# class
		'html.html':                           '<html class="html"></html>',
		'html.top>body.bottom':                '<html class="top">\n\t<body class="bottom"></body>\n</html>',
		'html.top>body.bottom.right':          '<html class="top">\n\t<body class="bottom right"></body>\n</html>',
		'html.top#html>body.bottom#body':      '<html class="top" id="html">\n\t<body class="bottom" id="body"></body>\n</html>',
		'html.top.left#html>body.bottom#body': '<html class="top left" id="html">\n\t<body class="bottom" id="body"></body>\n</html>',

		# multiplication
		'html*3':                     '<html></html>\n<html></html>\n<html></html>',
		'html*2>body':                '<html>\n\t<body></body>\n</html>\n<html>\n\t<body></body>\n</html>',
		'html*2>body*2':              '<html>\n\t<body></body>\n\t<body></body>\n</html>\n<html>\n\t<body></body>\n\t<body></body>\n</html>',
		'html*2>body>h1':             '<html>\n\t<body>\n\t\t<h1></h1>\n\t</body>\n</html>\n<html>\n\t<body>\n\t\t<h1></h1>\n\t</body>\n</html>',
		'html*2>body#body':           '<html>\n\t<body id="body"></body>\n</html>\n<html>\n\t<body id="body"></body>\n</html>',
		'html*2>body>h1#h1':          '<html>\n\t<body>\n\t\t<h1 id="h1"></h1>\n\t</body>\n</html>\n<html>\n\t<body>\n\t\t<h1 id="h1"></h1>\n\t</body>\n</html>',
		'html*2>body#body>h1#h1':     '<html>\n\t<body id="body">\n\t\t<h1 id="h1"></h1>\n\t</body>\n</html>\n<html>\n\t<body id="body">\n\t\t<h1 id="h1"></h1>\n\t</body>\n</html>',
		'html*2>body#body.exer':      '<html>\n\t<body id="body" class="exer"></body>\n</html>\n<html>\n\t<body id="body" class="exer"></body>\n</html>',
		'html*2>body#body.exer.cise': '<html>\n\t<body id="body" class="exer cise"></body>\n</html>\n<html>\n\t<body id="body" class="exer cise"></body>\n</html>',
		# test parent stacking
		'html*2>body^html2':          '<html>\n\t<body></body>\n</html>\n<html>\n\t<body></body>\n</html>\n<html2></html2>',
		'html*2>body>h1^html2':       '<html>\n\t<body>\n\t\t<h1></h1>\n\t</body>\n\t<html2></html2>\n</html>\n<html>\n\t<body>\n\t\t<h1></h1>\n\t</body>\n\t<html2></html2>\n</html>',
		'html*2>body>h1^^html2':      '<html>\n\t<body>\n\t\t<h1></h1>\n\t</body>\n</html>\n<html>\n\t<body>\n\t\t<h1></h1>\n\t</body>\n</html>\n<html2></html2>\n<html2></html2>',

		# item numbering
		'ul>li.item$*1':   '<ul>\n\t<li class="item1"></li>\n</ul>',
		'ul>li.item$$*1':  '<ul>\n\t<li class="item01"></li>\n</ul>',
		'ul>li.item$*2':   '<ul>\n\t<li class="item1"></li>\n\t<li class="item2"></li>\n</ul>',
		'ul>li.item$$*2':  '<ul>\n\t<li class="item01"></li>\n\t<li class="item02"></li>\n</ul>',
		'ul>li.it$em$*2':  '<ul>\n\t<li class="it1em1"></li>\n\t<li class="it2em2"></li>\n</ul>',
		'ul*2>li.item$*2': '<ul>\n\t<li class="item1"></li>\n\t<li class="item2"></li>\n</ul>\n<ul>\n\t<li class="item1"></li>\n\t<li class="item2"></li>\n</ul>',

		# item numbering base

		# text
		'html{text}': '<html>text</html>',
		'html{text$}': '<html>text1</html>',
		'html{text$}>body':   '<html>text1\n\t<body></body>\n</html>',
		'html{text$}>body>p{text$}^head':       '<html>text1\n\t<body>\n\t\t<p>text1</p>\n\t</body>\n\t<head></head>\n</html>',
		'ul*2>li.item$*2{item nr. $}': '<ul>\n\t<li class="item1">item nr. 1</li>\n\t<li class="item2">item nr. 2</li>\n</ul>\n<ul>\n\t<li class="item1">item nr. 1</li>\n\t<li class="item2">item nr. 2</li>\n</ul>',

		# error handling
		# --------------

		# ignore whitespace
		'html ':       '<html></html>',
		'html > body': '<html>\n\t<body></body>\n</html>',

		# test wrong input
		# '{text}': '<html>text</html>',
		# '>html':       '<html></html>',
		# '+html':       '<html></html>',
		# '^html':       '<html></html>',
		# 'html++body':  '<html></html>',
		# 'html>>body':  '<html></html>',
		# 'html^body':   '<html></html>',
		# 'html#id#id2': '<html></html>',
		# '#id#id2':     '<html></html>',
		# '#id':         '<html></html>',
		# '.class':      '<html></html>',

		}


test_results = {
		True: 'pass',
		False: 'failure',
		}


def test_write(t, snip):
	for k, v in tests.items():
		try:
			e = emmet.parse(k)
			ok = str(e) == v
			snip += '%s: %s' % (k, test_results[ok])
			if not ok:
				snip += '---------------- got:'
				snip += str(e)
				snip += '---------------- expected:'
				snip += str(v)
				snip += '----------------'
		except Exception as err:
			import traceback
			snip += '%s: %s' % (k, test_results[False])
			snip += traceback.format_exc()
