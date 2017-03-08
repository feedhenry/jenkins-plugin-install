"""Jenkins Package Install

Usage:
  jpi install [--conf conf] [--tmp tmpdir] [--dry-run] [--restart] <file_with_packages>
  jpi list [--conf conf] [--tmp tmpdir]

Options:
  --conf conf   Configuration file [default: ./config.ini]
  --tmp tmpdir  Configuration file [default: /tmp/]
  --dry-run     Don't install any packages on jenkins
  --restart     Force jenkins restart after plugin installation
"""

import ConfigParser

import requests
from docopt import docopt

from jpinstall.deps import deduplicate_downloads, plugin_str_to_data
from jpinstall.download import download_all
from jpinstall.jenkins import JenkinsPlugins


def list_plugins(plugins):
    """
    Utility function to pretty print the list of plugins
    """
    for plugin in plugins:
        for version in plugins[plugin]:
            print plugin+":"+version
    return

def install_plugins(jenkins, opts):
    """
    Implementation of the install sub-command
    """
    plugins = jenkins.plugins()
    path = opts['<file_with_packages>']
    plugin_str = ""
    with open(path, 'r') as plugins_file:
        plugin_str = str(plugins_file.read())
    plugins_to_install = plugin_str_to_data(plugin_str)
    plugins, downloaded = download_all(
        plugins_to_install,
        opts['--tmp'],
        plugins,
        [])
    downloaded = list(reversed(deduplicate_downloads(plugins, downloaded)))

    print "Plugins to be installed:"
    for plugin, version, path in downloaded:
        print plugin + ":" + version

    if opts['--dry-run']:
        print "Dry run, not uploading packages."
    else:
        print "Uploading plugins to " + jenkins.url
        for plugins, version, path in downloaded:
            print "Uploading " + path
            try:
                response = jenkins.upload(path)
                response.raise_for_status()
            except requests.exceptions.HTTPError as ex:
                print ex.strerror
        if opts['--restart']:
            response = jenkins.restart()
            response.raise_for_status()

def main():
    """
    The main function stand-in
    """
    opts = docopt(__doc__)
    config = ConfigParser.ConfigParser()
    config.read([opts['--conf']])
    print config
    user = config.get('jenkins', 'user')
    password = config.get('jenkins', 'password')
    url = config.get('jenkins', 'url')

    jenkins = JenkinsPlugins(url, user, password)

    if opts['list']:
        list_plugins(jenkins.plugins())
        return
    if opts['install']:
        install_plugins(jenkins, opts)
        return
