import sys
import shutil
import os
import nose.tools as nt  # contains testing tools like ok_, eq_, etc.
import jpinstall as jpi
from subprocess import Popen, PIPE

def kill_and_remove(ctr_name):
    for action in ('kill', 'rm'):
        p = Popen('docker %s %s' % (action, ctr_name), shell=True,
                  stdout=PIPE, stderr=PIPE)
        if p.wait() != 0:
            raise RuntimeError(p.stderr.read())

def start_jenkins():
    ctr_name = 'jenkins_docker'
    p = Popen(['docker', 'run', '-d', '--name', ctr_name,
               '-e', 'JENKINS_PASSWORD=admin', '-p', '127.0.0.1:8080:8080', '-p', '50000:50000',
                'openshift/jenkins-2-centos7'],
              stdout=PIPE)
    return p

def stop_jenkins():
    kill_and_remove('jenkins_docker')

j = jpi.jenkins.JenkinsPlugins("http://127.0.0.1:8080", "admin", "admin")

def setUpModule():
    start_jenkins()
    j.wait(10, 10)
    if os.path.isdir('./tmp'):
        shutil.rmtree('./tmp')
    os.mkdir('./tmp')
    print "SETUP!"

def tearDownModule():
    stop_jenkins()
    print "TEAR DOWN!"

EXPECTED_PLUGIN_LIST = [
    ['envinject', '1.93.1'],
    ['aws-credentials', '1.17'],
    ['credentials-binding', '1.10'],
    ['ws-cleanup', '0.32'],
    ['jobConfigHistory', '2.15'],
    ['copyartifact', '1.38.1'],
    ['s3', '0.10.10'],
    ['ssh-agent', '1.13'],
    ['extended-choice-parameter', '0.75'],
    ['rebuild', '1.25']
]


EXPECTED_DOWNLOADS = [
    ['envinject', '1.93.1', './tmp/envinject_1.93.1.hpi'],
    ['ivy', '1.21', './tmp/ivy_1.21.hpi'],
    ['nant', '1.4.1', './tmp/nant_1.4.1.hpi'],
    ['aws-credentials', '1.17', './tmp/aws-credentials_1.17.hpi'],
    ['aws-java-sdk', '1.10.16', './tmp/aws-java-sdk_1.10.16.hpi'],
    ['ws-cleanup', '0.32', './tmp/ws-cleanup_0.32.hpi'],
    ['resource-disposer', '0.3', './tmp/resource-disposer_0.3.hpi'],
    ['jobConfigHistory', '2.15', './tmp/jobConfigHistory_2.15.hpi'],
    ['maven-plugin', '2.0', './tmp/maven-plugin_2.0.hpi'],
    ['javadoc', '1.0', './tmp/javadoc_1.0.hpi'],
    ['copyartifact', '1.38.1', './tmp/copyartifact_1.38.1.hpi'],
    ['maven-plugin', '2.7.1', './tmp/maven-plugin_2.7.1.hpi'],
    ['s3', '0.10.10', './tmp/s3_0.10.10.hpi'],
    ['aws-java-sdk', '1.10.50', './tmp/aws-java-sdk_1.10.50.hpi'],
    ['ssh-agent', '1.13', './tmp/ssh-agent_1.13.hpi'],
    ['bouncycastle-api', '1.0.2', './tmp/bouncycastle-api_1.0.2.hpi'],
    ['extended-choice-parameter', '0.75', './tmp/extended-choice-parameter_0.75.hpi'],
    ['jquery', '1.11.2-0', './tmp/jquery_1.11.2-0.hpi'],
    ['rebuild', '1.25', './tmp/rebuild_1.25.hpi']]

def test_plugin_list():
    plugins_to_install = jpi.cli.get_plugins_to_install("./fixtures/plugins.txt")
    nt.eq_(plugins_to_install, EXPECTED_PLUGIN_LIST)

def test_plugin_install():
    plugins, downloaded = jpi.download.download_all(
        EXPECTED_PLUGIN_LIST,
        "./tmp",
        j.plugins(), [])
    nt.eq_(downloaded, EXPECTED_DOWNLOADS)
    j.install_plugins(plugins, downloaded)
    plugins, downloaded = jpi.download.download_all(
        EXPECTED_PLUGIN_LIST,
        "./tmp",
        j.plugins(), [])
    nt.eq_(downloaded, [])


