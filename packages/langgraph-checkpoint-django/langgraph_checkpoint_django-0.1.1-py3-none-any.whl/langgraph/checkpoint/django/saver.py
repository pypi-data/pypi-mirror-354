import json
import random
from collections.abc import Sequence
from typing import Any, Dict, Iterator, Optional, Tuple, cast

from django.db import connection
from django.db.models import Prefetch, Q
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.base import (
    WRITES_IDX_MAP,
    BaseCheckpointSaver,
    ChannelVersions,
    Checkpoint,
    CheckpointMetadata,
    CheckpointTuple,
    get_checkpoint_id,
    get_checkpoint_metadata,
)
from packaging import version

from langgraph.checkpoint.django.checkpoint.models import Checkpoint as CheckpointModel
from langgraph.checkpoint.django.checkpoint.models import Write as WriteModel
from langgraph.checkpoint.serde.base import SerializerProtocol
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer
from langgraph.checkpoint.serde.types import ChannelProtocol


class DjangoSaver(BaseCheckpointSaver[str]):
    def __init__(
            self,
            *,
            serde: Optional[SerializerProtocol] = None,
    ):
        self._check_sqlite_compatibility()
        super().__init__(serde=serde)
        self.jsonplus_serde = JsonPlusSerializer()

    def _check_sqlite_compatibility(self):
        if connection.vendor != "sqlite":
            return

        with connection.cursor() as cursor:
            cursor.execute("select sqlite_version();")
            version_str = cursor.fetchone()[0]

            if version.parse(version_str) < version.parse("3.9.0"):
                raise RuntimeError(
                    f"SQLite {version_str} does not support JSONField (requires >= 3.9.0)"
                )

            try:
                cursor.execute("SELECT json_extract('{\"a\": 1}', '$.a');")
            except Exception as e:
                raise RuntimeError(
                    f"SQLite JSON1 extension is not enabled or available: {e}"
                )

    def get_tuple(self, config: RunnableConfig) -> Optional[CheckpointTuple]:
        thread_id = config["configurable"]["thread_id"]
        checkpoint_id = get_checkpoint_id(config)
        checkpoint_ns = config["configurable"].get("checkpoint_ns", "")

        queryset = CheckpointModel.objects.filter(thread_id=thread_id, checkpoint_ns=checkpoint_ns)
        queryset = queryset.prefetch_related(
            Prefetch(
                "writes",
                queryset=WriteModel.objects.order_by("task_id", "idx").only("task_id", "channel", "type", "value"),
            )
        )

        if checkpoint_id:
            obj = queryset.filter(checkpoint_id=checkpoint_id).first()
        else:
            obj = queryset.order_by("-checkpoint_id").first()

        if not obj:
            return None

        return CheckpointTuple(
            {
                "configurable": {
                    "thread_id": thread_id,
                    "checkpoint_ns": checkpoint_ns,
                    "checkpoint_id": obj.checkpoint_id,
                }
            },
            self.serde.loads_typed((obj.type, obj.checkpoint)),
            cast(
                CheckpointMetadata,
                self.jsonplus_serde.loads(self.jsonplus_serde.dumps(obj.metadata)) if obj.metadata else {},
            ),
            (
                {
                    "configurable": {
                        "thread_id": thread_id,
                        "checkpoint_ns": checkpoint_ns,
                        "checkpoint_id": obj.parent_checkpoint_id,
                    }
                }
                if obj.parent_checkpoint_id
                else None
            ),
            [
                (write.task_id, write.channel, self.serde.loads_typed((write.type, write.value)))
                for write in obj.writes.all()
            ],
        )

    def list(
        self,
        config: Optional[RunnableConfig],
        *,
        filter: Optional[Dict[str, Any]] = None,
        before: Optional[RunnableConfig] = None,
        limit: Optional[int] = None,
    ) -> Iterator[CheckpointTuple]:
        queryset = CheckpointModel.objects.order_by("-checkpoint_id")
        queryset = queryset.prefetch_related(
            Prefetch(
                "writes",
                queryset=WriteModel.objects.order_by("task_id", "idx").only("task_id", "channel", "type", "value"),
            )
        )

        if config:
            queryset = queryset.filter(thread_id=config["configurable"]["thread_id"])
            checkpoint_ns = config["configurable"].get("checkpoint_ns")
            if checkpoint_ns is not None:
                queryset = queryset.filter(checkpoint_ns=checkpoint_ns)
            if checkpoint_id := get_checkpoint_id(config):
                queryset = queryset.filter(checkpoint_id=checkpoint_id)

        if filter:
            metadata_filters = Q()
            for key, value in filter.items():
                metadata_filters &= Q(**{f"metadata__{key}": value})
            if metadata_filters:
                queryset = queryset.filter(metadata_filters)

        if before:
            before_checkpoint_id = get_checkpoint_id(before)
            if before_checkpoint_id:
                queryset = queryset.filter(checkpoint_id__lt=before_checkpoint_id)

        if limit:
            queryset = queryset[:limit]

        for obj in queryset:
            yield CheckpointTuple(
                {
                    "configurable": {
                        "thread_id": obj.thread_id,
                        "checkpoint_ns": obj.checkpoint_ns,
                        "checkpoint_id": obj.checkpoint_id,
                    }
                },
                self.serde.loads_typed((obj.type, obj.checkpoint)),
                cast(
                    CheckpointMetadata,
                    self.jsonplus_serde.loads(self.jsonplus_serde.dumps(obj.metadata)) if obj.metadata else {},
                ),
                (
                    {
                        "configurable": {
                            "thread_id": obj.thread_id,
                            "checkpoint_ns": obj.checkpoint_ns,
                            "checkpoint_id": obj.parent_checkpoint_id,
                        }
                    }
                    if obj.parent_checkpoint_id
                    else None
                ),
                [
                    (write.task_id, write.channel, self.serde.loads_typed((write.type, write.value)))
                    for write in obj.writes.all()
                ],
            )

    def put(
        self,
        config: RunnableConfig,
        checkpoint: Checkpoint,
        metadata: CheckpointMetadata,
        new_versions: ChannelVersions,
    ) -> RunnableConfig:
        configurable = config["configurable"].copy()
        thread_id = configurable.pop("thread_id")
        checkpoint_ns = configurable.pop("checkpoint_ns")
        checkpoint_id = configurable.pop("checkpoint_id", configurable.pop("thread_ts", None))
        type_, serialized_checkpoint = self.serde.dumps_typed(checkpoint)
        serialized_metadata = json.loads(
            self.jsonplus_serde.dumps(get_checkpoint_metadata(config, metadata)).decode().replace("\\u0000", "")
        )
        next_config = {
            "configurable": {
                "thread_id": thread_id,
                "checkpoint_ns": checkpoint_ns,
                "checkpoint_id": checkpoint["id"],
            }
        }
        CheckpointModel.objects.update_or_create(
            composite_id=f"{thread_id}-{checkpoint_ns}-{checkpoint['id']}",
            thread_id=thread_id,
            checkpoint_ns=checkpoint_ns,
            checkpoint_id=checkpoint["id"],
            defaults={
                "parent_checkpoint_id": checkpoint_id,
                "type": type_,
                "checkpoint": serialized_checkpoint,
                "metadata": serialized_metadata,
            },
        )

        return next_config

    def put_writes(
        self,
        config: RunnableConfig,
        writes: Sequence[Tuple[str, Any]],
        task_id: str,
        task_path: str = "",
    ) -> None:
        thread_id = config["configurable"]["thread_id"]
        checkpoint_ns = config["configurable"]["checkpoint_ns"]
        checkpoint_id = config["configurable"]["checkpoint_id"]

        writes_list = []
        for idx, (channel, value) in enumerate(writes):
            type_, value = self.serde.dumps_typed(value)
            writes_list.append(
                WriteModel(
                    checkpoint_id=f"{thread_id}-{checkpoint_ns}-{checkpoint_id}",
                    task_id=task_id,
                    task_path=task_path,
                    idx=WRITES_IDX_MAP.get(channel, idx),
                    channel=channel,
                    type=type_,
                    value=value,
                )
            )

        if all(w[0] in WRITES_IDX_MAP for w in writes):
            WriteModel.objects.bulk_create(
                writes_list,
                update_conflicts=True,
                update_fields=["channel", "type", "value"],
                unique_fields=["checkpoint_id", "task_id", "idx"],
            )
        else:
            WriteModel.objects.bulk_create(
                writes_list,
                ignore_conflicts=True,
            )

    def delete_thread(self, thread_id: str) -> None:
        CheckpointModel.objects.filter(thread_id=thread_id).delete()

    def get_next_version(self, current: Optional[str], channel: ChannelProtocol) -> str:
        if current is None:
            current_v = 0
        elif isinstance(current, int):
            current_v = current
        else:
            current_v = int(current.split(".")[0])
        next_v = current_v + 1
        next_h = random.random()
        return f"{next_v:032}.{next_h:016}"
