import logging

from same_version.checkers.file_checker import FileChecker
from same_version.utils import parse_version_semver

logger = logging.getLogger(__name__)

class PackageJsonChecker(FileChecker):

    def check(self, base_version_str: str | None) -> bool:
        if base_version_str is None:
            return True
        base_version_pep440 = self.create_pep440_version(version_str=base_version_str)
        if base_version_pep440 is None:
            return True
        
        if self.target_exists:
            target_version_str = self.target_version_str
            target_name = self.target_name

            try:
                base_version_semver_str: str = f"{base_version_pep440.major}.{base_version_pep440.minor}.{base_version_pep440.micro}"
                if base_version_pep440.is_prerelease and base_version_pep440.pre is not None:
                    base_version_semver_str += f"-{base_version_pep440.pre[0]}.{base_version_pep440.pre[1]}"

                base_version_semver = parse_version_semver(base_version_semver_str)
                target_version_semver = parse_version_semver(target_version_str)

                if base_version_semver != target_version_semver:
                    logger.error(f"❌ Version mismatch: {target_name} {target_version_str} != base version {base_version_str}")
                    return False
                else:
                    return True
            
            except Exception as e:
                logger.error(f"❌ Parse error: Could not parse tag version as SemVer for {self.target_name}: {e}")
                return False
        else:
            self._log_missing_target()
            return False
