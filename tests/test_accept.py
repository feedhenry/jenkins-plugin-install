import shutil
import os
import nose.tools as nt  # contains testing tools like ok_, eq_, etc.
import jpinstall as jpi


def setUpModule():
    if os.path.isdir('./tmp'):
        shutil.rmtree('./tmp')
    os.mkdir('./tmp')
    print("SETUP!")


def tearDownModule():
    print("TEAR DOWN!")


EXPECTED_PLUGIN_LIST = [
    ['envinject', '1.93.1'],
    ['aws-credentials', '1.17'],
    ['credentials-binding', '1.10'],
    ['s3', '0.10.10'],
    ['ssh-agent', '1.13'],
    ['extended-choice-parameter', '0.75'],
]


EXPECTED_DOWNLOADS = [
    ['envinject', '1.93.1', './tmp/envinject_1.93.1.hpi'],
    ['ivy', '1.21', './tmp/ivy_1.21.hpi'],
    ['nant', '1.4.1', './tmp/nant_1.4.1.hpi'],
    ['matrix-project', '1.7', './tmp/matrix-project_1.7.hpi'],
    ['script-security', '1.13', './tmp/script-security_1.13.hpi'],
    ['junit', '1.2', './tmp/junit_1.2.hpi'],
    ['aws-credentials', '1.17', './tmp/aws-credentials_1.17.hpi'],
    ['credentials', '1.22', './tmp/credentials_1.22.hpi'],
    ['aws-java-sdk', '1.10.16', './tmp/aws-java-sdk_1.10.16.hpi'],
    ['credentials-binding', '1.7', './tmp/credentials-binding_1.7.hpi'],
    ['credentials', '1.23', './tmp/credentials_1.23.hpi'],
    ['plain-credentials', '1.0', './tmp/plain-credentials_1.0.hpi'],
    ['workflow-step-api', '1.7', './tmp/workflow-step-api_1.7.hpi'],
    ['credentials-binding', '1.10', './tmp/credentials-binding_1.10.hpi'],
    ['workflow-step-api', '2.4', './tmp/workflow-step-api_2.4.hpi'],
    ['structs', '1.3', './tmp/structs_1.3.hpi'],
    ['credentials', '2.1.7', './tmp/credentials_2.1.7.hpi'],
    ['plain-credentials', '1.3', './tmp/plain-credentials_1.3.hpi'],
    ['structs', '1.5', './tmp/structs_1.5.hpi'],
    ['s3', '0.10.10', './tmp/s3_0.10.10.hpi'],
    ['aws-java-sdk', '1.10.50', './tmp/aws-java-sdk_1.10.50.hpi'],
    ['jackson2-api', '2.5.4', './tmp/jackson2-api_2.5.4.hpi'],
    ['maven-plugin', '2.0', './tmp/maven-plugin_2.0.hpi'],
    ['token-macro', '1.1', './tmp/token-macro_1.1.hpi'],
    ['mailer', '1.5', './tmp/mailer_1.5.hpi'],
    ['javadoc', '1.0', './tmp/javadoc_1.0.hpi'],
    ['copyartifact', '1.37', './tmp/copyartifact_1.37.hpi'],
    ['maven-plugin', '2.7.1', './tmp/maven-plugin_2.7.1.hpi'],
    ['mailer', '1.7', './tmp/mailer_1.7.hpi'],
    ['ssh-agent', '1.13', './tmp/ssh-agent_1.13.hpi'],
    ['bouncycastle-api', '1.0.2', './tmp/bouncycastle-api_1.0.2.hpi'],
    ['ssh-credentials', '1.11', './tmp/ssh-credentials_1.11.hpi'],
    ['extended-choice-parameter', '0.75', './tmp/extended-choice-parameter_0.75.hpi'],
    ['script-security', '1.19', './tmp/script-security_1.19.hpi'],
    ['jquery', '1.11.2-0', './tmp/jquery_1.11.2-0.hpi']
]


def test_plugin_list():
    plugins_to_install = jpi.cli.get_plugins_to_install("./fixtures/plugins.txt")
    nt.eq_(plugins_to_install, EXPECTED_PLUGIN_LIST)


def test_plugin_download():
    plugins, downloaded = jpi.download.download_all(
        EXPECTED_PLUGIN_LIST,
        "./tmp",
        {}, [])
    nt.eq_(downloaded, EXPECTED_DOWNLOADS)
