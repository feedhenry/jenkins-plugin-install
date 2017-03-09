

Jenkins Plugin Install
============

Simple cli util to install hpi packages of specific versions to jenkins, with their dependencies.

Inspired by [install plugin script](https://github.com/jenkinsci/docker/blob/master/install-plugins.sh) used by jenkins docker.

Installation
----
```
pip install -r requirements.txt && python setup.py install
```

Usage
-----
```
Usage
 jpi install [--conf conf] [--tmp tmpdir] [--dry-run] <file_with_packages>
 jpi list [--conf conf] [--tmp tmpdir]
 jpi restart

Options:
  --conf conf   Configuration file [default: ./config.ini]
  --tmp tmpdir  Configuration file [default: /tmp/]
  --dry-run     Don't install any packages on jenkins
```

