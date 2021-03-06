import logging

from infrastructure.consul.consul_handler import ConsulHandler

logging.basicConfig(level=logging.INFO)

import grpc
import signal
from concurrent import futures
from infrastructure.mysql import sql
from application.servicers import register_outing_servicers


class gRPCApplication:
    def __init__(self, config, consul):
        self._consul: ConsulHandler = consul
        self._config = config
        self._app = grpc.server(futures.ThreadPoolExecutor(max_workers=self._config.max_workers))
        signal.signal(signal.SIGTERM, self.stop_sig_handler)

        self._logger = logging.getLogger(__name__)

        self._app.add_insecure_port(self._config.address)
        self.register_db()
        self.register_servicers()

    def register_db(self):
        sql.base.metadata.create_all(sql.engine)

    def register_servicers(self):
        register_outing_servicers(self._app, self._consul)

    def stop(self):
        self._consul.deregister_consul()
        self._logger.info("* Service is down")

    def serve(self):
        try:
            self._logger.info(f"* Serve gRPC Application ..")
            self._app.start()
            self._consul.register_consul(self._config.port)
            self._consul.update_address()
            self._logger.info(f"* gRPC Application is served in {self._config.address}")
            self._app.wait_for_termination()
        except Exception as e:
            self.stop()

    def stop_sig_handler(self, signum, frame):
        self.stop()
