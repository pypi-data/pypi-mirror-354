import abc
import json
import signal
import sys
from vyomcloudbridge.utils.logger_setup import setup_logger
from vyomcloudbridge.utils.configs import Configs
import os


class AbcListener(abc.ABC):
    """
    Abstract base class for listener services that can receive and process incoming messages.
    All listener implementations should inherit from this class.
    """

    def __init__(self, multi_thread: bool = False):
        # compulsory fields
        self.name = ""
        self.combine_by_target_id = False

        # class specific
        self.is_running = False
        self.multi_thread = multi_thread
        self.logger = setup_logger(
            name=self.__class__.__module__ + "." + self.__class__.__name__,
            show_terminal=False,
        )
        self.machine_config = Configs.get_machine_config()
        self.machine_id = self.machine_config.get("machine_id", "-") or "-"
        self._setup_signal_handlers()

    def _setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown."""

        def signal_handler(sig, frame):
            self.logger.info(
                f"Received signal {sig}, shutting down {self.__class__.__name__}..."
            )
            self.stop()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

    def get_topic_info(
        self, name
    ):
        """
        @brief Retrieves the data type and normalized name of a topic from a JSON file.

        This method searches for a topic by name in a JSON file containing topic definitions.
        If the topic is found, it logs the discovery and returns the topic's data type and the
        normalized (lowercase) name. If not found, returns (None, None).

        @param name (str): The name of the topic to search for.
        @param json_path (str, optional): Path to the JSON file containing topic definitions.
            Defaults to "../../utils/communication_topics.json".

        @return tuple: A tuple containing:
            - data_type (str or None): The data type of the found topic, or None if not found.
            - normalized_name (str or None): The lowercase name of the found topic, or None if not found.
        """
        
        json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../vyomcloudbridge/utils/communication_topics.py'))
        self.logger.info(f"Loading topic info from {json_path}")
        
        with open(json_path, "r") as f:
            topic_list = json.load(f)

        for topic in topic_list:
            if topic["name"].lower() == name.lower():
                self.logger.info(
                    f"Found topic '{name}' with data type '{topic['data_type']}'"
                )

                return topic["data_type"], name.lower()

        return None, None


    def handle_message(self, typ, msg, destination_id, source_id):
        """
        @brief Handles incoming messages and processes them based on the destination ID.
        This method logs the receipt of a message, checks if the message is intended for the current machine,
        and either processes the message or passes it to another handler.
        @param typ The type or topic name of the received message.
        @param msg The message payload.
        @param destination_id The identifier of the intended recipient machine.
        @param source_id The identifier of the source machine that sent the message.
        If the destination ID matches the current machine's ID, the message is processed and published.
        Otherwise, the message is ignored or forwarded as needed.
        @exception Exception Logs any exceptions that occur during message handling.
        """

        self.logger.info(
            f"Received message for destination_id {destination_id}: self.machine_id {self.machine_id}"
        )

        self.logger.info(
            f"type for self.machine_id:{type(self.machine_id)} and type for destination_id: {type(destination_id)} "
        )
        if destination_id == self.machine_id:
            self.logger.info(
                f"Received message for machine {self.machine_id}: {msg} with ros_topic {typ}"
            )
            try:
                # Log the received message
                self.logger.info(f"Received message from topic name'{typ}': {msg}")

            except Exception as e:
                self.logger.error(f"Error in handle_message of AbcListener: {str(e)}")
        else:
            # push it to vyom sender
            pass

    @abc.abstractmethod
    def start(self):
        """
        Start the listener service to begin receiving incoming messages.
        Must be implemented by subclasses.

        This method should:
        - Start any background processes for listening to incoming messages
        - Set up any required connections
        - Set is_running to True when the service is successfully started
        - Handle any initial setup required for message processing
        """
        pass

    @abc.abstractmethod
    def stop(self):
        """
        Stop the listener service and and call cleanup.
        Must be implemented by subclasses.

        This method should:
        - Stop any background processes for listening to incoming messages
        - is_running to False, and call cleanup
        - Set is_running to False when the service is successfully stopped
        -
        """
        self.cleanup()
        pass

    def is_healthy(self):
        """
        Check if the listener service is healthy.
        Can be overridden by subclasses to implement specific health checks.

        Returns:
            bool: True if the listener is healthy and operational, False otherwise
        """
        return self.is_running

    @abc.abstractmethod
    def cleanup(self):
        """
        Release any resources, connection being used by this service class
        """
        try:
            pass
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")

    def __del__(self):
        """Destructor called by garbage collector to ensure resources are cleaned up, when object is about to be destroyed"""
        try:
            self.logger.error(
                "Destructor called by garbage collector to cleanup AbcListener"
            )
            self.stop()
        except Exception as e:
            # Cannot log here as logger might be destroyed already
            pass
