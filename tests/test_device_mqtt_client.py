"""Tests for DeviceMqttClient service."""

from private_assistant_picture_display_skill.services.device_mqtt_client import DeviceMqttClient


class TestDeviceMqttClientStaticMethods:
    """Tests for DeviceMqttClient static methods."""

    def test_decode_payload_bytes(self) -> None:
        """Test decoding bytes payload."""
        payload = b'{"device_id": "test"}'
        result = DeviceMqttClient.decode_payload(payload)
        assert result == {"device_id": "test"}

    def test_decode_payload_bytearray(self) -> None:
        """Test decoding bytearray payload."""
        payload = bytearray(b'{"key": "value"}')
        result = DeviceMqttClient.decode_payload(payload)
        assert result == {"key": "value"}

    def test_decode_payload_string(self) -> None:
        """Test decoding string payload."""
        payload = '{"key": "value"}'
        result = DeviceMqttClient.decode_payload(payload)
        assert result == {"key": "value"}

    def test_decode_payload_invalid_json(self) -> None:
        """Test decoding invalid JSON payload."""
        payload = b"not valid json"
        result = DeviceMqttClient.decode_payload(payload)
        assert result is None

    def test_extract_device_id_valid_topic(self) -> None:
        """Test extracting device ID from valid status topic."""
        topic = "inky/kitchen/status"
        result = DeviceMqttClient.extract_device_id_from_topic(topic)
        assert result == "kitchen"

    def test_extract_device_id_underscore(self) -> None:
        """Test extracting device ID with underscore."""
        topic = "inky/living_room/status"
        result = DeviceMqttClient.extract_device_id_from_topic(topic)
        assert result == "living_room"

    def test_extract_device_id_invalid_prefix(self) -> None:
        """Test extracting from topic with invalid prefix."""
        topic = "other/livingroom/status"
        result = DeviceMqttClient.extract_device_id_from_topic(topic)
        assert result is None

    def test_extract_device_id_invalid_suffix(self) -> None:
        """Test extracting from topic with invalid suffix."""
        topic = "inky/livingroom/command"
        result = DeviceMqttClient.extract_device_id_from_topic(topic)
        assert result is None

    def test_extract_device_id_too_few_parts(self) -> None:
        """Test extracting from topic with too few parts."""
        topic = "inky/status"
        result = DeviceMqttClient.extract_device_id_from_topic(topic)
        assert result is None

    def test_extract_device_id_too_many_parts(self) -> None:
        """Test extracting from topic with too many parts."""
        topic = "inky/livingroom/sensor/status"
        result = DeviceMqttClient.extract_device_id_from_topic(topic)
        assert result is None
