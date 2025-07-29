
import flwr as fl
from flwr.server.strategy import FedAvg
from flwr.server.server import ServerConfig
from typing import  Optional, Any
from MEDfl.rw.strategy import Strategy

class FederatedServer:
    """
    Wrapper for launching a Flower federated-learning server,
    using a Strategy instance as its strategy attribute.
    """
    def __init__(
        self,
        host: str = "0.0.0.0",
        port: int = 8080,
        num_rounds: int = 3,
        strategy: Optional[Strategy] = None,
        certificates: Optional[Any] = None,
    ):
        self.server_address = f"{host}:{port}"
        self.server_config = ServerConfig(num_rounds=num_rounds)
        # If no custom strategy provided, use default
        self.strategy_wrapper = strategy or Strategy()
        # Build the actual Flower strategy object
        self.strategy_wrapper.create_strategy()
        if self.strategy_wrapper.strategy_object is None:
            raise ValueError("Strategy object not initialized. Call create_strategy() first.")
        self.strategy = self.strategy_wrapper.strategy_object
        self.certificates = certificates

    def start(self) -> None:
        """
        Start the Flower server with the configured strategy.
        """
        print(f"Starting Flower server on {self.server_address} with strategy {self.strategy_wrapper.name}")
        fl.server.start_server(
            server_address=self.server_address,
            config=self.server_config,
            strategy=self.strategy,
            certificates=self.certificates,
        )