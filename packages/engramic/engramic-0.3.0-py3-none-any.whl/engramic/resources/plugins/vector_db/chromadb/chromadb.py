# Copyright (c) 2025 Preisz Consulting, LLC.
# This file is part of Engramic, licensed under the Engramic Community License.
# See the LICENSE file in the project root for more details.
import os
import uuid
from collections.abc import Mapping, Sequence
from typing import Any, cast

import chromadb
from chromadb.config import Settings

from engramic.core.index import Index
from engramic.core.interface.vector_db import VectorDB
from engramic.infrastructure.system.plugin_specifications import vector_db_impl


class ChromaDB(VectorDB):
    DEFAULT_THRESHOLD = 0.4
    DEFAULT_N_RESULTS = 2

    def __init__(self) -> None:
        db_path = os.path.join('local_storage', 'chroma_db')

        local_storage_root_path = os.getenv('LOCAL_STORAGE_ROOT_PATH')
        if local_storage_root_path is not None:
            db_path = os.path.join(local_storage_root_path, 'chroma_db')

        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.client = chromadb.PersistentClient(
            path='local_storage/chroma_db', settings=Settings(anonymized_telemetry=False)
        )
        self.collection = {}
        metadata = {
            'hnsw:space': 'cosine',
        }

        self.collection['main'] = self.client.get_or_create_collection(name='main', metadata=metadata)
        self.collection['meta'] = self.client.get_or_create_collection(name='meta', metadata=metadata)

    @vector_db_impl
    def query(
        self, collection_name: str, embeddings: list[float], filters: list[str], args: dict[str, Any]
    ) -> dict[str, Any]:
        embeddings_typed: Sequence[float] = embeddings
        n_results = self.DEFAULT_N_RESULTS
        threshold: float = self.DEFAULT_THRESHOLD

        if args.get('threshold') is not None:
            threshold = args['threshold']

        if args.get('threshold') is not None:
            n_results = args['n_results']

        # all_items = self.collection[collection_name].get()
        where: dict[str, Any] | None = None
        ret_ids: list[str] = []

        if filters:
            metadatas: list[dict[str, Any]] = [{repo_filter: {'$eq': True}} for repo_filter in filters]

            if len(filters) == 1:
                where = {filters[0]: True}
            elif len(filters) > 1:
                where = {'$or': metadatas}
        else:
            where = {'null': True}

        results = self.collection[collection_name].query(
            query_embeddings=embeddings_typed, n_results=n_results, where=where
        )

        distances_groups = results.get('distances') or []
        documents_groups = results.get('documents') or []

        for i in range(len(distances_groups)):
            distances = distances_groups[i]
            documents = documents_groups[i]

            for j, distance in enumerate(distances):
                if distance < threshold:
                    ret_ids.append(documents[j])

        return {'query_set': set(ret_ids)}

    @vector_db_impl
    def insert(
        self, collection_name: str, index_list: list[Index], obj_id: str, args: dict[str, Any], filters: list[str]
    ) -> None:
        # start = time.perf_counter()
        del args
        documents = []
        embeddings = []
        ids = []
        metadatas_container: list[dict[str, str | int | float | bool | None]] = []

        for embedding in index_list:
            documents.append(obj_id)
            embeddings.append(cast(Sequence[float], embedding.embedding))
            ids.append(str(uuid.uuid4()))
            metadatas: dict[str, str | int | float | bool | None] = {}
            if filters is not None:
                for repo_filter in filters:
                    metadatas.update({repo_filter: True})
                metadatas_container.append(metadatas)
            else:
                metadatas.update({'null': True})
                metadatas_container.append(metadatas)

        self.collection[collection_name].add(
            documents=documents,
            embeddings=embeddings,
            ids=ids,
            metadatas=cast(list[Mapping[str, str | int | float | bool | None]], metadatas_container),
        )

        # end = time.perf_counter()

        # print(f"Function took {end - start:.4f} seconds")
