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

### Display API

| Variable | Description | Example |
|----------|-------------|---------|
| `DISPLAY_API_BASE_URL` | Display API base URL | `http://picture-display-api.apps.svc:8000` |
| `DISPLAY_API_TIMEOUT` | HTTP request timeout (seconds) | `10.0` |

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

## External Dependencies

### Database Tables

The skill uses `global_devices` and related tables managed by `private-assistant-commons`.
Device and image tables are managed by the display API.

### Display API

The skill requires a running [picture-display-api](https://github.com/stkr22/private-assistant-picture-display-api) instance.
The API manages devices, images, and display rotation.

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
          command: ["private-assistant-picture-display-skill", "main"]
          envFrom:
            - secretRef:
                name: picture-skill-db
          env:
            - name: MQTT_HOST
              value: mosquitto.messaging.svc
            - name: MQTT_PORT
              value: "1883"
            - name: DISPLAY_API_BASE_URL
              value: http://picture-display-api.apps.svc:8000
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
