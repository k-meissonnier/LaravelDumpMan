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
				regionPosition = region.begin()

				if self.view.substr(regionPosition - 1) == '$':
					content = "dd($" + selection + ");\n"
				else:
					content = "dd(" + selection + ");\n"

				line = self.view.line(region)
				lineStr = self.view.substr(line)
				indentation = lineStr.replace(lineStr.lstrip(),'')

				self.view.insert(edit, line.end() + 1, indentation + content)