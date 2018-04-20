def color(string, status=True, warning=False, bold=True, yellow=False):
	attr = []
	if status:
		attr.append('32')
	if warning:
		attr.append('31')
	if bold:
		attr.append('1')
	if yellow:
		attr.append('33')
	return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), string)