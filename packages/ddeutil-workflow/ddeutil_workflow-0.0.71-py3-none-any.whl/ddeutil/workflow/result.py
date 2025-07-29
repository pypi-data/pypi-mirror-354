# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
"""A Result module. It is the data context transfer objects that use by all
object in this package. This module provide Status enum object and Result
dataclass.
"""
from __future__ import annotations

from dataclasses import field
from datetime import datetime
from enum import Enum
from typing import Optional, Union
from zoneinfo import ZoneInfo

from pydantic import ConfigDict
from pydantic.dataclasses import dataclass
from pydantic.functional_validators import model_validator
from typing_extensions import Self

from . import (
    JobCancelError,
    JobError,
    JobSkipError,
    StageCancelError,
    StageError,
    StageSkipError,
    WorkflowCancelError,
    WorkflowError,
)
from .__types import DictData
from .audits import TraceModel, get_trace
from .conf import dynamic
from .errors import ResultError
from .utils import default_gen_id, gen_id, get_dt_now


def get_dt_tznow(tz: Optional[ZoneInfo] = None) -> datetime:  # pragma: no cov
    """Return the current datetime object that passing the config timezone.

    :rtype: datetime
    """
    return get_dt_now(tz=dynamic("tz", f=tz))


class Status(str, Enum):
    """Status Int Enum object that use for tracking execution status to the
    Result dataclass object.
    """

    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    WAIT = "WAIT"
    SKIP = "SKIP"
    CANCEL = "CANCEL"

    @property
    def emoji(self) -> str:  # pragma: no cov
        """Return the emoji value of this status.

        :rtype: str
        """
        return {
            "SUCCESS": "✅",
            "FAILED": "❌",
            "WAIT": "🟡",
            "SKIP": "⏩",
            "CANCEL": "🚫",
        }[self.name]

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.name

    def is_result(self) -> bool:
        return self in ResultStatuses


SUCCESS = Status.SUCCESS
FAILED = Status.FAILED
WAIT = Status.WAIT
SKIP = Status.SKIP
CANCEL = Status.CANCEL

ResultStatuses: list[Status] = [SUCCESS, FAILED, CANCEL, SKIP]


def validate_statuses(statuses: list[Status]) -> Status:
    """Validate the final status from list of Status object.

    :param statuses: (list[Status]) A list of status that want to validate the
        final status.

    :rtype: Status
    """
    if any(s == CANCEL for s in statuses):
        return CANCEL
    elif any(s == FAILED for s in statuses):
        return FAILED
    elif any(s == WAIT for s in statuses):
        return WAIT
    for status in (SUCCESS, SKIP):
        if all(s == status for s in statuses):
            return status
    return FAILED if FAILED in statuses else SUCCESS


def get_status_from_error(
    error: Union[
        StageError,
        StageCancelError,
        StageSkipError,
        JobError,
        JobCancelError,
        JobSkipError,
        WorkflowError,
        WorkflowCancelError,
        Exception,
        BaseException,
    ]
) -> Status:
    """Get the Status from the error object."""
    if isinstance(error, (StageSkipError, JobSkipError)):
        return SKIP
    elif isinstance(
        error, (StageCancelError, JobCancelError, WorkflowCancelError)
    ):
        return CANCEL
    return FAILED


def default_context() -> DictData:
    return {"status": WAIT}


@dataclass(
    config=ConfigDict(arbitrary_types_allowed=True, use_enum_values=True),
)
class Result:
    """Result Pydantic Model for passing and receiving data context from any
    module execution process like stage execution, job execution, or workflow
    execution.

        For comparison property, this result will use ``status``, ``context``,
    and ``_run_id`` fields to comparing with other result instance.

    Warning:
        I use dataclass object instead of Pydantic model object because context
    field that keep dict value change its ID when update new value to it.
    """

    status: Status = field(default=WAIT)
    context: DictData = field(default_factory=default_context)
    run_id: Optional[str] = field(default_factory=default_gen_id)
    parent_run_id: Optional[str] = field(default=None, compare=False)
    ts: datetime = field(default_factory=get_dt_tznow, compare=False)

    trace: Optional[TraceModel] = field(default=None, compare=False, repr=False)
    extras: DictData = field(default_factory=dict, compare=False, repr=False)

    @classmethod
    def construct_with_rs_or_id(
        cls,
        result: Optional[Result] = None,
        run_id: Optional[str] = None,
        parent_run_id: Optional[str] = None,
        id_logic: Optional[str] = None,
        *,
        extras: DictData | None = None,
    ) -> Self:
        """Create the Result object or set parent running id if passing Result
        object.

        :param result: A Result instance.
        :param run_id: A running ID.
        :param parent_run_id: A parent running ID.
        :param id_logic: A logic function that use to generate a running ID.
        :param extras: An extra parameter that want to override the core config.

        :rtype: Self
        """
        if result is None:
            return cls(
                run_id=(run_id or gen_id(id_logic or "", unique=True)),
                parent_run_id=parent_run_id,
                ts=get_dt_now(dynamic("tz", extras=extras)),
                extras=(extras or {}),
            )
        elif parent_run_id:
            result.set_parent_run_id(parent_run_id)

        if extras is not None:
            result.extras.update(extras)

        return result

    @model_validator(mode="after")
    def __prepare_trace(self) -> Self:
        """Prepare trace field that want to pass after its initialize step.

        :rtype: Self
        """
        if self.trace is None:  # pragma: no cov
            self.trace: TraceModel = get_trace(
                self.run_id,
                parent_run_id=self.parent_run_id,
                extras=self.extras,
            )
        return self

    def set_parent_run_id(self, running_id: str) -> Self:
        """Set a parent running ID.

        :param running_id: (str) A running ID that want to update on this model.

        :rtype: Self
        """
        self.parent_run_id: str = running_id
        self.trace: TraceModel = get_trace(
            self.run_id, parent_run_id=running_id, extras=self.extras
        )
        return self

    def catch(
        self,
        status: Union[int, Status],
        context: DictData | None = None,
        **kwargs,
    ) -> Self:
        """Catch the status and context to this Result object. This method will
        use between a child execution return a result, and it wants to pass
        status and context to this object.

        :param status: A status enum object.
        :param context: A context data that will update to the current context.

        :rtype: Self
        """
        self.__dict__["status"] = (
            Status(status) if isinstance(status, int) else status
        )
        self.__dict__["context"].update(context or {})
        self.__dict__["context"]["status"] = self.status
        if kwargs:
            for k in kwargs:
                if k in self.__dict__["context"]:
                    self.__dict__["context"][k].update(kwargs[k])
                # NOTE: Exclude the `info` key for update information data.
                elif k == "info":
                    self.__dict__["context"][k].update(kwargs[k])
                else:
                    raise ResultError(
                        f"The key {k!r} does not exists on context data."
                    )
        return self

    def alive_time(self) -> float:  # pragma: no cov
        """Return total seconds that this object use since it was created.

        :rtype: float
        """
        return (
            get_dt_now(tz=dynamic("tz", extras=self.extras)) - self.ts
        ).total_seconds()
