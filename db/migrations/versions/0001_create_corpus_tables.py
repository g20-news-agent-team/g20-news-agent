"""Create the sources and documents tables."""

import sqlalchemy as sa
from alembic import op

revision = "0001_corpus"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "sources",
        sa.Column("id", sa.Text(), primary_key=True),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("kind", sa.Text(), nullable=False),
        sa.Column("entry_url", sa.Text(), nullable=False),
    )
    op.create_table(
        "documents",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("source_id", sa.Text(), sa.ForeignKey("sources.id"), nullable=False),
        sa.Column("canonical_url", sa.Text(), nullable=False),
        sa.Column("original_url", sa.Text(), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("content_text", sa.Text(), nullable=False),
        sa.Column("content_kind", sa.Text(), nullable=False),
        sa.Column("published_at", sa.DateTime(timezone=True)),
        sa.Column("fetched_at", sa.DateTime(timezone=True)),
        sa.Column("publisher", sa.Text()),
        sa.Column("author", sa.Text()),
        sa.Column("source_label", sa.Text()),
        sa.Column("section", sa.Text()),
        sa.Column("suggested_type", sa.Text()),
        sa.Column("document_type", sa.Text()),
        sa.Column("review_status", sa.Text(), server_default="pending_review", nullable=False),
        sa.Column("classification_reason", sa.Text()),
        sa.Column("imported_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("source_id", "canonical_url", name="uq_documents_source_canonical_url"),
        sa.CheckConstraint("content_kind IN ('full_text', 'summary')", name="ck_documents_content_kind"),
        sa.CheckConstraint(
            "(review_status = 'pending_review' AND document_type IS NULL) OR "
            "(review_status = 'confirmed' AND document_type IS NOT NULL AND "
            "document_type IN ('official_release', 'news_report', 'other'))",
            name="ck_documents_review_status",
        ),
    )


def downgrade() -> None:
    op.drop_table("documents")
    op.drop_table("sources")
