
import streamlit as st

from chatbot import load_cases, get_response
from nlp_processor import analyze_sentiment


# -----------------------------------
# PAGE CONFIGURATION
# -----------------------------------

st.set_page_config(
    page_title="CaseMind | Detective Bureau",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded"
)


# -----------------------------------
# CUSTOM DARK THEME
# -----------------------------------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

.stApp {
    background: #090D16;
    color: #E9E9ED;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stSidebar"] {
    background: #101725;
    border-right: 1px solid #263247;
}

[data-testid="stHeader"] {
    background: transparent;
}

#MainMenu, footer {
    visibility: hidden;
}

.main-title {
    font-family: 'Playfair Display', serif;
    font-size: 43px;
    color: #D9B779;
    letter-spacing: 4px;
    margin-bottom: 0;
}

.subtitle {
    color: #8491A5;
    font-size: 11px;
    letter-spacing: 3px;
}

.section-title {
    color: #D9B779;
    font-family: 'Playfair Display', serif;
    font-size: 23px;
}

.case-card {
    background: linear-gradient(145deg, #172235, #111927);
    border: 1px solid #2C3B51;
    border-radius: 13px;
    padding: 20px;
    margin-bottom: 12px;
}

.gold {
    color: #D9B779;
}

.muted {
    color: #8996A8;
    font-size: 13px;
}

.stat-card {
    background: #141E2D;
    border: 1px solid #29374B;
    border-radius: 12px;
    padding: 17px;
    text-align: center;
}

.stat-number {
    color: #D9B779;
    font-size: 29px;
    font-weight: 700;
}

.stButton > button {
    background: #D9B779;
    color: #101725;
    border: none;
    border-radius: 8px;
    font-weight: 700;
    transition: 0.2s;
}

.stButton > button:hover {
    background: #F0D49C;
    color: #101725;
    border: none;
}

.stChatInput textarea {
    background: #172235 !important;
    color: white !important;
}

[data-testid="stChatMessage"] {
    background: #141E2D;
    border: 1px solid #26364B;
    border-radius: 12px;
}

.stSelectbox div[data-baseweb="select"] > div {
    background: #172235;
    border-color: #34445B;
}

hr {
    border-color: #29374B;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------------
# LOAD CASES
# -----------------------------------

cases = load_cases()

if "selected_case" not in st.session_state:
    st.session_state.selected_case = cases[0]["id"]

if "active_case" not in st.session_state:
    st.session_state.active_case = cases[0]["id"]

if "messages" not in st.session_state:
    st.session_state.messages = []

if "discovered_clues" not in st.session_state:
    st.session_state.discovered_clues = set()

if "solved" not in st.session_state:
    st.session_state.solved = False

if "score" not in st.session_state:
    st.session_state.score = 0

if "accusation" not in st.session_state:
    st.session_state.accusation = ""


# -----------------------------------
# SIDEBAR
# -----------------------------------

with st.sidebar:

    st.markdown(
        "<h2 style='color:#D9B779;'>🔎 CASEMIND</h2>",
        unsafe_allow_html=True
    )

    st.caption("DIGITAL INVESTIGATION BUREAU")

    st.divider()

    st.markdown("### 🗂️ Investigation Menu")

    case_ids = [case["id"] for case in cases]

    selected = st.selectbox(
        "Select Investigation",
        case_ids,
        index=case_ids.index(st.session_state.active_case),
        format_func=lambda cid: next(
            c["title"] for c in cases if c["id"] == cid
        )
    )

    if selected != st.session_state.active_case:

        st.session_state.active_case = selected
        st.session_state.messages = []
        st.session_state.discovered_clues = set()
        st.session_state.solved = False
        st.session_state.score = 0
        st.session_state.accusation = ""

        st.rerun()

    case = next(
        c for c in cases
        if c["id"] == st.session_state.active_case
    )

    st.divider()

    st.markdown("### 🕵️ Detective Profile")

    st.markdown("**Rank:** Junior Investigator")
    st.markdown("**Cases solved:** " + str(
        int(st.session_state.solved)
    ))

    st.markdown("**Current score:** " + str(
        st.session_state.score
    ))

    st.divider()

    st.markdown("### 📌 Investigation Status")

    if st.session_state.solved:
        st.success("Case Solved")
    else:
        st.info("Investigation Active")

    st.caption("Every detail matters, Detective.")


# -----------------------------------
# HEADER
# -----------------------------------

st.markdown(
    '<p class="main-title">CASEMIND</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">EVERY CLUE TELLS A STORY. EVERY DETAIL MATTERS.</p>',
    unsafe_allow_html=True
)

st.divider()


# -----------------------------------
# WELCOME
# -----------------------------------

st.markdown(
    f"<h2 style='color:#E8DCC7;'>Welcome, Detective. 🕵️</h2>",
    unsafe_allow_html=True
)

st.markdown(
    f"<p style='color:#8996A8;'>{case['description']}</p>",
    unsafe_allow_html=True
)


# -----------------------------------
# STATISTICS
# -----------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="muted">ACTIVE CASE</div>
        <div class="stat-number">01</div>
        <div class="muted">Current investigation</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-card">
        <div class="muted">SUSPECTS</div>
        <div class="stat-number">{len(case['suspects']):02d}</div>
        <div class="muted">Under investigation</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stat-card">
        <div class="muted">CLUES FOUND</div>
        <div class="stat-number">{len(st.session_state.discovered_clues):02d}</div>
        <div class="muted">Evidence collected</div>
    </div>
    """, unsafe_allow_html=True)


st.write("")


# -----------------------------------
# MAIN LAYOUT
# -----------------------------------

chat_col, info_col = st.columns([1.8, 1])


# -----------------------------------
# CHATBOT SECTION
# -----------------------------------

with chat_col:

    st.markdown(
        '<p class="section-title">💬 Detective Assistant</p>',
        unsafe_allow_html=True
    )

    st.caption("Ask questions. Discover evidence. Find the truth.")

    if not st.session_state.messages:

        st.session_state.messages.append({
            "role": "assistant",
            "content": (
                f"Welcome, Detective! We are investigating "
                f"{case['title']}. You can ask me about suspects, "
                "their motives, alibis and available evidence. "
                "Let's solve this mystery."
            )
        })

    # Display conversation

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

    # Chat input

    user_input = st.chat_input(
        "Ask your detective assistant anything..."
    )

    if user_input and not st.session_state.solved:

        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        response = get_response(
            user_input,
            case,
            st.session_state.discovered_clues
        )

        sentiment = analyze_sentiment(user_input)

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

        st.session_state.last_sentiment = sentiment

        st.rerun()

    # Quick actions

    st.markdown("#### Quick Investigation Actions")

    quick1, quick2 = st.columns(2)

    with quick1:

        if st.button("💡 Request a Hint", use_container_width=True):

            response = get_response(
                "give me a hint",
                case,
                st.session_state.discovered_clues
            )

            st.session_state.messages.append({
                "role": "user",
                "content": "Give me a hint."
            })

            st.session_state.messages.append({
                "role": "assistant",
                "content": response
            })

            st.rerun()

    with quick2:

        if st.button("👥 Show Suspects", use_container_width=True):

            response = get_response(
                "who are the suspects",
                case,
                st.session_state.discovered_clues
            )

            st.session_state.messages.append({
                "role": "user",
                "content": "Show me the suspects."
            })

            st.session_state.messages.append({
                "role": "assistant",
                "content": response
            })

            st.rerun()


# -----------------------------------
# RIGHT SIDE: CASE INFORMATION
# -----------------------------------

with info_col:

    st.markdown(
        '<p class="section-title">📁 Case File</p>',
        unsafe_allow_html=True
    )

    st.markdown(f"""
    <div class="case-card">
        <p class="gold"><b>{case['title']}</b></p>
        <p class="muted">CASE ID: {case['id'].upper()}</p>
        <hr>
        <p><b>Location:</b> {case['location']}</p>
        <p><b>Incident time:</b> {case['time']}</p>
        <p><b>Victim:</b> {case['victim']}</p>
    </div>
    """, unsafe_allow_html=True)

    # Suspects

    st.markdown("### 👤 Suspect Profiles")

    for suspect in case["suspects"]:

        with st.expander(suspect["name"]):

            st.markdown(f"**Role:** {suspect['role']}")

            st.markdown(f"**Statement:** {suspect['statement']}")

            st.markdown(f"**Alibi:** {suspect['alibi']}")

            st.markdown(f"**Possible motive:** {suspect['motive']}")

    # Evidence

    st.markdown("### 🔍 Evidence Room")

    for index, clue in enumerate(case["clues"]):

        if index in st.session_state.discovered_clues:

            st.success("✓ " + clue["name"])

            st.caption(clue["description"])

        else:

            st.markdown(
                f"🔒 Evidence #{index + 1} — Undiscovered"
            )


# -----------------------------------
# FINAL ACCUSATION
# -----------------------------------

st.divider()

st.markdown(
    '<p class="section-title">⚖️ Final Accusation</p>',
    unsafe_allow_html=True
)

st.write(
    "After reviewing the evidence, who do you believe "
    "is responsible?"
)

suspect_names = [
    suspect["name"] for suspect in case["suspects"]
]

with st.form("accusation_form"):

    chosen_suspect = st.selectbox(
        "Select your suspect",
        suspect_names
    )

    submitted = st.form_submit_button(
        "⚖️ SUBMIT FINAL ACCUSATION"
    )

    if submitted:

        if st.session_state.solved:

            st.info("You have already solved this case.")

        elif chosen_suspect == case["solution"]:

            st.session_state.solved = True

            st.session_state.score += (
                100 + len(st.session_state.discovered_clues) * 20
            )

            st.session_state.accusation = chosen_suspect

            st.success("🎉 CASE SOLVED! Excellent detective work!")

            st.markdown(
                f"### The culprit was {case['solution']}!"
            )

            st.write(case["explanation"])

            st.balloons()

        else:

            st.error(
                "Incorrect accusation! Review the evidence "
                "and investigate further, Detective."
            )


if st.session_state.solved:

    st.success(
        f"Investigation complete! Final score: "
        f"{st.session_state.score}"
    )

st.divider()

st.markdown(
    "<center style='color:#65738A;'>"
    "CASEMIND • DIGITAL INVESTIGATION BUREAU • "
    "TRUST THE EVIDENCE"
    "</center>",
    unsafe_allow_html=True
)
