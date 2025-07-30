import re
from packaging.version import Version

def cleandict(d):
    if not isinstance(d, dict):
        return d
    return dict((k, cleandict(v)) for k, v in d.items() if v is not None)

def get_version(version_str: str):
    if re.fullmatch(r'[0-9a-fA-F]{7,40}', version_str):
        return Version("0.0.0")
    
    return Version(version_str)
