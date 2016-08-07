#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def emmet_stack_parents(o):
	def attach_at_parent(ct, s):
		t = o(ct, s)
		if issubclass(t.__class__, EmmetTagList):
			for obj in t:
				obj.parent < obj
				obj.parent.parent > obj
		else:
			t.parent < t
			t.parent.parent > t
		return t
	return attach_at_parent


emmet_operators = {
	# positioning
	'>': lambda ct, s: ct > EmmetTag(s),  # child
	'+': lambda ct, s: ct.parent > EmmetTag(s),  # sibling
	'^': lambda ct, s: ct.parent.parent > EmmetTag(s) if not callable(ct) else emmet_stack_parents(ct),  # parent

	# attributes and special attributes
	'#': lambda ct, s: ct + EmmetAttribute('id', s),  # attribute
	'[': None,  # custom attributes
	']': None,
	'.': lambda ct, s: ct + EmmetAttribute('class', s),  # class

	'{': None,  # text
	'}': None,

	# operation applies to one or multiple tags and even tag structures
	'*': lambda ct, s: EmmetTagList([ct] + [ct.parent > ct.clone() for i in range(int(s) - 1)]),  # multiplication
	'(': None,  # grouping
	')': None,

	# in combination with multiplication
	'$': None,  # item numbering, applies to class and attributes
	'@-': None,  # change direction of numbering
	'@[0-9]*': None,  # change number to start with
}


class EmmetAttribute():
	def __init__(self, name, value=''):
		self.name = name
		if type(value) == list:
			self.value = value
		else:
			self.value = [value]

		self.padding = 0  # succes probably
		self.start = 1
		self.ascending = True

	def __str__(self):
		return '%s="%s"' % (self.name, ' '.join(self.value))

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


class EmmetTag():
	def __init__(self, name):
		self.parent = None
		# children could also be operations, grouping is evil
		self.children = []

		self.name = name
		# children could include operations
		self.attributes = []
		self.text = None

	def tostr(self, level=0):
		return '%(indent)s<%(name)s%(attributes)s>%(block)s%(children)s%(blockindent)s</%(name)s>' % {
				'name': self.name,
				'indent': '\t' * level,
				'block': ('\n' if self.children else ''),
				'blockindent': ('\n' + ('\t' * level) if self.children else ''),
				'children': '\n'.join(map(lambda t: t.tostr(level + 1), self.children)),
				'attributes': (' ' if self.attributes else '') + ' '.join(map(lambda a: str(a), self.attributes)),
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

	def clone(self):
		t = self.__class__(self.name)
		t.children = [c.clone() for c in self.children]
		t.attributes = [a.clone() for a in self.attributes]
		t.text = self.text
		t.parent = self.parent
		return t


class EmmetTagList():
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


class Emmet():
	def __init__(self):
		# nicht tags, opps
		self.children = []

	def __str__(self):
		return '\n'.join([t.tostr() for t in self.children])

	def __gt__(self, o):
		o.parent = self
		self.children.append(o)
		return o


def emmet_parse(emmet):
	# base element
	e = Emmet()
	# current object
	ct = e
	# operation
	o = None
	# string that has been read
	s = ''

	for c in emmet:
		if c not in emmet_operators.keys():
			if c == ' ':
				continue
			s += c
		else:
			if o and s:
				ct = o(ct, s)
				s = ''
				o = None
			o = emmet_operators[c](o, s) if o else emmet_operators[c]
			if ct is e and s:
				ct = e > EmmetTag(s)
				s = ''

	# fall back, end of string reached
	if s and (o or ct is e):
		if ct is e:
			e > EmmetTag(s)
		else:
			o(ct, s)
	return e


emmet_tests = {
		# simple tags
		'html': '<html></html>',

		# childen
		'html>body': '<html>\n\t<body></body>\n</html>',
		'html>body>p': '<html>\n\t<body>\n\t\t<p></p>\n\t</body>\n</html>',

		# siblings
		'html+body': '<html></html>\n<body></body>',

		# parent
		'html>body>p^head': '<html>\n\t<body>\n\t\t<p></p>\n\t</body>\n\t<head></head>\n</html>',
		'html>body>p^head^html2': '<html>\n\t<body>\n\t\t<p></p>\n\t</body>\n\t<head></head>\n</html>\n<html2></html2>',
		'html>body>p^^head': '<html>\n\t<body>\n\t\t<p></p>\n\t</body>\n</html>\n<head></head>',
		'html>body>p>p^^^head': '<html>\n\t<body>\n\t\t<p>\n\t\t\t<p></p>\n\t\t</p>\n\t</body>\n</html>\n<head></head>',

		# id
		'html#html': '<html id="html"></html>',
		'html#top>body#bottom': '<html id="top">\n\t<body id="bottom"></body>\n</html>',

		# class
		'html.html': '<html class="html"></html>',
		'html.top>body.bottom': '<html class="top">\n\t<body class="bottom"></body>\n</html>',
		'html.top>body.bottom.right': '<html class="top">\n\t<body class="bottom right"></body>\n</html>',
		'html.top#html>body.bottom#body': '<html class="top" id="html">\n\t<body class="bottom" id="body"></body>\n</html>',
		'html.top.left#html>body.bottom#body': '<html class="top left" id="html">\n\t<body class="bottom" id="body"></body>\n</html>',

		# multiplication
		'html*3': '<html></html>\n<html></html>\n<html></html>',
		'html*2>body': '<html>\n\t<body></body>\n</html>\n<html>\n\t<body></body>\n</html>',
		'html*2>body>h1': '<html>\n\t<body>\n\t\t<h1></h1>\n\t</body>\n</html>\n<html>\n\t<body>\n\t\t<h1></h1>\n\t</body>\n</html>',
		'html*2>body#body': '<html>\n\t<body id="body"></body>\n</html>\n<html>\n\t<body id="body"></body>\n</html>',
		'html*2>body>h1#h1': '<html>\n\t<body>\n\t\t<h1 id="h1"></h1>\n\t</body>\n</html>\n<html>\n\t<body>\n\t\t<h1 id="h1"></h1>\n\t</body>\n</html>',
		'html*2>body#body>h1#h1': '<html>\n\t<body id="body">\n\t\t<h1 id="h1"></h1>\n\t</body>\n</html>\n<html>\n\t<body id="body">\n\t\t<h1 id="h1"></h1>\n\t</body>\n</html>',
		'html*2>body#body.exer': '<html>\n\t<body id="body" class="exer"></body>\n</html>\n<html>\n\t<body id="body" class="exer"></body>\n</html>',
		'html*2>body#body.exer.cise': '<html>\n\t<body id="body" class="exer cise"></body>\n</html>\n<html>\n\t<body id="body" class="exer cise"></body>\n</html>',
		# test parent stacking
		'html*2>body^html2': '<html>\n\t<body></body>\n</html>\n<html>\n\t<body></body>\n</html>\n<html2></html2>',
		'html*2>body>h1^html2': '<html>\n\t<body>\n\t\t<h1></h1>\n\t</body>\n\t<html2></html2>\n</html>\n<html>\n\t<body>\n\t\t<h1></h1>\n\t</body>\n\t<html2></html2>\n</html>',
		'html*2>body>h1^^html2': '<html>\n\t<body>\n\t\t<h1></h1>\n\t</body>\n</html>\n<html>\n\t<body>\n\t\t<h1></h1>\n\t</body>\n</html>\n<html2></html2>\n<html2></html2>',


		# error handling

		# ignore whitespace
		'html ': '<html></html>',
		'html > body': '<html>\n\t<body></body>\n</html>',

		# test wrong input
		# >html
		# html^body
		# ^html
		# +html
		# html>>body
		# html#id#id2
		# #id#id2
		}


emmet_test_results = {
		True: 'pass',
		False: 'failure',
		}


def emmet_test_write(t, snip):
	for k, v in emmet_tests.items():
		try:
			e = emmet_parse(k)
			ok = str(e) == v
			snip += '%s: %s' % (k, emmet_test_results[ok])
			if not ok:
				snip += '---------------- got:'
				snip += str(e)
				snip += '---------------- expected:'
				snip += str(v)
				snip += '----------------'
		except Exception as err:
			import traceback
			snip += '%s: %s' % (k, emmet_test_results[False])
			snip += traceback.format_exc()


def emmet_write(t, snip):
	if not t[1]:
		snip += 'Syntax: http://docs.emmet.io/abbreviations/syntax/'
		return
	try:
		e = emmet_parse(t[1])
		if e:
			snip += str(e)
	except Exception as err:
		import traceback
		snip += traceback.format_exc()