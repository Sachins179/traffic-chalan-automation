"""
Traffic Chalan Automation — Streamlit UI.
Run: streamlit run app.py
"""
import datetime
from pathlib import Path

import streamlit as st

from src.database import user_repo
from src.pipeline.runner import run_pipeline
from src.utils.config_loader import config
from src.utils.logger import get_logger

log = get_logger("ui")

# ---------------------------------------------------------------------------
# Page setup
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Traffic Chalan Automation",
    page_icon="🚦",
    layout="wide",
)

st.title("🚦 Traffic Chalan Automation System")
st.caption("AI-powered traffic violation detection & automatic chalan generation")

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Pipeline Steps")
    st.markdown("""
    1. 🔍 Violation detection (LLM)
    2. 💰 Fine lookup (database)
    3. 📸 Plate detection (OpenCV)
    4. 🔤 Plate OCR (LLM)
    5. 👤 Owner lookup (database)
    6. 📄 PDF chalan
    7. 📱 WhatsApp (manual)
    """)
    st.divider()
    st.caption(f"Model: `{config.env['GROQ_VISION_MODEL']}`")

# ---------------------------------------------------------------------------
# File upload
# ---------------------------------------------------------------------------
uploaded = st.file_uploader(
    "📤 Upload a traffic image",
    type=["jpg", "jpeg", "png"],
    help="Upload a traffic camera image to analyze",
)

if uploaded is None:
    st.info("👆 Upload an image to get started")
    st.stop()

# ---------------------------------------------------------------------------
# Save uploaded file
# ---------------------------------------------------------------------------
input_dir = config.abs_path("input_dir")
input_dir.mkdir(parents=True, exist_ok=True)
save_path = input_dir / uploaded.name
save_path.write_bytes(uploaded.getbuffer())

# ---------------------------------------------------------------------------
# Two-column layout
# ---------------------------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📷 Input Image")
    st.image(str(save_path), use_container_width=True)

with col2:
    st.subheader("🔍 Analysis")

    if st.button(
        "🚀 Analyze & Generate Chalan",
        type="primary",
        use_container_width=True,
    ):
        with st.spinner("Running pipeline... (10-30 seconds)"):
            try:
                result = run_pipeline(str(save_path))

                if result is None:
                    st.warning("⚠️ No violation detected in this image.")
                else:
                    st.success("✅ Chalan generated!")

                    # ---------------- Chalan preview ----------------
                    st.markdown("---")
                    st.markdown("## 🧾 Chalan Preview")
                    st.caption("These details are also present in the PDF:")

                    owner_row = user_repo.get_user_by_plate(
                        result.get("plate_number", "")
                    )
                    chalan_date = datetime.datetime.now().strftime(
                        "%d-%b-%Y %H:%M"
                    )

                    col_a, col_b = st.columns(2)

                    with col_a:
                        st.metric(
                            "🚦 Violations",
                            ", ".join(result["violations"]),
                        )
                        st.metric(
                            "🚗 Vehicle",
                            result.get("plate_number") or "—",
                        )

                    with col_b:
                        st.metric(
                            "💰 Total Fine",
                            f"₹{result['total_fine']}",
                        )
                        st.metric("📅 Date", chalan_date)

                    # ---------------- Fine breakdown ----------------
                    st.markdown("#### 💵 Fine Breakdown")
                    for violation, amount in result["fine_breakdown"].items():
                        st.write(f"• **{violation}**: ₹{amount}")
                    st.markdown(
                        f"**Total: ₹{result['total_fine']}**"
                    )

                    # ---------------- Owner info ----------------
                    if owner_row:
                        st.markdown("#### 👤 Owner")
                        st.write(f"**{owner_row['name']}** — {owner_row['mobile']}")

                    # ---------------- PDF download ----------------
                    if result.get("pdf_path"):
                        pdf_path = Path(result["pdf_path"])
                        if pdf_path.exists():
                            with open(pdf_path, "rb") as pdf_file:
                                st.download_button(
                                    "📄 Download Chalan PDF",
                                    data=pdf_file.read(),
                                    file_name=pdf_path.name,
                                    mime="application/pdf",
                                    use_container_width=True,
                                )

                    # ---------------- WhatsApp button ----------------
                    st.markdown("---")
                    st.markdown("## 📱 Send WhatsApp Notification")

                    if result.get("whatsapp_link"):
                        st.link_button(
                            "📱 Open WhatsApp & Send Message",
                            result["whatsapp_link"],
                            use_container_width=True,
                            type="primary",
                        )
                        owner = result.get("owner")
                        if owner:
                            st.caption(
                                f"Recipient: {owner['name']} "
                                f"({owner['mobile']})"
                            )
                    else:
                        st.warning(
                            "⚠️ WhatsApp link unavailable — "
                            "owner not found in database"
                        )

            except Exception as exc:
                log.exception("Pipeline error")
                st.error(f"❌ Error: {exc}")
                st.exception(exc)

st.divider()
st.caption(
    "Traffic Chalan Automation • "
    "Powered by Groq Vision LLM + OpenCV + PostgreSQL"
)