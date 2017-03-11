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
		'html': ('<html></html>',
				'<html>$2</html>'),

		# childen
		'html>body':   ('<html>\n\t<body></body>\n</html>',
						'<html>\n\t<body>$2</body>\n</html>'),
		'html>body>p': ('<html>\n\t<body>\n\t\t<p></p>\n\t</body>\n</html>',
						'<html>\n\t<body>\n\t\t<p>$2</p>\n\t</body>\n</html>'),

		# siblings
		'html+body': ('<html></html>\n<body></body>',
					'<html>$2</html>\n<body>$3</body>'),

		# parent
		'html>body>p^head':       ('<html>\n\t<body>\n\t\t<p></p>\n\t</body>\n\t<head></head>\n</html>',
									'<html>\n\t<body>\n\t\t<p>$2</p>\n\t</body>\n\t<head>$3</head>\n</html>'),
		'html>body>p^head^html2': ('<html>\n\t<body>\n\t\t<p></p>\n\t</body>\n\t<head></head>\n</html>\n<html2></html2>',
									'<html>\n\t<body>\n\t\t<p>$2</p>\n\t</body>\n\t<head>$3</head>\n</html>\n<html2>$4</html2>'),
		'html>body>p^^head':      ('<html>\n\t<body>\n\t\t<p></p>\n\t</body>\n</html>\n<head></head>',
									'<html>\n\t<body>\n\t\t<p>$2</p>\n\t</body>\n</html>\n<head>$3</head>'),
		'html>body>p>p^^^head':   ('<html>\n\t<body>\n\t\t<p>\n\t\t\t<p></p>\n\t\t</p>\n\t</body>\n</html>\n<head></head>',
									'<html>\n\t<body>\n\t\t<p>\n\t\t\t<p>$2</p>\n\t\t</p>\n\t</body>\n</html>\n<head>$3</head>'),

		# id
		'html#html':            ('<html id="html"></html>',
									'<html id="${2:html}">$3</html>'),
		'html#top>body#bottom': ('<html id="top">\n\t<body id="bottom"></body>\n</html>',
									'<html id="${2:top}">\n\t<body id="${3:bottom}">$4</body>\n</html>'),

		# class
		'html.html':                           ('<html class="html"></html>',
												'<html class="${2:html}">$3</html>'),
		'html.top>body.bottom':                ('<html class="top">\n\t<body class="bottom"></body>\n</html>',
												'<html class="${2:top}">\n\t<body class="${3:bottom}">$4</body>\n</html>'),
		'html.top>body.bottom.right':          ('<html class="top">\n\t<body class="bottom right"></body>\n</html>',
												'<html class="${2:top}">\n\t<body class="${3:bottom right}">$4</body>\n</html>'),
		'html.top#html>body.bottom#body':      ('<html class="top" id="html">\n\t<body class="bottom" id="body"></body>\n</html>',
												'<html class="${2:top}" id="${3:html}">\n\t<body class="${4:bottom}" id="${5:body}">$6</body>\n</html>'),
		'html.top.left#html>body.bottom#body': ('<html class="top left" id="html">\n\t<body class="bottom" id="body"></body>\n</html>',
												'<html class="${2:top left}" id="${3:html}">\n\t<body class="${4:bottom}" id="${5:body}">$6</body>\n</html>'),

		# multiplication
		'html*3':                     ('<html></html>\n<html></html>\n<html></html>',
										'<html>$2</html>\n<html>$3</html>\n<html>$4</html>'),
		'html*2>body':                ('<html>\n\t<body></body>\n</html>\n<html>\n\t<body></body>\n</html>',
										'<html>\n\t<body>$2</body>\n</html>\n<html>\n\t<body>$3</body>\n</html>'),
		'html*2>body*2':              ('<html>\n\t<body></body>\n\t<body></body>\n</html>\n<html>\n\t<body></body>\n\t<body></body>\n</html>',
										'<html>\n\t<body>$2</body>\n\t<body>$3</body>\n</html>\n<html>\n\t<body>$4</body>\n\t<body>$5</body>\n</html>'),
		'html*2>body>h1':             ('<html>\n\t<body>\n\t\t<h1></h1>\n\t</body>\n</html>\n<html>\n\t<body>\n\t\t<h1></h1>\n\t</body>\n</html>',
										'<html>\n\t<body>\n\t\t<h1>$2</h1>\n\t</body>\n</html>\n<html>\n\t<body>\n\t\t<h1>$3</h1>\n\t</body>\n</html>'),
		'html*2>body#body':           ('<html>\n\t<body id="body"></body>\n</html>\n<html>\n\t<body id="body"></body>\n</html>',
										'<html>\n\t<body id="${2:body}">$3</body>\n</html>\n<html>\n\t<body id="${4:body}">$5</body>\n</html>'),
		'html*2>body>h1#h1':          ('<html>\n\t<body>\n\t\t<h1 id="h1"></h1>\n\t</body>\n</html>\n<html>\n\t<body>\n\t\t<h1 id="h1"></h1>\n\t</body>\n</html>',
										'<html>\n\t<body>\n\t\t<h1 id="${2:h1}">$3</h1>\n\t</body>\n</html>\n<html>\n\t<body>\n\t\t<h1 id="${4:h1}">$5</h1>\n\t</body>\n</html>'),
		'html*2>body#body>h1#h1':     ('<html>\n\t<body id="body">\n\t\t<h1 id="h1"></h1>\n\t</body>\n</html>\n<html>\n\t<body id="body">\n\t\t<h1 id="h1"></h1>\n\t</body>\n</html>',
										'<html>\n\t<body id="${2:body}">\n\t\t<h1 id="${3:h1}">$4</h1>\n\t</body>\n</html>\n<html>\n\t<body id="${5:body}">\n\t\t<h1 id="${6:h1}">$7</h1>\n\t</body>\n</html>'),
		'html*2>body#body.exer':      ('<html>\n\t<body id="body" class="exer"></body>\n</html>\n<html>\n\t<body id="body" class="exer"></body>\n</html>',
										'<html>\n\t<body id="${2:body}" class="${3:exer}">$4</body>\n</html>\n<html>\n\t<body id="${5:body}" class="${6:exer}">$7</body>\n</html>'),
		'html*2>body#body.exer.cise': ('<html>\n\t<body id="body" class="exer cise"></body>\n</html>\n<html>\n\t<body id="body" class="exer cise"></body>\n</html>',
										'<html>\n\t<body id="${2:body}" class="${3:exer cise}">$4</body>\n</html>\n<html>\n\t<body id="${5:body}" class="${6:exer cise}">$7</body>\n</html>'),
		# test parent stacking
		'html*2>body^html2':          ('<html>\n\t<body></body>\n</html>\n<html>\n\t<body></body>\n</html>\n<html2></html2>',
										'<html>\n\t<body>$2</body>\n</html>\n<html>\n\t<body>$3</body>\n</html>\n<html2>$4</html2>'),
		'html*2>body>h1^html2':       ('<html>\n\t<body>\n\t\t<h1></h1>\n\t</body>\n\t<html2></html2>\n</html>\n<html>\n\t<body>\n\t\t<h1></h1>\n\t</body>\n\t<html2></html2>\n</html>',
										'<html>\n\t<body>\n\t\t<h1>$2</h1>\n\t</body>\n\t<html2>$3</html2>\n</html>\n<html>\n\t<body>\n\t\t<h1>$4</h1>\n\t</body>\n\t<html2>$5</html2>\n</html>'),
		'html*2>body>h1^^html2':      ('<html>\n\t<body>\n\t\t<h1></h1>\n\t</body>\n</html>\n<html>\n\t<body>\n\t\t<h1></h1>\n\t</body>\n</html>\n<html2></html2>\n<html2></html2>',
										'<html>\n\t<body>\n\t\t<h1>$2</h1>\n\t</body>\n</html>\n<html>\n\t<body>\n\t\t<h1>$3</h1>\n\t</body>\n</html>\n<html2>$4</html2>\n<html2>$5</html2>'),

		# item numbering
		'ul>li.item$*1':   ('<ul>\n\t<li class="item1"></li>\n</ul>',
							'<ul>\n\t<li class="${2:item1}">$3</li>\n</ul>'),
		'ul>li.item$$*1':  ('<ul>\n\t<li class="item01"></li>\n</ul>',
							'<ul>\n\t<li class="${2:item01}">$3</li>\n</ul>'),
		'ul>li.item$*2':   ('<ul>\n\t<li class="item1"></li>\n\t<li class="item2"></li>\n</ul>',
							'<ul>\n\t<li class="${2:item1}">$3</li>\n\t<li class="${4:item2}">$5</li>\n</ul>'),
		'ul>li.item$$*2':  ('<ul>\n\t<li class="item01"></li>\n\t<li class="item02"></li>\n</ul>',
							'<ul>\n\t<li class="${2:item01}">$3</li>\n\t<li class="${4:item02}">$5</li>\n</ul>'),
		'ul>li.it$em$*2':  ('<ul>\n\t<li class="it1em1"></li>\n\t<li class="it2em2"></li>\n</ul>',
							'<ul>\n\t<li class="${2:it1em1}">$3</li>\n\t<li class="${4:it2em2}">$5</li>\n</ul>'),
		'ul*2>li.item$*2': ('<ul>\n\t<li class="item1"></li>\n\t<li class="item2"></li>\n</ul>\n<ul>\n\t<li class="item1"></li>\n\t<li class="item2"></li>\n</ul>',
							'<ul>\n\t<li class="${2:item1}">$3</li>\n\t<li class="${4:item2}">$5</li>\n</ul>\n<ul>\n\t<li class="${6:item1}">$7</li>\n\t<li class="${8:item2}">$9</li>\n</ul>'),

		# item numbering base

		# text
		'html{text}':                     ('<html>text</html>',
											'<html>${2:text}</html>'),
		'html{text$}':                    ('<html>text1</html>',
											'<html>${2:text1}</html>'),
		'html{text$}>body':               ('<html>text1\n\t<body></body>\n</html>',
											'<html>${2:text1}\n\t<body>$3</body>\n</html>'),
		'html{text$}>body>p{text$}^head': ('<html>text1\n\t<body>\n\t\t<p>text1</p>\n\t</body>\n\t<head></head>\n</html>',
											'<html>${2:text1}\n\t<body>\n\t\t<p>${3:text1}</p>\n\t</body>\n\t<head>$4</head>\n</html>'),
		'ul*2>li.item$*2{item nr. $}':    ('<ul>\n\t<li class="item1">item nr. 1</li>\n\t<li class="item2">item nr. 2</li>\n</ul>\n<ul>\n\t<li class="item1">item nr. 1</li>\n\t<li class="item2">item nr. 2</li>\n</ul>',
											'<ul>\n\t<li class="${2:item1}">${3:item nr. 1}</li>\n\t<li class="${4:item2}">${5:item nr. 2}</li>\n</ul>\n<ul>\n\t<li class="${6:item1}">${7:item nr. 1}</li>\n\t<li class="${8:item2}">${9:item nr. 2}</li>\n</ul>'),

		# custom attributes
		'td.test[title colspan=3]':                       ('<td class="test" title="" colspan="3"></td>',
															'<td class="${2:test}" title="$3" colspan="${4:3}">$5</td>'),
		'td.test[title="Hello world!" colspan=3]':        ('<td class="test" title="Hello world!" colspan="3"></td>',
															'<td class="${2:test}" title="${3:Hello world!}" colspan="${4:3}">$5</td>'),
		'td.test[title="Hello world!" colspan=$]*3':      ('<td class="test" title="Hello world!" colspan="1"></td>\n<td class="test" title="Hello world!" colspan="2"></td>\n<td class="test" title="Hello world!" colspan="3"></td>',
															'<td class="${2:test}" title="${3:Hello world!}" colspan="${4:1}">$5</td>\n<td class="${6:test}" title="${7:Hello world!}" colspan="${8:2}">$9</td>\n<td class="${10:test}" title="${11:Hello world!}" colspan="${12:3}">$13</td>'),
		'tr*2>td{my text$}*3':                            ('<tr>\n\t<td>my text1</td>\n\t<td>my text2</td>\n\t<td>my text3</td>\n</tr>\n<tr>\n\t<td>my text1</td>\n\t<td>my text2</td>\n\t<td>my text3</td>\n</tr>',
															'<tr>\n\t<td>${2:my text1}</td>\n\t<td>${3:my text2}</td>\n\t<td>${4:my text3}</td>\n</tr>\n<tr>\n\t<td>${5:my text1}</td>\n\t<td>${6:my text2}</td>\n\t<td>${7:my text3}</td>\n</tr>'),
		'tr*2>td.test[title="Hello world!" colspan=$]*3': ('<tr>\n\t<td class="test" title="Hello world!" colspan="1"></td>\n\t<td class="test" title="Hello world!" colspan="2"></td>\n\t<td class="test" title="Hello world!" colspan="3"></td>\n</tr>\n<tr>\n\t<td class="test" title="Hello world!" colspan="1"></td>\n\t<td class="test" title="Hello world!" colspan="2"></td>\n\t<td class="test" title="Hello world!" colspan="3"></td>\n</tr>',
															'<tr>\n\t<td class="${2:test}" title="${3:Hello world!}" colspan="${4:1}">$5</td>\n\t<td class="${6:test}" title="${7:Hello world!}" colspan="${8:2}">$9</td>\n\t<td class="${10:test}" title="${11:Hello world!}" colspan="${12:3}">$13</td>\n</tr>\n<tr>\n\t<td class="${14:test}" title="${15:Hello world!}" colspan="${16:1}">$17</td>\n\t<td class="${18:test}" title="${19:Hello world!}" colspan="${20:2}">$21</td>\n\t<td class="${22:test}" title="${23:Hello world!}" colspan="${24:3}">$25</td>\n</tr>'),

		# default attributes
		'a':       ('<a href=""></a>',
					'<a href="$2">$3</a>'),
		'link':       ('<link rel="stylesheet" href=""></link>',
					'<link rel="${2:stylesheet}" href="$3">$4</link>'),

		# error handling
		# --------------

		# ignore whitespace
		'html ':       ('<html></html>',
						'<html>$2</html>'),
		'html > body': ('<html>\n\t<body></body>\n</html>',
						'<html>\n\t<body>$2</body>\n</html>'),

		# test wrong input
		# '{text}': ('<html>text</html>',
		#					'<html>text</html>'),
		# '>html':       ('<html></html>',
		#					'<html></html>'),
		# '+html':       ('<html></html>',
		#					'<html></html>'),
		# '^html':       ('<html></html>',
		#					'<html></html>'),
		# 'html++body':  ('<html></html>',
		#					'<html></html>'),
		# 'html>>body':  ('<html></html>',
		#					'<html></html>'),
		# 'html^body':   ('<html></html>',
		#					'<html></html>'),
		# 'html#id#id2': ('<html></html>',
		#					'<html></html>'),
		# '#id#id2':     ('<html></html>',
		#					'<html></html>'),
		# '#id':         ('<html></html>',
		#					'<html></html>'),
		# '.class':      ('<html></html>',
		#					'<html></html>'),

		}


test_results = {
		True: 'pass',
		False: 'failure',
		}


def test_write(t, snip):
	for k, v in tests.items():
		try:
			e = emmet.parse(k, snip.ft)
			r = str(e) 
			ok = r == v[0]
			snip += '%s: %s' % (k, test_results[ok])
			if not ok:
				snip += '---------------- got:'
				snip += r
				snip += '---------------- expected:'
				snip += v[0]
				snip += '----------------'
			r = e.tostr(emmet.Jumpcount(True))
			ok = r == v[1]
			snip += '(jumps) %s: %s' % (k, test_results[ok])
			if not ok:
				snip += '---------------- got:'
				snip += r
				snip += '---------------- expected:'
				snip += v[1]
				snip += '----------------'
		except Exception as err:
			import traceback
			snip += '%s: %s' % (k, test_results[False])
			snip += traceback.format_exc()
