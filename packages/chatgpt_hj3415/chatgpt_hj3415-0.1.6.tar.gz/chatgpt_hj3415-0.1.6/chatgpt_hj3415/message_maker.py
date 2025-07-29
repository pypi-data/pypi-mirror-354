from typing import Dict, List, Iterator
from db_hj3415 import myredis
from utils_hj3415.tools import replace_nan_to_none, to_int
import pandas as pd

def _make_table_data(cxxx) -> Dict[str, List[dict]]:
    # C103, C104, C106 의 전체 테이블의 열을 반환한다.
    rows_per_page = {}
    for page in cxxx.PAGES:
        cxxx.page = page
        rows_per_page[page] = replace_nan_to_none(cxxx.list_rows())
        # print(rows_per_page[page])
    return rows_per_page

def to_csv(records: List[dict], cleaning: bool = True)-> str:
    df = pd.DataFrame(records)
    df.set_index('항목', inplace=True)

    if cleaning:
        # 모든 값이 NaN(또는 빈 문자열 등)인 행 삭제
        df_cleaned = df.dropna(how='all', axis=1)  # 열 전체가 NaN일 경우 열 제거
        df_cleaned = df_cleaned.dropna(how='all', axis=0)  # 행 전체가 NaN일 경우 행 제거

        # 또는 아래와 같이 빈 셀('')로 이루어진 행 제거도 가능
        df_cleaned = df_cleaned.loc[~(df_cleaned == '').all(axis=1)]

        csv_text = df_cleaned.to_csv(index=True)
    else:
        csv_text = df.to_csv(index=True)
    return csv_text

def get_c103_data(code:str)-> Iterator[tuple[str, str]]:
    c103 = myredis.C103(code, 'c103손익계산서q')
    data = _make_table_data(c103)

    for page, records in data.items():
        yield page, to_csv(records, cleaning=True)

def get_c104_data(code: str)-> Iterator[tuple[str, str]]:
    c104 = myredis.C104(code, 'c104q')
    data = _make_table_data(c104)

    for page, records in data.items():
        yield page, to_csv(records, cleaning=True)

def get_c106_data(code: str)-> Iterator[tuple[str, str]]:
    c106 = myredis.C106(code, 'c106q')
    data = _make_table_data(c106)

    for page, records in data.items():
        yield page, to_csv(records, cleaning=True)

def get_c101_chart_data(code: str, last_days) -> list:
    trend = myredis.C101(code).get_trend('주가')
    data = []
    """
    {'2025.02.18': '55376', '2025.02.19': 57981.0} 
    -> [{'x': '2025-02-18', 'y': '55376'}, {'x': '2025-02-19', 'y': '57981.0'}]
    """
    for x, y in trend.items():
        data.append({'x': str(x).replace("'", '"').replace(".", "-"),
                     'y': to_int(str(y).replace("'", ""))})
    return data[-last_days:]

def make_messages(code:str, last_days:int = 60) -> List[dict]:
    name = myredis.C101(code).get_name()
    csv_103 = ""
    for page, records in get_c103_data(code):
        if page.endswith('y'):
            page = page[4:-1] + "(연간)"
        elif page.endswith('q'):
            page = page[4:-1] + "(분기)"
        else:
            page = page[4:-1]
        csv_103 += f"{page} - {records}\n"
    csv_104 = ""
    for page, records in get_c104_data(code):
        if page.endswith('y'):
            page = "투자지표(연간)"
        elif page.endswith('q'):
            page = "투자지표(분기)"
        else:
            page = "투자지표"
        csv_104 += f"{page} - {records}\n"
    csv_106 = ""
    for page, records in get_c106_data(code):
        if page.endswith('y'):
            page = "동종업종비교(연간)"
        elif page.endswith('q'):
            page = "동종업종비교(분기)"
        else:
            page = "동종업종비교"
        csv_106 += f"{page} - {records}\n"
    chart_data = f"직전{last_days}일간 주가 추이: {get_c101_chart_data(code, last_days=last_days)}"

    content = (f"{name}({code})의 다음의 데이터(재무분석, 투자지표, 업종비교, 주가)와 이외의 관련 정보(산업 동향, 경기 사이클 등)를 바탕으로,"
               f"현재 기업의 상황을 항목별로 구체적으로 분석해 줘. 또한, 향후 주가에 대한 보수적/낙관적 관점에서 합리적인 시나리오를 "
               f"제시해 주고 어떤 시나리오의 가능성이 높은지 예측해줘.\n"
               f"{csv_103}"
               f"{csv_104}"
               f"{csv_106}"
               f"{chart_data}")

    return [
        {"role": "system",
         "content": "당신은 한국어를 사용하는 금융 애널리스트입니다. 주식에 대해 잘 모르는 고객에게 설명하듯 친절하고 쉽게 안내해 주세요."},
        {"role": "user",
         "content": content},
    ]