"""Defines EIP-7932 specification constants and functions."""

from dataclasses import dataclass

from ethereum_test_tools import (
    Address
)

@dataclass(frozen=True)
class ReferenceSpec:
    """Defines the reference spec version and git path."""

    git_path: str
    version: str


ref_spec_7932 = ReferenceSpec("EIPS/eip-7932.md", "70cf8d85254df8fb2df1a8a6abb2cabf31fb8b97")


@dataclass(frozen=True)
class Spec:
    """Constants and helpers for EIP-7932 behaviours."""
    SIGRECOVER_PRECOMPILE_ADDRESS = Address(0x12)
    SIGRECOVER_PRECOMPILE_BASE_GAS = 3000
    
