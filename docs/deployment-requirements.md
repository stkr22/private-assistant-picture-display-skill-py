# Picture Display Skill Deployment Requirements

Requirements for deploying the Picture Display Skill to Kubernetes via ArgoCD.

## Environment Variables

### PostgreSQL Database

| Variable | Description | Example |
|----------|-------------|---------|
| `POSTGRES_HOST` | PostgreSQL hostname | `cnpg-cluster-rw.database.svc` |
| `POSTGRES_PORT` | PostgreSQL port | `5432` |
| `POSTGRES_USER` | Database username | `picture_skill` |
| `POSTGRES_PASSWORD` | Database password | (from secret) |
| `POSTGRES_DB` | Database name | `private_assistant` |

### MQTT (Internal - Intent Engine)

| Variable | Description | Example |
|----------|-------------|---------|
| `MQTT_HOST` | MQTT broker hostname | `mosquitto.messaging.svc` |
| `MQTT_PORT` | MQTT broker port | `1883` |

### Device MQTT (for Inky display communication)

Uses the same MQTT broker as the internal communication.

| Variable | Description | Example |
|----------|-------------|---------|
| `DEVICE_MQTT_HOST` | Device MQTT broker hostname | `mosquitto.messaging.svc` |
| `DEVICE_MQTT_PORT` | Device MQTT broker port | `1883` |
| `DEVICE_MQTT_USERNAME` | Device MQTT username | (optional, from secret) |
| `DEVICE_MQTT_PASSWORD` | Device MQTT password | (optional, from secret) |

### S3-Compatible Storage (Image Storage)

| Variable | Description | Example |
|----------|-------------|---------|
| `S3_ENDPOINT` | S3 endpoint (host:port) | `garage.storage.svc:3900` |
| `S3_BUCKET` | Bucket name for images | `inky-images` |
| `S3_READER_ACCESS_KEY` | Read-only access key | (from secret) |
| `S3_READER_SECRET_KEY` | Read-only secret key | (from secret) |

## Required Secrets

### Database Credentials

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: picture-skill-db
type: Opaque
stringData:
  POSTGRES_USER: picture_skill
  POSTGRES_PASSWORD: <password>
```

### S3 Credentials

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: picture-skill-s3
type: Opaque
stringData:
  S3_READER_ACCESS_KEY: <access-key>
  S3_READER_SECRET_KEY: <secret-key>
```

## External Dependencies

### S3 Bucket

Create bucket `inky-images` with:
- Reader policy for skill to serve image URLs to devices
- Writer policy for external image ingest (future agents)

### Database Tables

Tables are auto-created by SQLModel on startup:
- `images` - Image metadata and storage paths
- `picture_devices` - Registered Inky display devices
- `device_display_states` - Current display state per device

## Deployment Manifest

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: picture-display-skill
spec:
  replicas: 1
  selector:
    matchLabels:
      app: picture-display-skill
  template:
    metadata:
      labels:
        app: picture-display-skill
    spec:
      containers:
        - name: skill
          image: ghcr.io/stkr22/private-assistant-picture-display-skill:latest
          command: ["private-assistant-picture-display-skill", "run"]
          envFrom:
            - secretRef:
                name: picture-skill-db
            - secretRef:
                name: picture-skill-s3
          env:
            - name: MQTT_HOST
              value: mosquitto.messaging.svc
            - name: MQTT_PORT
              value: "1883"
            - name: DEVICE_MQTT_HOST
              value: mosquitto.messaging.svc
            - name: DEVICE_MQTT_PORT
              value: "1883"
            - name: S3_ENDPOINT
              value: garage.storage.svc:3900
            - name: S3_BUCKET
              value: inky-images
            - name: POSTGRES_HOST
              value: cnpg-cluster-rw.database.svc
            - name: POSTGRES_PORT
              value: "5432"
            - name: POSTGRES_DB
              value: private_assistant
          resources:
            requests:
              memory: "128Mi"
              cpu: "100m"
            limits:
              memory: "256Mi"
              cpu: "500m"
```

## MQTT Topics

### Subscribed Topics

- `assistant/intent_engine/result` - Intent requests from intent engine

### Published Topics

- `assistant/skill/register` - Skill registration on startup
- `{client_output_topic}` - Responses to voice commands

### Device Topics

- Subscribe: `inky/register` - Device registration requests
- Subscribe: `inky/+/status` - Device status heartbeats
- Publish: `inky/{device_id}/command` - Display commands
- Publish: `inky/{device_id}/registered` - Registration confirmations
