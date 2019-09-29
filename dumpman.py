import sublime, sublime_plugin, re

class DumpmanCommand(sublime_plugin.TextCommand):


	def run(self, edit):
		content = ''
		for region in self.view.sel():
			line = self.view.line(region)
			lineStr = self.view.substr(line)
			indentation = lineStr.replace(lineStr.lstrip(),'')

			if region.empty():
				content = self.getDump("")
				variables = re.compile(r'(\$[a-zA-Z0-9_]+)')
				offset = region.begin() - line.begin()
				for m in variables.finditer(lineStr):
					if (m.start() < offset) and (offset < m.start() + len(m.group())):
						content = self.getDump(m.group())
						break
				self.view.insert(edit, line.end() + 1, indentation + content)

			else:
				selection = self.view.substr(region)

				if self.view.substr(region.begin() - 1) == '$':
					content = self.getDump('$' + selection)

				elif self.view.substr(region.end()) == '(':
					errorFunction = 0
					i = region.end() + 1
					while (self.view.substr(i) != ')'):
						if self.view.substr(i) == "\n":
							errorFunction = 1
							break
						i = i + 1

					if errorFunction:
						content = self.getDump("")

					else:
						selection = self.view.substr(sublime.Region(region.begin(), i+1))
						content = self.getDump(selection)

				else:
					content = self.getDump(selection)
				self.view.insert(edit, line.end() + 1, indentation + content)

	def getDump(self, content):
		if not content:
			return "dd(" + "'DumpMan'" + ");\n"
		else:
			return "dd(" + content + ");\n"
