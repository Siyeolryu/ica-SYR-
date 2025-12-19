"""
yahooquery Screener 테스트
"""
from yahooquery import Screener

print("=" * 60)
print("yahooquery Screener 테스트")
print("=" * 60)

try:
    # Screener 인스턴스 생성
    screener = Screener()
    print("\n[OK] Screener 인스턴스 생성 완료")

    # 스크리너 데이터 조회
    print("\n스크리너 데이터 조회 중...")
    data = screener.get_screeners(['most_actives'], count=3)

    print(f"\n데이터 타입: {type(data)}")
    print(f"데이터 내용:")
    print(data)

    # dict인 경우
    if isinstance(data, dict):
        print("\n[OK] 데이터는 dict 형식입니다")
        print(f"키 목록: {list(data.keys())}")

        if 'most_actives' in data:
            print("\n[OK] 'most_actives' 키 존재")
            print(f"most_actives 데이터 타입: {type(data['most_actives'])}")
            print(f"most_actives 키 목록: {list(data['most_actives'].keys())}")

            if 'quotes' in data['most_actives']:
                quotes = data['most_actives']['quotes']
                print(f"\n[OK] quotes 개수: {len(quotes)}")
                print(f"\n첫 번째 종목:")
                print(quotes[0])

    # DataFrame인 경우
    elif hasattr(data, 'empty'):
        print("\n[OK] 데이터는 DataFrame 형식입니다")
        print(f"행 수: {len(data)}")
        print(f"열 목록: {data.columns.tolist()}")
        print(f"\n첫 번째 행:")
        print(data.iloc[0].to_dict())

except Exception as e:
    print(f"\n[ERROR] 오류 발생: {str(e)}")
    import traceback
    traceback.print_exc()
