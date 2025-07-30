from typing import Any, TypedDict

class TimeSignature(TypedDict):
    numerator: int
    denominator: int

class Note(TypedDict, total=False):
    id: str
    start: float
    duration: float
    pitch: int
    velocity: int
    startFlicks: float | None
    durationFlicks: float | None
    startSeconds: float | None
    durationSeconds: float | None
    endSeconds: float | None
    startBeats: float | None
    durationBeats: float | None
    startTicks: int | None
    durationTicks: int | None
    startSample: int | None
    durationSamples: int | None
    lyric: str | None
    phoneme: str | None

class LineDataPoint(TypedDict):
    x: float
    y: float

class LineLayerConfig(TypedDict, total=False):
    color: str
    lineWidth: float
    yMin: float
    yMax: float
    position: str | None
    renderMode: str | None
    visible: bool | None
    opacity: float | None
    dataType: str | None
    unit: str | None
    originalRange: dict[str, Any] | None
    data: list[LineDataPoint]

class PianoRollData(TypedDict, total=False):
    notes: list[Note]
    tempo: int
    timeSignature: TimeSignature
    editMode: str
    snapSetting: str
    pixelsPerBeat: float | None
    sampleRate: int | None
    ppqn: int | None
    audio_data: str | None
    curve_data: dict[str, Any] | None
    segment_data: list[dict[str, Any]] | None
    line_data: dict[str, LineLayerConfig] | None
    use_backend_audio: bool | None
    waveform_data: list[dict[str, float]] | None

def validate_note(note: dict[str, Any]) -> list[str]: ...
def validate_piano_roll_data(data: dict[str, Any]) -> list[str]: ...
def validate_and_warn(data: dict[str, Any], context: str = 'Piano roll data') -> dict[str, Any]: ...
def create_default_piano_roll_data() -> PianoRollData: ...
def ensure_note_ids(data: dict[str, Any]) -> dict[str, Any]: ...
def clean_piano_roll_data(data: dict[str, Any]) -> dict[str, Any]: ...
