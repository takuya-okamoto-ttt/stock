import pandas as pd
import yfinance as yf
import altair as alt
import streamlit as st

st.title('米国株価、ETF（セクター別他）、仮想通貨 可視化アプリ')

st.sidebar.write("""
# 米国株価、ETF、仮想通貨
株価可視化ツールです。
以下のオプションから表示日数を指定できます。
""")

st.sidebar.write("""
## 表示日数選択
""")

days = st.sidebar.slider('日数', 1, 360, 180)

st.write(f"""
### 過去 **{days}日間** の株価
""")

@st.cache
def get_data(days, tickers):
    df = pd.DataFrame()
    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])
        hist = tkr.history(period=f'{days}d')
        hist.index = hist.index.strftime('%d %B %Y')
        hist = hist[['Close']]
        hist.columns = [company]
        hist = hist.T
        hist.index.name = 'Name'
        df = pd.concat([df, hist])
    return df

try:
    st.sidebar.write("""
    ## 株価の範囲指定
    """)

    ymin, ymax = st.sidebar.slider(
        '範囲を指定してください。',
        0.0, 1400.0, (0.0, 1400.0)
    )

    tickers = {
        'google': 'GOOGL',
        'amazon': 'AMZN',
        'meta': 'META',
        'apple': 'AAPL',
        'microsoft': 'MSFT',
        'netflix': 'NFLX',
        'baidu': 'BIDU',
        'alibaba': 'BABA',
        'tencent': 'TCEHY',
        'berkshire': 'BRK-B',
        'tesla': 'TSLA',
        'nvidia': 'NVDA',
        'p&g': 'PG',
        'cocacola': 'KO',
        'pfizer': 'PFE',
        'mcdonalds': 'MCD',
        'accenture': 'ACN',
        'nike': 'NKE'
    }
    df = get_data(days, tickers)
    
    companies = st.multiselect(
        '会社名（米国株式）を選択してください。',
        list(df.index),
        ['google', 'amazon', 'meta', 'apple', 'microsoft', 'netflix',
         'baidu', 'alibaba', 'tencent', 'berkshire', 'tesla', 'nvidia',
         'p&g', 'cocacola', 'pfizer', 'mcdonalds', 'accenture', 'nike']
    )

    if not companies:
        st.error('少なくとも一社は選んでください。')
    else:
        data = df.loc[companies]
        st.write("### 株価（USD）", data.sort_index())
        data = data.T.reset_index()
        data = pd.melt(data, id_vars=['Date']).rename(
            columns={'value': 'Stock Prices(USD)'}
        )

        chart = (
            alt.Chart(data)
            .mark_line(opacity=0.8, clip=True)
            .encode(
                x="Date:T",
                y=alt.Y("Stock Prices(USD):Q", stack=None, scale=alt.Scale(domain=[ymin, ymax])),
                color='Name:N'
            )
        )
        st.altair_chart(chart, use_container_width=True)
except:
    st.error(
        "エラーが起きているようです。少々お待ちください。"
    )

@st.cache
def get_data(days, tickers):
    df = pd.DataFrame()
    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])
        hist = tkr.history(period=f'{days}d')
        hist.index = hist.index.strftime('%d %B %Y')
        hist = hist[['Close']]
        hist.columns = [company]
        hist = hist.T
        hist.index.name = 'Name'
        df = pd.concat([df, hist])
    return df

try:
    tickers = {
        'エネルギー(VDE)': 'VDE',
        '素材(VAW)': 'VAW',
        '資本財(VIS)': 'VIS',
        '一般消費財(VCR)': 'VCR',
        '生活必需品(VDC)': 'VDC',
        'ヘルスケア(VHT)': 'VHT',
        '金融(VFH)': 'VFH',
        '情報技術(VGT)': 'VGT',
        'コミュニケーションサービス(VOX)': 'VOX',
        '公益事業(VPU)': 'VPU',
        '不動産(VNQ)': 'VNQ',
        'ゴールド(GLD)': 'GLD',
        'シルバー(SLV)': 'SLV',
        'プラチナ(PPLT)': 'PPLT',
        '原油(USO)': 'USO',
        '天然ガス(UNG)': 'UNG',
        '米国債20年(TLT)': 'TLT',
        '高配当(SPYD)': 'SPYD',
        '高配当(HDV)': 'HDV',
        '高配当(VYM)': 'VYM'
    }
    df = get_data(days, tickers)
    
    companies = st.multiselect(
        'ETF名を選択してください。',
        list(df.index),
          ['エネルギー(VDE)', '素材(VAW)', '資本財(VIS)', '一般消費財(VCR)', '生活必需品(VDC)', 'ヘルスケア(VHT)',
          '金融(VFH)', '情報技術(VGT)', 'コミュニケーションサービス(VOX)', '公益事業(VPU)', '不動産(VNQ)',
          'ゴールド(GLD)','シルバー(SLV)','プラチナ(PPLT)','原油(USO)','天然ガス(UNG)',
          '米国債20年(TLT)','高配当(SPYD)', '高配当(HDV)', '高配当(VYM)']
    )

    if not companies:
        st.error('少なくとも一社は選んでください。')
    else:
        data = df.loc[companies]
        st.write("### 株価（USD）", data.sort_index())
        data = data.T.reset_index()
        data = pd.melt(data, id_vars=['Date']).rename(
            columns={'value': 'Stock Prices(USD)'}
        )

        chart = (
            alt.Chart(data)
            .mark_line(opacity=0.8, clip=True)
            .encode(
                x="Date:T",
                y=alt.Y("Stock Prices(USD):Q", stack=None, scale=alt.Scale(domain=[ymin, ymax])),
                color='Name:N'
            )
        )
        st.altair_chart(chart, use_container_width=True)
except:
    st.error(
        "エラーが起きているようです。少々お待ちください。"
    )

    
@st.cache
def get_data(days, tickers):
    df = pd.DataFrame()
    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])
        hist = tkr.history(period=f'{days}d')
        hist.index = hist.index.strftime('%d %B %Y')
        hist = hist[['Close']]
        hist.columns = [company]
        hist = hist.T
        hist.index.name = 'Name'
        df = pd.concat([df, hist])
    return df

try:
    tickers = {
        'Bitcoin': 'BTC-USD',
        'Ethereum': 'ETH-USD',
        'XRP': 'XRP-USD',
        'Litecoin': 'LTC-USD',
        'BinanceCoin': 'BNB-USD',
        'Cardano': 'ADA-USD',
        'Dogecoin': 'DOGE-USD',
        'Polkadot': 'DOT-USD'
    }
    df = get_data(days, tickers)
    
    companies = st.multiselect(
        '仮想通貨名を選択してください。',
        list(df.index),
          ['Bitcoin', 'Ethereum', 'XRP', 'Litecoin', 
          'BinanceCoin', 'Cardano','Dogecoin', 'Polkadot']
    )

    if not companies:
        st.error('少なくとも一社は選んでください。')
    else:
        data = df.loc[companies]
        st.write("### 価格（USD）", data.sort_index())
        data = data.T.reset_index()
        data = pd.melt(data, id_vars=['Date']).rename(
            columns={'value': 'Stock Prices(USD)'}
        )

        chart = (
            alt.Chart(data)
            .mark_line(opacity=0.8, clip=True)
            .encode(
                x="Date:T",
                y=alt.Y("Stock Prices(USD):Q", stack=None, scale=alt.Scale(domain=[ymin, ymax])),
                color='Name:N'
            )
        )
        st.altair_chart(chart, use_container_width=True)
except:
    st.error(
        "エラーが起きているようです。少々お待ちください。"
    )