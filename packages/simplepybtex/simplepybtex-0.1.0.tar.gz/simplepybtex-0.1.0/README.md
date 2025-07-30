# simplepybtex

WARNING: While this package copies some of the code and functionality of the `pybtex` package,
it is by no means a full drop-in replacement. It was created because `pybtex` appears to be no
longer maintained and the imminent removal of `pkg_resources` - which is a dependency of current
`pybtex` - would render `pybtex` un-installable (see 
https://bitbucket.org/pybtex-devs/pybtex/issues/169/replace-pkg_resources-with ). 
We (the maintainers of `simplepybtex`) are unable, though, to maintain a package with the full 
scope of `pybtex` - in particular because we only use a fraction of this functionality in our 
packages. Thus, `simplepybtex` rips the functionality we rely on (basically, parsing BibTeX) out 
of `pybtex` and provides it in a package that will be installable beyond Python 3.12.

Thus, if you are looking for a replacement for `pybtex`, `simplepybtex` might work. But if you are
interested in a "classic" open-source project, with an interest in feature requests and a bright
future, you might want to look somewhere else. `simplepybtex` just keeps our software running for
the time being, until we know what the "proper" way to replace `pybtex` will be.
