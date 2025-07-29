
import logging

logger = logging.getLogger(__name__)

class Extractor:
    def __init__(self):
        pass

    def _get_data(self) -> dict:
        raise NotImplementedError()
    
    def _get_version_from_data(self, data: dict) -> str | None:
        raise NotImplementedError()
    
    def _log_missing_version_error(self, data: dict):
        logger.error(f"❌ {self.target_name} missing 'version' field")

    def _log_found_version_info(self, version: str, data: dict):
        logger.info(f"📖 {self.target_name} version: {version}")

    def extract_version(self) -> str | None:
        data: dict = self._get_data()
        version = self._get_version_from_data(data=data)
        if not version:
            if self.target_exists:
                # only print this error if the target exists
                self._log_missing_version_error(data=data)
            return None
        self._log_found_version_info(version=version, data=data)
        return version
    
    @property
    def target_exists(self) -> bool:
        raise NotImplementedError()
    
    @property
    def target_name(self) -> str | None:
        raise NotImplementedError()
    
    @property
    def target_cli_parameter_name(self) -> str | None:
        raise NotImplementedError()
