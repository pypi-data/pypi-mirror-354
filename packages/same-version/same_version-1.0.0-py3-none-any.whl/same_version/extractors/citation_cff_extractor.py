import logging
from argparse import Namespace

import yaml

from same_version.extractors.file_extractor import FileExtractor

logger = logging.getLogger(__name__)

class CitationCffExtractor(FileExtractor):

    def __init__(self, cli_args: Namespace):
        target_cli_parameter_name: str = '--citation-cff-path'
        default_target_name: str = "CITATION.cff"
        super().__init__(
            target_file_path=self._create_target_file_path_from_cli_arg(cli_args=cli_args, cli_arg_parameter=target_cli_parameter_name), 
            default_target_name=default_target_name, 
            target_cli_parameter_name=target_cli_parameter_name
        )
    
    def extract_version(self) -> str | None:
        data: dict = {}
        if self.target_file_path:
            with open(self.target_file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        version = data.get('version')
        if not version:
            logger.error(f"❌ {self.target_name} missing 'version' field!")
            return None
        logger.info(f"📖 {self.target_name} version: {version}")
        return version