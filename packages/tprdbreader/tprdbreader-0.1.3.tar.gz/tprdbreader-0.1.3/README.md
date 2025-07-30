# tprdbreader

[![PyPI](https://img.shields.io/pypi/v/tprdbreader.svg)](https://pypi.org/project/tprdbreader)
[![Python](https://img.shields.io/pypi/pyversions/tprdbreader.svg)](https://pypi.org/project/tprdbreader)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

*A tiny helper that fetches Translation Process Research Database (TPR-DB) tables from **Google Cloud Storage** and returns them as Pandas DataFrames—no manual downloads, no local staging.*

---

## Why tprdbreader?

* **One function, one line:**  
    `readTPRDBtable_GCP(["ACS08", "AR20"], ext="kd")`
* **Streams directly into Pandas:** handles multiple studies and large Tables without blowing up RAM.
* **MIT-licensed & lightweight:** only two runtime deps—`pandas` and `google-cloud-storage`.

---

## Installation

```bash
pip install tprdbreader          # requires Python 3.6+
```

---

## Quick-start

```python
from tprdbreader import readTPRDBtable_GCP

# Pull all *.kd files (Keystroke Burst layer) from two studies
df = readTPRDBtable_GCP(
        studies=["ACS08", "AR20"],
        ext="kd",              # extension WITHOUT dot works too
        user="TPRDB",          # public user
        verbose=1)             # print per-study stats

print(df.head())
```

Example verbose output

```
ACS08  #sessions: 33   .kd:152  ...
AR20   #sessions: 29   .kd:131
```

---

## API Reference

```python
readTPRDBtable_GCP(studies, ext, user="TPRDB", verbose=0) -> pandas.DataFrame
```

| Argument | Type | Description |
|----------|------|-------------|
| `studies` | `list[str]` | List of study IDs (folder names) such as `["ACS08", "AR20"]`. |
| `ext` | `str` | File extension *without* the leading dot, e.g. `"kd"`, `"au"`, `"ss"`. |
| `user` | `str` | Default `"TPRDB"`. |
| `verbose` | `int` | `0` = silent, any non-zero prints per-study stats. |

> **Returns:** a single concatenated `pandas.DataFrame`.  
> Columns depend on the specific Table you load (`*.kd`, `*.au`, `*.ss` …).

### Internal path logic

For each study `<S>` the function builds  
`data/critt/tprdb/<user>/<S>/Tables/`  
and downloads every file whose name ends with `.<ext>`.

---


## License

Released under the MIT License — see [`LICENSE`](LICENSE) for full text.

<sub>© 2025 Devisri Bandaru.  Affiliated with the official TPRDB maintainers.</sub>


