import sublime, sublime_plugin, re

class DumpmanCommand(sublime_plugin.TextCommand):


	def run(self, edit):
		content = ''
		for region in self.view.sel():

			if region.empty():
				line = self.view.line(region)
				content = self.getDump("")
				self.view.insert(edit, line.end() + 1, content)

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

					if(errorFunction):
						content = self.getDump("")

					else:
						selection = self.view.substr(sublime.Region(region.begin(), i+1))
						content = self.getDump(selection)

				else:
					content = self.getDump(selection)

				line = self.view.line(region)
				lineStr = self.view.substr(line)
				indentation = lineStr.replace(lineStr.lstrip(),'')


				self.view.insert(edit, line.end() + 1, indentation + content)

	def getDumpFooter(self):
		return "" + self.view.file_name()

	def getDump(self, content):
		if content == "":
			return "dd(" + "'" + self.getDumpFooter() + "'" + ");\n"
		else:
			return "dd(" + content + " .' " + self.getDumpFooter() + "');\n"
