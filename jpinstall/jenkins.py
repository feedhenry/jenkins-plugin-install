"""
Plugin management utilities for interacting with jenkins
"""
import time
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class JenkinsPlugins(object):
    """
    Class wrapping several plugin-related post-requests
    to interact with jenkins
    """
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password

    def script(self, script):
        """
        Executes a groovy script and returns response text
        """
        response = requests.post(
            self.url+"/scriptText",
            auth=(self.username, self.password),
            verify=False, data={'script':script})
        response.raise_for_status()
        return response.text

    def plugins(self):
        """
        Returns the list of plugins in format {name:{version:[]}
        """
        installed_plugins_str = self.script("""
        println(
            Jenkins.instance.pluginManager.plugins.collect {
            [it.getShortName(),it.getVersion()]})""")
        return {
            p.strip():{v.strip():[]}
            for p, v  in
            [k.split(',')
             for k in installed_plugins_str.replace("]]", "").replace("[", "").split("],")]}

    def upload(self, path):
        """
        Uploads a file to the plugin upload endpoint of jenkins.
        """
        with open(path, 'rb') as hpi:
            return requests.post(
                self.url+"/pluginManager/uploadPlugin",
                auth=(self.username, self.password),
                verify=False,
                files={'files':hpi})

    def restart(self, retries, pause):
        """
        Triggers a restart of the jenkins server
        """
        try:
            response = requests.post(
                self.url + "/safeRestart",
                auth=(self.username, self.password),
                verify=False)
            response.raise_for_status()
        except requests.exceptions.HTTPError as ex:
            if retries > 0:
                for i in range(0, retries):
                    time.sleep(pause)
                    try:
                        response = self.version()
                        print "Jenkins " + response + " running"
                        return
                    except requests.exceptions.HTTPError as ex:
                        if i < retries:
                            print "Jenkins returned" + ex.strerror
                            print "Retrying in 20s"
                        else:
                            raise ex
            else:
                raise ex
        return

    def version(self):
        """
        Triggers a restart of the jenkins server
        """
        return self.script("println(Jenkins.version)").strip()
