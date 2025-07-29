<div align="center" size="15px">

# backports.zstd

Backport of [PEP-784 “adding Zstandard to the standard library”][PEP-784]

[![GitHub build status](https://img.shields.io/github/actions/workflow/status/rogdham/backports.zstd/build.yml?branch=master)](https://github.com/rogdham/backports.zstd/actions?query=branch:master)
[![Release on PyPI](https://img.shields.io/pypi/v/backports.zstd)](https://pypi.org/project/backports.zstd/)

---

[📖 PEP-784][PEP-784]&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;[📃 Changelog](./CHANGELOG.md)

[PEP-784]: https://peps.python.org/pep-0784/

</div>

---

## ⚠️ Work in progress

Not all features nor Python versions are supported at this time.

See the [🎯 Roadmap](https://github.com/Rogdham/backports.zstd/issues/2) for more
details on the status of this project.

---

## Install

Add the following dependency to your project:

```
backports.zstd ; python_version<'3.14'
```

## Usage

Use the following conditional import:

```python
import sys

if sys.version_info < (3, 14):
    from backports import zstd
else:
    from compression import zstd
```

Refer to the [official Python documentation][python-doc] for usage of the module.

[python-doc]: https://docs.python.org/3.14/library/compression.zstd.html
