# -*- coding: utf-8 -*-
import os
import shutil
from django.conf import settings
from django.core.management.base import BaseCommand
from togo.processor import FileProcessor
from togo.msgs import Msgs


class Command(BaseCommand, FileProcessor, Msgs):
    help = "Convert Django templates into Go templates"

    def add_arguments(self, parser):
        parser.add_argument('path',
                            help='Destination folder',
                            )
        parser.add_argument('-hugo',
                            dest="hugo",
                            action='store_true',
                            default=False,
                            help='Use Hugo templates format',
                            )

    def handle(self, *args, **options):
        dst = options["path"]
        hugo = options["hugo"]
        if self.check_path(dst) is False:
            return
        src = getattr(settings, "BASE_DIR") + "/templates"
        self.info("Found templates:")
        self.list_files(src)
        self.status("Copying templates to " + dst)
        self.copytree(src, dst)
        self.status("Converting Django templates to Go templates")
        self.run(dst, hugo)
        self.ok("Done")

    def list_files(self, startpath):
        for root, _, files in os.walk(startpath):
            level = root.replace(startpath, '').count(os.sep)
            indent = ' ' * 4 * (level)
            print('{}{}/'.format(indent, os.path.basename(root)))
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                print('{}{}'.format(subindent, f))

    def copytree(self, src, dst, symlinks=False, ignore=None):
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, symlinks, ignore)
            else:
                shutil.copy2(s, d)
            print("Copying ", item)

    def check_path(self, path):
        """
        Checks if a path exists and is a directory
        """
        if os.path.exists(path) is False:
            self.error("The path " + path + " does not exist")
            return False
        if os.path.isdir(path) is False:
            self.error("The path " + path + " is not a directory")
            return False
