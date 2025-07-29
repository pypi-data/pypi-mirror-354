#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
"""
ON1Builder – Chain Worker
=========================
Handles operations for a specific blockchain: init, monitoring, t            self.safety_guard = SafetyGuard(
                web3=self.web3,
                config=self.config,
                account=self.account,
                external_api_manager=self.api_manager,
                main_orchestrator=self.main_orchestrator,
            )ement.
License: MIT
"""

from __future__ import annotations

import asyncio
import os
import time
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Set

from eth_account.account import Account
from web3 import AsyncWeb3
from web3.middleware import ExtraDataToPOAMiddleware
from web3.providers import AsyncHTTPProvider

from ..config.settings import GlobalSettings
from ..integrations.external_apis import ExternalAPIManager
from .nonce_manager import NonceManager

# Break circular dependency
if TYPE_CHECKING:
    from .transaction_manager import TransactionManager

from ..engines.safety_guard import SafetyGuard
from ..monitoring.market_data_feed import MarketDataFeed
from ..monitoring.txpool_scanner import TxPoolScanner
from ..persistence.db_interface import DatabaseInterface, get_db_manager
from ..utils.container import Container, get_container
from ..utils.logging_config import get_logger
from ..utils.notification_service import get_notification_manager

logger = get_logger(__name__)


class ChainWorker:
    """Manages a single‐chain lifecycle: init, start, stop, metrics, monitoring."""

    def __init__(
        self,
        chain_cfg: Dict[str, Any],
        global_cfg: GlobalSettings,
        main_orchestrator: Optional[Any] = None,  # Add MainOrchestrator reference
    ) -> None:
        self.chain_cfg = chain_cfg
        self.config: GlobalSettings = global_cfg
        self.chain_id: str = str(chain_cfg.get("CHAIN_ID", "unknown"))
        self.chain_name: str = chain_cfg.get("CHAIN_NAME", f"chain-{self.chain_id}")
        self.main_orchestrator = main_orchestrator  # Store reference to MainOrchestrator

        # Endpoints
        self.http_endpoint: str = chain_cfg.get("HTTP_ENDPOINT", "")
        self.websocket_endpoint: str = chain_cfg.get("WEBSOCKET_ENDPOINT", "")
        self.ipc_endpoint: str = chain_cfg.get("IPC_ENDPOINT", "")

        # Wallet
        self.wallet_key: Optional[str] = chain_cfg.get("WALLET_KEY") or os.getenv(
            "WALLET_KEY"
        )
        self.wallet_address: Optional[str] = chain_cfg.get("WALLET_ADDRESS")

        # Components
        self.web3: Optional[AsyncWeb3] = None
        self.account: Optional[Any] = None  # eth_account.Account object
        self.api_config: Optional[ExternalAPIManager] = None
        self.db: Optional[DatabaseInterface] = None
        self.nonce_manager: Optional[NonceManager] = None
        self.safety_guard: Optional[SafetyGuard] = None
        self.market_data_feed: Optional[MarketDataFeed] = None
        self.txpool_scanner: Optional[TxPoolScanner] = None
        self.transaction_manager: Optional[TransactionManager] = None
        self.notification_manager = None

        # Dependency container for component management
        self.container: Container = get_container()
        self._closed_components: Set[str] = set()

        # State
        self.initialized: bool = False
        self.running: bool = False
        self._tasks: List[asyncio.Task[Any]] = []
        self._stop_event: asyncio.Event = asyncio.Event()

        # Metrics
        self.metrics: Dict[str, Any] = {
            "chain_id": self.chain_id,
            "chain_name": self.chain_name,
            "wallet_balance_eth": 0.0,
            "last_gas_price_gwei": 0.0,
            "last_block_number": 0,
            "transaction_count": 0,
            "total_profit_eth": 0.0,
            "total_gas_spent_eth": 0.0,
            "health_status": "initializing",
        }
        self._last_metrics_ts = time.time()

    async def initialize(self) -> bool:
        """Initialize Web3, account, configs, DB, cores and monitors."""
        try:
            logger.info(f"[{self.chain_name}] Initializing ChainWorker")
            self.metrics["health_status"] = "initializing"

            # — Web3 —
            if not await self._init_web3():
                self.metrics["health_status"] = "error_web3"
                return False

            # — Account —
            if not self.wallet_key:
                logger.error("No WALLET_KEY available")
                self.metrics["health_status"] = "error_account"
                return False
            self.account = Account.from_key(self.wallet_key)
            if (
                self.wallet_address
                and self.account
                and self.wallet_address.lower() != self.account.address.lower()
            ):
                logger.warning("Configured WALLET_ADDRESS differs from key")

            # Register our account in the container
            self.container.register(f"account_{self.chain_id}", self.account)
            self.container.register(f"web3_{self.chain_id}", self.web3)

            # — External APIs —
            if hasattr(self.config, 'api') and self.config.api is not None:
                self.api_manager = ExternalAPIManager(self.config.api)
                await self.api_manager.initialize()
                self.container.register(f"api_manager_{self.chain_id}", self.api_manager)
            else:
                self.api_manager = None
                logger.warning(f"[{self.chain_name}] No API settings found, ExternalAPIManager not initialized")

            # — Notifications —
            # Use shared notification manager if available
            if (
                self.main_orchestrator
                and hasattr(self.main_orchestrator, "components")
                and "notification_manager" in self.main_orchestrator.components
            ):
                self.notification_manager = self.main_orchestrator.components[
                    "notification_manager"
                ]
                logger.debug("Using shared notification manager from MainOrchestrator")
            else:
                self.notification_manager = get_notification_manager(
                    self.config, self.main_orchestrator
                )
                logger.debug("Initialized new notification manager")

            # — Persistence —
            # Use provided database manager if available, otherwise initialize a new one
            if (
                self.main_orchestrator
                and hasattr(self.main_orchestrator, "components")
                and "db_manager" in self.main_orchestrator.components
            ):
                self.db = self.main_orchestrator.components["db_manager"]
                logger.debug("Using shared database manager from MainOrchestrator")
            else:
                # Initialize or retrieve singleton DatabaseManager synchronously
                self.db = get_db_manager(self.config)
                # Ensure database schema is initialized
                try:
                    await self.db.initialize()
                except Exception as e:
                    logger.warning(f"DatabaseManager initialize error: {e}")
                logger.debug("Initialized new database manager")
            self.container.register(f"db_manager_{self.chain_id}", self.db)

            # — ABI Registry —
            self.abi_registry = None
            if (
                self.main_orchestrator
                and hasattr(self.main_orchestrator, "components")
                and "abi_registry" in self.main_orchestrator.components
            ):
                self.abi_registry = self.main_orchestrator.components["abi_registry"]
                logger.debug("Using shared ABI registry from MainOrchestrator")
            self.container.register(f"abi_registry_{self.chain_id}", self.abi_registry)

            # — Cores & Monitors —
            # Ensure web3 is initialized before passing to components
            if self.web3 is None:
                raise RuntimeError("Web3 connection must be established before initializing components")
                
            self.nonce_manager = NonceManager(
                web3=self.web3, configuration=self.config, main_orchestrator=self.main_orchestrator
            )
            await self.nonce_manager.initialize()
            self.container.register(f"nonce_core_{self.chain_id}", self.nonce_manager)

            self.safety_guard = SafetyGuard(
                web3=self.web3,
                config=self.config,
                account=self.account,
                external_api_manager=self.api_config,
                main_orchestrator=self.main_orchestrator,
            )
            await self.safety_guard.initialize()
            self.container.register(f"safety_net_{self.chain_id}", self.safety_guard)

            # Initialize market monitor
            self.market_data_feed = MarketDataFeed(
                web3=self.web3,
                config=self.config,
                api_config=self.config.api,
            )
            await self.market_data_feed.initialize()
            self.container.register(
                f"market_monitor_{self.chain_id}", self.market_data_feed
            )

            # Initialize txpool monitor
            tokens = self.config.monitored_tokens
            self.txpool_scanner = TxPoolScanner(
                web3=self.web3,
                safety_net=self.safety_guard,
                nonce_core=self.nonce_manager,
                api_config=self.api_config,
                monitored_tokens=tokens,
                configuration=self.config,
                market_monitor=self.market_data_feed,
            )
            await self.txpool_scanner.initialize()
            self.container.register(
                f"txpool_monitor_{self.chain_id}", self.txpool_scanner
            )

            # Import here to avoid circular dependency
            from .transaction_manager import TransactionManager

            # Initialize transaction core with both monitors
            # At this point, web3 and account should be initialized
            assert self.web3 is not None, "web3 should be initialized"
            assert self.account is not None, "account should be initialized"
            
            self.transaction_manager = TransactionManager(
                web3=self.web3,
                account=self.account,
                configuration=self.config,
                nonce_manager=self.nonce_manager,
                safety_guard=self.safety_guard,
                external_api_manager=self.api_config,
                market_monitor=self.market_data_feed,
                txpool_monitor=self.txpool_scanner,
                chain_id=int(self.chain_id) if self.chain_id.isdigit() else 1,
                main_orchestrator=self.main_orchestrator,
            )
            await self.transaction_manager.initialize()
            self.container.register(
                f"transaction_core_{self.chain_id}", self.transaction_manager
            )

            # — Warm‐up metrics —
            await self.get_wallet_balance()
            await self.get_gas_price()

            self.initialized = True
            self.metrics["health_status"] = "initialized"
            logger.info(f"[{self.chain_name}] Initialization complete")

            # Notify about successful initialization
            try:
                if self.notification_manager:
                    await self.notification_manager.send_notification(
                        f"ChainWorker for {self.chain_name} (ID: {self.chain_id}) initialized successfully",
                        level="INFO",
                        details={
                            "wallet": self.account.address,
                            "balance": self.metrics["wallet_balance_eth"],
                            "gas_price": self.metrics["last_gas_price_gwei"],
                        },
                    )
            except Exception as e:
                logger.warning(f"Failed to send initialization notification: {e}")

            return True

        except Exception as e:
            logger.exception(f"[{self.chain_name}] Initialization failed: {e}")

            # Notify about failed initialization
            try:
                if self.notification_manager:
                    await self.notification_manager.send_alert(
                        f"ChainWorker for {self.chain_name} (ID: {self.chain_id}) initialization failed",
                        level="ERROR",
                        details={
                            "wallet": getattr(self.account, "address", "unknown"),
                            "error": str(e),
                        },
                    )
            except Exception:
                pass  # Don't let notification error hide the original error

            self.metrics["health_status"] = "error"
            return False

    async def start(self) -> None:
        """Start monitors and periodic tasks."""
        if not self.initialized:
            logger.error("Cannot start before initialize()")
            return
        if self.running:
            logger.warning("Already running")
            return

        logger.info(f"[{self.chain_name}] Starting worker")
        self.running = True
        self._stop_event.clear()
        self.metrics["health_status"] = "starting"

        try:
            # Launch txpool + market monitors
            if self.txpool_scanner:
                self._tasks.append(
                    asyncio.create_task(
                        self.txpool_scanner.start_monitoring(), name=f"TXM_{self.chain_id}"
                    )
                )
            if self.market_data_feed:
                self._tasks.append(
                    asyncio.create_task(
                        self.market_data_feed.schedule_updates(), name=f"MM_{self.chain_id}"
                    )
                )

            # Launch heartbeat task
            self._tasks.append(
                asyncio.create_task(self._run_heartbeat(), name=f"HB_{self.chain_id}")
            )

            # Notify about successful start
            if self.notification_manager:
                await self.notification_manager.send_notification(
                    f"ChainWorker for {self.chain_name} (ID: {self.chain_id}) started",
                    level="INFO",
                )

            self.metrics["health_status"] = "running"
        except Exception as e:
            logger.exception(f"Error starting ChainWorker: {e}")
            self.metrics["health_status"] = "error_starting"

            # Notify about failed start
            if self.notification_manager:
                await self.notification_manager.send_alert(
                    f"Failed to start ChainWorker for {self.chain_name}",
                    level="ERROR",
                    details={"error": str(e)},
                )

    async def stop(self) -> None:
        """Stop all components and tasks."""
        if not self.running:
            return

        logger.info(f"[{self.chain_name}] Stopping worker")
        self.running = False
        self._stop_event.set()
        self.metrics["health_status"] = "stopping"

        try:
            # Cancel all background tasks
            for task in self._tasks:
                if not task.done() and not task.cancelled():
                    logger.debug(f"Cancelling task: {task.get_name()}")
                    task.cancel()

            # Wait for tasks to complete (with timeout)
            if self._tasks:
                try:
                    await asyncio.wait(self._tasks, timeout=10.0)
                except asyncio.TimeoutError:
                    logger.warning("Timeout waiting for tasks to cancel")
            self._tasks.clear()

            # Stop components in reverse order of dependencies
            await self._stop_component("txpool_monitor")
            await self._stop_component("market_monitor")
            await self._stop_component("transaction_core")
            await self._stop_component("safety_net")
            await self._stop_component("nonce_core")

            # Close API config at the end since other components might be using it
            await self._stop_component("api_config")

            # Don't stop components from main_orchestrator: they're managed by it

            logger.info(f"[{self.chain_name}] Worker stopped")
            self.metrics["health_status"] = "stopped"

            # Notify about successful stop
            if self.notification_manager and not getattr(
                self.notification_manager, "_from_main_orchestrator", False
            ):
                try:
                    await self.notification_manager.send_notification(
                        f"ChainWorker for {self.chain_name} (ID: {self.chain_id}) stopped",
                        level="INFO",
                    )
                    await self.notification_manager.stop()
                except Exception as e:
                    logger.warning(f"Failed to send stop notification: {e}")

        except Exception as e:
            logger.exception(f"Error during ChainWorker stop: {e}")
            self.metrics["health_status"] = "error_stopping"

    async def _stop_component(self, attr_name: str) -> None:
        """Stop a component if it exists and has a stop method."""
        if attr_name in self._closed_components:
            return

        component = getattr(self, attr_name, None)
        if not component:
            return

        # Check if this is a shared component from main_orchestrator
        is_shared = False
        if self.main_orchestrator and hasattr(self.main_orchestrator, "components"):
            for comp_name, comp in self.main_orchestrator.components.items():
                if component is comp:
                    is_shared = True
                    logger.debug(f"Skipping stop for shared {attr_name} from main_orchestrator")
                    break

        if is_shared:
            self._closed_components.add(attr_name)
            return

        # Stop the component
        try:
            if hasattr(component, "stop") and callable(component.stop):
                logger.debug(f"Stopping {attr_name}")
                if asyncio.iscoroutinefunction(component.stop):
                    await component.stop()
                else:
                    component.stop()
            elif hasattr(component, "close") and callable(component.close):
                logger.debug(f"Closing {attr_name}")
                if asyncio.iscoroutinefunction(component.close):
                    await component.close()
                else:
                    component.close()
        except Exception as e:
            logger.error(f"Error stopping {attr_name}: {e}")

        self._closed_components.add(attr_name)

    async def _run_heartbeat(self) -> None:
        """Periodic heartbeat to check component health and update metrics."""
        interval = self.config.heartbeat_interval
        logger.debug(f"Starting heartbeat at {interval}s interval")

        while not self._stop_event.is_set():
            try:
                await self._update_metrics()
                await self._check_component_health()

                # Check wallet balance and notify if low
                if self.metrics["wallet_balance_eth"] < self.config.min_wallet_balance:
                    if self.notification_manager:
                        await self.notification_manager.send_alert(
                            f"Low wallet balance for {self.chain_name}",
                            level="WARNING",
                            details={
                                "balance": self.metrics["wallet_balance_eth"],
                                "wallet": getattr(self.account, 'address', 'unknown'),
                                "chain_id": self.chain_id,
                            },
                        )
            except Exception as e:
                logger.error(f"Error in heartbeat: {e}")

            try:
                await asyncio.wait_for(self._stop_event.wait(), timeout=interval)
                break  # Stop event was set
            except asyncio.TimeoutError:
                pass  # Continue with next heartbeat

        logger.debug("Heartbeat stopped")

    async def _check_component_health(self) -> bool:
        """Check health status of all components."""
        components_health = {}
        all_healthy = True

        # Check Web3 connection
        try:
            if self.web3 is not None:
                web3_connected = await self.web3.is_connected()
                components_health["web3"] = web3_connected
                if not web3_connected:
                    all_healthy = False
            else:
                components_health["web3"] = False
                all_healthy = False
        except Exception:
            components_health["web3"] = False
            all_healthy = False

        # Check components with is_healthy method
        for name, component in [
            ("txpool_monitor", self.txpool_scanner),
            ("market_monitor", self.market_data_feed),
            ("transaction_core", self.transaction_manager),
            ("safety_net", self.safety_guard),
            ("nonce_core", self.nonce_manager),
        ]:
            if component and hasattr(component, "is_healthy"):
                try:
                    is_healthy = await component.is_healthy()
                    components_health[name] = is_healthy
                    if not is_healthy:
                        all_healthy = False
                except Exception as e:
                    logger.error(f"Error checking health of {name}: {e}")
                    components_health[name] = False
                    all_healthy = False

        self.metrics["components_health"] = components_health
        self.metrics["health_status"] = "healthy" if all_healthy else "degraded"
        return all_healthy

    # — Metrics —

    async def get_wallet_balance(self) -> float:
        """Get wallet balance in ETH."""
        try:
            if self.web3 is None or self.account is None:
                return 0.0
            balance_wei = await self.web3.eth.get_balance(self.account.address)
            balance_eth = float(self.web3.from_wei(balance_wei, "ether"))
            self.metrics["wallet_balance_eth"] = balance_eth
            return balance_eth
        except Exception as e:
            logger.error(f"[{self.chain_name}] Failed to get wallet balance: {e}")
            return 0.0

    async def get_gas_price(self) -> float:
        """Get current gas price in gwei."""
        try:
            if self.web3 is None:
                return 0.0
            gas_wei = await self.web3.eth.gas_price
            gas_gwei = float(self.web3.from_wei(gas_wei, "gwei"))
            self.metrics["last_gas_price_gwei"] = gas_gwei
            return gas_gwei
        except Exception as e:
            logger.error(f"[{self.chain_name}] Failed to get gas price: {e}")
            return 0.0

    async def _update_metrics(self) -> None:
        """Update various metrics for monitoring."""
        now = time.time()
        elapsed = now - self._last_metrics_ts
        self._last_metrics_ts = now

        try:
            # Update block number
            if self.web3 is not None:
                self.metrics["last_block_number"] = await self.web3.eth.block_number
        except Exception:
            pass

        # Update balance and gas price
        await self.get_wallet_balance()
        await self.get_gas_price()

        # Get transaction stats if DB is available
        if self.db and self.account is not None:
            try:
                # Convert chain_id to int for database methods
                chain_id_int = int(self.chain_id) if self.chain_id.isdigit() else None
                
                # Get transaction count using available method
                tx_count = await self.db.get_transaction_count(
                    address=self.account.address, chain_id=chain_id_int
                )
                self.metrics["transaction_count"] = tx_count
                
                # Get profit summary if available
                if hasattr(self.db, "get_profit_summary"):
                    profit_summary = await self.db.get_profit_summary(
                        address=self.account.address, chain_id=chain_id_int
                    )
                    if profit_summary:
                        self.metrics["total_profit_eth"] = profit_summary.get("total_profit", 0.0)
                        self.metrics["total_gas_spent_eth"] = profit_summary.get("total_gas_spent", 0.0)
            except Exception as e:
                logger.warning(f"Failed to get transaction stats: {e}")

        # Get memory usage
        import psutil

        process = psutil.Process(os.getpid())
        self.metrics["memory_usage_mb"] = process.memory_info().rss / 1024 / 1024

        # Check cpu usage
        self.metrics["cpu_percent"] = psutil.cpu_percent(interval=0.1)

        logger.debug(
            f"[{self.chain_name}] Updated metrics: balance={self.metrics['wallet_balance_eth']:.4f} ETH, "
            + f"gas={self.metrics['last_gas_price_gwei']:.2f} gwei, "
            + f"block={self.metrics['last_block_number']}"
        )

    # — Web3 setup & verify —

    async def _init_web3(self) -> bool:
        """Initialize Web3 connection with primary or fallback endpoints."""
        if not any([self.http_endpoint, self.websocket_endpoint, self.ipc_endpoint]):
            logger.error(f"[{self.chain_name}] No endpoints configured")
            return False

        # Check if we already have a Web3 instance from MainCore
        if self.main_orchestrator and hasattr(self.main_orchestrator, "web3") and self.main_orchestrator.web3:
            main_orchestrator_chain_id = await self.main_orchestrator.web3.eth.chain_id
            if str(main_orchestrator_chain_id) == str(self.chain_id):
                logger.info(
                    f"[{self.chain_name}] Using Web3 instance from MainOrchestrator (chain_id={main_orchestrator_chain_id})"
                )
                self.web3 = self.main_orchestrator.web3
                return True

        # Try HTTP endpoint
        if self.http_endpoint:
            try:
                provider = AsyncHTTPProvider(self.http_endpoint)
                web3 = AsyncWeb3(provider)
                chain_id = await web3.eth.chain_id

                # Apply PoA middleware if needed
                if chain_id in [
                    1,
                    3,
                    4,
                    5,
                    42,
                    56,
                    97,
                    100,
                ]:  # Known chains that may need PoA
                    web3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

                logger.info(
                    f"[{self.chain_name}] Connected to HTTP endpoint: {self.http_endpoint}"
                )
                logger.info(f"[{self.chain_name}] Chain ID: {chain_id}")

                if str(chain_id) != str(self.chain_id) and self.chain_id != "unknown":
                    logger.warning(
                        f"[{self.chain_name}] Chain ID mismatch: configured={self.chain_id}, actual={chain_id}"
                    )

                self.web3 = web3
                return True
            except Exception as e:
                logger.error(
                    f"[{self.chain_name}] Failed to connect to HTTP endpoint: {e}"
                )

        # Try WebSocket endpoint
        if self.websocket_endpoint:
            from web3.providers import WebSocketProvider

            try:
                provider = WebSocketProvider(self.websocket_endpoint)
                web3 = AsyncWeb3(provider)
                chain_id = await web3.eth.chain_id

                # Apply PoA middleware if needed
                if chain_id in [1, 3, 4, 5, 42, 56, 97, 100]:
                    web3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

                logger.info(
                    f"[{self.chain_name}] Connected to WebSocket endpoint: {self.websocket_endpoint}"
                )
                logger.info(f"[{self.chain_name}] Chain ID: {chain_id}")

                if str(chain_id) != str(self.chain_id) and self.chain_id != "unknown":
                    logger.warning(
                        f"[{self.chain_name}] Chain ID mismatch: configured={self.chain_id}, actual={chain_id}"
                    )

                self.web3 = web3
                return True
            except Exception as e:
                logger.error(
                    f"[{self.chain_name}] Failed to connect to WebSocket endpoint: {e}"
                )

        # Try IPC endpoint
        if self.ipc_endpoint:
            from web3.providers import AsyncIPCProvider

            try:
                provider = AsyncIPCProvider(self.ipc_endpoint)
                web3 = AsyncWeb3(provider)
                chain_id = await web3.eth.chain_id

                logger.info(
                    f"[{self.chain_name}] Connected to IPC endpoint: {self.ipc_endpoint}"
                )
                logger.info(f"[{self.chain_name}] Chain ID: {chain_id}")

                if str(chain_id) != str(self.chain_id) and self.chain_id != "unknown":
                    logger.warning(
                        f"[{self.chain_name}] Chain ID mismatch: configured={self.chain_id}, actual={chain_id}"
                    )

                self.web3 = web3
                return True
            except Exception as e:
                logger.error(
                    f"[{self.chain_name}] Failed to connect to IPC endpoint: {e}"
                )

        logger.error(f"[{self.chain_name}] Failed to connect to any endpoint")
        return False

    async def _verify_connection(self) -> bool:
        if self.web3 is None:
            logger.error("Web3 connection is None")
            return False
        
        try:
            onchain = await self.web3.eth.chain_id
            if str(onchain) != self.chain_id:
                logger.error(f"Chain ID mismatch: {onchain} != {self.chain_id}")
                return False
            blk = await self.web3.eth.get_block("latest")
            if "number" in blk:
                self.metrics["last_block_number"] = blk["number"]
            return True
        except Exception as e:
            logger.error(f"Web3 connection verify failed: {e}")
            return False
