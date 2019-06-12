"""Jenkins Package Install

Usage:
  jpi install [--conf conf] [--tmp tmpdir] [--dry-run] [--restart] <file_with_packages>
  jpi list [--conf conf]
  jpi restart [--conf conf]
  jpi version [--conf conf]

Options:
  --conf conf   Configuration file [default: ./config.ini]
  --tmp tmpdir  Configuration file [default: /tmp/]
  --dry-run     Don't install any packages on jenkins
"""

import ConfigParser

import requests
from docopt import docopt

from deps import deduplicate_downloads, plugin_str_to_data, installable_downloads
from download import download_all
from jenkins import JenkinsPlugins


def list_plugins(plugins):
    """
    Utility function to pretty print the list of plugins
    """
    for plugin in plugins:
        for version in plugins[plugin]:
            print plugin+":"+version
    return

def get_plugins_to_install(path):
    plugin_str = ""
    with open(path, 'r') as plugins_file:
        plugin_str = str(plugins_file.read())
        return plugin_str_to_data(plugin_str)


def install_plugins(jenkins, opts):
    """
    Implementation of the install sub-command
    """
    plugins = jenkins.plugins()
    path = opts['<file_with_packages>']
    plugins_to_install = get_plugins_to_install(path)
    plugins, downloaded = download_all(
        plugins_to_install,
        opts['--tmp'],
        plugins,
        [])
    downloaded = deduplicate_downloads(plugins, downloaded)

    if len(downloaded) > 0:
        print "Plugins to be installed:"
        for plugin, version, path in downloaded:
            print plugin + ":" + version

        if opts['--dry-run']:
            print "Dry run, not uploading packages."
        else:
            print "Uploading plugins to " + jenkins.url
            jenkins.install_plugins(plugins, downloaded)
    else:
        print "No new plugins will be installed"

def main():
    """
    The main function stand-in
    """
    opts = docopt(__doc__)
    config = ConfigParser.ConfigParser()
    config.read([opts['--conf']])
    user = config.get('jenkins', 'user')
    password = config.get('jenkins', 'password')
    url = config.get('jenkins', 'url')
    csrf_enabled = config.get('jenkins', 'csrf_enabled')

    jenkins = JenkinsPlugins(url, user, password, csrf_enabled)

    if opts['list']:
        list_plugins(jenkins.plugins())
        return
    if opts['install']:
        install_plugins(jenkins, opts)
        return
    if opts['restart']:
        jenkins.restart(5, 20)
        return
    if opts['version']:
        response = jenkins.version()
        print response
        return

if __name__ == "__main__":
    main()
