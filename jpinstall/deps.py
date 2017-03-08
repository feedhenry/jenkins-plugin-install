"""
Helper functions related to resolving *.hpi dependencies
"""
import sys
import re
from zipfile import ZipFile

def remove_dep_metadata(depstr):
    """
    Plugin dependencies can have metadata we don't care about,
    i.e both "a:1.3" and "a:1.3;some-data" should result in ["a","1.3"]
    """
    if ";" in depstr:
        return depstr[:depstr.rfind(";")].strip().split(":")
    return depstr.strip().split(":")

def assume_min_or_latest(dep):
    """
    If no version number is present, assume "latest"
    """
    if len(dep) == 1:
        return [dep[0], "latest"]
    else:
        return dep[0:2]

def plugin_str_to_data(plugin_str):
    """
    Parses a newline delimited string to
    list of [[plugin_name,plugin_version]]
    """
    return [x.strip().split(":")
            for x in plugin_str.strip().split("\n")
            if x != ""]

def dep_str_to_data(plugin_str):
    """
    Parses the depstring in manifest.xml to
    list of [[plugin_name,plugin_version]]

    It filters out optional deps, and removes other metadata.
    """
    return [assume_min_or_latest(remove_dep_metadata(x))
            for x in plugin_str.split(",")
            if x != "" and not "resolution:=optional" in x]

def str_to_ver(version):
    """
    Converts semver to list of ints
    i.e. "1.2.3-0" to [1,2,3,0]
    "latest" is represented as maxint
    """
    if version == "latest":
        return sys.maxint
    return [int(p) for p  in re.split(r"\.|-", version)]

def ver_to_str(version):
    """
    Converts list of ints to string
    i.e. [1,2,3,0] to "1.2.3.0"
    """
    if version == sys.maxint:
        return "latest"
    return ".".join(str(x) for x in version)

def add_plugin(plugins, name, version, deps):
    """
    Utility function for adding to map of maps
    """
    if not name in plugins:
        plugins[name] = {}
    plugins[name][version] = deps
    return plugins

def get_latest_version_present(plugins, plugin):
    """
    From all of the stated versions of the plugin, get the newest.
    """
    return max(str_to_ver(v) for v in plugins[plugin].keys())

def is_greater_version_present(plugins, plugin, version):
    """
    For i.e. comparing plugins version to the versions of the plugins already downloaded.
    Returns True, if there already is greater version.
    """
    if not plugin in plugins:
        return False
    latest = get_latest_version_present(plugins, plugin)
    current = str_to_ver(version)
    return current <= latest

def normalize_manifest(manifest_bin):
    """
    Manifest file has crlf line ends, as well as sometimes incorrectly split lines.
    We first remove the bad splits, and then replace crlf with | as a separator.
    """
    normalized = manifest_bin \
        .replace(b"\r\n ", b"") \
        .replace(b"\r\n", b"|")

    return str(normalized)

def parse_manifest(manifest_str):
    """
    Parse the normalized manifest_str to a dictionary
    """
    return {
        k:v
        for k, v
        in [l.strip().split(":", 1)
            for l
            in manifest_str.split("|") if ":" in l]}

def deduplicate_downloads(plugins, downloaded):
    """
    Function to remove references to downloaded plugins,
    where there is already a newer version present.
    """
    return [
        [plugin, version, path]
        for plugin, version, path in downloaded
        if get_latest_version_present(plugins, plugin) == str_to_ver(version)]

def get_manifest_for_hpi(path):
    """
    Extracts and returns manifest from hpi file
    """
    with ZipFile(path) as hpi:
        with hpi.open('META-INF/MANIFEST.MF', "r") as manifest:
            return manifest.read()

def get_dependencies_for_hpi(path):
    """
    Extracts dependencies for a hpi file from its manifest
    """
    manifest_bin = get_manifest_for_hpi(path)
    manifest_str = normalize_manifest(manifest_bin)
    manifest_data = parse_manifest(manifest_str)
    if 'Plugin-Dependencies' in manifest_data:
        return dep_str_to_data(manifest_data['Plugin-Dependencies'])
    else:
        return []
