# Retail Store Location Analytics System

Streamlit 기반의 소매점 위치 분석 대시보드 시스템입니다.

## 프로젝트 구조

```
Code_DeepSpace/
├── Data/                          # 데이터 폴더
│   ├── Day_description/          # 날씨 및 날짜 정보
│   ├── Map/                      # 매장 지도 이미지
│   ├── Rawdata/                  # 원시 신호 데이터
│   └── SWard_description/        # S-Ward 설명
├── src/                          # 소스 코드
│   ├── config/                   # 설정 파일
│   │   └── settings.py          # 전역 설정
│   ├── data_loader/             # 데이터 로딩
│   │   └── loader.py            # 데이터 로더 클래스
│   ├── localization/            # 위치 계산
│   │   └── device_localizer.py  # 디바이스 위치 추정 알고리즘
│   ├── ui/                      # UI 컴포넌트
│   │   ├── components.py        # 재사용 가능한 UI 요소
│   │   └── pages.py             # 페이지 로직
│   ├── utils/                   # 유틸리티
│   │   └── helpers.py           # 헬퍼 함수
│   ├── visualization/           # 시각화
│   │   └── map_visualizer.py    # 지도 시각화 클래스
│   └── main.py                  # 메인 애플리케이션
└── main.py                       # 실행 진입점
```

## 주요 기능

### 1. Daily Localization (일일 위치 추적)
- 날짜별 디바이스 위치 계산
- RSSI 기반 가중 중심 알고리즘
- EMA 스무딩 적용
- 실시간 지도 시각화

### 2. Analytics (분석)
- 디바이스 이동 궤적 표시
- 히트맵 생성
- 상세 통계 정보

### 3. Settings (설정)
- 데이터 경로 확인
- 시스템 상태 모니터링

## 설치 방법

```bash
# 필수 패키지 설치
pip install streamlit pandas numpy opencv-python pillow
```

## 실행 방법

```bash
# 대시보드 실행
streamlit run main.py

# 또는
python -m streamlit run main.py
```

## ⚠️ 중요 사항

### 지도 좌표계
- **좌측 상단이 (0, 0)**
- **X축: 좌 → 우 증가**
- **Y축: 상 → 하 증가**
- **픽셀 단위 좌표**
- **⚠️ 지도 이미지 크기/비율 절대 변경 금지!**

### 요일 정보
- 각 날짜의 요일 정보는 **매우 중요**
- `Data/Day_description/Day_Weather.csv`에서 관리
- 휴일, 영업일, 날씨 정보 포함

### 데이터 파일 경로
- S-Ward 설정: `Data/SWard_description/swards.csv`
- 날짜 정보: `Data/Day_description/Day_Weather.csv`
- 지도 이미지: `Data/Map/map_image.png`
- Raw 데이터: `Data/Rawdata/Lottemart_singal_YYYY-MM-DD_parsing.csv`

## 모듈 설명

### config/settings.py
- 전역 설정 및 경로 관리
- 색상, 크기 등 시각화 파라미터
- 좌표계 정의

### data_loader/loader.py
- 데이터 로딩 담당
- CSV, 이미지 파일 읽기
- 날짜 정보 관리

### localization/device_localizer.py
- 디바이스 위치 계산 알고리즘
- RSSI → 가중치 변환
- EMA 스무딩

### visualization/map_visualizer.py
- 지도 위 위치 시각화
- 궤적 표시
- 히트맵 생성

### ui/components.py
- 재사용 가능한 UI 컴포넌트
- 사이드바, 메트릭, 테이블 등

### ui/pages.py
- 각 탭의 페이지 로직
- 데이터 흐름 관리

## 디버깅 팁

각 모듈이 독립적으로 분리되어 있어 디버깅이 용이합니다:

1. **데이터 로딩 문제**: `data_loader/loader.py` 확인
2. **위치 계산 오류**: `localization/device_localizer.py` 확인
3. **시각화 이슈**: `visualization/map_visualizer.py` 확인
4. **UI 문제**: `ui/pages.py` 또는 `ui/components.py` 확인

## 향후 개선 사항

- [ ] 실시간 스트리밍 데이터 지원
- [ ] 더 많은 분석 기능 추가
- [ ] 데이터 내보내기 기능
- [ ] 사용자 정의 알고리즘 파라미터
- [ ] 다중 매장 지원
