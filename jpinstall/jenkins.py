"""Plugin management utilities for interacting with jenkins"""
import time
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from jpinstall.deps import installable_downloads

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class JenkinsPlugins(object):
    """Class wrapping several plugin-related post-requests to interact with jenkins."""

    def __init__(self, url, username, password):
        """Constructor saving the url, username and password.

        We expect connecting to jenkins through http basic-auth.
        """
        self.url = url
        self.username = username
        self.password = password

    def script(self, script):
        """Executes a groovy script and returns response text."""
        response = requests.post(
            self.url + "/scriptText",
            auth=(self.username, self.password),
            verify=False, data={'script': script})
        response.raise_for_status()
        return response.text

    def upload_plugins(self, downloaded):
        """Uploads *.hpi files in the list to the jenkins server"""
        errors = []
        installed = []
        for plugin, version, path in downloaded:
            print("Uploading " + path)
            try:
                self.upload(path)
                installed.append([plugin, version])
            except requests.exceptions.HTTPError as ex:
                errors.append([plugin, version, ex.strerror])
        return installed, errors

    def install_plugins(self, plugins, downloaded):
        """Installs all the downloaded plugins.

        It will install them in sets that have their requirements satisfied,
        triggering restart of jenkins between each set.
        """
        remaining = downloaded
        while len(remaining) > 0:
            installed = self.plugins()
            installable, remaining = installable_downloads(installed, plugins, downloaded)
            self.upload_plugins(installable)
            time.sleep(30)
            self.restart(6, 30)

    def plugins(self):
        """Returns the list of plugins in format `{name: {version: []}`"""
        installed_plugins_str = self.script("""
        println(
            Jenkins.instance.pluginManager.plugins.collect {
            [it.getShortName(),it.getVersion()]})""")
        return {
            p.strip(): {v.strip(): []}
            for p, v in
            [k.split(',')
             for k in installed_plugins_str.replace("]]", "").replace("[", "").split("],")]}

    def upload(self, path):
        """Uploads a file to the plugin upload endpoint of Jenkins."""
        with open(path, 'rb') as hpi:
            response = requests.post(
                self.url + "/pluginManager/uploadPlugin",
                auth=(self.username, self.password),
                verify=False,
                files={'files': hpi})
            response.raise_for_status()
            return response

    def wait(self, retries, pause):
        """Polls jenkins untill it is able to return a version."""
        if retries > 0:
            for i in range(0, retries):
                time.sleep(pause)
                try:
                    response = self.version()
                    print("Jenkins " + response + " running")
                    return
                except Exception as ex:
                    if i < retries:
                        print("Jenkins returned error")
                        print("Retrying in 20s")
                    else:
                        raise Exception("Couldn't resume after " + str(retries * pause) + "s")

    def restart(self, retries, pause):
        """Triggers a restart of the jenkins server."""
        try:
            response = requests.post(
                self.url + "/safeRestart",
                auth=(self.username, self.password),
                verify=False)
            response.raise_for_status()
        except Exception as ex:
            if retries > 0:
                self.wait(retries, pause)
            else:
                raise ex
        return

    def version(self):
        """Triggers a restart of the jenkins server."""
        return self.script("println(Jenkins.version)").strip()
