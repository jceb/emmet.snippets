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


def stack_parents(o):
	def attach_at_parent(ct, s):
		t = o(ct, s)
		if issubclass(t.__class__, TagList):
			for obj in t:
				obj.parent < obj
				obj.parent.parent > obj
		else:
			t.parent < t
			t.parent.parent > t
		return t
	return attach_at_parent


operators = {
	# positioning
	'>': lambda ct, s: ct > Tag(s),  # child
	'+': lambda ct, s: ct.parent > Tag(s),  # sibling
	'^': lambda ct, s: ct.parent.parent > Tag(s) if not callable(ct) else stack_parents(ct),  # parent

	# attributes and special attributes
	'#': lambda ct, s: ct + Attribute('id', s),  # attribute
	'[': None,  # custom attributes
	']': None,
	'.': lambda ct, s: ct + Attribute('class', s),  # class

	'{': None,  # text
	'}': None,

	# operation applies to one or multiple tags and even tag structures
	'*': lambda ct, s: TagList([ct.setmul(end=int(s))] + [ct.parent > ct.clone(i) for i in range(2, int(s) + 1)]) if not issubclass(ct.__class__, TagList) else ct.clone(int(s)),  # multiplication
	'(': None,  # grouping
	')': None,

	# in combination with multiplication
	'@-': None,  # change direction of numbering
	'@[0-9]*': None,  # change number to start with
}


class Attribute():
	def __init__(self, name, value=''):
		self.name = name
		if type(value) == list:
			self.value = value
		else:
			self.value = [value]

	def tostr(self, jm, mul=1):
		res = []
		for v in self.value:
			nv = ''
			pad = 0
			for c in v:
				if pad and c != '$':
					nv += ('%0' + str(pad) + 'd') % mul
					pad = 0
				if c == '$':
					pad += 1
				else:
					nv += c
			if pad:
				nv += ('%0' + str(pad) + 'd') % mul
			res.append(nv)
		if not res:
			jm.inc
		return '%s="%s"' % (self.name, ' '.join(res), '$%d' % jm.c if jm.count and res else '')

	def __eq__(self, a):
		return a and a.name == self.name

	def __add__(self, a):
		if a == self:
			if self.name == 'class':
				self.value += a.value
			else:
				self.value[0] = a.value
		return self

	def clone(self):
		a = self.__class__(self.name, self.value[:])
		return a


class Tag():
	def __init__(self, name):
		self.parent = None
		# children could also be operations, grouping is evil
		self.children = []

		self.name = name
		# children could include operations
		self.attributes = []
		self.mul_pos = 1
		self.mul_end = 1

	def tostr(self, jm, level=0, mul=1):
		_mul = self.mul_end * (mul - 1) + self.mul_pos if STACKED_MULTIPLICATION else self.mul_pos
		c = jm.inc
		return '%(indent)s<%(name)s%(attributes)s>%(block)s%(children)s%(blockindent)s</%(name)s>' % {
				'name': self.name,
				'indent': '\t' * level,
				'block': ('\n' if self.children else ('$%d' % c if jm.count else '')),
				'blockindent': ('\n' + ('\t' * level) if self.children else ''),
				'children': '\n'.join(map(lambda t: t.tostr(jm, level=level + 1, mul=_mul), self.children)),
				'attributes': (' ' if self.attributes else '') + ' '.join(map(lambda a: a.tostr(jm, mul=_mul), self.attributes)),
				}

	def __gt__(self, t):
		t.parent = self
		self.children.append(t)
		return t

	def __lt__(self, t):
		self.children.remove(t)
		return t

	def __add__(self, a):
		if a not in self.attributes:
			self.attributes.append(a)
		else:
			self.attributes[self.attributes.index(a)] + a
		return self

	def setmul(self, pos=1, end=1):
		self.mul_pos = pos
		self.mul_end = end
		return self

	def clone(self, mul=1):
		t = self.__class__(self.name)
		t.children = [c.clone() for c in self.children]
		t.attributes = [a.clone() for a in self.attributes]
		t.parent = self.parent
		t.setmul(mul, end=self.mul_end)
		return t


class TagList():
	def __init__(self, objs):
		if type(objs) in (list, set):
			self.objs = objs
		elif issubclass(objs.__class__, self.__class__):
			self.objs = objs.objs
		else:
			self.objs = (objs, )

	def __iter__(self):
		for obj in self.objs:
			yield obj

	def _iter_objs(self, f, o):
		res = []
		for obj in self:
			res.append(f(obj, o))
		if len(res) == 1:
			return res[0]
		return self.__class__(res)

	@property
	def parent(self):
		return self.__class__(set([obj.parent for obj in self]))

	def __lt__(self, t):
		# not sure if it makes sense to implement this function
		pass

	def __gt__(self, t):
		return self._iter_objs(lambda obj, t: obj > t.clone(), t)

	def __add__(self, a):
		return self._iter_objs(lambda obj, a: obj + a.clone(), a)

	def clone(self, mul=1):
		nobjs = []
		for obj in self:
			nobjs += [obj.setmul(end=mul)] + [obj.parent > obj.clone(i) for i in range(2, mul + 1)]
		self.objs = nobjs
		return self


STACKED_MULTIPLICATION = True


class Emmet():
	def __init__(self):
		# nicht tags, opps
		self.children = []

	def __str__(self):
		return self.tostr(Jumpcount())

	def __gt__(self, o):
		o.parent = self
		self.children.append(o)
		return o

	def tostr(self, jm):
		global STACKED_MULTIPLICATION
		import vim
		STACKED_MULTIPLICATION = int(vim.vars.get('emmet_stacked_multiplication', 1))
		return '\n'.join([t.tostr(jm) for t in self.children])


class Jumpcount():
	def __init__(self, count=False):
		self.c = 1
		self.count = count

	@property
	def inc(self):
		self.c += 1
		return self.c


def parse(emmet):
	# base element
	e = Emmet()
	# current object
	ct = e
	# operation
	o = None
	# string that has been read
	s = ''

	for c in emmet:
		if c not in operators.keys():
			if c == ' ':
				continue
			s += c
		else:
			if o and s:
				ct = o(ct, s)
				s = ''
				o = None
			o = operators[c](o, s) if o else operators[c]
			if ct is e and s:
				ct = e > Tag(s)
				s = ''

	# fall back, end of string reached
	if s and (o or ct is e):
		if ct is e:
			e > Tag(s)
		else:
			o(ct, s)
	return e


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
		'ul*2>li.item$*2': '<ul>\n\t<li class="item1"></li>\n\t<li class="item2"></li>\n</ul>\n<ul>\n\t<li class="item3"></li>\n\t<li class="item4"></li>\n</ul>',

		# item numbering base

		# error handling
		# --------------

		# ignore whitespace
		'html ':       '<html></html>',
		'html > body': '<html>\n\t<body></body>\n</html>',

		# test wrong input
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
			e = parse(k)
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


def write(t, snip):
	if not t[1]:
		snip += 'Syntax: http://docs.emmet.io/abbreviations/syntax/'
		return
	try:
		e = parse(t[1])
		if e:
			for line in str(e).split('\n'):
				snip.reset_indent()
				snip.shift(line.count('\t'))
				snip += line.replace('\t', '')
	except Exception as err:
		import traceback
		snip += traceback.format_exc()


def post_jump(snip):
	if snip.snippet_start[0] + 1 < snip.snippet_end[0] or \
			not snip.buffer[snip.snippet_end[0]].strip().startswith('Syntax: http://docs.emmet.io/abbreviations/syntax/'):
		# reload emmet contents, expensive but I don't know how else to
		# transport the Emmet object .. a global variable might cause some
		# trouble if in parallel a second snippet is expanded
		e_line = snip.buffer[snip.snippet_start[0]]
		# delete first line
		del snip.buffer[snip.snippet_start[0]:snip.snippet_end[0]]

		i = e_line.index('#')
		ind = ''
		if i != -1:
			ind = e_line[:i]
		e = parse(e_line.lstrip()[2:])
		snip.buffer[snip.snippet_start[0]+1] = ind

		snip.expand_anon(e.tostr(Jumpcount(True)))
