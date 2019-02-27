"""Helper functions related to resolving *.hpi dependencies."""
import sys
import re
from zipfile import ZipFile


def remove_dep_metadata(depstr):
    """
    Removes metadata  we don't care about from dependencies.

    i.e both "package:1.3" and "package:1.3;some-data" should result in ["package","1.3"]
    """
    if ";" in depstr:
        return depstr[:depstr.rfind(";")].strip().split(":")
    return depstr.strip().split(":")


def assume_min_or_latest(dep):
    """
    Normalizes the list of dependencies to have only major version

    Assumes a list of versions where version is a list containing at least one .
    If no version number is present, assume "latest"
    """
    if len(dep) == 1:
        return [dep[0], "latest"]
    else:
        return dep[0:2]


def plugin_str_to_data(plugin_str):
    """Parses a newline delimited string to list of `[[plugin_name,plugin_version]]`."""
    return [x.strip().split(":")
            for x in plugin_str.strip().split("\n")
            if x != ""]


def dep_str_to_data(plugin_str):
    """
    Parses the depstring in manifest.xml to list of [[plugin_name,plugin_version]]

    It filters out optional deps, and removes other metadata.
    """
    return [assume_min_or_latest(remove_dep_metadata(x))
            for x in plugin_str.split(",")
            if x != ""]


def str_to_ver(version):
    """Converts semver to list of ints

    i.e. "1.2.3-0" to [1,2,3,0]
    "latest" is represented as maxint
    """
    if version == "latest":
        return sys.maxsize
    return [int(p) for p in re.split(r"\.|-", version)]


def ver_to_str(version):
    """
    Converts list of ints to string

    i.e. [1,2,3,0] to "1.2.3.0"
    """
    if version == sys.maxsize:
        return "latest"
    return ".".join(str(x) for x in version)


def add_plugin(plugins, name, version, deps):
    """Utility function for adding to map of maps."""
    if name not in plugins:
        plugins[name] = {}
    plugins[name][version] = deps
    return plugins


def get_latest_version_present(plugins, plugin):
    """From all of the stated versions of the plugin, get the newest."""
    return max(str_to_ver(v) for v in plugins[plugin].keys())


def is_greater_version_present(plugins, plugin, version):
    """
    Compares plugins version to the versions of the plugins already downloaded.

    Returns True, if there already is greater version in the `plugins` list.
    """
    if plugin not in plugins:
        return False
    latest = get_latest_version_present(plugins, plugin)
    current = str_to_ver(version)
    return current <= latest


def normalize_manifest(manifest_bin):
    """Normalizes manifest.

    Manifest file has crlf line ends, as well as sometimes incorrectly split lines.
    These can be identified as lines that start with a space.
    We first remove the bad splits, and then replace crlf with | as a separator.
    """
    correct_lines = manifest_bin.replace(b"\r\n ", b"")
    normalized = correct_lines.replace(b"\r\n", b"|")
    return normalized.decode('utf-8')


def parse_manifest(manifest_str):
    """Parse the normalized manifest_str to a dictionary"""
    return {
        k: v
        for k, v
        in [l.strip().split(":", 1)
            for l
            in manifest_str.split("|") if ":" in l]}


def deduplicate_downloads(plugins, downloaded):
    """Removes references to downloaded plugins, where there is already a newer version present."""
    return list(reversed([
        [plugin, version, path]
        for plugin, version, path in downloaded
        if get_latest_version_present(plugins, plugin) == str_to_ver(version)]))


def installable_downloads(installed, plugins, downloaded):
    """Filters the downloaded plugins to ones actually installable.

    The plugin is installable if all of its dependencies (found in the `plugins` param)
    are satisfied by plugins in the `installed` list.
    """
    installable = []
    remaining = []
    for plugin, version, path in downloaded:
        deps = plugins[plugin][version]
        if all(is_greater_version_present(installed, dep, dep_ver)
               for dep, dep_ver in deps):
            installable.append([plugin, version, path])
        else:
            remaining.append([plugin, version, path])
    return installable, remaining


def get_manifest_for_hpi(path):
    """Extracts and returns manifest from hpi file."""
    with ZipFile(path) as hpi:
        with hpi.open('META-INF/MANIFEST.MF', "r") as manifest:
            return manifest.read()


def get_dependencies_for_hpi(path):
    """Extracts dependencies for a hpi file from its manifest."""
    manifest_bin = get_manifest_for_hpi(path)
    manifest_str = normalize_manifest(manifest_bin)
    manifest_data = parse_manifest(manifest_str)
    if 'Plugin-Dependencies' in manifest_data:
        return dep_str_to_data(manifest_data['Plugin-Dependencies'])
    else:
        return []
