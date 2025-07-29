import logging
from typing import List, Dict, Any, Union, Optional

from prometheus_client.parser import text_string_to_metric_families

from pypergraph.core.cross_platform.di.rest_client import RESTClient, HttpxClient
from pypergraph.core.cross_platform.rest_api_client import RestAPIClient
from pypergraph.network.models.network import PeerInfo, TotalSupply
from pypergraph.network.models.account import Balance
from pypergraph.network.models.network import Ordinal
from pypergraph.network.models.snapshot import SignedGlobalIncrementalSnapshot
from pypergraph.network.models.transaction import (
    TransactionReference,
    DelegatedStakesInfo,
    SignedWithdrawDelegatedStake,
    SignedCreateDelegatedStake,
    NodeCollateralsInfo,
    SignedWithdrawNodeCollateral,
    SignedCreateNodeCollateral,
)


def _handle_metrics(response: str) -> List[Dict[str, Any]]:
    """
    Parse Prometheus metrics output from a text response.

    :param response: Prometheus text output.
    :return: List of dictionaries with metric details.
    """
    metrics = []
    for family in text_string_to_metric_families(response):
        for sample in family.samples:
            metrics.append(
                {
                    "name": sample[0],
                    "labels": sample[1],
                    "value": sample[2],
                    "type": family.type,
                }
            )
    return metrics


class L0Api:
    def __init__(
        self, host: str, client: Optional[RESTClient] = None, timeout: int = 25
    ):
        if not host:
            logging.warning("L0Api | ML0 :: Layer 0 API object not set.")
        self._host = host
        self.client = client or HttpxClient(timeout=timeout)

    def config(self, host: Optional[str] = None, client: Optional[RESTClient] = None):
        """Reconfigure the RestAPIClient."""
        if host:
            self._host = host
        if client:
            self.client = client

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Dict[str, Any] = None,
        payload: Dict[str, Any] = None,
    ) -> Union[Dict, List, str]:
        """
        Helper function to create a new RestAPIClient instance and make a request.
        """
        async with RestAPIClient(base_url=self._host, client=self.client) as client:
            return await client.request(
                method=method, endpoint=endpoint, params=params, payload=payload
            )

    async def get_cluster_info(self) -> List[PeerInfo]:
        result = await self._make_request("GET", "/cluster/info")
        return PeerInfo.process_cluster_peers(data=result)

    async def get_metrics(self) -> List[Dict[str, Any]]:
        """
        Get metrics from the L0 endpoint.

        :return: Prometheus output as a list of dictionaries.
        """
        response = await self._make_request("GET", "/metrics")
        return _handle_metrics(response)

    async def get_total_supply(self) -> TotalSupply:
        result = await self._make_request("GET", "/dag/total-supply")
        return TotalSupply(**result)

    async def get_address_balance(self, address: str) -> Balance:
        result = await self._make_request("GET", f"/dag/{address}/balance")
        return Balance(**result, meta=result.get("meta"))

    async def get_latest_snapshot(self) -> SignedGlobalIncrementalSnapshot:
        result = await self._make_request("GET", "/global-snapshots/latest")
        return SignedGlobalIncrementalSnapshot(**result)

    async def get_latest_snapshot_ordinal(self) -> Ordinal:
        result = await self._make_request("GET", "/global-snapshots/latest/ordinal")
        return Ordinal(**result)

    async def post_state_channel_snapshot(self, address: str, snapshot: dict):
        # TODO: How to test this?
        return await self._make_request(
            "POST", f"/state-channel/{address}/snapshot", payload=snapshot
        )

    async def get_delegated_stake_last_reference(
        self, address: str
    ) -> TransactionReference:
        result = await self._make_request(
            "GET", f"/delegated-stakes/last-reference/{address}"
        )
        return await TransactionReference(**result)

    async def get_delegated_stakes_info(self, address) -> DelegatedStakesInfo:
        result = await self._make_request("GET", f"/delegated-stakes/{address}/info")
        return DelegatedStakesInfo(**result)

    async def put_delegated_stake_withdrawal(self, tx: SignedWithdrawDelegatedStake):
        return await self._make_request(
            "PUT", "/delegated-stakes", payload=tx.model_dump()
        )

    async def post_delegated_stake(self, tx: SignedCreateDelegatedStake):
        return await self._make_request(
            "POST", "/delegated-stakes", payload=tx.model_dump()
        )

    async def get_node_collateral_last_reference(
        self, address: str
    ) -> TransactionReference:
        result = await self._make_request(
            "GET", f"/node-collateral/last-reference/{address}"
        )
        return TransactionReference(**result)

    async def get_node_collaterals_info(self, address) -> NodeCollateralsInfo:
        result = await self._make_request("GET", f"/node-collateral/{address}/info")
        return NodeCollateralsInfo(**result)

    async def put_node_collateral_withdrawal(self, tx: SignedWithdrawNodeCollateral):
        return await self._make_request(
            "PUT", "/node-collateral", payload=tx.model_dump()
        )

    async def post_node_collateral(self, tx: SignedCreateNodeCollateral):
        return await self._make_request(
            "POST", "/node-collateral", payload=tx.model_dump()
        )
