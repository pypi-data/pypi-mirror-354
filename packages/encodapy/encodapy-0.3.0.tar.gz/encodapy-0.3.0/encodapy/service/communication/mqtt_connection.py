"""
Description: This file contains the class MqttConnection,
which is used to store the connection parameters for the MQTT broker.
Author: Maximilian Beyer
"""

import json
import os
from datetime import datetime
from typing import Optional, Union

import paho.mqtt.client as mqtt
from loguru import logger
from paho.mqtt.enums import CallbackAPIVersion

from encodapy.config import (
    ConfigModel,
    DataQueryTypes,
    DefaultEnvVariables,
    InputModel,
    Interfaces,
    OutputModel,
)
from encodapy.utils.error_handling import ConfigError, NotSupportedError
from encodapy.utils.models import (
    AttributeModel,
    InputDataAttributeModel,
    InputDataEntityModel,
    OutputDataEntityModel,
)


class MqttConnection:
    """
    Class for the connection to a MQTT broker.
    Only a helper class.
    """

    def __init__(self) -> None:
        self.mqtt_params = {}
        # make ConfigModel-Class available in the MqttConnection-Class
        self.config: Optional[ConfigModel] = None
        self.mqtt_client: Optional[mqtt.Client] = None
        self._mqtt_loop_running = False
        # mqtt_message_store is filled by on_messages
        # messages are stored with topic as key and payload as value
        # dict is used to get the data in the get_data_from_mqtt function
        self.mqtt_message_store = {}

    def load_mqtt_params(self) -> None:
        """
        Function to load the MQTT parameters from the environment variables
        or use the default values from the DefaultEnvVariables class.
        """
        # the IP of the broker
        self.mqtt_params["broker"] = os.environ.get(
            "MQTT_BROKER", DefaultEnvVariables.MQTT_BROKER.value
        )
        # the port of the broker
        self.mqtt_params["port"] = int(
            os.environ.get("MQTT_PORT", DefaultEnvVariables.MQTT_PORT.value)
        )
        # the username to connect to the broker
        self.mqtt_params["username"] = os.environ.get(
            "MQTT_USERNAME", DefaultEnvVariables.MQTT_USERNAME.value
        )
        # the password to connect to the broker
        self.mqtt_params["password"] = os.environ.get(
            "MQTT_PASSWORD", DefaultEnvVariables.MQTT_PASSWORD.value
        )
        # the topic prefix to use for the topics
        self.mqtt_params["topic_prefix"] = os.environ.get(
            "MQTT_TOPIC_PREFIX", DefaultEnvVariables.MQTT_TOPIC_PREFIX.value
        )

        if not self.mqtt_params["broker"] or not self.mqtt_params["port"]:
            raise ConfigError("MQTT broker and port must be set")

    def prepare_mqtt_connection(self) -> None:
        """
        Function to prepare the MQTT connection
        """
        # initialize the MQTT client
        if not self.mqtt_client:
            self.mqtt_client = mqtt.Client(
                callback_api_version=CallbackAPIVersion.VERSION2
            )

        # set username and password for the MQTT client
        self.mqtt_client.username_pw_set(
            self.mqtt_params["username"], self.mqtt_params["password"]
        )

        # try to connect to the MQTT broker
        try:
            self.mqtt_client.connect(
                self.mqtt_params["broker"], self.mqtt_params["port"]
            )
        except Exception as e:
            raise ConfigError(
                f"Could not connect to MQTT broker {self.mqtt_params['broker']}:"
                f"{self.mqtt_params['port']} with given login information - {e}"
            ) from e

        # prepare the message store
        self.prepare_mqtt_message_store()

        # subscribe to all topics in the message store
        self.subscribe_to_message_store_topics()

        # start the MQTT client loop
        self.start_mqtt_client()

    def prepare_mqtt_message_store(self) -> None:
        """
        Function to prepare the MQTT message store for all in- and outputs
        (means subscribes to controller itself) and set the default values
        """
        if self.mqtt_message_store:
            logger.warning("MQTT message store is not empty and will be overwritten.")

        # check if the config is set
        if self.config is None:
            raise ConfigError(
                "ConfigModel is not set. Please set the config before using the MQTT connection."
            )

        # set the message store with default values for all mqtt attributes in config
        for entity in self.config.inputs + self.config.outputs:
            if entity.interface == Interfaces.MQTT:
                for attribute in entity.attributes:
                    # set the topic for the attribute
                    topic = self.assemble_topic_parts(
                        [
                            self.mqtt_params["topic_prefix"],
                            entity.id_interface,
                            attribute.id_interface,
                        ]
                    )

                    if topic in self.mqtt_message_store:
                        logger.warning(
                            f"Topic {topic} from {entity.id} already exists in message store, "
                            f"overwriting it with new value. "
                            f"This should not happen, check your configuration. "
                        )

                    # set the default value for the attribute
                    if hasattr(attribute, "value"):
                        value = attribute.value
                    else:
                        value = None

                    self.mqtt_message_store[topic] = value

    def assemble_topic_parts(self, parts: list[str]) -> str:
        """
        Function to build a topic from a list of strings.
        Ensures that the resulting topic is correctly formatted with exactly one '/' between parts.

        Args:
            parts (list[str]): List of strings to be joined into a topic.

        Returns:
            str: The correctly formatted topic.

        Raises:
            ValueError: If the resulting topic is not correctly formatted.
        """
        if not parts:
            raise ValueError("The list of parts cannot be empty.")

        # drop a part if it is None or empty
        parts = [part for part in parts if part not in (None, "")]

        # Join the parts with a single '/',
        # stripping leading/trailing slashes from each part to avoid double slashes in the topic
        topic = "/".join(part.strip("/") for part in parts)

        return topic

    def publish(self, topic, payload) -> None:
        """
        Function to publish a message to a topic
        """
        if not self.mqtt_client:
            raise NotSupportedError(
                "MQTT client is not prepared. Call prepare_mqtt_connection() first."
            )
        self.mqtt_client.publish(topic, payload)

    def subscribe(self, topic) -> None:
        """
        Function to subscribe to a topic
        """
        if not self.mqtt_client:
            raise NotSupportedError(
                "MQTT client is not prepared. Call prepare_mqtt_connection() first."
            )
        self.mqtt_client.subscribe(topic)

    def subscribe_to_message_store_topics(self) -> None:
        """
        Function to subscribe to all topics in the message store.
        """
        if not self.mqtt_message_store:
            raise NotSupportedError(
                "MQTT message store is initialized, but empty. Cannot subscribe to topics."
            )

        for topic in self.mqtt_message_store:
            self.subscribe(topic)
            logger.debug(f"Subscribed to topic: {topic}")

    def on_message(self, client, userdata, message):
        """
        Callback function for received messages, stores the decoded message in the message store
        """
        if not hasattr(self, "mqtt_message_store"):
            raise NotSupportedError(
                "MQTT message store is not initialized. Call prepare_mqtt_connection() first."
            )
        # decode the message payload
        try:
            storage_value = message.payload.decode("utf-8")
        except UnicodeDecodeError as e:
            logger.error(f"Failed to decode message payload: {e}")
            return
        # store it in the message store
        self.mqtt_message_store[message.topic] = storage_value
        logger.debug(
            f"MQTT storage received message on topic {message.topic}: {storage_value}"
        )

    def start_mqtt_client(self):
        """
        Function to hang in on_message hook and start the MQTT client loop
        """
        if not hasattr(self, "mqtt_client") or self.mqtt_client is None:
            raise NotSupportedError(
                "MQTT client is not prepared. Call prepare_mqtt_connection() first."
            )

        if hasattr(self, "_mqtt_loop_running") and self._mqtt_loop_running:
            raise NotSupportedError("MQTT client loop is already running.")

        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.loop_start()
        self._mqtt_loop_running = True  # state variable to check if the loop is running

    def stop_mqtt_client(self):
        """
        Function to stop the MQTT client loop and clean up resources
        """
        if isinstance(self.mqtt_client, mqtt.Client) and self._mqtt_loop_running:
            self.mqtt_client.loop_stop()
            self.mqtt_client.disconnect()
            self._mqtt_loop_running = False

    def get_data_from_mqtt(
        self,
        method: DataQueryTypes,
        entity: InputModel,
    ) -> Union[InputDataEntityModel, None]:
        """
        Function to get the data from the MQTT broker

        Args:
            method (DataQueryTypes): Keyword for type of query
            entity (InputModel): Input entity

        Returns:
            Union[InputDataEntityModel, None]: Model with input data or None if no data available
        """
        if not hasattr(self, "mqtt_message_store"):
            raise NotSupportedError(
                "MQTT message store is not initialized. Call prepare_mqtt_connection() first."
            )

        attributes_values = []

        for attribute in entity.attributes:
            # Construct the topic for the attribute
            topic = self.assemble_topic_parts(
                [
                    self.mqtt_params["topic_prefix"],
                    entity.id_interface,
                    attribute.id_interface,
                ]
            )

            # check if the topic is in the message store
            if topic not in self.mqtt_message_store:
                # If the topic is not in the message store, mark the data as unavailable
                attributes_values.append(
                    InputDataAttributeModel(
                        id=attribute.id,
                        data=None,
                        data_type=attribute.type,
                        data_available=False,
                        latest_timestamp_input=None,
                        unit=None,
                    )
                )
                continue

            # extract the data from message payload
            message_payload = self.mqtt_message_store[topic]
            try:
                data = self._extract_payload_value(message_payload)

                attributes_values.append(
                    InputDataAttributeModel(
                        id=attribute.id,
                        data=data,
                        data_type=attribute.type,
                        data_available=True,
                        latest_timestamp_input=None,
                        unit=None,  # TODO MB: Add unit handling if necessary
                    )
                )
            except (json.JSONDecodeError, KeyError):
                # Handle invalid or missing data in the payload
                # TODO MB: check if error handling is working correctly
                logger.error(
                    f"Invalid payload for topic {topic}: {message_payload}. "
                    f"Setting data as None and unavailable."
                )

                attributes_values.append(
                    InputDataAttributeModel(
                        id=attribute.id,
                        data=None,
                        data_type=attribute.type,
                        data_available=False,
                        latest_timestamp_input=None,
                        unit=None,
                    )
                )

        return InputDataEntityModel(id=entity.id, attributes=attributes_values)

    def send_data_to_mqtt(
        self,
        output_entity: OutputModel,
        output_attributes: list[AttributeModel],
        # output_commands: list[CommandModel],
    ) -> None:
        """
        Function to send the output data to MQTT (publish the data to the MQTT broker)

        Args:
            - output_entity: OutputModel with the output entity
            - output_attributes: list with the output attributes
            # - output_commands: list with the output commands
        """
        if not hasattr(self, "mqtt_client"):
            raise NotSupportedError(
                "MQTT client is not prepared. Call prepare_mqtt_connection() first."
            )

        # check if the config is set
        if self.config is None:
            raise ConfigError(
                "ConfigModel is not set. Please set the config before using the MQTT connection."
            )

        # publish the data to the MQTT broker
        for attribute in output_attributes:
            topic = self.assemble_topic_parts(
                [
                    self.mqtt_params["topic_prefix"],
                    output_entity.id_interface,
                    attribute.id_interface,
                ]
            )
            payload = attribute.value
            self.publish(topic, payload)
            logger.debug(f"Published to topic {topic}: {payload}")

    def _extract_payload_value(self, payload) -> Union[float, bool]:
        """
        Function to extract data from the payload as needed.
        """
        # Check if the payload is a JSON string and try to parse it
        if isinstance(payload, str):
            try:
                payload = json.loads(payload)
            except json.JSONDecodeError:
                # If the payload is not a valid JSON but a string, split first string part as value
                # (workaround for cases where payload is a string from number and unit, e.g. 22 °C)
                # Added strip() to remove leading/trailing spaces (e.g., " 6552.0 h")
                payload = payload.strip().split(" ")[0]

        # If the payload is a valid JSON string or dict, extract the value from it if possible
        if isinstance(payload, dict):
            if "value" in payload.keys():
                # Extract the value from the dictionary
                value = payload["value"]
            else:
                raise ValueError(
                    f"Invalid payload format: 'value' key not found in payload {payload}"
                )
        # If the payload itself is a number, boolean or string, use it directly
        elif isinstance(payload, (float, int, str, bool)):
            value = payload
        else:
            raise ValueError(f"Invalid payload format: {type(payload)}")

        # if remaining value is bool, return it
        if isinstance(value, bool):
            return value

        # else try to convert it to float
        try:
            return float(value)
        except ValueError as exc:
            raise ValueError(
                f"Invalid data type for payload value: {type(value)}"
            ) from exc

    def _get_last_timestamp_for_mqtt_output(
        self, output_entity: OutputModel
    ) -> tuple[OutputDataEntityModel, Union[datetime, None]]:
        """
        Function to get the latest timestamps of the output entity from a MQTT message, if exitst

        Args:
            output_entity (OutputModel): Output entity

        Returns:
            tuple[OutputDataEntityModel, Union[datetime, None]]:
                - OutputDataEntityModel with timestamps for the attributes
                - the latest timestamp of the output entity for the attribute
                with the oldest value (None if no timestamp is available)
        TODO:
            - is it really nessesary to get a timestamp for MQTT-calculations /
            during calculation time is set to input_time
        """

        output_id = output_entity.id_interface

        timestamps = []
        timestamp_latest_output = None

        return (
            OutputDataEntityModel(id=output_id, attributes_status=timestamps),
            timestamp_latest_output,
        )
