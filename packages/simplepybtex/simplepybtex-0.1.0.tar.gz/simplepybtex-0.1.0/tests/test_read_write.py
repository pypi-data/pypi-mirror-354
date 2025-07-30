import pytest

from simplepybtex.bibtex.exceptions import BibTeXError
from simplepybtex.database import parse_string, parse_file
from simplepybtex.database.output.bibtex import Writer as BaseWriter
from simplepybtex.database.input.bibtex import LowLevelParser
from simplepybtex.scanner import TokenRequired, PybtexSyntaxError


class Writer(BaseWriter):
    def quote(self, s):
        self.check_braces(s)
        return '{%s}' % s

    def _encode(self, text):
        #
        # FIXME: We overwrite a private method here!
        #
        return text


def test_read_write(tmp_path):
    bib_data = parse_string('''
@String{SCI = "Science"}

@String{JFernandez = "Fernandez, Julio M."}
@String{HGaub = "Gaub, Hermann E."}
@String{MGautel = "Gautel, Mathias"}
@String{FOesterhelt = "Oesterhelt, Filipp"}
@String{MRief = "Rief, Matthias"}

@Article{rief97b,
  author =       MRief #" and "# MGautel #" and "# FOesterhelt
                 #" and "# JFernandez #" and "# HGaub,
  title =        "Reversible Unfolding of Individual Titin
                 Immunoglobulin Domains by {AFM}",
  journal =      SCI,
  volume =       276,
  number =       5315,
  pages =        "1109--1112",
  year =         1997,
  doi =          "10.1126/science.276.5315.1109",
  URL =          "http://www.sciencemag.org/cgi/content/abstract/276/5315/1109",
  eprint =       "http://www.sciencemag.org/cgi/reprint/276/5315/1109.pdf",
}
''', 'bibtex')

    assert bib_data.entries['rief97b'] == bib_data.entries['RIEF97B']

    rief97b = bib_data.entries['rief97b']
    authors = rief97b.persons['author']
    for author in authors:
        assert str(author) == 'Rief, Matthias'
        break

    # field names are case-insensitive
    assert rief97b.fields['URL'] == 'http://www.sciencemag.org/cgi/content/abstract/276/5315/1109'

    with tmp_path.joinpath('test.bib').open('w', encoding='utf8') as f:
        Writer(encoding='utf8').write_stream(bib_data, f)
    assert (tmp_path.joinpath('test.bib').read_text(encoding='utf8') ==
            '@Article{rief97b,\n    author = {Rief, Matthias and Gautel, Mathias and Oesterhelt, '
            'Filipp and Fernandez, Julio M. and Gaub, Hermann E.},\n    title = {Reversible '
            'Unfolding of Individual Titin Immunoglobulin Domains by {AFM}},\n    '
            'journal = {Science},\n    '
            'volume = {276},\n    '
            'number = {5315},\n    '
            'pages = {1109--1112},\n    '
            'year = {1997},\n    '
            'doi = {10.1126/science.276.5315.1109},\n    '
            'URL = {http://www.sciencemag.org/cgi/content/abstract/276/5315/1109},\n    '
            'eprint = {http://www.sciencemag.org/cgi/reprint/276/5315/1109.pdf}\n}\n')
    assert len(parse_file(str(tmp_path.joinpath('test.bib')), 'bibtex').entries) == 1

    bib_data.to_file(str(tmp_path.joinpath('test.bib')))


def test_LowLevelParser():
    p = LowLevelParser('@{}}')
    with pytest.raises(TokenRequired):
        for _ in p:
            pass  # pragma: no cover
    assert p.get_error_context(p.get_error_context_info())

    p = LowLevelParser('@article{1,\ntitle=' '{'*150 + '}'*150 + '}')
    with pytest.raises(PybtexSyntaxError):
        for _ in p:
            pass
