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


# wrapper function for stacking multiple "attach at parent tag" operations
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


# Emmet syntax objects and that directly implement the required functionality
O_C_ATTR     = '['
O_C_ATTR_END = ']'
O_TEXT       = '{'
O_TEXT_END   = '}'

operators = {
	# positioning
	'>': lambda ct, s: ct > Tag(s),  # child
	'+': lambda ct, s: ct.parent > Tag(s),  # sibling
	'^': lambda ct, s: ct.parent.parent > Tag(s) if not callable(ct) else stack_parents(ct),  # parent

	# attributes and special attributes
	'#': lambda ct, s: ct + Attribute('id', s),  # attribute

	O_C_ATTR:     lambda ct, s: ct + Attribute.parse(s),  # custom attributes
	O_C_ATTR_END: None,

	'.': lambda ct, s: ct + Attribute('class', s),  # class

	O_TEXT:     lambda ct, s: ct + Text(s),  # text
	O_TEXT_END: None,

	# operation applies to one or multiple tags and even tag structures
	'*': lambda ct, s: TagList([ct.setmul(end=int(s))] + \
			[ct.parent > ct.clone(i) for i in range(2, int(s) + 1)]) \
			if not issubclass(ct.__class__, TagList) else \
			ct.clone(int(s)),  # multiplication

	'(': None,  # grouping
	')': None,

	# in combination with multiplication
	'@-': None,  # change direction of numbering
	'@[0-9]*': None,  # change number to start with
}


class Text():
	"""
	Representation of text
	"""
	def __init__(self, value=''):
		self.value = value

	def clone(self):
		t = self.__class__(self.value)
		return t

	def tostr(self, jm, mul=1):
		nv = ''
		pad = 0
		for c in self.value:
			if pad and c != '$':
				nv += ('%0' + str(pad) + 'd') % mul
				pad = 0
			if c == '$':
				pad += 1
			else:
				nv += c
		if pad:
			nv += ('%0' + str(pad) + 'd') % mul
		jm.inc
		return '%s' % nv \
				if not jm.count else \
				'${%d:%s}' % (jm.c, nv) if nv else '$%d' % jm.c


class Attribute():
	"""
	Representation of a single attribute that belongs to a tag
	"""
	def __init__(self, name, value=''):
		self.name = name
		if type(value) == list:
			self.value = value
		else:
			self.value = [value]

	def __add__(self, a):
		if a == self:
			if self.name == 'class':
				self.value += a.value
			else:
				self.value[0] = a.value
		return self

	def __eq__(self, a):
		return a and a.name == self.name

	def clone(self):
		a = self.__class__(self.name, self.value[:])
		return a

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
			if nv:
				res.append(nv)
		jm.inc
		return '%(name)s="%(value)s"' % {
			'name': self.name,
			'value': \
				' '.join(res) \
				if not jm.count else \
				'${%d:%s}' % (jm.c, ' '.join(res)) if res else '$%d' % jm.c
			}


	@classmethod
	def parse(cls, s):
		"""
		Parse string into attributes
		"""
		attrs = []
		a = '' # attribute
		v = '' # value
		q = '' # quote string
		i = '' # incomplete string
		for c in s:
			if c in ('"', "'"):
				if not a:
					continue
				if not q:
					q = c
					continue
				if q and q == c:
					q = ''
					if not a:
						i = ''
						continue
					v = i
					i = ''
					attrs.append(Attribute(a, v))
					a = ''
					v = ''
					continue
			elif c == '=':
				if not i:
					continue
				a = i
				i = ''
			else:
				if c in (' ', '\t') and not q:
					if not (i or a):
						continue
					if not a:
						a = i
						i = ''
					v = i
					i = ''
					attrs.append(Attribute(a, v))
					a = ''
					v = ''
					continue
				i += c

		if i and not a:
			a = i
			i =''
		if a:
			v = i
			attrs.append(Attribute(a, v))
		return attrs


class Tag():
	"""
	Representation of a single XML/HTML tag
	"""
	def __init__(self, name):
		self.parent = None
		self.text = None
		# children could also be operations, grouping is evil
		self.children = []

		self.name = name
		# children could include operations
		self.attributes = []
		self.mul_pos = 1
		self.mul_end = 1

		# attach default tags
		for k, v in DEFAULT_ATTRIBUTES.get(self.name, {}).items():
			self + Attribute(k, v)

	def __add__(self, a):
		if isinstance(a, Text):
			self.text = a
		else:
			if not isinstance(a, list):
				a = [a]
			for e in a:
				if e not in self.attributes:
					self.attributes.append(e)
				else:
					self.attributes[self.attributes.index(e)] + e
		return self

	def __gt__(self, t):
		t.parent = self
		self.children.append(t)
		return t

	def __lt__(self, t):
		self.children.remove(t)
		return t

	def clone(self, mul=1):
		t = self.__class__(self.name)
		t.children = [c.clone() for c in self.children]
		t.attributes = [a.clone() for a in self.attributes]
		t.parent = self.parent
		if self.text:
			t.text = self.text.clone()
		t.setmul(mul, end=self.mul_end)
		return t

	def setmul(self, pos=1, end=1):
		self.mul_pos = pos
		self.mul_end = end
		return self

	def tostr(self, jm, level=0, mul=1):
		_mul = self.mul_end * (mul - 1) + self.mul_pos if STACKED_MULTIPLICATION else self.mul_pos
		attrs = (' ' if self.attributes else '') + ' '.join(map(lambda a: a.tostr(jm, mul=_mul), self.attributes))
		b = '\n'
		if not self.children:
			b = ''
			if jm.count and not self.text:
				b = '$%d' % jm.inc
		return '%(indent)s<%(name)s%(attributes)s>%(text)s%(block)s%(children)s%(blockindent)s</%(name)s>' % {
				'name': self.name,
				'text': self.text.tostr(jm, mul=_mul) if self.text else '',
				'indent': '\t' * level,
				'block': b,
				'blockindent': ('\n' + ('\t' * level) if self.children else ''),
				'children': '\n'.join(map(lambda t: t.tostr(jm, level=level + 1, mul=_mul), self.children)),
				'attributes': attrs,
				}


class TagList():
	"""
	Wrapper around Tags that might appear in groups if multiplication is used
	"""
	def __init__(self, objs):
		if type(objs) in (list, set):
			self.objs = objs
		elif issubclass(objs.__class__, self.__class__):
			self.objs = objs.objs
		else:
			self.objs = (objs, )

	def __add__(self, a):
		if isinstance(a, list):
			return self._iter_objs(lambda obj, a: obj + [e.clone() for e in a], a)
		return self._iter_objs(lambda obj, a: obj + a.clone(), a)

	def __gt__(self, t):
		return self._iter_objs(lambda obj, t: obj > t.clone(), t)

	def __iter__(self):
		for obj in self.objs:
			yield obj

	def __lt__(self, t):
		# not sure if it makes sense to implement this function
		pass

	def _iter_objs(self, f, o):
		res = []
		for obj in self:
			res.append(f(obj, o))
		if len(res) == 1:
			return res[0]
		return self.__class__(res)

	def clone(self, mul=1):
		nobjs = []
		for obj in self:
			nobjs += [obj.setmul(end=mul)] + [obj.parent > obj.clone(i) for i in range(2, mul + 1)]
		self.objs = nobjs
		return self

	@property
	def parent(self):
		return self.__class__(set([obj.parent for obj in self]))


STACKED_MULTIPLICATION = False


class Emmet():
	"""
	Base class for stacking emmet syntax elements and turing them into text
	"""
	def __init__(self):
		self.children = []

	def __gt__(self, o):
		o.parent = self
		self.children.append(o)
		return o

	def __str__(self):
		return self.tostr(Jumpcount())

	def tostr(self, jm):
		global STACKED_MULTIPLICATION
		import vim
		STACKED_MULTIPLICATION = int(vim.vars.get('emmet_stacked_multiplication', 0))
		return '\n'.join([t.tostr(jm) for t in self.children])


class Jumpcount():
	"""
	Object for counting jumps figuring out the current jump id in order to
	implement dynamic jumps.  Jumps have to be represent by $N which doesn't
	look good in the preview.  Therefore, the output of the write function
	doesn't include jump ids.  They are added later on by the post_jump function
	that passes the resulting string to snip.expand_anon which will remove the
	jump ids before showing the results to the user.
	"""
	def __init__(self, count=False):
		self.c = 1
		self.count = count

	@property
	def inc(self):
		self.c += 1
		return self.c


# global variable to transport Emmet object to post_jump function
E = None
FT = None
DEFAULT_ATTRIBUTES = {}


def _setup(ft):
	import vim
	global FT, DEFAULT_ATTRIBUTES
	FT = ft
	DEFAULT_ATTRIBUTES = vim.vars.get('emmet_%s_default_attributes' % FT, {})


def parse(emmet, ft):
	"""
	Main method to parse the user's input and create an Emmet object structure
	"""
	_setup(ft)
	# base element
	e = Emmet()
	# current tag object
	ct = e
	# operation
	o = None
	o_trigger = None
	# string that has been read
	s = ''

	ops_keys = operators.keys()

	for c in emmet:
		if c not in ops_keys or \
				(o_trigger == O_TEXT and c != O_TEXT_END) or \
				(o_trigger == O_C_ATTR and c != O_C_ATTR_END):
			if c == ' ' and o_trigger not in (O_TEXT, O_C_ATTR):
				continue
			s += c
		else:
			if o and s:
				ct = o(ct, s)
				s = ''
				o = None
				o_trigger = c
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


def write(t, snip):
	"""
	Entrance function called by the snippet
	"""
	global E
	if not t[1]:
		snip += 'Syntax: http://docs.emmet.io/abbreviations/syntax/'
		return
	try:
		e = parse(t[1], snip.ft)
		if e:
			for line in str(e).split('\n'):
				snip.reset_indent()
				snip.shift(line.count('\t'))
				snip += line.replace('\t', '')
			E = e
	except Exception as err:
		import traceback
		snip += traceback.format_exc()


def post_jump(snip):
	"""
	Called right before the user tries to jump to the first jump point.  It ends
	the user's input and passes all jump points to UltiSnips
	"""
	if E and (snip.snippet_start[0] + 1 < snip.snippet_end[0] or \
			not snip.buffer[snip.snippet_end[0]].lstrip().startswith('Syntax: http://docs.emmet.io/abbreviations/syntax/')):
		# extract indentation
		e_line = snip.buffer[snip.snippet_start[0]]
		# delete first line
		del snip.buffer[snip.snippet_start[0]:snip.snippet_end[0]]

		i = e_line.index('#')
		ind = ''
		if i != -1:
			ind = e_line[:i]
		snip.buffer[snip.snippet_start[0]+1] = ind

		snip.expand_anon(E.tostr(Jumpcount(True)))
