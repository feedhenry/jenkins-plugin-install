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

EXPECTED_PRE_INSTALL = {
    u'git-client': {u'2.1.0': []},
    u'handlebars': {u'1.1.1': []},
    u'credentials-binding': {u'1.10': []},
    u'pipeline-github-lib': {u'1.0': []},
    u'credentials': {u'2.1.11': []},
    u'scm-api': {u'2.0.4': []},
    u'pubsub-light': {u'1.7': []},
    u'blueocean-config': {u'1.0.0-b24': []},
    u'plain-credentials': {u'1.3': []},
    u'workflow-multibranch': {u'2.12': []},
    u'pipeline-utility-steps': {u'1.1.5': []},
    u'blueocean-web': {u'1.0.0-b24': []},
    u'junit': {u'1.20': []},
    u'blueocean-autofavorite': {u'0.6': []},
    u'multiple-scms': {u'0.6': []},
    u'authentication-tokens': {u'1.3': []},
    u'token-macro': {u'2.0': []},
    u'pipeline-rest-api': {u'2.2': []},
    u'pipeline-build-step': {u'2.1': []}, 
    u'docker-workflow': {u'1.10': []}, 
    u'github-organization-folder': {u'1.6': []}, 
    u'mercurial': {u'1.54': []}, 
    u'blueocean-dashboard': {u'1.0.0-b24': []}, 
    u'branch-api': {u'2.0.2': []}, 
    u'blueocean-commons': {u'1.0.0-b24': []}, 
    u'pipeline-graph-analysis': {u'1.3': []}, 
    u'pipeline-model-api': {u'1.0.2': []}, 
    u'docker-commons': {u'1.6': []}, 
    u'display-url-api': {u'1.1.1': []}, 
    u'blueocean': {u'1.0.0-b23': []}, 
    u'workflow-support': {u'2.12': []}, 
    u'openshift-client': {u'0.9.2': []}, 
    u'blueocean-rest': {u'1.0.0-b24': []}, 
    u'jquery-detached': {u'1.2.1': []}, 
    u'workflow-basic-steps': {u'2.3': []}, 
    u'github-api': {u'1.84': []}, 
    u'git-server': {u'1.6': []}, 
    u'script-security': {u'1.25': []}, 
    u'openshift-sync': {u'0.1.7': []}, 
    u'matrix-auth': {u'1.4': []},
    u'blueocean-display-url': {u'1.5.1': []},
    u'blueocean-personalization': {u'1.0.0-b24': []}, 
    u'blueocean-pipeline-api-impl': {u'1.0.0-b24': []}, 
    u'blueocean-jwt': {u'1.0.0-b24': []},
    u'pipeline-input-step': {u'2.5': []},
    u'subversion': {u'2.5.7': []}, 
    u'git': {u'3.0.4': []}, 
    u'workflow-step-api': {u'2.8': []}, 
    u'workflow-remote-loader': {u'1.2': []}, 
    u'workflow-durable-task-step': {u'2.8': []}, 
    u'blueocean-events': {u'1.0.0-b24': []}, 
    u'openshift-pipeline': {u'1.0.42': []}, 
    u'github-branch-source': {u'2.0.3': []}, 
    u'blueocean-i18n': {u'1.0.0-b24': []}, 
    u'ssh-credentials': {u'1.12': []}, 
    u'pipeline-model-definition': {u'1.0.2': []}, 
    u'blueocean-git-pipeline': {u'1.0.0-b24': []}, 
    u'matrix-project': {u'1.7.1': []}, 
    u'workflow-cps': {u'2.25': []}, 
    u'favorite': {u'2.0.4': []}, 
    u'pipeline-stage-view': {u'2.2': []}, 
    u'mailer': {u'1.19': []}, 
    u'cloudbees-folder': {u'5.17': []}, 
    u'workflow-api': {u'2.8': []}, 
    u'workflow-cps-global-lib': {u'2.6': []}, 
    u'ace-editor': {u'1.1': []}, 
    u'pipeline-stage-tags-metadata': {u'1.0.2': []}, 
    u'workflow-aggregator': {u'2.1': []}, 
    u'sse-gateway': {u'1.15': []}, 
    u'structs': {u'1.5': []}, 
    u'momentjs': {u'1.1.1': []}, 
    u'icon-shim': {u'2.0.3': []}, 
    u'blueocean-github-pipeline': {u'1.0.0-b24': []}, 
    u'pipeline-stage-step': {u'2.2': []}, 
    u'mapdb-api': {u'1.0.1.0': []}, 
    u'kubernetes': {u'0.10': []}, 
    u'jackson2-api': {u'2.7.3': []}, 
    u'variant': {u'1.1': []}, 
    u'durable-task': {u'1.12': []}, 
    u'metrics': {u'3.1.2.9': []}, 
    u'pipeline-model-declarative-agent': {u'1.0.2': []}, 
    u'workflow-job': {u'2.9': []}, 
    u'github': {u'1.26.0': []}, 
    u'blueocean-rest-impl': {u'1.0.0-b24': []}, 
    u'openshift-login': {u'0.11': []}, 
    u'workflow-scm-step': {u'2.3': []}}

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

def test_clean_pre_install():
    installed_plugins = j.plugins()
    nt.eq_(installed_plugins, EXPECTED_PRE_INSTALL)
def test_plugin_install():
    plugins, downloaded = jpi.download.download_all(
        EXPECTED_PLUGIN_LIST,
        "./tmp",
        EXPECTED_PRE_INSTALL, [])
    nt.eq_(downloaded, EXPECTED_DOWNLOADS)
    j.install_plugins(plugins, downloaded)
    plugins, downloaded = jpi.download.download_all(
        EXPECTED_PLUGIN_LIST,
        "./tmp",
        j.plugins(), [])
    nt.eq_(downloaded, [])


