# -*- coding: utf-8 -
import os
from togo.msgs import Msgs


class FileProcessor(Msgs):
    """
    A class to parse Django templates and convert them to Go templates
    """

    def run(self, dst, hugo):
        """
        Runs the transformation
        """
        for root, dirnames, filenames in os.walk(dst):
            for filename in filenames:
                filecontent = self.read_file(root + "/" + filename)
                self.status("Processing " + filename)
                content = self.process(filecontent, hugo)
                self.write_file(root + "/" + filename, content)

    def read_file(self, filepath):
        """
        Reads a file
        """
        if not os.path.isfile(filepath):
            self.error(filepath + " is not a file")
        filex = open(filepath, "r")
        filecontent = filex.read()
        return filecontent

    def write_file(self, filepath, content):
        """
        Writes a file
        """
        filex = open(filepath, "w")
        filex.write(content)
        filex.close()

    def remove_load(self, line):
        """
        Remove the load tags
        """
        begin = line.find('{% load')
        end = line.find('%}') + 1
        if begin > -1:
            if begin == 0:
                line = line[end + 1:]
        return line

    def remove_blocks(self, line):
        """
        Removes {% block foo %} and {% endblock %} tags
        """
        line = line.replace("{% endblock %}", "")
        begin = line.find('{%')
        end = line.find('%}') + 1
        if begin > -1:
            word = line[begin:end + 1]
            line = line.replace(word, "")
            line = self.remove_blocks(line)
        return line

    def transform_includes(self, line, hugo):
        """
        Transforms {% include "foo.html" %} tags into  {{ template "foo.html" . }}
        Uses {{ partial "foo.html" . }} if the Hugo format is selected
        """
        begin = line.find('{% include')
        end = line.find('%}')
        if begin > -1:
            newt = "{{ template "
            if hugo is True:
                newt = "{{ partial "
            line = line.replace('{% include', newt)
            beginline = line[0:end + 1]
            endline = line[end + 4: len(line) + 1]
            line = beginline + " . }} " + endline
        return line

    def process(self, filecontent, hugo):
        new_content = ""
        for line in filecontent.split("\n"):
            # print(line)
            line = line.replace("{{ ", "{{ .")
            line = self.remove_load(line)
            line = self.transform_includes(line, hugo)
            line = self.remove_blocks(line)
            if line != "":
                #print("NEW", line)
                new_content = new_content + "\n" + line
        return new_content
