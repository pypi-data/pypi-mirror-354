# Copyright (c) 2006-2021  Andrey Golovizin
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import io

import simplepybtex.io


class BaseWriter:
    unicode_io = False

    def __init__(self, encoding=None):
        self.encoding = encoding or simplepybtex.io.get_default_encoding()

    def write_file(self, bib_data, filename):
        open_file = simplepybtex.io.open_unicode if self.unicode_io else simplepybtex.io.open_raw
        mode = 'w' if self.unicode_io else 'wb'
        with open_file(filename, mode, encoding=self.encoding) as stream:
            self.write_stream(bib_data, stream)
            if hasattr(stream, 'getvalue'):
                return stream.getvalue()  # pragma: no cover

    def _to_string_or_bytes(self, bib_data):
        stream = io.StringIO() if self.unicode_io else io.BytesIO()
        self.write_stream(bib_data, stream)
        return stream.getvalue()

    def to_string(self, bib_data):
        result = self._to_string_or_bytes(bib_data)
        return result if self.unicode_io else result.decode(self.encoding)

    def to_bytes(self, bib_data):
        result = self._to_string_or_bytes(bib_data)
        return result.encode(self.encoding) if self.unicode_io else result
