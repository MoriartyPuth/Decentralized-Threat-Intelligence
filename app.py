import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import blockchain_backend as backend
from datetime import datetime

# --- 1. SETTINGS & THEME ---
st.set_page_config(page_title="IIoT Security SOC", layout="wide")

# --- 2. SESSION STATE INITIALIZATION ---
if 'initialized' not in st.session_state:
    try:
        w3_conn = backend.get_blockchain_connection()
        accs = w3_conn.eth.accounts
        st.session_state.update({
            "w3": w3_conn,
            "accounts": accs,
            "reputations": {accs[i][:10]: 100 for i in range(1, 4)},
            "history": [],
            "logs": [f"[{datetime.now().strftime('%H:%M:%S')}] [SYS] Decentralized Network Online."],
            "initialized": True
        })
    except Exception as e:
        st.error(f"Blockchain Initialization Failed: {e}")
        st.stop()

def add_log(msg, level="INFO"):
    t = datetime.now().strftime("%H:%M:%S")
    st.session_state.logs.append(f"[{t}] [{level}] {msg}")

def trigger_rerun():
    """Handles compatibility for st.rerun across versions"""
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()

# --- 3. UI LAYOUT ---
st.title("🛡️ IIoT Security Operations Center")
tab1, tab2 = st.tabs(["🚀 Live Operations", "📊 Scientific Evaluation"])

with tab1:
    col_ctrl, col_viz = st.columns([1, 2])
    
    with col_ctrl:
        st.subheader("Training Parameters")
        sigma = st.slider("Differential Privacy (σ)", 0.1, 5.0, 1.2)
        
        if st.button("🚀 Execute Federated Round"):
            add_log("Starting Round. Requesting local updates...")
            
            # Node Simulation: 0&1 are Honest, 2 is the Malicious Node 3
            updates = [
                backend.apply_differential_privacy(backend.MalwareDetector(), sigma),
                backend.apply_differential_privacy(backend.MalwareDetector(), sigma),
                backend.model_poisoning_attack(backend.MalwareDetector())
            ]
            
            # Krum Aggregation
            best_weights, honest_idx = backend.krum_aggregation(updates)
            
            # --- SECURITY ALERT POPUP ---
            if honest_idx != 2: # Node 3 was successfully blocked
                st.toast("🛡️ Attack Blocked: Poisoning attempt from Node 3 detected!", icon="🚨")
                add_log("Consensus: Node 3 identified as Byzantine outlier. Rejected.", "SECURITY")
            else:
                st.toast("⚠️ Breach: Malicious update accepted!", icon="🔥")
                add_log("CRITICAL: Poisoned update bypassed the Krum filter.", "CRITICAL")
            
            # Update Reputation Scores
            for i in range(3):
                addr = st.session_state.accounts[i+1][:10]
                if i == honest_idx:
                    st.session_state.reputations[addr] += 5
                else:
                    st.session_state.reputations[addr] -= 35
            
            # Save History
            st.session_state.history.append({
                "Round": len(st.session_state.history) + 1,
                "Winner": st.session_state.accounts[honest_idx+1][:10],
                "Outcome": "Defended" if honest_idx != 2 else "Breach"
            })
            
            trigger_rerun()

    with col_viz:
        st.subheader("Real-Time Trust Ledger")
        rep_df = pd.DataFrame(list(st.session_state.reputations.items()), columns=['Node ID', 'Reputation'])
        fig = px.bar(rep_df, x='Node ID', y='Reputation', color='Reputation', 
                     color_continuous_scale='RdYlGn', range_y=[0, 150])
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("📉 Privacy vs. Utility Analysis")
    if hasattr(backend, 'calculate_privacy_utility_tradeoff'):
        s_range = np.linspace(0.1, 5.0, 15)
        accs = backend.calculate_privacy_utility_tradeoff(s_range)
        eval_df = pd.DataFrame({'Noise (σ)': s_range, 'Accuracy (%)': accs})
        fig_eval = px.line(eval_df, x='Noise (σ)', y='Accuracy (%)', markers=True)
        st.plotly_chart(fig_eval, use_container_width=True)
    else:
        st.warning("Analysis function not found in blockchain_backend.py")

# --- 4. SYSTEM DEBUG TERMINAL (The Only Terminal Block) ---
st.divider()
header_col, btn_col = st.columns([4, 1])

with header_col:
    st.subheader("🛠️ System Debug Terminal")

with btn_col:
    if st.button("🗑️ Clear Terminal"):
        st.session_state.logs = [f"[{datetime.now().strftime('%H:%M:%S')}] [SYS] Logs cleared by admin."]
        trigger_rerun()

# This is the single code block for logs
st.code("\n".join(st.session_state.logs[-8:]), language="bash")

# --- 5. BLOCKCHAIN HISTORY ---
if st.session_state.history:
    st.subheader("🔗 Blockchain Transaction Ledger")
    st.dataframe(pd.DataFrame(st.session_state.history).iloc[::-1], use_container_width=True)

# Sidebar Admin Tools
with st.sidebar:
    st.header("Admin Center")
    st.download_button("📥 Export Logs", "\n".join(st.session_state.logs), "soc_audit.txt")
    if st.button("♻️ Factory Reset"):
        st.session_state.clear()
        trigger_rerun()
