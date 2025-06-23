"""
Tests all precompile operations for EIP-7932
"""

import pytest
from ethereum_test_forks.base_fork import BaseFork
from ethereum_test_forks.helpers import Fork
from ethereum_test_tools import (
    Account,
    Alloc,
    Environment,
    StateTestFiller,
    Transaction,
    YulCompiler,
)
from ethereum_test_checklists import EIPChecklist

from .spec import Spec, ref_spec_7932

REFERENCE_SPEC_GIT_PATH = ref_spec_7932.git_path
REFERENCE_SPEC_VERSION = ref_spec_7932.version


@pytest.mark.valid_from("Osaka")
@pytest.mark.compile_yul_with("Cancun")
@EIPChecklist.Precompile.Test.CallContexts.Normal
@EIPChecklist.Precompile.Test.ValueTransfer.NoFee
@EIPChecklist.Precompile.Test.Inputs.AllZeros
@EIPChecklist.Precompile.Test.InputLengths.Dynamic.Valid
def test_algorithmic_transactions_module(state_test: StateTestFiller, pre: Alloc, yul: YulCompiler):
    env = Environment()

    caller_contract = pre.deploy_contract(
        code=yul(
            f"""
            {{
                if eq(call(100000, {Spec.SIGRECOVER_PRECOMPILE_ADDRESS}, 100, 0, 64, 128, 32), 0) {{
                    revert(0, 0)
                }}

                sstore(0, mload(128))
                return(0, 32)
            }}
            """
        ),
        balance=0x0123456789,
        storage={
            0x00: 0xff,
        }
    )

    sender = pre.fund_eoa(amount=0x0123456789)

    tx = Transaction(
        ty=0x0,
        chain_id=0x01,
        sender=sender,
        to=caller_contract,
        gas_limit=500000,
        gas_price=10,
        protected=True
    )

    post = {
        caller_contract: Account(
            storage={
                0x00: 0x0,
            },
        ),
    }

    state_test(env=env, pre=pre, post=post, tx=tx)


Spec.SIGRECOVER_PRECOMPILE_ADDRESS