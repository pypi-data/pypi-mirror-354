import os
from extractor_wrapper import ExtractorFactory

from loggerplusplus import LoggerManager, LoggerConfig, Logger

LoggerManager.enable_dynamic_config_update = True
LoggerManager.enable_unique_logger_identifier = True

LoggerManager.global_config = LoggerConfig.from_kwargs(
    # Loggers Output
    write_to_file=False,
    # Monitoring
    display_monitoring=False,
    files_monitoring=False,
    # Placement
    filename_lineno_max_width=18,
    identifier_max_width=24
)

logger = Logger(
    identifier="Main",
    follow_logger_manager_rules=True
)

# Répertoire contenant les fichiers à tester
TEST_DIR = "test_files"


def test_extractor(file_path):
    file_type = os.path.splitext(file_path)[1].lower().lstrip(".") or "no_ext"
    logger.info(f"=== Testing extraction for {file_type.upper()} ({file_path}) ===")
    try:
        content = ExtractorFactory.auto_extract(file_path)
        logger.info(f"Extraction SUCCESS for {file_type.upper()}:")
        logger.debug(f"--- Extracted content preview ---\n{content[:500]}")  # Affiche les 500 premiers caractères
    except Exception as e:
        logger.error(f"Extraction FAILED for {file_type.upper()}: {e}")


def main():
    if not os.path.isdir(TEST_DIR):
        logger.error(f"Le répertoire '{TEST_DIR}' n'existe pas.")
        return

    # Parcours récursif ou non ? Ici, on ne descend pas dans les sous-dossiers
    for fname in os.listdir(TEST_DIR):
        full_path = os.path.join(TEST_DIR, fname)
        if os.path.isfile(full_path):
            test_extractor(full_path)
        else:
            logger.debug(f"Ignored (not a file): {full_path}")


if __name__ == "__main__":
    main()
