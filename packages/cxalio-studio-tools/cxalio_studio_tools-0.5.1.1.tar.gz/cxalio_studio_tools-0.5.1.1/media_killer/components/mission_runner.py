import asyncio
import itertools
import os
import random
from datetime import datetime
from pathlib import Path
from pprint import saferepr
from typing import override

from cx_studio.core.cx_time import CxTime
from cx_studio.ffmpeg import FFmpegAsync
from cx_studio.utils import PathUtils
from cx_wealth import rich_types as r
from cx_wealth.indexed_list_panel import IndexedListPanel
from cx_wealth.wealth_detail import WealthDetailPanel
from media_killer.appenv import appenv
from .exception import SafeError
from .mission import Mission


class MissionRunner:
    def __init__(self, mission: Mission):
        self.mission = mission
        self._ffmpeg: FFmpegAsync = FFmpegAsync(self.mission.ffmpeg)
        self._input_files = [self.mission.source] + list(
            self.mission.iter_input_filenames()
        )
        self._output_files = [self.mission.standard_target] + list(
            self.mission.iter_output_filenames()
        )

        self._task_description: str = self.mission.name
        self._task_completed: float = 0
        self._task_total: float | None = None
        self._task_speed: float = 0

        self._cancel_event = asyncio.Event()

        self._start_time: datetime | None = None
        self._end_time: datetime | None = None
        self._running_cond = asyncio.Condition()
        self._ffmpeg_outputs = []

    def cancel(self):
        # self._canceled = True
        self._cancel_event.set()

    @property
    def task_description(self):
        return self._task_description

    @property
    def task_completed(self):
        return self._task_completed

    @property
    def task_total(self):
        return self._task_total

    @property
    def task_start_time(self):
        return self._start_time

    @property
    def task_end_time(self):
        return self._end_time

    @property
    def task_speed(self):
        return self._task_speed

    def done(self):
        return self._start_time is not None and self._end_time is not None

    def is_running(self):
        return self._running_cond.locked()

    def make_line_report(self, right_side: str):
        header = "[bright_black]M[/] [dim green][{i_count}->{o_count}][/] ".format(
            i_count=len(self.mission.inputs), o_count=len(self.mission.outputs)
        )
        name = "[yellow]{}[/]".format(self.mission.name)

        label = header + name

        left = r.Text.from_markup(label, end="", justify="left", overflow="ellipsis")
        left.no_wrap = True
        right = r.Text.from_markup(right_side, justify="right")

        return r.Columns([left, right], expand=True)

    async def _on_started(self):
        report = self.make_line_report("[yellow]开始[/]")
        g = r.Group(
            WealthDetailPanel(self.mission, title=str(self.mission.mission_id)), report
        )
        appenv.whisper(g)

    async def _on_progress_updated(self, c: CxTime, t: CxTime | None):
        c_seconds = c.total_seconds
        t_seconds = t.total_seconds if t else None
        self._task_completed = c_seconds
        self._task_total = t_seconds
        self._task_speed = self._ffmpeg.coding_info.current_speed

    async def _on_finished(self):
        appenv.say(self.make_line_report("[green]完成[/]"))

    async def _on_terminated(self):
        appenv.whisper(IndexedListPanel(self._ffmpeg_outputs, title="FFmpeg 输出"))
        appenv.say(self.make_line_report("[red]运行异常[/]"))
        await self._clean_up()

    async def _on_canceled(self, reason: str | None = None):
        appenv.say(
            self.make_line_report("[bright_blue]{}[/]".format(reason or "被取消"))
        )
        await self._clean_up()
        if self._cancel_event.is_set():
            self._cancel_event.clear()

    async def _clean_up(self):
        self._ffmpeg_outputs.clear()
        safe_outputs = set(self._output_files) - set(self._input_files)
        deleting_files = set(filter(lambda x: x.exists(), safe_outputs))
        if deleting_files:
            appenv.whisper(IndexedListPanel(deleting_files, title="未完成的目标文件"))
            appenv.add_garbage_files(*deleting_files)

    async def _on_verbose(self, line: str):
        self._ffmpeg_outputs.append(line)

    def _prepare_mission(self):
        conflicts = set(self._input_files) & set(self._output_files)
        if len(conflicts) > 0:
            appenv.whisper(IndexedListPanel(conflicts, title="发现重叠文件"))
            raise SafeError("检测到重叠的输入输出文件")

        if not PathUtils.is_executable(Path(self._ffmpeg.executable)):
            raise SafeError("ffmpeg可执行文件无效:{}".format(self._ffmpeg.executable))

        no_existed_input_files = set(
            itertools.filterfalse(lambda a: a.exists(), self._input_files)
        )
        if no_existed_input_files:
            raise SafeError(
                "输入文件不存在: {}".format(";".join(map(str, no_existed_input_files)))
            )

        o_dirs = set(map(lambda a: a.parent, self._output_files))
        invalid_o_dirs = set(
            itertools.filterfalse(
                lambda a: os.access(a, os.W_OK),
                filter(lambda a: a.exists(), o_dirs),
            )
        )
        if invalid_o_dirs:
            raise SafeError("输出目录无效")

        non_existent_o_dirs = set(itertools.filterfalse(lambda a: a.exists(), o_dirs))
        if non_existent_o_dirs:
            self._task_description = "创建目标文件夹"
            for x in non_existent_o_dirs:
                x.mkdir(parents=True, exist_ok=True)
            appenv.whisper(
                IndexedListPanel(non_existent_o_dirs, title="自动创建目标文件夹")
            )
        self._task_description = self.mission.name

    async def execute(self):
        async with self._running_cond:
            self._ffmpeg.add_listener("started", self._on_started)
            self._ffmpeg.add_listener("progress_updated", self._on_progress_updated)
            self._ffmpeg.add_listener("finished", self._on_finished)
            self._ffmpeg.add_listener("canceled", self._on_canceled)
            self._ffmpeg.add_listener("terminated", self._on_terminated)
            self._ffmpeg.add_listener("verbose", self._on_verbose)

            self._start_time = datetime.now()
            self._task_description = self.mission.name

            result = None

            try:
                self._prepare_mission()

                main_task = asyncio.create_task(
                    self._ffmpeg.execute(self.mission.iter_arguments())
                )

                while not main_task.done():
                    await asyncio.sleep(0.1)
                    if self._cancel_event.is_set():
                        self._ffmpeg.cancel()
                        self._cancel_event.clear()
                        break

                # await asyncio.wait([main_task])
                result = main_task.result()

            except asyncio.CancelledError:
                self.cancel()
                result = False

            except SafeError as e:
                await self._on_canceled(reason=e.message)
                result = False

            finally:
                # async with self._cancelling_cond:
                # await asyncio.wait([main_task])
                self._end_time = datetime.now()
                await self._ffmpeg.wait_for_complete()
                return result

        # running condition


class MissionPretender(MissionRunner):
    def _init__(self, mission: Mission):
        super().__init__(mission)

    async def _pretending_prepare_mission(self):
        self._task_description = "检查输入输出文件"
        await asyncio.sleep(0.5)
        conflicts = set(self._input_files) & set(self._output_files)
        if len(conflicts) > 0:
            appenv.whisper(IndexedListPanel(conflicts, title="发现重叠文件"))
            raise SafeError("检测到重叠的输入输出文件")

        self._task_description = "检查ffmpeg可执行文件"
        await asyncio.sleep(0.3)
        if not PathUtils.is_executable(Path(self._ffmpeg.executable)):
            raise SafeError("ffmpeg可执行文件无效:{}".format(self._ffmpeg.executable))

        self._task_description = "检查输入文件"
        await asyncio.sleep(0.5)
        no_existed_input_files = set(
            itertools.filterfalse(lambda x: x.exists(), self._input_files)
        )
        if no_existed_input_files:
            raise SafeError(
                "输入文件不存在: {}".format(
                    ";".join(map(saferepr, no_existed_input_files))
                )
            )

        self._task_description = "检查输出目录"
        await asyncio.sleep(0.2)
        o_dirs = set(map(lambda x: x.parent, self._output_files))
        invalid_o_dirs = set(
            itertools.filterfalse(
                lambda x: os.access(x, os.W_OK),
                filter(lambda x: x.exists(), o_dirs),
            )
        )
        if invalid_o_dirs:
            appenv.whisper(IndexedListPanel(invalid_o_dirs, title="无效的输出目录"))
            raise SafeError("输出目录无效")

        self._task_description = "创建输出目录"
        non_existent_o_dirs = set(itertools.filterfalse(lambda x: x.exists(), o_dirs))
        if non_existent_o_dirs:
            self._task_total = len(non_existent_o_dirs)
            for _ in non_existent_o_dirs:
                self._task_completed += 1
                await asyncio.sleep(0.25)
            self._task_total = None
            appenv.whisper(
                IndexedListPanel(non_existent_o_dirs, title="自动创建目标文件夹")
            )

    @override
    async def execute(self):
        async with self._running_cond:
            try:
                await self._pretending_prepare_mission()

                self._task_total = 1000
                self._task_completed = 0
                self._task_description = self.mission.name
                self._start_time = datetime.now()

                while self._task_completed < self._task_total:
                    step = random.randint(5, 25)
                    self._task_completed += step
                    self._task_speed = random.randint(1200, 9999) / 100
                    await asyncio.sleep(0.05)
                    if self._cancel_event.is_set():
                        await self._on_canceled()
                        break
            except asyncio.CancelledError:
                self.cancel()
            except SafeError as e:
                await self._on_canceled(reason=e.message)
            finally:
                self._end_time = datetime.now()
                return True
