# ELBE - Debian Based Embedded Rootfilesystem Builder
# Copyright (c) 2014 Torben Hohn <torbenh@linutronix.de>
# Copyright (c) 2014, 2017 Manuel Traut <manut@linutronix.de>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED
import os


def create_zip_archive(zipfilename, path, inarchpath):
    with ZipFile(zipfilename, "w", ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(path):
            archpath = os.path.join(inarchpath, os.path.relpath(root, path))
            zf.write(root, archpath)
            for f in files:
                filename = os.path.join(root, f)
                if not os.path.isfile(filename):
                    continue
                archname = os.path.join(archpath, f)
                # this hack is needed to avoid leading ./ in the archive
                while archname.startswith('./'):
                    archname = archname[2:]
                zi = ZipInfo(archname)
                stat = os.stat(f'{path}/{archname}')
                zi.external_attr = stat.st_mode << 16
                # this hack is needed to use the external attributes
                # there is no way to set a zipinfo object directly to an
                # archive
                with open(filename, 'rb') as f:
                    zf.writestr(zi, f.read())
