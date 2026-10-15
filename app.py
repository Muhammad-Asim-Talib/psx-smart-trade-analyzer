import html
import math
import streamlit as st

st.set_page_config(page_title="FinPilot | PSX Trade Analyzer", page_icon="📈", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
:root { --navy:#142b45; --emerald:#0f9f78; --muted:#66778a; }
.stApp {background:#f3f6fa;color:#142b45;}
.block-container {max-width:1260px;padding-top:1.15rem;padding-bottom:.6rem;}
header[data-testid="stHeader"] {background:transparent;}
[data-testid="stToolbar"] {visibility:hidden;}
h1,h2,h3 {letter-spacing:-.035em;}
.brand {display:flex;align-items:center;gap:12px;margin-bottom:13px;}
.brand-icon {display:grid;place-items:center;background:#142b45;color:#64e0b5;border-radius:13px;width:44px;height:44px;font-size:25px;}
.brand-name {font-size:1.22rem;font-weight:800;color:#142b45;line-height:1.05;}
.brand-tag {font-size:.73rem;color:#738196;letter-spacing:.08em;margin-top:4px;}
.hero {background:linear-gradient(115deg,#142b45,#1c4564);border-radius:17px;padding:19px 24px;color:white;margin-bottom:13px;}
.hero-kicker {color:#6be0b8;font-size:.7rem;font-weight:800;letter-spacing:.13em;}
.hero-title {font-size:1.65rem;font-weight:800;letter-spacing:-.04em;margin:3px 0;line-height:1.12;}
.hero-sub {font-size:.86rem;color:#c8d8e5;}
.section-label {font-size:1rem;font-weight:800;color:#142b45;margin:0 0 4px;}
[data-testid="stForm"] {background:#fff;border:1px solid #e2e9f0;border-radius:15px;padding:14px 17px 9px;}
[data-testid="stForm"] label {font-size:.77rem;font-weight:650;color:#34495e;}
[data-testid="stForm"] [data-testid="stNumberInput"] input,
[data-testid="stForm"] [data-testid="stTextInput"] input {background:#f8fafc;border-radius:8px;}
[data-testid="stFormSubmitButton"] button {background:#0f9f78;border:0;border-radius:9px;color:white;font-weight:750;min-height:40px;}
[data-testid="stFormSubmitButton"] button:hover {background:#087d60;color:white;border:0;}
.metric-card {background:white;border:1px solid #e2e9f0;border-radius:13px;padding:15px 17px;min-height:104px;}
.metric-label {font-size:.75rem;color:#687b8e;font-weight:700;}
.metric-value {font-size:clamp(1.15rem,2vw,1.7rem);font-weight:850;letter-spacing:-.045em;margin-top:5px;white-space:nowrap;}
.metric-note {font-size:.72rem;color:#8191a1;margin-top:3px;}
.pos {color:#07855e;} .neg {color:#d4484e;} .neutral {color:#142b45;}
.detail-card {background:white;border:1px solid #e2e9f0;border-radius:13px;padding:13px 17px;margin-top:4px;}
.detail-title {font-weight:800;color:#142b45;margin-bottom:8px;font-size:.91rem;}
.detail-row {display:flex;justify-content:space-between;gap:10px;font-size:.77rem;padding:4px 0;border-bottom:1px solid #f0f3f7;}
.detail-row:last-child {border-bottom:0;font-weight:800;color:#142b45;}
.detail-row span:first-child {color:#6c7d8f;}
.detail-row span:last-child {text-align:right;white-space:nowrap;}
.footer {display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;border-top:1px solid #dfe7ef;padding-top:11px;margin-top:15px;font-size:.7rem;color:#8390a1;}
div[data-testid="stAlert"] {padding:.5rem .8rem;}
@media(max-width:700px){.block-container{padding-top:.65rem;padding-left:.85rem;padding-right:.85rem;}.hero{padding:17px;}.hero-title{font-size:1.45rem;}.metric-card{padding:12px;min-height:90px;}.metric-value{font-size:1.2rem;}.footer{font-size:.67rem;}}
</style>
""", unsafe_allow_html=True)

st.markdown('''<div class="brand"><div class="brand-icon">↗</div><div><div class="brand-name">FinPilot</div><div class="brand-tag">SMART FINANCIAL TOOLS</div></div></div>''', unsafe_allow_html=True)
st.markdown('''<div class="hero"><div class="hero-kicker">PSX ANALYTICS</div><div class="hero-title">PSX Smart Trade Analyzer</div><div class="hero-sub">Brokerage, net returns and break-even — all in one clear view.</div></div>''', unsafe_allow_html=True)

with st.form("trade_inputs"):
    st.markdown('<div class="section-label">Trade calculator</div>', unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3, gap="medium")
    with c1:
        stock_symbol=st.text_input("Stock symbol", value="FABL").strip().upper()
        purchase_price=st.number_input("Buy price (PKR)", min_value=0.0, value=100.0, step=.01, format="%.2f")
    with c2:
        quantity=st.number_input("Quantity", min_value=1, value=100, step=1)
        sell_price=st.number_input("Sell price (PKR)", min_value=0.0, value=110.0, step=.01, format="%.2f")
    with c3:
        purchase_brokerage_per=st.number_input("Buy brokerage (%)", min_value=0.0, max_value=99.99, value=1.0, step=.1, format="%.2f")
        sell_brokerage_per=st.number_input("Sell brokerage (%)", min_value=0.0, max_value=99.99, value=1.0, step=.1, format="%.2f")
    st.form_submit_button("Analyze Trade  →", type="primary", use_container_width=True)

errors=[]
if not stock_symbol: errors.append("Please enter a stock symbol.")
if purchase_price<=0: errors.append("Buy price must be greater than zero.")
if sell_price<0: errors.append("Sell price cannot be negative.")
if not 0<=purchase_brokerage_per<100 or not 0<=sell_brokerage_per<100: errors.append("Brokerage must be at least 0% and below 100%.")
for err in errors: st.error(err)

def metric(label, value, note, color="neutral"):
    return f'<div class="metric-card"><div class="metric-label">{html.escape(label)}</div><div class="metric-value {color}">{html.escape(value)}</div><div class="metric-note">{html.escape(note)}</div></div>'

def detail(title, rows):
    inner="".join(f'<div class="detail-row"><span>{html.escape(k)}</span><span>{html.escape(v)}</span></div>' for k,v in rows)
    return f'<div class="detail-card"><div class="detail-title">{html.escape(title)}</div>{inner}</div>'

if not errors:
    gross_purchase=purchase_price*quantity
    purchase_brokerage=gross_purchase*purchase_brokerage_per/100
    total_investment=gross_purchase+purchase_brokerage
    gross_sell=sell_price*quantity
    sell_brokerage=gross_sell*sell_brokerage_per/100
    net_sale_proceeds=gross_sell-sell_brokerage
    net_profit_loss=net_sale_proceeds-total_investment
    net_return_percentage=net_profit_loss/total_investment*100
    break_even_price=total_investment/(quantity*(1-sell_brokerage_per/100))
    # Display negative returns smaller than 0.005% as <0.01% rather than -0.00%.
    if 0<abs(net_return_percentage)<.005:
        return_text=("−" if net_return_percentage<0 else "+")+"<0.01%"
    else:
        return_text=f"{net_return_percentage:+.2f}%"
    color="pos" if net_profit_loss>0 else "neg" if net_profit_loss<0 else "neutral"
    st.markdown('<div class="section-label" style="margin:12px 0 7px">Trade summary</div>', unsafe_allow_html=True)
    m1,m2,m3=st.columns(3, gap="medium")
    with m1: st.markdown(metric("NET PROFIT / LOSS",f"PKR {net_profit_loss:+,.2f}",f"{stock_symbol} · {quantity:,} shares",color),unsafe_allow_html=True)
    with m2: st.markdown(metric("NET RETURN",return_text,"After buy and sell brokerage",color),unsafe_allow_html=True)
    with m3: st.markdown(metric("BREAK-EVEN SELL PRICE",f"PKR {break_even_price:,.2f}","Per share · displayed to 2 decimals"),unsafe_allow_html=True)
    d1,d2=st.columns(2, gap="medium")
    with d1: st.markdown(detail("↘  Purchase breakdown",[("Gross purchase",f"PKR {gross_purchase:,.2f}"),(f"Brokerage ({purchase_brokerage_per:.2f}%)",f"PKR {purchase_brokerage:,.2f}"),("Total investment",f"PKR {total_investment:,.2f}")]),unsafe_allow_html=True)
    with d2: st.markdown(detail("↗  Sale breakdown",[("Gross sale",f"PKR {gross_sell:,.2f}"),(f"Brokerage ({sell_brokerage_per:.2f}%)",f"PKR {sell_brokerage:,.2f}"),("Net sale proceeds",f"PKR {net_sale_proceeds:,.2f}")]),unsafe_allow_html=True)

st.markdown('<div class="footer"><span>© 2026 FinPilot · Built with Python & Streamlit</span><span>Educational estimates only · Not investment advice · Taxes and exchange fees excluded</span></div>', unsafe_allow_html=True)
