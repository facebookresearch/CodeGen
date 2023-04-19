# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#


class CompilationError(Exception):
    pass


class TestRuntimeError(Exception):
    pass


class MissingTest(Exception):
    pass


class InvalidTest(Exception):
    pass


class Timeout(Exception):
    pass
