# Copyright 2024-2025 Yaroslav Petrov <yaroslav.v.petrov@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from functools import cache
from pydantic import BaseModel, RootModel
from typing import TypeVar, Union, cast

T = TypeVar("T", bound=BaseModel)
U = TypeVar("U")


class UnionModel(RootModel[U]):
    """A trick to allow unions as constructor types"""


def encode_message(message: T) -> bytes:
    return message.model_dump_json().encode()


def decode_message(message: bytes, schema: type[T]) -> T:
    payload = schema.model_validate_json(message)
    if isinstance(payload, UnionModel):
        payload = cast(T, payload.root)
    return payload


@cache
def union_model(types: tuple[type[U], ...]) -> type[UnionModel[U]]:
    UnionType = Union.__getitem__(types)
    return UnionModel[UnionType]  # type: ignore
