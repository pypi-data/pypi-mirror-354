from argparse import Action
import re
import copy
from datetime import datetime
from dateutil.relativedelta import relativedelta
from typing import get_args, Optional, Literal, List, Dict, Tuple

from box import Box

from ..common import logger
from .item import TodoItem, Status, Priority
from .result import AddResult, EditResult, ViewResult, QueryResult
from .select import (
    FilterMixin, GroupMixin, SortMixin, FilterBy, FilterValue, GroupBy, SortBy)


class ActionError(Exception):
    pass


class ActionValueError(ActionError):
    """An exception raised when a value set operation fails."""


class TaskBook(FilterMixin, GroupMixin, SortMixin):
    todos: List[TodoItem]
    path: Optional[str]

    def __init__(
        self, config: Box, todos: Optional[List[TodoItem]] = None,
    ):
        super().__init__()
        self.config = config
        self.todos = todos or []
        self.next_id = max([todo.id for todo in self.todos], default=0) + 1

    def add(
        self, title: str, description: Optional[str] = None,
        project: str = "inbox", tags: Optional[List[str]] = None,
        status: Status = "pending", priority: Priority = "normal",
        deadline: Optional[datetime] = None,
    ) -> AddResult:
        if tags is None:
            tags = []
        todo = TodoItem(self.next_id, title)
        todo.description = self.description(todo, description)
        todo.project = self.project(todo, project)
        if tags:
            todo.tags = self.tags(todo, tags)
        todo.status = self.status(todo, status)
        todo.priority = self.priority(todo, priority)
        todo.deadline = self.deadline(todo, deadline)
        self.todos.append(todo)
        self.next_id += 1
        return AddResult([todo])

    def id(self, todo: TodoItem, id: int) -> int:
        return id

    def title(self, todo: TodoItem, title: str) -> str:
        return self._resolve_alias("title", title.strip())

    def description(
        self, todo: TodoItem, description: Optional[str]
    ) -> Optional[str]:
        if description:
            description = description.strip()
            if description:
                return self._resolve_alias('description', description)
        return None

    def status(self, todo: TodoItem, status: str) -> Status:
        if status:
            status = self._resolve_alias("status", status)
            if status not in get_args(Status):
                raise ActionValueError(f"Unrecognized status {status!r}.")
            return status
        status_changes: Dict[Status, Status] = {
            "done": "pending",
            "pending": "done",
        }
        try:
            return status_changes[todo.status]
        except KeyError as e:
            raise ActionValueError(
                "Cannot toggle status of an item "
                f"with status {todo.status!r}.") from e

    def priority(self, todo: TodoItem, priority: Priority) -> Priority:
        new_priority = self._resolve_alias("priority", priority)
        if new_priority in get_args(Priority):
            return new_priority
        priority_changes: Dict[Tuple[str, Priority], Priority] = {
            ("", "high"): "normal",
            ("", "normal"): "high",
            ("", "low"): "normal",
            ("+", "high"): "high",
            ("+", "normal"): "high",
            ("+", "low"): "normal",
            ("-", "high"): "normal",
            ("-", "normal"): "low",
            ("-", "low"): "low",
        }
        try:
            new_priority = priority_changes[priority, todo.priority]
        except KeyError:
            new_priority = None
        if not new_priority:
            raise ActionValueError(
                "Cannot change priority from "
                f"{todo.priority!r} to {priority!r}.")
        return new_priority

    def project(self, todo: TodoItem, project: str) -> str:
        return self._resolve_alias('project', project)

    def tags(self, todo: TodoItem, tags: List[str]) -> List[str]:
        new_tags: List[str] = list(todo.tags)
        for tag in tags:
            tag = self._resolve_alias("tag", tag.strip())
            if tag.startswith("+"):
                if tag[1:] not in new_tags:
                    new_tags.append(tag[1:])
            elif tag.startswith("-"):
                if tag[1:] in new_tags:
                    new_tags.remove(tag[1:])
            elif tag not in new_tags:
                new_tags.append(tag)
            else:
                new_tags.remove(tag)
        return new_tags

    def deadline(
        self, todo: TodoItem, deadline: Optional[datetime | relativedelta]
    ) -> Optional[datetime]:
        if not isinstance(deadline, relativedelta):
            return deadline
        if not todo.deadline:
            logger.warn(
                f"Cannot relative adjust an item without a deadline.")
            return None
        return todo.deadline + deadline

    def select(
        self, filters: Optional[Dict[FilterBy, FilterValue]],
        group_by: GroupBy = "id", sort_by: SortBy = "id",
    ) -> ViewResult:
        filtered_todos = self.todos
        if filters is not None:
            filtered_todos = self.filter(self.todos, filters)
        gtodos = self.group_by(filtered_todos, group_by)
        for group, todos in gtodos.items():
            gtodos[group] = self.sort_by(todos, sort_by)
        is_all = len(filtered_todos) == len(self.todos)
        return ViewResult(gtodos, group_by, sort_by, is_all)

    def query(self, todos: List[TodoItem], query: List[str]) -> QueryResult:
        values = []
        for todo in todos:
            values.append([getattr(todo, key) for key in query])
        return QueryResult(query, values)

    def _update_and_return(
        self, before: List[TodoItem], after: List[TodoItem]
    ) -> EditResult:
        before_id_todos = {t.id: t for t in before}
        after_id_todos = {t.id: t for t in after}
        all_id_todos = {
            t.id: t for t in self.todos if t.id not in before_id_todos}
        all_id_todos |= after_id_todos
        self.todos = list(sorted(all_id_todos.values(), key=lambda t: t.id))
        updates = []
        for b, a in zip(before, after):
            if b != a:
                updates.append((b, a))
        before, after = zip(*updates) if updates else ([], [])
        result = EditResult(before, after)
        logger.debug(f"Result: {result}")
        return result

    def action(
        self, todos: List[TodoItem],
        actions: Optional[Dict[str, Literal["editor"] | str | List[str]]],
    ) -> EditResult:
        if actions is None:
            return EditResult(todos, todos)
        after = copy.deepcopy(todos)
        for todo in after:
            for action, value in actions.items():
                try:
                    value = getattr(self, action)(todo, value)
                except ValueError as e:
                    logger.warn(e)
                else:
                    logger.debug(
                        f"Setting {action!r} to {value!r} for {todo.id}.")
                    setattr(todo, action, value)
        return self._update_and_return(todos, after)

    def re_index(self) -> EditResult:
        before = copy.deepcopy(self.todos)
        for i, todo in enumerate(self.todos):
            todo.id = self.id(todo, i + 1)
        updates = [(b, a) for b, a in zip(before, self.todos) if b != a]
        if not updates:
            result = EditResult([], [])
        else:
            before, after = zip(*updates)
            result = EditResult(before, after)
        logger.debug(f"Result: {result}")
        return result
