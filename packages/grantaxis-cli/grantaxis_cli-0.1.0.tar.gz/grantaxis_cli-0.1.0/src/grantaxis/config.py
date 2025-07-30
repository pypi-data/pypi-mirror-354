from __future__ import annotations
import logging
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Pattern, Sequence, Tuple, Union

import yaml

"""
GrantAxis – config.py
====================
Load **grantaxis.yml** once, compile all regex filters, and expose helper
functions to trim the `added`/`removed`/`changed` collections produced by
`diff.py`.

Supported keys (all optional)
----------------------------
```yaml
ignore_objects:   # object FQN or schema.DB pattern
  - "^RAW\\.EVENT_.*$"
ignore_grantees:  # ROLE_ or USER_ names
  - "^ROLE_ETL_TMP_.*$"
ignore_privileges:
  - "^USAGE$"
critical_privileges:  # drift fails CI only if privilege matches (future)
  - "OWNERSHIP"
```

If **grantaxis.yml** is missing, defaults to "allow all" (no filters).
"""


# Configure module logger
logger = logging.getLogger(__name__)

# Type aliases for better readability
DriftRecord = Dict[str, str]
ChangedRecord = Tuple[DriftRecord, DriftRecord]
FilterResult = Tuple[List[DriftRecord], List[DriftRecord], List[ChangedRecord]]


class ConfigError(Exception):
    """Raised when configuration loading or validation fails."""

    pass


class ValidationError(ConfigError):
    """Raised when configuration validation fails."""

    pass


@dataclass(slots=True, frozen=True)
class Config:
    """Configuration holder with compiled regex patterns for filtering grant drift."""

    ignore_objects: List[Pattern[str]]
    ignore_grantees: List[Pattern[str]]
    ignore_privileges: List[Pattern[str]]
    critical_privileges: List[Pattern[str]]

    @classmethod
    def load(cls, path: Union[str, Path, None] = "grantaxis.yml") -> Config:
        """
        Load configuration from YAML file.

        Args:
            path: Path to configuration file. Defaults to 'grantaxis.yml'

        Returns:
            Config instance with compiled patterns

        Raises:
            ConfigError: If file cannot be read or parsed
            ValidationError: If configuration structure is invalid
        """
        config_path = Path(path) if path else Path("grantaxis.yml")

        try:
            if config_path.exists():
                logger.info(f"Loading configuration from {config_path}")
                with config_path.open("r", encoding="utf-8") as f:
                    data = yaml.safe_load(f) or {}
            else:
                logger.info(
                    f"Configuration file {config_path} not found, using defaults"
                )
                data = {}

        except yaml.YAMLError as exc:
            raise ConfigError(f"Failed to parse YAML in {config_path}: {exc}") from exc
        except (OSError, IOError) as exc:
            raise ConfigError(
                f"Failed to read config file {config_path}: {exc}"
            ) from exc

        # Validate configuration structure
        cls._validate_config(data, config_path)

        return cls(
            ignore_objects=cls._compile_patterns("ignore_objects", data),
            ignore_grantees=cls._compile_patterns("ignore_grantees", data),
            ignore_privileges=cls._compile_patterns("ignore_privileges", data),
            critical_privileges=cls._compile_patterns("critical_privileges", data),
        )

    @staticmethod
    def _validate_config(data: Dict, config_path: Path) -> None:
        """Validate configuration structure and types."""
        if not isinstance(data, dict):
            raise ValidationError(
                f"Configuration root must be a dictionary in {config_path}"
            )

        valid_keys = {
            "ignore_objects",
            "ignore_grantees",
            "ignore_privileges",
            "critical_privileges",
        }
        invalid_keys = set(data.keys()) - valid_keys

        if invalid_keys:
            logger.warning(
                f"Unknown configuration keys in {config_path}: {invalid_keys}"
            )

        for key, value in data.items():
            if key in valid_keys and value is not None:
                if not isinstance(value, list):
                    raise ValidationError(
                        f"Configuration key '{key}' must be a list in {config_path}"
                    )
                if not all(isinstance(item, str) for item in value):
                    raise ValidationError(
                        f"All items in '{key}' must be strings in {config_path}"
                    )

    @staticmethod
    def _compile_patterns(key: str, data: Dict) -> List[Pattern[str]]:
        """
        Compile regex patterns from configuration.

        Args:
            key: Configuration key to extract patterns from
            data: Configuration dictionary

        Returns:
            List of compiled regex patterns

        Raises:
            ValidationError: If regex compilation fails
        """
        patterns: Sequence[str] = data.get(key, []) or []
        compiled_patterns = []

        for pattern in patterns:
            try:
                compiled_patterns.append(re.compile(pattern))
                logger.debug(f"Compiled pattern for {key}: {pattern}")
            except re.error as exc:
                raise ValidationError(
                    f"Invalid regex pattern '{pattern}' in {key}: {exc}"
                ) from exc

        return compiled_patterns

    def is_ignored(self, record: DriftRecord) -> bool:
        """
        Check if a drift record matches any ignore rule.

        Args:
            record: Dictionary containing grant information

        Returns:
            True if record should be ignored, False otherwise
        """
        if not isinstance(record, dict):
            logger.warning(f"Expected dictionary record, got {type(record)}")
            return False

        object_fqn = self._build_object_fqn(record)
        grantee = record.get("grantee_name", "")
        privilege = record.get("privilege", "")

        # Check each filter type
        if self._matches_patterns(object_fqn, self.ignore_objects):
            logger.debug(f"Ignoring object: {object_fqn}")
            return True

        if self._matches_patterns(grantee, self.ignore_grantees):
            logger.debug(f"Ignoring grantee: {grantee}")
            return True

        if self._matches_patterns(privilege, self.ignore_privileges):
            logger.debug(f"Ignoring privilege: {privilege}")
            return True

        return False

    def is_critical(self, record: DriftRecord) -> bool:
        """
        Check if a drift record contains a critical privilege.

        Args:
            record: Dictionary containing grant information

        Returns:
            True if record contains critical privilege, False otherwise
        """
        if not self.critical_privileges:
            return True  # All privileges are critical if none specified

        privilege = record.get("privilege", "")
        return self._matches_patterns(privilege, self.critical_privileges)

    @staticmethod
    def _build_object_fqn(record: DriftRecord) -> str:
        """Build fully qualified name from record components."""
        components = [
            record.get("database_name", ""),
            record.get("schema_name", ""),
            record.get("object_name", ""),
        ]
        return ".".join(component for component in components if component)

    @staticmethod
    def _matches_patterns(text: str, patterns: List[Pattern[str]]) -> bool:
        """Check if text matches any of the provided patterns."""
        return any(pattern.search(text) for pattern in patterns)

    def filter_drift(
        self,
        added: List[DriftRecord],
        removed: List[DriftRecord],
        changed: List[ChangedRecord],
    ) -> FilterResult:
        """
        Filter drift lists by removing ignored items.

        Args:
            added: List of added grant records
            removed: List of removed grant records
            changed: List of (old, new) changed grant record pairs

        Returns:
            Tuple of (filtered_added, filtered_removed, filtered_changed)
        """
        logger.info(
            f"Filtering drift: {len(added)} added,"
            f"{len(removed)} removed, {len(changed)} changed"
        )

        filtered_added = [r for r in added if not self.is_ignored(r)]
        filtered_removed = [r for r in removed if not self.is_ignored(r)]
        filtered_changed = [pair for pair in changed if not self.is_ignored(pair[0])]

        logger.info(
            f"After filtering: {len(filtered_added)} added,"
            f"{len(filtered_removed)} removed, {len(filtered_changed)} changed"
        )

        return filtered_added, filtered_removed, filtered_changed

    def get_stats(self) -> Dict[str, int]:
        """Get statistics about configured patterns."""
        return {
            "ignore_objects": len(self.ignore_objects),
            "ignore_grantees": len(self.ignore_grantees),
            "ignore_privileges": len(self.ignore_privileges),
            "critical_privileges": len(self.critical_privileges),
        }


def load_config(path: Optional[Union[str, Path]] = None) -> Config:
    """
    Convenience function to load configuration.

    Args:
        path: Optional path to configuration file

    Returns:
        Loaded Config instance
    """
    return Config.load(path)


# ---------------------------------------------------------------------------
# Manual test and example usage
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    try:
        # Try to load from examples directory first, then fallback to default
        example_path = Path("examples/grantaxis.yml")
        config_path = example_path if example_path.exists() else None

        cfg = load_config(config_path)

        print("Configuration loaded successfully!")
        print(f"Pattern statistics: {cfg.get_stats()}")

        # Test data
        dummy_added = [
            {
                "database_name": "RAW",
                "schema_name": "PUBLIC",
                "object_name": "EVENT_123",
                "privilege": "SELECT",
                "grantee_name": "ROLE_RAW_INGEST",
            },
            {
                "database_name": "PROD",
                "schema_name": "SALES",
                "object_name": "ORDERS",
                "privilege": "OWNERSHIP",
                "grantee_name": "ROLE_SYSADMIN",
            },
        ]

        filtered_added, filtered_removed, filtered_changed = cfg.filter_drift(
            dummy_added, [], []
        )

        print("\nTest results:")
        print(f"Original records: {len(dummy_added)}")
        print(f"After filtering: {len(filtered_added)}")

        for record in filtered_added:
            object_fqn = cfg._build_object_fqn(record)
            is_critical = cfg.is_critical(record)
            print(
                f"  - {object_fqn}: {record['privilege']} -> {record['grantee_name']}"
                f"(critical: {is_critical})"
            )

    except (ConfigError, ValidationError) as e:
        logger.error(f"Configuration error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise
