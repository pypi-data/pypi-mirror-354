import asyncio
import json
from collections.abc import Sequence
from typing import Any, Dict, Iterator, Optional, Tuple, cast, AsyncIterator

import django
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
from langgraph.checkpoint.django.checkpoint.models import Checkpoint as CheckpointModel
from langgraph.checkpoint.django.checkpoint.models import Write as WriteModel
from langgraph.checkpoint.serde.base import SerializerProtocol
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer


class AsyncDjangoSaver(BaseCheckpointSaver[str]):
    def __init__(
        self,
        *,
        serde: Optional[SerializerProtocol] = None,
    ):
        self._check_django_async_support()
        super().__init__(serde=serde)
        self.jsonplus_serde = JsonPlusSerializer()
        self.lock = asyncio.Lock()
        self.loop = asyncio.get_running_loop()

    def _check_django_async_support(self):
        if django.VERSION < (4, 1):
            raise RuntimeError("Django 4.1+ required for AsyncDjangoSaver...")

    async def aget_tuple(self, config: RunnableConfig) -> Optional[CheckpointTuple]:
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
            obj = await queryset.filter(checkpoint_id=checkpoint_id).afirst()
        else:
            obj = await queryset.order_by("-checkpoint_id").afirst()

        if not obj:
            return None

        writes_list = []
        async for write in obj.writes.all():
            writes_list.append(write)

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
                for write in writes_list
            ],
        )

    async def alist(
        self,
        config: Optional[RunnableConfig],
        *,
        filter: Optional[Dict[str, Any]] = None,
        before: Optional[RunnableConfig] = None,
        limit: Optional[int] = None,
    ) -> AsyncIterator[CheckpointTuple]:
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

        async for obj in queryset:
            writes_list = []
            async for write in obj.writes.all():
                writes_list.append(write)

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
                    for write in writes_list
                ],
            )

    async def aput(
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

        await CheckpointModel.objects.aupdate_or_create(
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

    async def aput_writes(
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
            await WriteModel.objects.abulk_create(
                writes_list,
                update_conflicts=True,
                update_fields=["channel", "type", "value"],
                unique_fields=["checkpoint_id", "task_id", "idx"],
            )
        else:
            await WriteModel.objects.abulk_create(
                writes_list,
                ignore_conflicts=True,
            )

    async def adelete_thread(self, thread_id: str) -> None:
        await CheckpointModel.objects.filter(thread_id=thread_id).adelete()

    def list(
        self,
        config: Optional[RunnableConfig],
        *,
        filter: Optional[dict[str, Any]] = None,
        before: Optional[RunnableConfig] = None,
        limit: Optional[int] = None,
    ) -> Iterator[CheckpointTuple]:
        """List checkpoints from the database.

        This method retrieves a list of checkpoint tuples from the Postgres database based
        on the provided config. The checkpoints are ordered by checkpoint ID in descending order (newest first).

        Args:
            config (Optional[RunnableConfig]): Base configuration for filtering checkpoints.
            filter (Optional[Dict[str, Any]]): Additional filtering criteria for metadata.
            before (Optional[RunnableConfig]): If provided, only checkpoints before the specified checkpoint ID are returned. Defaults to None.
            limit (Optional[int]): Maximum number of checkpoints to return.

        Yields:
            Iterator[CheckpointTuple]: An iterator of matching checkpoint tuples.
        """
        try:
            # check if we are in the main thread, only bg threads can block
            # we don't check in other methods to avoid the overhead
            if asyncio.get_running_loop() is self.loop:
                raise asyncio.InvalidStateError(
                    "Synchronous calls to AsyncPostgresSaver are only allowed from a "
                    "different thread. From the main thread, use the async interface. "
                    "For example, use `checkpointer.alist(...)` or `await "
                    "graph.ainvoke(...)`."
                )
        except RuntimeError:
            pass
        aiter_ = self.alist(config, filter=filter, before=before, limit=limit)
        while True:
            try:
                yield asyncio.run_coroutine_threadsafe(
                    anext(aiter_),  # noqa: F821
                    self.loop,
                ).result()
            except StopAsyncIteration:
                break

    def get_tuple(self, config: RunnableConfig) -> Optional[CheckpointTuple]:
        """Get a checkpoint tuple from the database.

        This method retrieves a checkpoint tuple from the Postgres database based on the
        provided config. If the config contains a "checkpoint_id" key, the checkpoint with
        the matching thread ID and "checkpoint_id" is retrieved. Otherwise, the latest checkpoint
        for the given thread ID is retrieved.

        Args:
            config (RunnableConfig): The config to use for retrieving the checkpoint.

        Returns:
            Optional[CheckpointTuple]: The retrieved checkpoint tuple, or None if no matching checkpoint was found.
        """
        try:
            # check if we are in the main thread, only bg threads can block
            # we don't check in other methods to avoid the overhead
            if asyncio.get_running_loop() is self.loop:
                raise asyncio.InvalidStateError(
                    "Synchronous calls to AsyncPostgresSaver are only allowed from a "
                    "different thread. From the main thread, use the async interface. "
                    "For example, use `await checkpointer.aget_tuple(...)` or `await "
                    "graph.ainvoke(...)`."
                )
        except RuntimeError:
            pass
        return asyncio.run_coroutine_threadsafe(self.aget_tuple(config), self.loop).result()

    def put(
        self,
        config: RunnableConfig,
        checkpoint: Checkpoint,
        metadata: CheckpointMetadata,
        new_versions: ChannelVersions,
    ) -> RunnableConfig:
        """Save a checkpoint to the database.

        This method saves a checkpoint to the Postgres database. The checkpoint is associated
        with the provided config and its parent config (if any).

        Args:
            config (RunnableConfig): The config to associate with the checkpoint.
            checkpoint (Checkpoint): The checkpoint to save.
            metadata (CheckpointMetadata): Additional metadata to save with the checkpoint.
            new_versions (ChannelVersions): New channel versions as of this write.

        Returns:
            RunnableConfig: Updated configuration after storing the checkpoint.
        """
        return asyncio.run_coroutine_threadsafe(
            self.aput(config, checkpoint, metadata, new_versions), self.loop
        ).result()

    def put_writes(
        self,
        config: RunnableConfig,
        writes: Sequence[tuple[str, Any]],
        task_id: str,
        task_path: str = "",
    ) -> None:
        """Store intermediate writes linked to a checkpoint.

        This method saves intermediate writes associated with a checkpoint to the database.

        Args:
            config (RunnableConfig): Configuration of the related checkpoint.
            writes (Sequence[Tuple[str, Any]]): List of writes to store, each as (channel, value) pair.
            task_id (str): Identifier for the task creating the writes.
            task_path (str): Path of the task creating the writes.
        """
        return asyncio.run_coroutine_threadsafe(
            self.aput_writes(config, writes, task_id, task_path), self.loop
        ).result()

    def delete_thread(self, thread_id: str) -> None:
        """Delete all checkpoints and writes associated with a thread ID.

        Args:
            thread_id (str): The thread ID to delete.

        Returns:
            None
        """
        try:
            # check if we are in the main thread, only bg threads can block
            # we don't check in other methods to avoid the overhead
            if asyncio.get_running_loop() is self.loop:
                raise asyncio.InvalidStateError(
                    "Synchronous calls to AsyncPostgresSaver are only allowed from a "
                    "different thread. From the main thread, use the async interface. "
                    "For example, use `await checkpointer.aget_tuple(...)` or `await "
                    "graph.ainvoke(...)`."
                )
        except RuntimeError:
            pass
        return asyncio.run_coroutine_threadsafe(self.adelete_thread(thread_id), self.loop).result()
