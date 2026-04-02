# Configuration

The Picture Display Skill uses a YAML configuration file for skill settings and environment variables for external service credentials.

## YAML Configuration File

The skill requires a YAML configuration file path, provided via:
- CLI argument: `private-assistant-picture-display-skill main /path/to/config.yaml`
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
| `S3_*` | Image Storage | `S3_ENDPOINT`, `S3_READER_ACCESS_KEY` |

## Immich Sync Configuration

The `immich-sync` command fetches images from Immich and stores them in S3-compatible storage.
Sync jobs are configured in the database via the `immich_sync_jobs` table.

### Usage

```bash
# Run all active sync jobs
private-assistant-picture-display-skill immich-sync

# Preview what would be synced
private-assistant-picture-display-skill immich-sync --dry-run
```

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `IMMICH_BASE_URL` | Yes | Immich server URL |
| `IMMICH_API_KEY` | Yes | API key for authentication |
| `S3_WRITER_ENDPOINT` | Yes | S3-compatible server endpoint |
| `S3_WRITER_ACCESS_KEY` | Yes | S3 access key |
| `S3_WRITER_SECRET_KEY` | Yes | S3 secret key |
| `S3_WRITER_BUCKET` | No | Bucket name (default: `inky-images`) |
| `S3_WRITER_SECURE` | No | Use HTTPS (default: `false`) |
| `S3_WRITER_REGION` | No | S3 region (default: `us-east-1`) |
| `POSTGRES_*` | Yes | Database connection |

### Sync Job Configuration (Database)

Sync jobs are stored in the `immich_sync_jobs` table:

**Core Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | str | Yes | Unique job identifier |
| `is_active` | bool | No | Enable/disable (default: true) |
| `target_device_id` | UUID | Yes | FK to global_devices - determines dimensions/orientation |
| `strategy` | enum | No | `RANDOM` or `SMART` (default: RANDOM) |
| `query` | str | For SMART | Semantic search query (CLIP-based) |
| `count` | int | No | Images per run (default: 10) |
| `random_pick` | bool | No | Random sample from smart results (default: false) |
| `overfetch_multiplier` | int | No | Fetch N× for client-side filtering (default: 3) |
| `min_color_score` | float | No | Color threshold 0.0-1.0 (default: 0.5) |

**API Filters** (sent to Immich):

| Field | Type | Description |
|-------|------|-------------|
| `album_ids` | list[str] | Album UUIDs |
| `person_ids` | list[str] | Person UUIDs |
| `tag_ids` | list[str] | Tag UUIDs |
| `is_favorite` | bool | Only favorites |
| `city`, `state`, `country` | str | Location filters |
| `taken_after`, `taken_before` | datetime | Date range |
| `rating` | int | Minimum rating (0-5) |

### Device Requirements

Each sync job references a `target_device_id`. The device must exist in `global_devices` with these attributes in the `device_attributes` JSON:

- `display_width`: Target image width (pixels)
- `display_height`: Target image height (pixels)
- `orientation`: `landscape`, `portrait`, or `square`

Images are filtered client-side to match device orientation and minimum dimensions, then processed (resized/cropped) to exact device dimensions.

### Color Profile Compatibility

The `min_color_score` field analyzes image colors against the Inky Impression Spectra 6 palette (black, white, red, yellow, green, blue). Images with colors naturally close to this palette display better with less dithering artifacts.

- **Score 1.0**: Perfect match (colors exactly match palette)
- **Score 0.5**: Moderate match (default threshold)
- **Score 0.0**: Poor match (colors far from palette)

Set `min_color_score: 0` to disable color filtering.

### Example: Creating a Sync Job

```sql
INSERT INTO immich_sync_jobs (
    name, target_device_id, strategy, count, is_favorite
) VALUES (
    'family-favorites',
    '550e8400-e29b-41d4-a716-446655440000',
    'RANDOM',
    20,
    true
);
```

### Getting Immich Filter IDs

To find album, person, or tag IDs for filtering:

1. **Albums**: Use Immich web UI → Albums → Copy album URL (contains UUID)
2. **People**: Use Immich web UI → People → Click person → Copy URL
3. **Tags**: Use Immich web UI → Explore → Tags
