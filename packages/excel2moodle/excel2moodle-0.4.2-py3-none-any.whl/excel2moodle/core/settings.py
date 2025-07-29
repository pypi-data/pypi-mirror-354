"""Settings module provides the adjusted subclass of ``PySide6.QtCore.QSettings``."""

import logging
from enum import StrEnum
from pathlib import Path
from typing import ClassVar, Literal, overload

from PySide6.QtCore import QSettings, QTimer, Signal

import excel2moodle

logger = logging.getLogger(__name__)


class Tags(StrEnum):
    """Tags and Settings Keys are needed to always acess the correct Value.

    The Tags can be used to acess the settings or the QuestionData respectively.
    As the QSettings settings are accesed via strings, which could easily gotten wrong.
    Further, this Enum defines, which type a setting has to be.
    """

    def __new__(
        cls,
        key: str,
        typ: type,
        default: str | float | Path | bool | None,
        place: str = "project",
    ):
        """Define new settings class."""
        obj = str.__new__(cls, key)
        obj._value_ = key
        obj._typ_ = typ
        obj._default_ = default
        obj._place_ = place
        return obj

    def __init__(
        self,
        _,
        typ: type,
        default: str | float | Path | None,
        place: str = "project",
    ) -> None:
        self._typ_: type = typ
        self._place_: str = place
        self._default_ = default
        self._full_ = f"{self._place_}/{self._value_}"

    @property
    def default(self) -> str | int | float | Path | bool | None:
        """Get default value for the key."""
        return self._default_

    @property
    def place(self) -> str:
        return self._place_

    @property
    def full(self) -> str:
        return self._full_

    def typ(self) -> type:
        """Get type of the keys data."""
        return self._typ_

    QUESTIONVARIANT = "defaultQuestionVariant", int, 0, "testgen"
    INCLUDEINCATS = "includeCats", bool, False, "testgen"
    TOLERANCE = "tolerance", float, 0.01, "parser/nf"
    PICTUREFOLDER = "pictureFolder", Path, None, "core"
    PICTURESUBFOLDER = "imgfolder", str, "Abbildungen", "project"
    SPREADSHEETPATH = "spreadsheetFolder", Path, None, "core"
    LOGLEVEL = "loglevel", str, "INFO", "core"
    LOGFILE = "logfile", str, "excel2moodleLogFile.log", "core"
    CATEGORIESSHEET = "categoriessheet", str, "Kategorien", "core"

    IMPORTMODULE = "importmodule", str, None
    TEXT = "text", list, None
    BPOINTS = "bulletpoint", list, None
    TRUE = "true", list, None
    FALSE = "false", list, None
    TYPE = "type", str, None
    NAME = "name", str, None
    RESULT = "result", float, None
    EQUATION = "formula", str, None
    PICTURE = "picture", str, False
    NUMBER = "number", int, None
    ANSTYPE = "answertype", str, None
    QUESTIONPART = "part", list, None
    PARTTYPE = "parttype", str, None
    VERSION = "version", int, 1
    POINTS = "points", float, 1.0
    PICTUREWIDTH = "imgwidth", int, 500
    ANSPICWIDTH = "answerimgwidth", int, 120
    WRONGSIGNPERCENT = "wrongsignpercentage", int, 50
    FIRSTRESULT = "firstresult", float, None


class Settings(QSettings):
    """Settings for Excel2moodle."""

    shPathChanged = Signal(Path)
    localSettings: ClassVar[dict[str, str | float | Path]] = {}

    def __init__(self) -> None:
        """Instantiate the settings."""
        super().__init__("jbosse3", "excel2moodle")
        if excel2moodle.isMainState():
            logger.info("Settings are stored under: %s", self.fileName())
            if self.contains(Tags.SPREADSHEETPATH.full):
                self.sheet = self.get(Tags.SPREADSHEETPATH)
                if self.sheet.is_file():
                    QTimer.singleShot(300, self._emitSpreadsheetChanged)

    def _emitSpreadsheetChanged(self) -> None:
        self.shPathChanged.emit(self.sheet)

    @overload
    def get(
        self,
        key: Literal[Tags.POINTS],
    ) -> float: ...
    @overload
    def get(
        self,
        key: Literal[
            Tags.QUESTIONVARIANT,
            Tags.TOLERANCE,
            Tags.VERSION,
            Tags.PICTUREWIDTH,
            Tags.ANSPICWIDTH,
            Tags.WRONGSIGNPERCENT,
        ],
    ) -> int: ...
    @overload
    def get(self, key: Literal[Tags.INCLUDEINCATS]) -> bool: ...
    @overload
    def get(
        self,
        key: Literal[
            Tags.PICTURESUBFOLDER,
            Tags.LOGLEVEL,
            Tags.LOGFILE,
            Tags.CATEGORIESSHEET,
            Tags.IMPORTMODULE,
        ],
    ) -> str: ...
    @overload
    def get(
        self,
        key: Literal[Tags.PICTUREFOLDER, Tags.SPREADSHEETPATH],
    ) -> Path: ...

    def get(self, key: Tags):
        """Get the typesafe settings value.

        If local Settings are stored, they are returned.
        If no setting is made, the default value is returned.
        """
        if key in type(self).localSettings:
            val = key.typ()(type(self).localSettings[key])
            logger.debug("Returning project setting: %s = %s", key, val)
            return val
        if not excel2moodle.isMainState():
            logger.warning("No GUI: Returning default value.")
            return key.default
        if key.typ() is Path:
            path: Path = self.value(key.full, defaultValue=key.default)
            try:
                path.resolve(strict=True)
            except ValueError:
                logger.warning(
                    f"The settingsvalue {key} couldn't be fetched with correct typ",
                )
                return key.default
            logger.debug("Returning path setting: %s = %s", key, path)
            return path
        raw = self.value(key.full, defaultValue=key.default, type=key.typ())
        logger.debug("read a settings Value: %s of type: %s", key, key.typ())
        try:
            logger.debug("Returning global setting: %s = %s", key, raw)
            return key.typ()(raw)
        except (ValueError, TypeError):
            logger.warning(
                f"The settingsvalue {key} couldn't be fetched with correct typ",
            )
            return key.default

    def set(
        self,
        key: Tags | str,
        value: float | bool | Path | str,
        local: bool = False,
    ) -> None:
        """Set the setting to value.

        Parameters
        ----------
        local
            True saves local project specific settings.
            Defaults to False
            The local settings are meant to be set in the first sheet `settings`

        """
        if not excel2moodle.isMainState():
            local = True
        if local:
            if key in Tags:
                type(self).localSettings[key] = value
                logger.info("Saved the project setting %s = %s", key, value)
            else:
                logger.warning("got invalid local Setting %s = %s", key, value)
            return
        if not local and isinstance(key, Tags):
            if not isinstance(value, key.typ()):
                logger.error("trying to save setting with wrong type not possible")
                return
            self.setValue(key.full, value)
            logger.info("Saved the global setting %s = %s", key, value)

    def setSpreadsheet(self, sheet: Path) -> None:
        """Save spreadsheet path and emit the changed event."""
        if isinstance(sheet, Path):
            self.sheet = sheet.resolve(strict=True)
            logpath = str(self.sheet.parent / "excel2moodleLogFile.log")
            self.set(Tags.LOGFILE, logpath)
            self.set(Tags.SPREADSHEETPATH, self.sheet)
            self.shPathChanged.emit(sheet)
            return
