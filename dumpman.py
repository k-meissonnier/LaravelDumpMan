import sublime, sublime_plugin, re

class DumpmanCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		for region in self.view.sel():
			if region.empty():
				line = self.view.line(region)
				content = "dd(" + self.view.substr(line) + ");\n"
				self.view.insert(edit, line.end() + 1, content)

			else:
				selection = self.view.substr(region)
				# self.view.insert(edit, 0, self.view.substr(region.end() + 1))

				if self.view.substr(region.begin() - 1) == '$':
					content = "dd($" + selection + ");\n"
				elif self.view.substr(region.end()) == '(':
					errorFunction = 0
					i = region.end() + 1
					while (self.view.substr(i) != ')'):
						if self.view.substr(i) == "\n":
							errorFunction = 1
							break
						i = i + 1
					if(errorFunction):
						content = "dd(" + selection + ");\n"
					else:
						selection = self.view.substr(sublime.Region(region.begin(),i+1))
						content = "dd(" + selection + ");\n"

				else:
					content = "dd(" + selection + ");\n"

				line = self.view.line(region)
				lineStr = self.view.substr(line)
				indentation = lineStr.replace(lineStr.lstrip(),'')

				self.view.insert(edit, line.end() + 1, indentation + content)