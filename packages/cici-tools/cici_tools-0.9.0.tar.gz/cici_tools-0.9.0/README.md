# cici-tools

<!-- BADGIE TIME -->

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

<!-- END BADGIE TIME -->

Power tools for CI/CD.

> Do not use this software unless you are an active collaborator on the
> associated research project.
>
> This project is an output of an ongoing, active research project. It is
> published without warranty, is subject to change at any time, and has not been
> certified, tested, assessed, or otherwise assured of safety by any person or
> organization. Use at your own risk.

## Usage

### `bundle`

Flatten `extends` keywords to make zero-dependency GitLab CI/CD files.

```bash
cici bundle
```

```console
$ cici bundle
⚡ python-autoflake.yml
⚡ python-black.yml
⚡ python-build-sdist.yml
⚡ python-build-wheel.yml
⚡ python-import-linter.yml
⚡ python-isort.yml
⚡ python-mypy.yml
⚡ python-pyroma.yml
⚡ python-pytest.yml
⚡ python-setuptools-bdist-wheel.yml
⚡ python-setuptools-sdist.yml
⚡ python-twine-upload.yml
⚡ python-vulture.yml
```

### `fmt`

Normalize the style of your GitLab CI/CD files:

```bash
cici fmt
```

```console
$ cici fmt
.gitlab-ci.yml formatted
```

### `readme`

Generate a README for your pipeline project:

```bash
cici readme
```

To customize the output, copy the default README template to `README.md.j2` in
your project root and modify:

```j2
# {{ name }} pipeline

{%- include "brief.md.j2" %}
{%- include "description.md.j2" %}

{%- include "groups.md.j2" %}

{%- include "targets.md.j2" %}

{%- include "variables.md.j2" %}
```

### `update`

Update to the latest GitLab CI/CD `include` versions available.

```bash
cici update
```

```console
$ cici update
updated saferatday0/library/python to 0.5.1
updated saferatday0/library/gitlab from 0.1.0 to 0.2.2
```
