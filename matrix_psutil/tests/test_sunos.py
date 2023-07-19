#!/usr/bin/env python3

# Copyright (c) 2009, Giampaolo Rodola'. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Sun OS specific tests."""

import os
import unittest

import matrix_psutil
from matrix_psutil import SUNOS
from matrix_psutil.tests import PsutilTestCase
from matrix_psutil.tests import sh


@unittest.skipIf(not SUNOS, "SUNOS only")
class SunOSSpecificTestCase(PsutilTestCase):

    def test_swap_memory(self):
        out = sh('env PATH=/usr/sbin:/sbin:%s swap -l' % os.environ['PATH'])
        lines = out.strip().split('\n')[1:]
        if not lines:
            raise ValueError('no swap device(s) configured')
        total = free = 0
        for line in lines:
            fields = line.split()
            total = int(fields[3]) * 512
            free = int(fields[4]) * 512
        used = total - free

        psutil_swap = matrix_psutil.swap_memory()
        self.assertEqual(psutil_swap.total, total)
        self.assertEqual(psutil_swap.used, used)
        self.assertEqual(psutil_swap.free, free)

    def test_cpu_count(self):
        out = sh("/usr/sbin/psrinfo")
        self.assertEqual(matrix_psutil.cpu_count(), len(out.split('\n')))


if __name__ == '__main__':
    from matrix_psutil.tests.runner import run_from_name
    run_from_name(__file__)
