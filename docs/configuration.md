# Configuration

The Picture Display Skill uses a YAML configuration file for skill settings and environment variables for external service credentials.

## YAML Configuration File

The skill requires a YAML configuration file path, provided via:
- CLI argument: `private-assistant-picture-display-skill /path/to/config.yaml`
- Environment variable: `PRIVATE_ASSISTANT_CONFIG_PATH`

### Example Configuration

```yaml
# Required
client_id: picture-display-skill

# MQTT settings (internal - intent engine communication)
mqtt_server_host: mosquitto.messaging.svc
mqtt_server_port: 1883
base_topic: assistant

# Optional skill-specific settings
default_display_duration: 3600    # Image display duration in seconds (default: 3600)
device_timeout_seconds: 120       # Seconds without heartbeat before device marked offline (default: 120)
```

### Configuration Fields

| Field | Required | Default | Description |
|-------|----------|---------|-------------|
| `client_id` | Yes | - | Unique identifier for this skill instance |
| `mqtt_server_host` | Yes | - | Internal MQTT broker hostname |
| `mqtt_server_port` | No | `1883` | Internal MQTT broker port |
| `base_topic` | No | `assistant` | Base topic prefix for MQTT messages |
| `default_display_duration` | No | `3600` | How long images display (seconds) |
| `device_timeout_seconds` | No | `120` | Device offline timeout (seconds) |

## Environment Variables

External service credentials are loaded from environment variables using pydantic-settings. See [deployment-requirements.md](deployment-requirements.md) for the complete list.

### Quick Reference

| Prefix | Service | Example Variables |
|--------|---------|-------------------|
| `POSTGRES_*` | Database | `POSTGRES_HOST`, `POSTGRES_PASSWORD` |
| `DEVICE_MQTT_*` | Device MQTT | `DEVICE_MQTT_HOST`, `DEVICE_MQTT_USERNAME` |
| `MINIO_*` | Image Storage | `MINIO_ENDPOINT`, `MINIO_READER_ACCESS_KEY` |
