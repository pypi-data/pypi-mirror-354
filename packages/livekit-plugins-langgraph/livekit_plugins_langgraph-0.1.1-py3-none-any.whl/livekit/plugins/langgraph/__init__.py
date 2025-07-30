# Copyright 2023 LiveKit, Inc.
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

"""Enhanced LiveKit plugin for LangGraph multi-agent workflows.

This plugin provides universal filtering for LangGraph multi-agent workflows,
ensuring only user-facing responses are spoken while filtering out tool calls,
SQL queries, and intermediate agent outputs.
"""

from .langgraph import LLMAdapter, LangGraphStream

__all__ = ["LLMAdapter", "LangGraphStream"]

__version__ = "0.1.0"