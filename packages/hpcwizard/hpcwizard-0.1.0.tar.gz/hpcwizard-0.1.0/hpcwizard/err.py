# ruff: noqa: D100

class HpcWizardError(Exception):
    """Main class for all vplayer errors."""

    def __init__(self, msg: str) -> None:
        """Object initialization."""
        super().__init__(f"HPC Wizard error: {msg}")
