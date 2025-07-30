from dcentrapi.Base import Base
from dcentrapi.Base import DapiError
from dcentrapi.eventPolling import EventPolling
from dcentrapi.rpcAggregation import RpcAggregation
from dcentrapi.tokenPrices import TokenPrices
from dcentrapi.txSimulation import TxSimulation
from dcentrapi.gas_fee_estimator import GasFeeEstimator
from dcentrapi.event_poller import EventPoller
from dcentrapi.hackMitigation import HackMitigation
from dcentrapi.requests_dappi import requests_get, requests_post
from dcentrapi.rpc_aggregation_async import AsyncRpcAggregation
from dcentrapi.rpc_aggregation_sync import RpcAggregation as SyncRpcAggregation

__version__ = "0.5.9"

# from dcentrapi.gasMonitor import GasMonitor
# from dcentrapi.merkleTree import MerkleTree, MerkleTreeNode

# Explicitly define the public API
__all__ = [
    "Base",
    "DapiError",
    "EventPolling",
    "RpcAggregation",
    "TokenPrices",
    "TxSimulation",
    "GasFeeEstimator",
    "EventPoller",
    "HackMitigation",
    "requests_get",
    "requests_post",
    "AsyncRpcAggregation",
    "SyncRpcAggregation",
]
