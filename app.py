import os
import json
import datetime
import streamlit as st
from google import genai
from google.genai import types

# 1. SETUP PAGE CONFIGURATION
st.set_page_config(page_title="Enterprise Agent AI", layout="wide")

# Fetch API Key from system environment variables
API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not API_KEY:
    st.error("❌ Configure 'GEMINI_API_KEY' in your server/deployment environment variables.")
    st.stop()

# Initialize official unified Google Gen AI SDK
client = genai.Client(api_key=API_KEY)
MODEL_NAME = "gemini-2.5-flash"
DB_FILE = "enterprise_knowledge_base.json"

# 2. LOCAL MEMORY FILE STORAGE HANDLERS
def load_db() -> dict:
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            try: return json.load(f)
            except json.JSONDecodeError: return {}
    return {}

def save_db(data: dict):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# Sync database with application memory state
if "db" not in st.session_state:
    st.session_state.db = load_db()
if "temp_prompt" not in st.session_state:
    st.session_state.temp_prompt = ""
if "teach_mode" not in st.session_state:
    st.session_state.teach_mode = False

# 3. CORE COGNITIVE ROUTER LOGIC
def check_recall(user_prompt: str, database: dict) -> str:
    if not database: return "UNKNOWN"
    system_prompt = (
        f"You are a memory indexing node. Look at this list of keys: {list(database.keys())}. "
        f"Does input '{user_prompt}' mean contextually the same thing as one of those keys? "
        f"If YES, reply with exactly that key name. If NO, reply with exactly 'UNKNOWN'."
    )
    res = client.models.generate_content(
        model=MODEL_NAME, contents="Analyze context match.",
        config=types.GenerateContentConfig(system_instruction=system_prompt, temperature=0.1)
    )
    return res.text.strip()

def detect_env_mode(topic: str, instruction: str) -> str:
    prompt = (
        f"Topic: {topic}\nInstruction: {instruction}\n\n"
        f"Is this instructing on private company info, custom software, or personal staff names? "
        f"Reply exactly with 'CLOSED_ENVIRONMENT' if private/internal. "
        f"Reply exactly with 'GENERIC_ENVIRONMENT' if general public knowledge, science, or math."
    )
    res = client.models.generate_content(model=MODEL_NAME, contents=prompt, config=types.GenerateContentConfig(temperature=0.1))
    return "CLOSED_ENVIRONMENT" if "CLOSED_ENVIRONMENT" in res.text.strip() else "GENERIC_ENVIRONMENT"

def verify_facts(topic: str, claim: str) -> dict:
    prompt = (
        f"Topic: {topic}\nClaim: {claim}\n\n"
        f"Verify this claim. Return raw JSON using exactly these keys:\n"
        f"{{\"is_accurate\": true/false, \"corrected_fact\": \"If user is wrong write accurate explanation, else repeat claim.\"}}"
    )
    res = client.models.generate_content(
        model=MODEL_NAME, contents=prompt,
        config=types.GenerateContentConfig(response_mime_type="application/json", temperature=0.2)
    )
    try: return json.loads(res.text.strip())
    except: return {"is_accurate": True, "corrected_fact": claim}

# 4. TABBED INTERFACE ARCHITECTURE
st.title("🏢 Adaptive Enterprise AI Agent")
tab_prod, tab_learn = st.tabs(["🚀 Production Preview", "🧠 Learning Environment"])

# ==================== TAB 1: PRODUCTION PREVIEW ====================
with tab_prod:
    st.subheader("Client Interface")
    prod_input = st.text_input("Ask a question:", key="prod_query")
    
    if st.button("Submit Inquiry", key="prod_btn") and prod_input:
        match = check_recall(prod_input, st.session_state.db)
        if "UNKNOWN" not in match and match in st.session_state.db:
            st.success(f"**Answer:** {st.session_state.db[match]['final_knowledge']}")
        else:
            st.warning("🤖 AI: This question is not found in our corporate database records yet. Please request an administrator to update the system rules.")

# ==================== TAB 2: LEARNING ENVIRONMENT ====================
with tab_learn:
    st.subheader("Admin Knowledge Management Panel")
    
    # Live Database Matrix JSON Display
    with st.expander("📁 View Persistent JSON Database Storage File Matrix", expanded=True):
        st.json(st.session_state.db)
        
    st.markdown("---")
    learn_input = st.text_input("Enter Topic/Keyword to teach or modify:", key="learn_query")
    
    if st.button("Analyze Topic", key="learn_btn") and learn_input:
        st.session_state.temp_prompt = learn_input
        match = check_recall(learn_input, st.session_state.db)
        
        if "UNKNOWN" not in match and match in st.session_state.db:
            data = st.session_state.db[match]
            st.info(f"💡 Found match on key: **'{match}'**")
            st.write(f"**Current Answer:** {data['final_knowledge']}")
            st.write(f"**Metadata:** Environment: `{data['environment_mode']}` | Verified: `{data['is_accurate']}` | Last Updated: `{data['timestamp']}`")
        else:
            st.warning("🔍 Key is completely unmapped.")
        st.session_state.teach_mode = True

    if st.session_state.teach_mode:
        st.markdown("### Update Knowledge Logic Payload")
        user_rule = st.text_area(f"Define response for: '{st.session_state.temp_prompt}'")
        
        if st.button("Commit Rule to System Memory") and user_rule:
            with st.spinner("Executing system validations..."):
                mode = detect_env_mode(st.session_state.temp_prompt, user_rule)
                
                if mode == "CLOSED_ENVIRONMENT":
                    st.toast("🔒 Private data tracked. Skipping external validation.", icon="🔒")
                    final_ans, acc = user_rule, True
                else:
                    st.toast("🌐 General data detected. Running truth scanner...", icon="🌐")
                    check = verify_facts(st.session_state.temp_prompt, user_rule)
                    acc = check["is_accurate"]
                    final_ans = user_rule if acc else check["corrected_fact"]
                
                # Save rules down to states and system files
                st.session_state.db[st.session_state.temp_prompt] = {
                    "user_raw_input": user_rule,
                    "final_knowledge": final_ans,
                    "environment_mode": mode,
                    "is_accurate": acc,
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                save_db(st.session_state.db)
                st.success("💾 Knowledge committed! File synchronized successfully.")
                st.session_state.teach_mode = False
                st.rerun()
