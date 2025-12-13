"""Image model for storing picture metadata."""

from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class Image(SQLModel, table=True):
    """Image metadata stored in the database.

    Images are fetched from various sources (manual upload, Immich, Unsplash, etc.)
    and stored in MinIO. This table tracks metadata for display scheduling and
    voice command responses.

    Attributes:
        id: Unique identifier for the image
        source_name: Source identifier (e.g., "manual", "immich", "unsplash")
        storage_path: Path to image in MinIO bucket
        title: Optional title for voice responses
        description: Optional description for "what am I seeing?" queries
        author: Optional author/photographer name
        source_url: Optional URL to original source
        display_duration_seconds: How long to show this image (default 3600)
        priority: Weight for future priority-based selection (default 0)
        original_width: Image width in pixels
        original_height: Image height in pixels
        fetched_at: When the image was added to the system
        last_displayed_at: When the image was last shown (for FIFO selection)
        display_count: Number of times this image has been displayed
        expires_at: Optional expiration time for auto-cleanup
        tags: List of tags for categorization
        extra: Source-specific metadata (JSONB)
    """

    __tablename__ = "images"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    source_name: str = Field(index=True, description="Source identifier (e.g. manual, unsplash)")
    storage_path: str = Field(description="MinIO object path")

    # Metadata for voice responses
    title: str | None = Field(default=None, description="Image title for voice responses")
    description: str | None = Field(default=None, description="Description for 'what am I seeing?'")
    author: str | None = Field(default=None, description="Author/photographer name")
    source_url: str | None = Field(default=None, description="Original source URL")

    # Display settings
    display_duration_seconds: int = Field(default=3600, description="Display duration in seconds")
    priority: int = Field(default=0, description="Priority weight for selection (higher = more likely)")

    # Image dimensions for device compatibility
    original_width: int | None = Field(default=None, description="Image width in pixels")
    original_height: int | None = Field(default=None, description="Image height in pixels")

    # Timestamps
    fetched_at: datetime = Field(default_factory=datetime.now, description="When image was added")
    last_displayed_at: datetime | None = Field(default=None, description="Last display time for FIFO")
    expires_at: datetime | None = Field(default=None, description="Expiration time for cleanup")
