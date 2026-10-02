"""
========================================================================================
🏆 STREAMLIT CLOUD PRODUCTION ML WEB APPLICATION
========================================================================================
Deployable to Streamlit Community Cloud (share.streamlit.io) or Hugging Face Spaces.
Features:
- Dynamic 200k-row CSV ingestion + Memory Optimization
- Real-time GBDT Trifecta Training (LightGBM / XGBoost / CatBoost / Ensemble)
- Interactive Plotly Feature Importance & KPI Metrics Dashboard
- Live Single Prediction & Batch Prediction CSV Download
- Downloadable Serialized Model Bundle (.joblib)
========================================================================================
"""

import io
import time
import joblib
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from train_pipeline import (
    reduce_mem_usage,
    generate_demo_dataset,
    train_model,
    predict_batch,
)

# ======================================================================================
# PAGE CONFIGURATION & CUSTOM AESTHETICS (DARK/MODERN GRADIENT DESIGN)
# ======================================================================================
st.set_page_config(
    page_title="Grandmaster ML Studio | Hackathon AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for modern styling
st.markdown("""
<style>
    /* Gradient Headers & Modern Font */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .main-title {
        font-size: 2.3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    
    .sub-title {
        font-size: 1.05rem;
        color: #94a3b8;
        margin-bottom: 1.5rem;
    }
    
    /* Metric Card Styling */
    div[data-testid="stMetric"] {
        background: rgba(30, 41, 59, 0.45);
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        font-weight: 700;
        color: #38bdf8 !important;
    }
    
    /* Custom Badge */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 600;
        background: rgba(56, 189, 248, 0.15);
        color: #38bdf8;
        border: 1px solid rgba(56, 189, 248, 0.3);
        margin-right: 8px;
    }
    
    /* Card Container */
    .glass-card {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(51, 65, 85, 0.5);
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)


# ======================================================================================
# SESSION STATE INITIALIZATION
# ======================================================================================
if "dataset" not in st.session_state:
    st.session_state.dataset = None
if "trained_pipeline" not in st.session_state:
    st.session_state.trained_pipeline = None
if "metrics" not in st.session_state:
    st.session_state.metrics = None
if "fi_df" not in st.session_state:
    st.session_state.fi_df = None


# ======================================================================================
# SIDEBAR NAVIGATION
# ======================================================================================
with st.sidebar:
    st.markdown("## ⚡ **ML Studio Control**")
    app_mode = st.radio(
        "Navigation",
        [
            "🚀 Model Training & Tuning",
            "🔮 Live Single Prediction",
            "📂 Batch Prediction & CSV Export",
            "ℹ️ Architecture & Deployment Guide"
        ],
        index=0
    )
    st.markdown("---")
    st.markdown("### 🏆 **System Engine**")
    st.markdown("<span class='badge'>LightGBM</span> <span class='badge'>XGBoost</span> <span class='badge'>CatBoost</span>", unsafe_allow_html=True)
    st.markdown("Designed for high-throughput tabular competitions (200k+ rows) with automated memory downcasting.")
    st.markdown("---")
    st.caption("Grandmaster ML Engine v2.0 • Ready for Streamlit Cloud")


# ======================================================================================
# VIEW 1: MODEL TRAINING & METRICS DASHBOARD
# ======================================================================================
if app_mode == "🚀 Model Training & Tuning":
    st.markdown("<div class='main-title'>Kaggle Grandmaster Tabular ML Studio</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>Train, tune, and evaluate production-grade GBDT models on 200,000+ row tabular datasets.</div>", unsafe_allow_html=True)

    # 1. Dataset Source Section
    col_upload, col_demo = st.columns([2, 1])
    with col_upload:
        uploaded_file = st.file_uploader("📂 Upload Dataset CSV (Handles up to 200,000+ rows)", type=["csv"])
    with col_demo:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🎲 Load 50k-Row Benchmark Demo", use_container_width=True):
            with st.spinner("Synthesizing 50,000-row benchmark dataset..."):
                demo_df = generate_demo_dataset(n_rows=50_000, problem_type="classification")
                st.session_state.dataset = demo_df
                st.success("Loaded 50,000 benchmark rows into memory!")

    # Ingest uploaded file if present
    if uploaded_file is not None:
        try:
            with st.spinner("Loading and downcasting memory for large dataset..."):
                df_raw = pd.read_csv(uploaded_file)
                st.session_state.dataset = reduce_mem_usage(df_raw, verbose=False)
                st.success(f"Successfully loaded dataset with {len(st.session_state.dataset):,} rows and {st.session_state.dataset.shape[1]} columns!")
        except Exception as e:
            st.error(f"Error loading CSV: {e}")

    # Dataset Preview & Configuration
    if st.session_state.dataset is not None:
        df = st.session_state.dataset

        with st.expander("🔍 Dataset Quick Preview (First 5 Rows)", expanded=False):
            st.dataframe(df.head(5), use_container_width=True)
            col_info1, col_info2, col_info3 = st.columns(3)
            col_info1.metric("Total Rows", f"{len(df):,}")
            col_info2.metric("Total Columns", f"{df.shape[1]}")
            mem_mb = df.memory_usage().sum() / 1024**2
            col_info3.metric("RAM Footprint", f"{mem_mb:.2f} MB")

        st.markdown("### ⚙️ **Model & Pipeline Configuration**")
        c1, c2, c3 = st.columns(3)

        with c1:
            all_cols = list(df.columns)
            target_default = "target" if "target" in all_cols else all_cols[-1]
            target_col = st.selectbox("🎯 Target Column", all_cols, index=all_cols.index(target_default))

        with c2:
            problem_type = st.selectbox(
                "📊 Problem Type",
                ["classification", "regression"],
                index=0
            )

        with c3:
            model_algo = st.selectbox(
                "🤖 Algorithm Choice",
                [
                    "ensemble",
                    "lightgbm",
                    "xgboost",
                    "catboost"
                ],
                format_func=lambda x: {
                    "ensemble": "🔥 Trifecta Ensemble (LGBM + XGB + Cat)",
                    "lightgbm": "⚡ LightGBM (Fastest & Scalable)",
                    "xgboost": "🌲 XGBoost (Histogram Tree)",
                    "catboost": "🐱 CatBoost (Categorical Specialist)"
                }[x]
            )

        available_features = [c for c in df.columns if c != target_col]
        selected_features = st.multiselect(
            "📋 Select Feature Columns (Auto-defaults to all available)",
            options=available_features,
            default=available_features
        )

        col_cv, col_sample = st.columns(2)
        with col_cv:
            cv_folds = st.slider("Stratified Cross-Validation Folds", min_value=2, max_value=5, value=3)
        with col_sample:
            max_sample_options = [20000, 50000, 100000, len(df)]
            sample_cap = st.select_slider(
                "Sample rows for training (Speed optimization)",
                options=sorted(list(set(max_sample_options))),
                value=min(50000, len(df))
            )

        # Train Trigger Button
        if st.button("🚀 Train Competitive ML Pipeline", type="primary", use_container_width=True):
            if not selected_features:
                st.error("Please select at least one feature column to train.")
            else:
                progress_bar = st.progress(0.0)
                status_text = st.empty()

                def update_progress(pct, text):
                    progress_bar.progress(pct)
                    status_text.text(f"⏳ {text}")

                start_time = time.time()
                try:
                    pipeline_art, metrics, fi_df = train_model(
                        df=df,
                        target_col=target_col,
                        feature_cols=selected_features,
                        problem_type=problem_type,
                        model_name=model_algo,
                        cv_folds=cv_folds,
                        sample_size=sample_cap,
                        progress_callback=update_progress
                    )
                    elapsed = time.time() - start_time
                    progress_bar.progress(1.0)
                    status_text.text(f"✅ Training completed in {elapsed:.1f} seconds!")

                    st.session_state.trained_pipeline = pipeline_art
                    st.session_state.metrics = metrics
                    st.session_state.fi_df = fi_df
                    st.balloons()
                except Exception as ex:
                    st.error(f"Training failed: {ex}")

        # Metrics & Visualizations Display
        if st.session_state.metrics is not None:
            st.markdown("---")
            st.markdown("### 📈 **Out-Of-Fold Validation Performance**")
            metric_cols = st.columns(len(st.session_state.metrics))
            for col, (m_name, m_val) in zip(metric_cols, st.session_state.metrics.items()):
                col.metric(label=m_name, value=f"{m_val:.4f}")

            # Plot Feature Importance using Plotly
            if st.session_state.fi_df is not None and not st.session_state.fi_df.empty:
                st.markdown("### 🌟 **Top Feature Importances**")
                top_fi = st.session_state.fi_df.head(15)
                fig = px.bar(
                    top_fi,
                    x="Importance (%)",
                    y="Feature",
                    orientation="h",
                    title="Top Predictive Features Across Folds",
                    color="Importance (%)",
                    color_continuous_scale="Viridis"
                )
                fig.update_layout(
                    yaxis=dict(autorange="reversed"),
                    margin=dict(l=0, r=0, t=40, b=0),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#cbd5e1")
                )
                st.plotly_chart(fig, use_container_width=True)

            # Download Model Artifact Button
            st.markdown("### 💾 **Model Artifact Export**")
            buf = io.BytesIO()
            joblib.dump(st.session_state.trained_pipeline, buf)
            buf.seek(0)
            st.download_button(
                label="📥 Download Trained Model Bundle (.joblib)",
                data=buf,
                file_name="trained_hackathon_model.joblib",
                mime="application/octet-stream",
                use_container_width=True
            )
    else:
        st.info("👆 Upload your CSV dataset above or click **'Load 50k-Row Benchmark Demo'** to begin.")


# ======================================================================================
# VIEW 2: LIVE SINGLE PREDICTION
# ======================================================================================
elif app_mode == "🔮 Live Single Prediction":
    st.markdown("<div class='main-title'>🔮 Real-Time Inference Simulator</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>Simulate individual customer or record predictions using the trained ensemble models.</div>", unsafe_allow_html=True)

    if st.session_state.trained_pipeline is None:
        st.warning("⚠️ No trained model found in current session. Please train a model in the 'Model Training' tab first!")
    else:
        pipeline = st.session_state.trained_pipeline
        features = pipeline["feature_cols"]
        dataset_sample = st.session_state.dataset

        st.markdown("#### Input Features:")
        user_inputs = {}

        # Render input widgets dynamically in 3 columns
        cols = st.columns(3)
        for i, col_name in enumerate(features):
            col_target = cols[i % 3]
            is_num = pd.api.types.is_numeric_dtype(dataset_sample[col_name]) if dataset_sample is not None else True

            if is_num:
                min_v = float(dataset_sample[col_name].min()) if dataset_sample is not None else 0.0
                max_v = float(dataset_sample[col_name].max()) if dataset_sample is not None else 1000.0
                mean_v = float(dataset_sample[col_name].median()) if dataset_sample is not None else 50.0
                user_inputs[col_name] = col_target.number_input(
                    f"{col_name}",
                    value=round(mean_v, 2),
                    min_value=round(min_v, 2),
                    max_value=round(max_v, 2)
                )
            else:
                categories = list(dataset_sample[col_name].dropna().unique()) if dataset_sample is not None else ["A", "B", "C"]
                user_inputs[col_name] = col_target.selectbox(f"{col_name}", options=categories)

        if st.button("⚡ Run Instant Prediction", type="primary", use_container_width=True):
            input_df = pd.DataFrame([user_inputs])
            pred = predict_batch(pipeline, input_df)[0]

            st.markdown("---")
            res_col1, res_col2 = st.columns([1, 1])

            with res_col1:
                if pipeline["problem_type"] == "classification":
                    prob = float(pred)
                    pred_class = int(prob >= 0.5)
                    st.metric(label="Predicted Probability (Positive Class)", value=f"{prob * 100:.2f}%")
                    st.markdown(f"**Predicted Class Label:** `{pred_class}`")
                else:
                    st.metric(label="Predicted Continuous Value", value=f"{pred:,.2f}")

            with res_col2:
                if pipeline["problem_type"] == "classification":
                    fig_gauge = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=prob * 100,
                        title={'text': "Prediction Confidence"},
                        gauge={
                            'axis': {'range': [0, 100]},
                            'bar': {'color': "#38bdf8"},
                            'steps': [
                                {'range': [0, 50], 'color': "#1e293b"},
                                {'range': [50, 100], 'color': "#0f766e"}
                            ]
                        }
                    ))
                    fig_gauge.update_layout(height=220, margin=dict(l=20, r=20, t=30, b=10))
                    st.plotly_chart(fig_gauge, use_container_width=True)


# ======================================================================================
# VIEW 3: BATCH PREDICTION & CSV EXPORT
# ======================================================================================
elif app_mode == "📂 Batch Prediction & CSV Export":
    st.markdown("<div class='main-title'>📂 Batch Prediction & Submission Generator</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>Upload an unlabelled test dataset to generate bulk predictions and download the final CSV.</div>", unsafe_allow_html=True)

    if st.session_state.trained_pipeline is None:
        st.warning("⚠️ No trained model found in current session. Please train a model in the 'Model Training' tab first!")
    else:
        pipeline = st.session_state.trained_pipeline
        batch_file = st.file_uploader("Upload Test CSV File", type=["csv"])

        if batch_file is not None:
            test_df = pd.read_csv(batch_file)
            st.write(f"Loaded test file with **{len(test_df):,} rows**.")
            st.dataframe(test_df.head(3), use_container_width=True)

            if st.button("🚀 Generate Predictions for Entire Test Set", type="primary", use_container_width=True):
                with st.spinner("Generating ensemble predictions..."):
                    test_df_mem = reduce_mem_usage(test_df.copy(), verbose=False)
                    preds = predict_batch(pipeline, test_df_mem)

                    output_df = test_df.copy()
                    target_name = f"pred_{pipeline['target_col']}"
                    output_df[target_name] = preds

                    if pipeline["problem_type"] == "classification":
                        output_df[f"{target_name}_label"] = (preds >= 0.5).astype(int)

                    st.success(f"Successfully generated predictions for all {len(output_df):,} rows!")
                    st.dataframe(output_df.head(5), use_container_width=True)

                    # Export to CSV
                    csv_data = output_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download Predictions CSV (submission.csv)",
                        data=csv_data,
                        file_name="predictions_submission.csv",
                        mime="text/csv",
                        use_container_width=True
                    )


# ======================================================================================
# VIEW 4: ARCHITECTURE & DEPLOYMENT GUIDE
# ======================================================================================
elif app_mode == "ℹ️ Architecture & Deployment Guide":
    st.markdown("<div class='main-title'>Deployment & Architecture Guide</div>", unsafe_allow_html=True)
    st.markdown("""
    ### 🚀 Deploy for FREE on Streamlit Community Cloud (Under 2 Minutes)
    
    1. **Push your code to GitHub**:
       ```bash
       git init
       git add .
       git commit -m "Grandmaster ML Web App"
       git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
       git push -u origin main
       ```
    
    2. **Connect to Streamlit Cloud**:
       - Go to [share.streamlit.io](https://share.streamlit.io) and log in with your GitHub account.
       - Click **"New App"**.
       - Select your repository, set **Branch** to `main`, and **Main file path** to `app.py`.
       - Click **"Deploy!"**.
    
    3. **Live Public URL**:
       - Streamlit Cloud will automatically install packages from `requirements.txt` and launch your live URL (e.g., `https://your-hackathon-ml.streamlit.app`).

    ---

    ### 🛠 Architectural Safeguards for 200,000 Rows:
    - **Memory Reduction**: `reduce_mem_usage` automatically downcasts 64-bit numerical columns to 16/32-bit floats and integers, maintaining memory consumption under 80MB.
    - **Interactive Sampling Slider**: Allows instant training on a chosen subset for fast experimentation, or full 200k-row training.
    - **Stratified CV Ensemble**: Prevents data leakage by encapsulating preprocessor fits and fold validation splits.
    """)
