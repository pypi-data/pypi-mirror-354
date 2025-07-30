from simplepybtex.utils import CaseInsensitiveSet


def test_CaseInsensitiveSet():
    s = CaseInsensitiveSet()
    s.add('A')
    assert len(s) == 1
    assert repr(s)
    for _ in s:
        break
    else:  # pragma: no cover
        raise ValueError()
    s.discard('a')
    assert len(s) == 0
