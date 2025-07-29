# 기본 데모 (Basic Demo)

🎼 **기본 데모**는 Gradio PianoRoll 컴포넌트의 가장 기본적인 사용법을 보여줍니다.
피아노롤 인터페이스를 통해 음표를 생성, 편집, 삭제하는 방법과 데이터 구조를 이해할 수 있습니다.

## 🎯 학습 목표

- PianoRoll 컴포넌트의 기본 개념 이해
- 음표 데이터 구조 파악
- 마우스와 키보드를 이용한 기본 조작법
- JSON 데이터 출력 확인

## 📋 전체 코드

```python
import gradio as gr
from gradio_pianoroll import PianoRoll

def convert_basic(piano_roll):
    """Basic conversion function (first tab)"""
    print("=== Basic Convert function called ===")
    print("Received piano_roll:")
    print(piano_roll)
    print("Type:", type(piano_roll))
    return piano_roll

with gr.Blocks(title="PianoRoll Basic Demo") as demo:
    gr.Markdown("# 🎹 기본 PianoRoll 데모")
    gr.Markdown("피아노롤 컴포넌트의 기본 기능을 테스트해보세요!")

    with gr.Row():
        with gr.Column():
            # 초기값 설정
            initial_value_basic = {
                "notes": [
                    {
                        "start": 80,
                        "duration": 80,
                        "pitch": 60,  # C4
                        "velocity": 100,
                        "lyric": "안녕"
                    },
                    {
                        "start": 160,
                        "duration": 160,
                        "pitch": 64,  # E4
                        "velocity": 90,
                        "lyric": "하세요"
                    }
                ],
                "tempo": 120,
                "timeSignature": {"numerator": 4, "denominator": 4},
                "editMode": "select",
                "snapSetting": "1/4"
            }

            piano_roll_basic = PianoRoll(
                height=600,
                width=1000,
                value=initial_value_basic,
                elem_id="piano_roll_basic",
                use_backend_audio=False  # 프론트엔드 오디오 엔진 사용
            )

    with gr.Row():
        with gr.Column():
            output_json_basic = gr.JSON(label="피아노롤 데이터")

    with gr.Row():
        with gr.Column():
            btn_basic = gr.Button("🔄 데이터 변환 및 디버그", variant="primary")

    # 이벤트 처리
    btn_basic.click(
        fn=convert_basic,
        inputs=piano_roll_basic,
        outputs=output_json_basic,
        show_progress=True
    )

if __name__ == "__main__":
    demo.launch()
```

## 🎹 주요 기능

### 1. 기본 인터페이스

#### 피아노롤 영역
- **가로축**: 시간 (픽셀 단위)
- **세로축**: 음높이 (MIDI 노트 번호)
- **그리드**: 박자와 음계에 맞춘 격자

#### 컨트롤 패널
- **편집 모드**: select (선택), create (생성), delete (삭제)
- **스냅 설정**: 1/4, 1/8, 1/16 박자 등
- **템포**: BPM (Beats Per Minute)

### 2. 음표 조작

#### 음표 생성
1. 편집 모드를 'create'로 설정
2. 원하는 위치에 마우스 클릭
3. 드래그하여 음표 길이 조정

#### 음표 선택 및 편집
1. 편집 모드를 'select'로 설정
2. 음표 클릭하여 선택
3. 드래그하여 위치 이동
4. 모서리 드래그하여 길이 조정

#### 음표 삭제
1. 편집 모드를 'delete'로 설정
2. 삭제할 음표 클릭

### 3. 키보드 단축키

| 키 | 기능 |
|---|---|
| `S` | Select 모드 |
| `C` | Create 모드 |
| `D` | Delete 모드 |
| `스페이스` | 재생/정지 |
| `Delete` | 선택된 음표 삭제 |

## 📊 데이터 구조

### 음표 객체 (Note Object)

```python
{
    "start": 80,        # 시작 위치 (픽셀)
    "duration": 80,     # 지속 시간 (픽셀)
    "pitch": 60,        # MIDI 노트 번호 (0-127)
    "velocity": 100,    # 세기 (0-127)
    "lyric": "안녕"     # 가사 (선택사항)
}
```

### 전체 피아노롤 데이터

```python
{
    "notes": [          # 음표 배열
        { /* 음표 객체 */ }
    ],
    "tempo": 120,       # 템포 (BPM)
    "timeSignature": {  # 박자표
        "numerator": 4,   # 분자
        "denominator": 4  # 분모
    },
    "editMode": "select",    # 편집 모드
    "snapSetting": "1/4",    # 스냅 설정
    "pixelsPerBeat": 80      # 박자당 픽셀 수
}
```

## 🔧 설정 옵션

### PianoRoll 컴포넌트 속성

```python
PianoRoll(
    height=600,              # 높이 (픽셀)
    width=1000,              # 너비 (픽셀)
    value=initial_value,     # 초기 데이터
    elem_id="unique_id",     # HTML 요소 ID
    use_backend_audio=False  # 오디오 엔진 선택
)
```

### 초기값 예제

```python
# 빈 피아노롤
empty_value = {
    "notes": [],
    "tempo": 120,
    "timeSignature": {"numerator": 4, "denominator": 4},
    "editMode": "select",
    "snapSetting": "1/4"
}

# C 메이저 스케일
c_major_scale = {
    "notes": [
        {"start": 0,   "duration": 80, "pitch": 60, "velocity": 100},  # C4
        {"start": 80,  "duration": 80, "pitch": 62, "velocity": 100},  # D4
        {"start": 160, "duration": 80, "pitch": 64, "velocity": 100},  # E4
        {"start": 240, "duration": 80, "pitch": 65, "velocity": 100},  # F4
        {"start": 320, "duration": 80, "pitch": 67, "velocity": 100},  # G4
        {"start": 400, "duration": 80, "pitch": 69, "velocity": 100},  # A4
        {"start": 480, "duration": 80, "pitch": 71, "velocity": 100},  # B4
        {"start": 560, "duration": 80, "pitch": 72, "velocity": 100},  # C5
    ],
    "tempo": 120,
    "timeSignature": {"numerator": 4, "denominator": 4},
    "editMode": "select",
    "snapSetting": "1/8"
}
```

## 🎵 MIDI 노트 번호 참조

| 옥타브 | C | C# | D | D# | E | F | F# | G | G# | A | A# | B |
|--------|---|----|----|----|----|----|----|----|----|----|----|---|
| 0 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 |
| 1 | 24 | 25 | 26 | 27 | 28 | 29 | 30 | 31 | 32 | 33 | 34 | 35 |
| 2 | 36 | 37 | 38 | 39 | 40 | 41 | 42 | 43 | 44 | 45 | 46 | 47 |
| 3 | 48 | 49 | 50 | 51 | 52 | 53 | 54 | 55 | 56 | 57 | 58 | 59 |
| 4 | 60 | 61 | 62 | 63 | 64 | 65 | 66 | 67 | 68 | 69 | 70 | 71 |
| 5 | 72 | 73 | 74 | 75 | 76 | 77 | 78 | 79 | 80 | 81 | 82 | 83 |

!!! note "참고"
    - **C4 (MIDI 60)**: 중앙 C (261.63 Hz)
    - **A4 (MIDI 69)**: 표준 A (440 Hz)

## 💡 실습 가이드

### 1. 기본 조작 연습

1. **음표 생성하기**
   - 편집 모드를 'create'로 설정
   - 빈 공간에 클릭하여 음표 생성
   - 다양한 위치와 길이로 여러 음표 만들기

2. **음표 편집하기**
   - 'select' 모드로 전환
   - 음표를 드래그하여 이동
   - 음표의 끝부분을 드래그하여 길이 조정

3. **음표 삭제하기**
   - 'delete' 모드로 전환
   - 삭제할 음표 클릭

### 2. 데이터 구조 이해

1. **JSON 출력 확인**
   - 음표를 수정한 후 "데이터 변환 및 디버그" 버튼 클릭
   - JSON 출력에서 변경사항 확인

2. **콘솔 로그 확인**
   - 브라우저 개발자 도구 열기 (F12)
   - Console 탭에서 상세 로그 확인

### 3. 실험해보기

- 템포 변경 (60, 120, 180 BPM)
- 박자표 변경 (3/4, 6/8 등)
- 다양한 스냅 설정 테스트
- 가사 입력해보기

## ❓ 문제 해결

### 자주 묻는 질문

**Q: 음표가 생성되지 않아요**
A: 편집 모드가 'create'로 설정되어 있는지 확인하세요.

**Q: 음표를 선택할 수 없어요**
A: 편집 모드를 'select'로 변경하세요.

**Q: 키보드 단축키가 작동하지 않아요**
A: 피아노롤 영역을 먼저 클릭하여 포커스를 맞추세요.

### 일반적인 문제

1. **브라우저 호환성**: Chrome, Firefox, Safari 권장
2. **JavaScript 오류**: 브라우저 콘솔 확인
3. **데이터 형식**: JSON 형식이 올바른지 검증

## 🔗 다음 단계

기본 기능을 익혔다면 다음 예제들을 확인해보세요:

- **[신디사이저 데모](synthesizer.md)**: 오디오 합성 기능
- **[음성학 처리](phoneme-processing.md)**: G2P 변환 기능
- **[API 참조](../api/components.md)**: 상세한 컴포넌트 명세