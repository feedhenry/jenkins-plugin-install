
import nose.tools as nt  # contains testing tools like ok_, eq_, etc.
import jpinstall as jpi
import sys

def setup():
    print sys.version

    print "SETUP!"

def teardown():
    print "TEAR DOWN!"

def test_min_or_latest():
    nt.eq_(jpi.deps.assume_min_or_latest(['a', '1', '2']), ['a', '1'])
    nt.eq_(jpi.deps.assume_min_or_latest(['a']), ['a', 'latest'])

def test_remove_dep_metadata():
    nt.eq_(jpi.deps.remove_dep_metadata("a:1.3"), ['a', '1.3'])
    nt.eq_(jpi.deps.remove_dep_metadata("a:1.3;resolution:=optional"), ['a', '1.3'])

def test_plugin_str_to_data():
    nt.eq_(
        jpi.deps.plugin_str_to_data("""
        a:1.3
        b:3.4
        c:4
        """),
        [['a', '1.3'], ['b', '3.4'], ['c', '4']])

def test_dep_str_to_data():
    nt.eq_(
        jpi.deps.dep_str_to_data("a:1.3,b:3.4;resolution:=optional,c:4,d:5;metadata"),
        [['a', '1.3'], ['b', '3.4'], ['c', '4'], ['d', '5']])

def test_str_to_ver():
    nt.eq_(
        jpi.deps.str_to_ver("1.3-0"), [1, 3, 0])
    nt.eq_(
        jpi.deps.str_to_ver("latest"), sys.maxint)

def test_ver_str():
    nt.eq_(
        jpi.deps.ver_to_str([1, 2, 3, 0]), "1.2.3.0")
    nt.eq_(
        jpi.deps.ver_to_str(sys.maxint), "latest")


def test_add_plugin():
    nt.eq_(
        jpi.deps.add_plugin({}, "a", "latest", []),
        {"a":{"latest":[]}})
    nt.eq_(
        jpi.deps.add_plugin({"a":{"1.2":[]}}, "a", "latest", []),
        {"a":{"1.2":[], "latest":[]}})

def test_get_latest_version_present():
    nt.eq_(jpi.deps.get_latest_version_present(
        {"a":{"1.0":[], "1.1":[], "2.3":[]}, "b":{"latest":[]}}, "a"
    ), [2, 3])

def test_is_greater_version_present():
    plugins = {"a":{"1.0":[], "1.1":[], "2.3":[]}}
    nt.eq_(jpi.deps.is_greater_version_present(plugins, "a", "1.2"), True)
    nt.eq_(jpi.deps.is_greater_version_present(plugins, "a", "2.4"), False)
    nt.eq_(jpi.deps.is_greater_version_present({}, "a", "2.4"), False)


def test_normalize_manifest():
    mangled = b"Name: a\r\nPlugins: aaa:1,bbb:2,cc\r\n c:3\r\nAuthor:"
    normalized = "Name: a|Plugins: aaa:1,bbb:2,ccc:3|Author:"
    nt.eq_(jpi.deps.normalize_manifest(mangled), normalized)

def test_get_dependencies_for_hpi():
    actuall = jpi.deps.get_dependencies_for_hpi("./fixtures/docker-workflow.hpi")
    expected = [
        ['docker-commons', '1.5'],
        ['workflow-step-api', '2.2'],
        ['script-security', '1.17'],
        ['workflow-cps', '2.7'],
        ['workflow-durable-task-step', '2.4']]
    nt.eq_(actuall, expected)

def test_get_dependencies_for_hpi_empty():
    actuall = jpi.deps.get_dependencies_for_hpi("./fixtures/aws-java-sdk.hpi")
    expected = []
    nt.eq_(actuall, expected)

def test_deduplicate_downloads():
    plugins = {"a":{"1.0":[], "1.2":[], "2.1":[]}, "b":{"1.2":[]}}
    downloaded = [
        ["a", "1.0", "a_1.0.hpi"],
        ["a", "1.2", "a_1.2.hpi"],
        ["b", "1.2", "b_1.2.hpi"],
        ["a", "2.1", "a_2.1.hpi"]
        ]
    actuall = jpi.deps.deduplicate_downloads(plugins, downloaded)
    expected = [["a", "2.1", "a_2.1.hpi"], ["b", "1.2", "b_1.2.hpi"]]
    nt.eq_(actuall, expected)

def test_installable_downloads():
    installed = {
    u'git-client': {u'2.1.0': []},
    u'credentials-binding': {u'1.10': []},
    }

    plugins = {
        u'pipeline-github-lib': {u'1.0': [['git-client', '2.0.0']]},
        u'pipeline-github': {u'1.0': [['pipeline-github-lib', '1.0']]}
    }

    downloaded = [
        [u'pipeline-github-lib','1.0','pipeline-gh-lib_1.0.hpi'],
        [u'pipeline-github','1.0','pipeline-gh_1.0.hpi']
    ]

    installable, remaining = jpi.deps.installable_downloads(installed,plugins,downloaded)
    nt.eq_(installable,[
        [u'pipeline-github-lib','1.0','pipeline-gh-lib_1.0.hpi']])
    nt.eq_(remaining,[
        [u'pipeline-github','1.0','pipeline-gh_1.0.hpi']])
          