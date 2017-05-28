#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import os
import zipfile


class Zip:
    ZIP_EXTENSION = 'zip'

    @staticmethod
    def zipdir(input_path, output_fullpath):
        zipf = zipfile.ZipFile(output_fullpath, 'w', zipfile.ZIP_DEFLATED)
        for root, dirs, files in os.walk(input_path):
            for file in files:
                zipf.write(os.path.join(root, file))
        zipf.close()
