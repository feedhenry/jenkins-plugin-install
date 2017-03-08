"""
Utility functions for downloading jenkins packages
"""
import os
import shutil
import requests
from jpinstall import deps

def download_file(url, path):
    """
    Simple wrapper for downloading files with requests
    """
    response = requests.get(url, stream=True)
    with open(path, 'wb') as opened:
        shutil.copyfileobj(response.raw, opened)
    return path

def download_plugin(name, version, folder='.'):
    """
    Downloads a plugin from https://updates.jenkins-ci.org/ based on
    shortname and version
    """
    if os.path.isdir(folder):
        url = "https://updates.jenkins-ci.org/"
        url += "download/plugins/{0}/{1}/{0}.hpi".format(name, version)
        path = "{0}/{1}_{2}.hpi".format(folder, name, version)
        print "Saving {0} to {1}".format(url, path)
        return download_file(url, path)

def download_all(plugin_data, folder, plugins, downloaded):
    """
    Downloads plugins and their dependencies recursively.
    """
    for name, version in [d for d in plugin_data if ":".join(d) not in plugins]:
        if deps.is_greater_version_present(plugins, name, version):
            ver = deps.ver_to_str(deps.get_latest_version_present(plugins, name))
            print name + " already has version "+ ver + " present"
        else:
            path = download_plugin(name, version, folder)
            downloaded.append([name, version, path])
            dependencies = deps.get_dependencies_for_hpi(path)
            if dependencies != []:
                plugins = deps.add_plugin(plugins, name, version, dependencies)
                plugins, downloaded = download_all(dependencies, folder, plugins, downloaded)
            else:
                plugins = deps.add_plugin(plugins, name, version, [])

    return plugins, downloaded
