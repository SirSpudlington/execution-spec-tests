"""
Tests all precompile operations for EIP-7932
"""

import pytest
from py_ecc.secp256k1 import secp256k1
from ethereum_test_tools import (
    Account,
    Alloc,
    Environment,
    StateTestFiller,
    TransactionTestFiller,
    Transaction,
    YulCompiler,
)
from ethereum_test_checklists import EIPChecklist
from ethereum_test_types.receipt_types import TransactionReceipt

from .spec import Spec, ref_spec_7932

REFERENCE_SPEC_GIT_PATH = ref_spec_7932.git_path
REFERENCE_SPEC_VERSION = ref_spec_7932.version


@pytest.mark.valid_from("Osaka")
@pytest.mark.compile_yul_with("Cancun")
@EIPChecklist.Precompile.Test.CallContexts.Normal
@EIPChecklist.Precompile.Test.ValueTransfer.NoFee
@EIPChecklist.Precompile.Test.Inputs.AllZeros
@EIPChecklist.Precompile.Test.InputLengths.Dynamic.Valid
def test_call_all_zeros(state_test: StateTestFiller, pre: Alloc, yul: YulCompiler):
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

@pytest.mark.valid_from("Osaka")
@pytest.mark.compile_yul_with("Cancun")
@EIPChecklist.Precompile.Test.CallContexts.Callcode
def test_callcode_all_zeros(state_test: StateTestFiller, pre: Alloc, yul: YulCompiler):
    env = Environment()

    caller_contract = pre.deploy_contract(
        code=yul(
            f"""
            {{
                if eq(
                    callcode(100000, {Spec.SIGRECOVER_PRECOMPILE_ADDRESS}, 0, 0, 64, 128, 32),
                    0
                ) {{
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

@pytest.mark.valid_from("Osaka")
@pytest.mark.compile_yul_with("Cancun")
@EIPChecklist.Precompile.Test.CallContexts.Delegate
def test_delegatecall_all_zeros(state_test: StateTestFiller, pre: Alloc, yul: YulCompiler):
    env = Environment()

    caller_contract = pre.deploy_contract(
        code=yul(
            f"""
            {{
                if eq(
                    delegatecall(100000, {Spec.SIGRECOVER_PRECOMPILE_ADDRESS}, 0, 64, 128, 32),
                    0
                ) {{
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

@pytest.mark.valid_from("Osaka")
@pytest.mark.compile_yul_with("Cancun")
@EIPChecklist.Precompile.Test.CallContexts.Static
def test_staticcall_all_zeros(state_test: StateTestFiller, pre: Alloc, yul: YulCompiler):
    env = Environment()

    caller_contract = pre.deploy_contract(
        code=yul(
            f"""
            {{
                if eq(
                    staticcall(100000, {Spec.SIGRECOVER_PRECOMPILE_ADDRESS}, 0, 64, 128, 32),
                    0
                ) {{
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

@pytest.mark.valid_from("Osaka")
@pytest.mark.compile_yul_with("Cancun")
@EIPChecklist.Precompile.Test.CallContexts.TxEntry
def test_tx_to(transaction_test: TransactionTestFiller, pre: Alloc):
    sender = pre.fund_eoa(amount=0x0123456789)

    tx = Transaction(
        ty=0x0,
        chain_id=0x01,
        sender=sender,
        to=Spec.SIGRECOVER_PRECOMPILE_ADDRESS,
        gas_limit=500000,
        gas_price=10,
        protected=True,
        expected_receipt=TransactionReceipt(status=0)
    )

    transaction_test(
        pre=pre,
        tx=tx,
    )

@pytest.mark.valid_from("Osaka")
@pytest.mark.compile_yul_with("Cancun")
@EIPChecklist.Precompile.Test.InputLengths.Zero
def test_call_empty_calldata(state_test: StateTestFiller, pre: Alloc, yul: YulCompiler):
    env = Environment()

    caller_contract = pre.deploy_contract(
        code=yul(
            f"""
            {{
                if eq(
                    call(100000, {Spec.SIGRECOVER_PRECOMPILE_ADDRESS}, 0, 0, 0, 128, 32),
                    1
                ) {{
                    revert(0, 0)
                }}

                // This is `0x` by default.
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

@pytest.mark.valid_from("Osaka")
@pytest.mark.compile_yul_with("Cancun")
@EIPChecklist.Precompile.Test.InputLengths.Dynamic.TooLong
def test_call_too_long(state_test: StateTestFiller, pre: Alloc, yul: YulCompiler):
    env = Environment()

    caller_contract = pre.deploy_contract(
        code=yul(
            f"""
            {{
                if eq(
                    call(100000, {Spec.SIGRECOVER_PRECOMPILE_ADDRESS}, 0, 0, 256, 128, 32),
                    0
                ) {{
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

@pytest.mark.valid_from("Osaka")
@pytest.mark.compile_yul_with("Cancun")
@EIPChecklist.Precompile.Test.InputLengths.Dynamic.TooShort
def test_call_too_short(state_test: StateTestFiller, pre: Alloc, yul: YulCompiler):
    env = Environment()

    caller_contract = pre.deploy_contract(
        code=yul(
            f"""
            {{  
                mstore(33, 0xff)
                if eq(
                    call(100000, {Spec.SIGRECOVER_PRECOMPILE_ADDRESS}, 0, 0, 64, 128, 32),
                    0
                ) {{
                    revert(0, 0)
                }}

                // This is `0x` by default.
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

@pytest.mark.valid_from("Osaka")
@pytest.mark.compile_yul_with("Cancun")
def test_call_null_should_not_work(state_test: StateTestFiller, pre: Alloc, yul: YulCompiler):
    env = Environment()

    sender = pre.fund_eoa(amount=0x0123456789)

    example_hash = b"\xFF" * 32
    example_key = b"\xFF" * 32

    (v, r, s) = secp256k1.ecdsa_raw_sign(example_hash, example_key)

    caller_contract = pre.deploy_contract(
        code=yul(
            f"""
            {{
                mstore(0, 0x{example_hash.hex()})
                mstore(32, 0xff)
                mstore(33, {65 << 8})
                mstore(64, {r})
                mstore(96, {s})
                mstore8(97, {v})
                if eq(
                    call(100000, {Spec.SIGRECOVER_PRECOMPILE_ADDRESS}, 0, 0, 98, 128, 32),
                    0
                ) {{
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

@pytest.mark.valid_from("Osaka")
@pytest.mark.compile_yul_with("Cancun")
@EIPChecklist.Precompile.Test.CallContexts.Initcode.Tx
def test_tx_create(transaction_test: TransactionTestFiller, pre: Alloc, yul: YulCompiler):
    code = yul(
            f"""
            object "Contract" {{
                code {{
                    if eq(
                        callcode(100000, {Spec.SIGRECOVER_PRECOMPILE_ADDRESS}, 0, 0, 64, 128, 32),
                        0
                    ) {{
                        revert(0, 0)
                    }}

                    if not(iszero(mload(128))) {{
                        revert(0, 0)
                    }}
                    
                    datacopy(0, dataoffset("runtime"), datasize("runtime"))
                    return(0, datasize("runtime"))
                }}

                object "runtime" {{
                    code {{
                        revert(0, 0)
                    }}
                }}
            }}
            """
        )

    sender = pre.fund_eoa(amount=0x0123456789)

    tx = Transaction(
        ty=0x0,
        chain_id=0x01,
        sender=sender,
        to=None,
        gas_limit=500000,
        gas_price=10,
        protected=True,
        input=code,
        expected_receipt=TransactionReceipt(status=1),
    )

    transaction_test(
        tx=tx,
        pre=pre
    )

@pytest.mark.valid_from("Osaka")
@pytest.mark.compile_yul_with("Cancun")
@EIPChecklist.Precompile.Test.GasUsage.Dynamic.Exact
def test_exact_gas(state_test: StateTestFiller, pre: Alloc, yul: YulCompiler):
    env = Environment()

    caller_contract = pre.deploy_contract(
        code=yul(
            f"""
            {{
                if eq(call(3000, {Spec.SIGRECOVER_PRECOMPILE_ADDRESS}, 0, 0, 64, 128, 32), 0) {{
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

@pytest.mark.valid_from("Osaka")
@pytest.mark.compile_yul_with("Cancun")
@EIPChecklist.Precompile.Test.GasUsage.Dynamic.Oog
def test_out_of_gas(state_test: StateTestFiller, pre: Alloc, yul: YulCompiler):
    env = Environment()

    caller_contract = pre.deploy_contract(
        code=yul(
            f"""
            {{
                if eq(call(2999, {Spec.SIGRECOVER_PRECOMPILE_ADDRESS}, 0, 0, 64, 128, 32), 1) {{
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

@pytest.mark.valid_until("Prague")
@pytest.mark.compile_yul_with("Cancun")
@EIPChecklist.Precompile.Test.ForkTransition.Before.Cold
@EIPChecklist.Precompile.Test.ForkTransition.Before.InvalidInput
@EIPChecklist.Precompile.Test.ForkTransition.Before.ZeroGas
def test_precompile_does_not_exist_before_osaka(transaction_test: TransactionTestFiller,
                                                pre: Alloc, yul: YulCompiler):
    sender = pre.fund_eoa(amount=0x0123456789)

    contract = pre.deploy_contract(
        code=yul(
            f"""
                {{
                    let start := gas()

                    if eq(
                        callcode(0, {Spec.SIGRECOVER_PRECOMPILE_ADDRESS}, 0, 0, 0, 128, 32),
                        0
                    ) {{
                        revert(0, 0)
                    }}

                    if lt(sub(start, gas()), 250) {{
                        revert(0, 0)
                    }}

                    if not(iszero(mload(128))) {{
                        revert(0, 0)
                    }}
                }}
            """
        )
    )

    tx = Transaction(
        ty=0x0,
        chain_id=0x01,
        sender=sender,
        to=contract,
        gas_limit=50000,
        gas_price=10,
        protected=True,
        expected_receipt=TransactionReceipt(status=1)
    )

    transaction_test(
        pre=pre,
        tx=tx,
    )

@pytest.mark.valid_from("Osaka")
@pytest.mark.compile_yul_with("Cancun")
@EIPChecklist.Precompile.Test.ForkTransition.After.Warm
def test_precompile_warm_after_osaka(transaction_test: TransactionTestFiller,
                                                pre: Alloc, yul: YulCompiler):
    sender = pre.fund_eoa(amount=0x0123456789)

    contract = pre.deploy_contract(
        code=yul(
            f"""
                {{
                    let start := gas()

                    if eq(
                        callcode(0, {Spec.SIGRECOVER_PRECOMPILE_ADDRESS}, 0, 0, 0, 128, 32),
                        1
                    ) {{
                        revert(0, 0)
                    }}

                    if gt(sub(start, gas()), 250) {{
                        revert(0, 0)
                    }}
                }}
            """
        )
    )

    tx = Transaction(
        ty=0x0,
        chain_id=0x01,
        sender=sender,
        to=contract,
        gas_limit=500000,
        gas_price=10,
        protected=True,
        expected_receipt=TransactionReceipt(status=1)
    )

    transaction_test(
        pre=pre,
        tx=tx,
    )
