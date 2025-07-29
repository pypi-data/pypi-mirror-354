# 🚀 same-version

Automatically ensures your software version metadata is consistent across key project files.

---

## 📦 What does it do?

`same-version` checks that software version metadata is consistent across your project files. It can stop GitHub pull requests and local git commits/pushes of projects with inconsistent software version metadata.

Helps ensure:

✅ Reproducibility  
✅ Correct citations  
✅ Consistent packaging metadata  
✅ Accurate DOIs (Zenodo)  
✅ Cross-language version consistency (Python / JS / metadata)

It can be used in **three ways**, each of which have different capabilities:

### 1️⃣ GitHub Action

- Runs in GitHub Actions
- Can block:
  - Inconsistent **pull requests** (which helps prevent inconsistent **tags** and **GitHub releases** )
- Can report (but only after the tag/release has been created):
  - Incorrect **tags**
  - Incorrect **GitHub releases**

  _Note: GitHub Actions cannot block tags or releases after they have been created.  
This workflow runs after the tag or release exists and can report problems, but cannot prevent them from appearing in GitHub UI._


### 2️⃣ Pre-commit hook

- Runs automatically **before each commit and push** (if enabled)
- Can block:
  - Inconsistent **commits**
  - Inconsistent **tags being pushed**

### 3️⃣ Python CLI

- You can run `same-version` manually from the command line
- Useful for:
  - Local checks before release
  - CI checks outside of GitHub Actions
  - Automated scripts

---

## 📋 Features

✅ Canonical tag version parsing (PEP 440)

✅ Compare software version metadata from:
- GitHub tag/release
- `CITATION.cff`
- `pyproject.toml`
- `setup.py`
- `codemeta.json`
- `.zenodo.json`
- `package.json`

✅ Cross-language support (e.g., Python, JS)

✅ Lightweight, pure Python — no third-party services  

✅ Easy to configure via GitHub Action inputs  

✅ Suitable for reproducible research and software citation best practices

✅ Blocks inconsistent GitHub pull requests (via GitHub Action) 

✅ Reports inconsistent GitHub releases/tags (via GitHub Action) 

✅ Blocks inconsistent commits and tags (via Pre-commit hook)

✅ Modular and extendable for additional software version metadata (via Python CLI)

---

## 🔍 What files does it check?

These files are currently supported out-of-the-box:

| File             | Parser used |
|------------------|-------------|
| `CITATION.cff`   | PEP 440 |
| `pyproject.toml` | PEP 440 |
| `setup.py`       | PEP 440 |
| `package.json`   | Strict SemVer (converted from canonical PEP 440 tag) |
| `codemeta.json`  | PEP 440 |
| `.zenodo.json`   | PEP 440 |

---

## ⚙️ Inputs

| CLI Parameter                 | GitHub Action Input                     | Description            | Required                 | Default           |
|-------------------------------|-----------------------------------------|--------------------|---------------------|-------------------|
| `--base-version`         | `base_version`                     | Base version from which to compare all other versions  | No | *(empty)*      |
| `--check-github-event`         | `check_github_event`                     | Check GitHut events? (`true` or `false`)  | No | `false`      |
| `--github-event-name`         | `github_event_name`                     | GitHub event name (`push` or `release` or `pull_request`) | No  | *(empty)*      |
| `--github-event-ref`                | `github_event_ref`                            | GitHub ref (for `push` event)       | No           | *(empty)*      |
| `--github-event-release-tag`        | `github_event_release_tag`                    | GitHub release tag name (for `release` event)  | No | *(empty)*      |
| `--fail-for-missing-file`     | `fail_for_missing_file`                 | Fail for any checked file that is missing| No | `false`           |
| `--check-citation-cff`        | `check_citation_cff`                    | Check `CITATION.cff`? (`true/false`)   | No  | `true`            |
| `--citation-cff-path`         | `citation_cff_path`                     | Path to `CITATION.cff`             | No      | `CITATION.cff`    |
| `--check-pyproject-toml`      | `check_pyproject_toml`                  | Check `pyproject.toml`? (`true/false`)  | No  | `true`            |
| `--pyproject-toml-path`       | `pyproject_toml_path`                   | Path to `pyproject.toml`         | No        | `pyproject.toml`  |
| `--check-codemeta-json`       | `check_codemeta_json`                   | Check `codemeta.json`? (`true/false`)  | No  | `true`            |
| `--codemeta-json-path`        | `codemeta_json_path`                    | Path to `codemeta.json`             | No     | `codemeta.json`   |
| `--check-zenodo-json`         | `check_zenodo_json`                     | Check `.zenodo.json`? (`true/false`)  | No   | `true`            |
| `--zenodo-json-path`          | `zenodo_json_path`                      | Path to `.zenodo.json`              | No     | `.zenodo.json`    |
| `--check-package-json`        | `check_package_json`                    | Check `package.json`? (`true/false`)  | No   | `true`            |
| `--package-json-path`         | `package_json_path`                     | Path to `package.json`               | No    | `package.json`    |
| `--check-setup-py`            | `check_setup_py`                        | Check `setup.py`? (`true/false`)     | No    | `true`            |
| `--setup-py-path`             | `setup_py_path`                         | Path to `setup.py`                 | No      | `setup.py`        |

---


## 🎯 When does it run?

### GitHub Action:

- On **pull requests** (blocks inconsistent PRs)
- On **push of version tags** (reports incorrect tags after tag creation)
- On **published GitHub releases** (reports incorrect releases after release creation)
- Manually (via `workflow_dispatch`)


### Pre-commit hook:

- **Before each commit** (`pre-commit` hook)
- **Before pushing commits or tags** (`pre-push` hook)

### CLI:

- **Anytime**, on demand

---

## 🛠 How to use

---

### 1️⃣ Using in GitHub Actions

#### To block inconsistent pull requests:

```yaml
name: Check version consistency on pull requests

on:
  pull_request:

jobs:
  check-version:
    runs-on: ubuntu-latest

    steps:

      - uses: actions/checkout@v4

      - name: Install Python
        uses: actions/setup-python@v5
        with:
          python-version: ">=3.12"
          cache: 'pip'

      - name: Run same-version
        uses: willynilly/same-version@v2.0.0
        with:
          fail_for_missing_file: false
          check_github_event: true
          github_event_name: ${{ github.event_name }}
          github_event_ref: ${{ github.ref }}
          github_event_release_tag: ${{ github.event.release.tag_name }}
          check_citation_cff: true
          citation_cff_path: CITATION.cff
          check_pyproject_toml: true
          pyproject_toml_path: pyproject.toml
          check_codemeta_json: true
          codemeta_json_path: codemeta.json
          check_zenodo_json: true
          zenodo_json_path: .zenodo.json
          check_package_json: true
          package_json_path: package.json
          check_setup_py: true
          setup_py_path: setup.py
```

---

#### To report (BUT NOT BLOCK) incorrect tags/releases:

```yaml
name: Check version consistency on tags/releases

on:
  push:
    tags:
      - 'v*.*.*'
  release:
    types: [published]

jobs:
  check-version:
    runs-on: ubuntu-latest

    steps:

      - uses: actions/checkout@v4

      - name: Install Python
        uses: actions/setup-python@v5
        with:
          python-version: ">=3.12"
          cache: 'pip'

      - name: Run same-version
        uses: willynilly/same-version@v2.0.0
        with:
          fail_for_missing_file: false
          check_github_event: true
          github_event_name: ${{ github.event_name }}
          github_event_ref: ${{ github.ref }}
          github_event_release_tag: ${{ github.event.release.tag_name }}
          check_citation_cff: true
          citation_cff_path: CITATION.cff
          check_pyproject_toml: true
          pyproject_toml_path: pyproject.toml
          check_codemeta_json: true
          codemeta_json_path: codemeta.json
          check_zenodo_json: true
          zenodo_json_path: .zenodo.json
          check_package_json: true
          package_json_path: package.json
          check_setup_py: true
          setup_py_path: setup.py
```

---

### 2️⃣ Using with pre-commit hooks

You can configure the pre-commit hook to block:

✅ Commits with inconsistent version metadata (`pre-commit`)  
✅ Tags with inconsistent version metadata (`pre-push`)

#### Adding the hook:

Add to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/willynilly/same-version
    rev: v2.0.0  # Use latest tag
    hooks:
      - id: same-version
```

#### Installing the hooks:

```bash
# Install for both pre-commit and pre-push
pre-commit install -t pre-commit -t pre-push
```

#### Manually run the hook (optional):

```bash
pre-commit run same-version --all-files
```

---

### 3️⃣ Using the CLI manually

After installing the package:

```bash
pip install same-version  # or pip install .
```

Run the CLI:

```bash
same-version
```

By default, it will scan all files, but not GitHub events. You can specify additiona parameters (see the `action.yml` of this GitHub Action for a robust example).

By default, the tool will not fail if some of the files are missing. This inclusively checks as many file types as possible without additional configuration.
However, you may want to be strict and fail if any files used during checking is missing.
Here's an example of failing if any files are missing for a Python project that uses a CITATION.CFF file and pyproject.toml file, any of the other supported files that contain software version metatadata (e.g., codemeta.json, setup.py, package.json, etc.)  

```bash
same-version --fail-for-missing-file "true" --check-package-json "false" --check-codemeta-json "false" --check-setup-py "false" --check-zenodo-json "false"
```

You can integrate this into:

✅ Local release scripts  
✅ CI pipelines (non-GitHub)  
✅ Manual checks

---

## 🤝 Contributing

Pull requests and contributions are welcome!

To set up your development environment:

```bash
git clone https://github.com/willynilly/same-version.git
cd same-version
pip install -e .
pre-commit install -t pre-commit -t pre-push
pre-commit run --all-files
```

---

## 🔍 Comparisons with similar tools

| Tool / Action | Scope / Limitations |
|---------------|--------------------|
| [`check-version`](https://github.com/marketplace/actions/check-version) | Typically compares only `package.json` or `pyproject.toml` to Git tag |
| [`validate-version-tag-action`](https://github.com/marketplace/actions/validate-version-tag-action) | Focused on NPM (`package.json` only), no support for Python or metadata files |
| [`python-semantic-release`](https://python-semantic-release.readthedocs.io/) | Automated release tool — not designed for cross-file version consistency checking |
| `check-tag-version` (various community actions) | Usually limited to one file — no multi-ecosystem, no citation support |

✅ **`same-version` is currently the only GitHub Action that provides:**

- Canonical **PEP 440 tag version parsing**
- Cross-ecosystem validation:
    - Python (`pyproject.toml`, `setup.py`)
    - JavaScript (`package.json`)
    - Citation / metadata (`CITATION.cff`, `codemeta.json`, `.zenodo.json`)
- Lightweight, non-invasive — designed to fit **any workflow**

---

## 📜 License

Apache License 2.0 — free to use, fork, extend 🚀

---

## 🙏 Acknowledgements

Inspired by best practices for reproducible research and software citation!

---
