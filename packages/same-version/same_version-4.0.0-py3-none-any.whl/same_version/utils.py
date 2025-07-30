
import packaging.version
import semver


def parse_version_pep440(v: str | None) -> packaging.version.Version | None:
    if v is None:
        return None
    return packaging.version.Version(v)

def parse_version_semver(v: str | None) -> semver.Version | None:
    if v is None:
        return None
    return semver.Version.parse(v)