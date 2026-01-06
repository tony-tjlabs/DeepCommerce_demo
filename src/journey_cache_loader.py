"""
Journey Analysis Cache Loading Functions
캐시 기반 빠른 데이터 로딩 함수들
"""
import streamlit as st
import pandas as pd
import json
from pathlib import Path
from typing import Dict, Optional


# Cache directory (src/ 폴더 안에서 실행되므로 parent.parent 사용)
PROJECT_ROOT = Path(__file__).parent.parent
JOURNEY_CACHE_DIR = PROJECT_ROOT / 'Data' / 'Cache' / 'Journey'


@st.cache_data(ttl=3600)
def load_zone_transitions() -> Optional[pd.DataFrame]:
    """
    캐시된 zone transition 데이터 로드
    
    Returns:
        DataFrame with columns:
        - from_zone, to_zone, weekday, weather, time_bucket
        - count, avg_dwell_time, probability
    """
    cache_file = JOURNEY_CACHE_DIR / 'zone_transitions.parquet'
    
    if not cache_file.exists():
        return None
    
    return pd.read_parquet(cache_file)


@st.cache_data(ttl=3600)
def load_zone_statistics() -> Optional[Dict]:
    """
    캐시된 zone 통계 로드
    
    Returns:
        Dict with zone statistics:
        - total_outflow, total_inflow
        - outflow_zones, inflow_zones
        - peak_weekday, weather_counts, time_counts
    """
    cache_file = JOURNEY_CACHE_DIR / 'zone_statistics.json'
    
    if not cache_file.exists():
        return None
    
    with open(cache_file, 'r', encoding='utf-8') as f:
        return json.load(f)


@st.cache_data(ttl=3600)
def load_journey_predictions() -> Optional[pd.DataFrame]:
    """
    캐시된 journey 예측 로드
    
    Returns:
        DataFrame with columns:
        - start_zone, weekday, weather, time_bucket, context_key
        - step, predicted_zone, probability
    """
    cache_file = JOURNEY_CACHE_DIR / 'journey_predictions.parquet'
    
    if not cache_file.exists():
        return None
    
    return pd.read_parquet(cache_file)


@st.cache_data(ttl=3600)
def load_comparative_analysis() -> Optional[pd.DataFrame]:
    """
    캐시된 비교 분석 데이터 로드
    
    Returns:
        DataFrame with weekday/weather/time comparisons per zone
    """
    cache_file = JOURNEY_CACHE_DIR / 'comparative_analysis.parquet'
    
    if not cache_file.exists():
        return None
    
    return pd.read_parquet(cache_file)


@st.cache_data(ttl=3600)
def load_model_info() -> Optional[Dict]:
    """
    캐시된 모델 정보 로드
    
    Returns:
        Dict with model info:
        - zones, num_zones, config, training_info
    """
    cache_file = JOURNEY_CACHE_DIR / 'model_info.json'
    
    if not cache_file.exists():
        return None
    
    with open(cache_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def check_cache_status() -> Dict:
    """
    캐시 상태 확인
    
    Returns:
        Dict with cache file status
    """
    files = [
        'zone_transitions.parquet',
        'zone_statistics.json',
        'journey_predictions.parquet',
        'comparative_analysis.parquet',
        'model_info.json'
    ]
    
    status = {
        'cache_dir': str(JOURNEY_CACHE_DIR),
        'exists': JOURNEY_CACHE_DIR.exists(),
        'files': {}
    }
    
    for f in files:
        path = JOURNEY_CACHE_DIR / f
        status['files'][f] = {
            'exists': path.exists(),
            'size_kb': path.stat().st_size / 1024 if path.exists() else 0
        }
    
    return status


def get_filtered_transitions(
    transitions_df: pd.DataFrame,
    weekday: Optional[int] = None,
    weather: Optional[str] = None,
    time_bucket: Optional[str] = None
) -> pd.DataFrame:
    """
    필터링된 transition 데이터 반환
    
    Args:
        transitions_df: Full transitions DataFrame
        weekday: Filter by weekday (0-6)
        weather: Filter by weather (Clear, Rainy, Cloudy)
        time_bucket: Filter by time (morning, afternoon, evening)
    
    Returns:
        Filtered DataFrame
    """
    if transitions_df is None or len(transitions_df) == 0:
        return pd.DataFrame()
    
    filtered = transitions_df.copy()
    
    if weekday is not None:
        filtered = filtered[filtered['weekday'] == weekday]
    
    if weather is not None:
        filtered = filtered[filtered['weather'] == weather]
    
    if time_bucket is not None:
        filtered = filtered[filtered['time_bucket'] == time_bucket]
    
    return filtered


def get_filtered_transitions_with_fallback(
    transitions_df: pd.DataFrame,
    weekday: Optional[int] = None,
    weather: Optional[str] = None,
    time_bucket: Optional[str] = None
) -> tuple:
    """
    필터링된 transition 데이터 반환 (Fallback 지원)
    
    정확히 일치하는 Context가 없으면 유사한 Context로 대체합니다:
    1. 정확한 매치 시도 (weekday + weather + time_bucket)
    2. 날씨만 변경 (Fallback 1)
    3. 시간대만 변경 (Fallback 2)
    4. 날씨 + 시간대 변경 (Fallback 3)
    5. 해당 요일 전체 데이터 (Last Resort)
    
    Returns:
        Tuple of (DataFrame, fallback_message or None)
    """
    if transitions_df is None or len(transitions_df) == 0:
        return pd.DataFrame(), None
    
    weekday_names = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
    weather_names_kr = {'Clear': '맑음', 'Sunny': '맑음', 'Rainy': '비', 'Cloudy': '흐림'}
    time_names_kr = {'morning': '오전', 'afternoon': '오후', 'evening': '저녁'}
    
    def try_filter(wd, wt, tb):
        filtered = transitions_df.copy()
        if wd is not None:
            filtered = filtered[filtered['weekday'] == wd]
        if wt is not None:
            filtered = filtered[filtered['weather'] == wt]
        if tb is not None:
            filtered = filtered[filtered['time_bucket'] == tb]
        return filtered
    
    # 1. 정확한 매치 시도
    result = try_filter(weekday, weather, time_bucket)
    if len(result) > 0:
        return result, None
    
    # Fallback 시작
    available_weathers = transitions_df['weather'].unique().tolist() if 'weather' in transitions_df.columns else []
    available_times = transitions_df['time_bucket'].unique().tolist() if 'time_bucket' in transitions_df.columns else []
    
    # 2. 다른 날씨로 시도 (우선순위: Cloudy > Clear > Rainy)
    weather_fallback_order = ['Cloudy', 'Clear', 'Rainy']
    if weather is not None:
        weather_fallback_order = [w for w in weather_fallback_order if w != weather and w in available_weathers]
    
    for alt_weather in weather_fallback_order:
        result = try_filter(weekday, alt_weather, time_bucket)
        if len(result) > 0:
            original_wt = weather_names_kr.get(weather, weather) if weather else '전체'
            fallback_wt = weather_names_kr.get(alt_weather, alt_weather)
            msg = f"ℹ️ **Fallback 적용**: '{original_wt}' 데이터가 없어 '{fallback_wt}' 데이터를 사용합니다."
            return result, msg
    
    # 3. 다른 시간대로 시도 (우선순위: afternoon > morning > evening)
    time_fallback_order = ['afternoon', 'morning', 'evening']
    if time_bucket is not None:
        time_fallback_order = [t for t in time_fallback_order if t != time_bucket and t in available_times]
    
    for alt_time in time_fallback_order:
        result = try_filter(weekday, weather, alt_time)
        if len(result) > 0:
            original_tb = time_names_kr.get(time_bucket, time_bucket) if time_bucket else '전체'
            fallback_tb = time_names_kr.get(alt_time, alt_time)
            msg = f"ℹ️ **Fallback 적용**: '{original_tb}' 데이터가 없어 '{fallback_tb}' 데이터를 사용합니다."
            return result, msg
    
    # 4. 날씨 + 시간대 모두 변경
    for alt_weather in weather_fallback_order:
        for alt_time in time_fallback_order:
            result = try_filter(weekday, alt_weather, alt_time)
            if len(result) > 0:
                original_context = f"{weather_names_kr.get(weather, weather) if weather else ''} {time_names_kr.get(time_bucket, time_bucket) if time_bucket else ''}".strip()
                fallback_context = f"{weather_names_kr.get(alt_weather, alt_weather)} {time_names_kr.get(alt_time, alt_time)}"
                wd_name = weekday_names[weekday] if weekday is not None else '전체'
                msg = f"ℹ️ **Fallback 적용**: {wd_name} '{original_context}' 데이터가 없어 '{fallback_context}' 데이터를 사용합니다."
                return result, msg
    
    # 5. 해당 요일 전체 데이터 (날씨/시간 무관)
    if weekday is not None:
        result = try_filter(weekday, None, None)
        if len(result) > 0:
            wd_name = weekday_names[weekday]
            msg = f"ℹ️ **Fallback 적용**: 정확한 맥락 데이터가 없어 '{wd_name}' 전체 데이터를 사용합니다."
            return result, msg
    
    # 6. 데이터 없음
    return pd.DataFrame(), "⚠️ 선택한 조건에 해당하는 데이터가 없습니다."


def get_zone_outflow_with_fallback(
    zone: str,
    transitions_df: pd.DataFrame,
    weekday: Optional[int] = None,
    weather: Optional[str] = None,
    time_bucket: Optional[str] = None
) -> tuple:
    """
    특정 zone에서 나가는 확률 분포 (Fallback 지원)
    
    Returns:
        Tuple of (Dict[str, float], fallback_message or None)
    """
    filtered, fallback_msg = get_filtered_transitions_with_fallback(
        transitions_df, weekday, weather, time_bucket
    )
    
    zone_outflow = filtered[filtered['from_zone'] == zone]
    
    if len(zone_outflow) == 0:
        return {}, fallback_msg
    
    # Calculate probability
    total = zone_outflow['count'].sum()
    probs = zone_outflow.groupby('to_zone')['count'].sum() / total
    
    return probs.to_dict(), fallback_msg


def get_zone_inflow_with_fallback(
    zone: str,
    transitions_df: pd.DataFrame,
    weekday: Optional[int] = None,
    weather: Optional[str] = None,
    time_bucket: Optional[str] = None
) -> tuple:
    """
    특정 zone으로 들어오는 확률 분포 (Fallback 지원)
    
    Returns:
        Tuple of (Dict[str, float], fallback_message or None)
    """
    filtered, fallback_msg = get_filtered_transitions_with_fallback(
        transitions_df, weekday, weather, time_bucket
    )
    
    zone_inflow = filtered[filtered['to_zone'] == zone]
    
    if len(zone_inflow) == 0:
        return {}, fallback_msg
    
    # Calculate probability
    total = zone_inflow['count'].sum()
    probs = zone_inflow.groupby('from_zone')['count'].sum() / total
    
    return probs.to_dict(), fallback_msg


def get_zone_outflow_probabilities(
    zone: str,
    transitions_df: pd.DataFrame,
    weekday: Optional[int] = None,
    weather: Optional[str] = None,
    time_bucket: Optional[str] = None
) -> Dict[str, float]:
    """
    특정 zone에서 나가는 확률 분포
    
    Args:
        zone: Source zone
        transitions_df: Transitions DataFrame
        weekday, weather, time_bucket: Context filters
    
    Returns:
        Dict of {next_zone: probability}
    """
    filtered = get_filtered_transitions(
        transitions_df, weekday, weather, time_bucket
    )
    
    zone_outflow = filtered[filtered['from_zone'] == zone]
    
    if len(zone_outflow) == 0:
        return {}
    
    # Recalculate probability for filtered context
    total = zone_outflow['count'].sum()
    probs = zone_outflow.groupby('to_zone')['count'].sum() / total
    
    return probs.to_dict()


def get_zone_inflow_sources(
    zone: str,
    transitions_df: pd.DataFrame,
    weekday: Optional[int] = None,
    weather: Optional[str] = None,
    time_bucket: Optional[str] = None
) -> Dict[str, float]:
    """
    특정 zone으로 들어오는 확률 분포 (역방향)
    
    Args:
        zone: Target zone
        transitions_df: Transitions DataFrame
        weekday, weather, time_bucket: Context filters
    
    Returns:
        Dict of {source_zone: probability}
    """
    filtered = get_filtered_transitions(
        transitions_df, weekday, weather, time_bucket
    )
    
    zone_inflow = filtered[filtered['to_zone'] == zone]
    
    if len(zone_inflow) == 0:
        return {}
    
    # Calculate probability
    total = zone_inflow['count'].sum()
    probs = zone_inflow.groupby('from_zone')['count'].sum() / total
    
    return probs.to_dict()


def get_journey_prediction(
    predictions_df: pd.DataFrame,
    start_zone: str,
    weekday: int,
    weather: str,
    time_bucket: str
) -> pd.DataFrame:
    """
    특정 조건에서의 journey 예측 조회
    
    Args:
        predictions_df: Predictions DataFrame
        start_zone: Starting zone
        weekday: Day of week (0-6)
        weather: Weather condition
        time_bucket: Time period
    
    Returns:
        DataFrame with predicted journey steps
    """
    if predictions_df is None:
        return pd.DataFrame()
    
    context_key = f"wd{weekday}_{weather}_{time_bucket}"
    
    filtered = predictions_df[
        (predictions_df['start_zone'] == start_zone) &
        (predictions_df['context_key'] == context_key)
    ].sort_values('step')
    
    return filtered


def get_weekday_comparison(
    zone: str,
    comp_df: pd.DataFrame
) -> Dict[int, int]:
    """
    Zone의 요일별 트래픽 비교
    
    Returns:
        Dict of {weekday: traffic_count}
    """
    if comp_df is None or len(comp_df) == 0:
        return {}
    
    zone_data = comp_df[comp_df['zone'] == zone]
    
    if len(zone_data) == 0:
        return {}
    
    return {
        i: int(zone_data[f'weekday_{i}'].iloc[0])
        for i in range(7)
    }


def get_weather_comparison(
    zone: str,
    comp_df: pd.DataFrame
) -> Dict[str, int]:
    """
    Zone의 날씨별 트래픽 비교
    
    Returns:
        Dict of {weather: traffic_count}
    """
    if comp_df is None or len(comp_df) == 0:
        return {}
    
    zone_data = comp_df[comp_df['zone'] == zone]
    
    if len(zone_data) == 0:
        return {}
    
    return {
        w: int(zone_data[f'weather_{w}'].iloc[0])
        for w in ['Clear', 'Rainy', 'Cloudy']
        if f'weather_{w}' in comp_df.columns
    }
