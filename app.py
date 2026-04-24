import os
import streamlit as st

from pawpal_system import Pet, Owner, PetCareTask, Scheduler

from datetime import date as Date, time as Time



st.set_page_config(page_title="PawPal+", page_icon="🍃", layout="centered")

st.markdown("""
<style>
/* ── Fonts ─────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif !important;
}

/* ── Page background — night sky ────────────────────────── */
.stApp {
    background-color: #1E1B2E;
    background-image:
        radial-gradient(circle at 12% 18%, #3a2f5540 90px, transparent 90px),
        radial-gradient(circle at 78% 12%, #2e3d2f40 70px, transparent 70px),
        radial-gradient(circle at 55% 82%, #2a2f4040 80px, transparent 80px),
        radial-gradient(circle at 6%  70%, #3b2e4040 60px, transparent 60px);
}

/* ── Main content card ───────────────────────────────────── */
section.main > div {
    background: rgba(30, 27, 46, 0.85);
    border-radius: 24px;
    padding: 2rem 2.5rem;
    box-shadow: 0 4px 32px rgba(0,0,0,0.35);
}

/* ── Title ───────────────────────────────────────────────── */
h1 {
    font-weight: 800 !important;
    color: #A8D8A8 !important;
    letter-spacing: -0.5px;
}

/* ── Subheaders ──────────────────────────────────────────── */
h2, h3 {
    font-weight: 700 !important;
    color: #C5E8C5 !important;
}

/* ── Body text & markdown ────────────────────────────────── */
p, .stMarkdown p, li {
    color: #F2EBD9 !important;
}

/* ── Buttons ─────────────────────────────────────────────── */
.stButton > button {
    font-weight: 700 !important;
    border-radius: 50px !important;
    border: 2px solid #6BAE7A !important;
    background: linear-gradient(135deg, #4E8C62, #3A7554) !important;
    color: #F2EBD9 !important;
    padding: 0.45rem 1.4rem !important;
    transition: all 0.18s ease !important;
    box-shadow: 0 3px 14px rgba(106,174,122,0.30) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) scale(1.03) !important;
    box-shadow: 0 6px 22px rgba(106,174,122,0.45) !important;
    background: linear-gradient(135deg, #6BAE7A, #4E8C62) !important;
    color: #fff !important;
}

/* ── Inputs ──────────────────────────────────────────────── */
input[type="text"], input[type="number"],
textarea, [data-baseweb="input"] input {
    border-radius: 14px !important;
    border: 1.5px solid #4A4560 !important;
    background: #2A2640 !important;
    color: #F2EBD9 !important;
}
input[type="text"]:focus, input[type="number"]:focus {
    border-color: #A8D8A8 !important;
    box-shadow: 0 0 0 3px rgba(168,216,168,0.18) !important;
}

/* ── Select boxes ────────────────────────────────────────── */
.stSelectbox > div > div,
[data-baseweb="select"] > div {
    border-radius: 14px !important;
    border: 1.5px solid #4A4560 !important;
    background: #2A2640 !important;
    color: #F2EBD9 !important;
}

/* ── Multiselect ─────────────────────────────────────────── */
[data-baseweb="multi-select"] {
    border-radius: 14px !important;
    background: #2A2640 !important;
    border: 1.5px solid #4A4560 !important;
}

/* ── Date / time pickers ─────────────────────────────────── */
[data-baseweb="datepicker"] input,
[data-baseweb="time-picker"] input {
    background: #2A2640 !important;
    color: #F2EBD9 !important;
    border-radius: 14px !important;
    border: 1.5px solid #4A4560 !important;
}

/* ── Expanders ───────────────────────────────────────────── */
.streamlit-expanderHeader {
    font-weight: 700 !important;
    color: #C5E8C5 !important;
    background: #2A2640 !important;
    border-radius: 14px !important;
}
.streamlit-expanderContent {
    background: #252238 !important;
    border-radius: 0 0 14px 14px !important;
    color: #F2EBD9 !important;
}

/* ── Alerts ──────────────────────────────────────────────── */
.stAlert {
    border-radius: 16px !important;
    background: #2A2640 !important;
}
.stAlert p { color: #F2EBD9 !important; }

/* ── Metrics ─────────────────────────────────────────────── */
[data-testid="metric-container"] {
    background: #2A2640;
    border-radius: 16px;
    padding: 0.6rem 1rem;
    border: 1.5px solid #4A4560;
}
[data-testid="metric-container"] label,
[data-testid="metric-container"] div {
    color: #C5E8C5 !important;
}
[data-testid="stMetricValue"] {
    color: #F2EBD9 !important;
}

/* ── Tables ──────────────────────────────────────────────── */
table {
    border-radius: 16px !important;
    overflow: hidden !important;
}
thead tr th {
    background: #2F2B50 !important;
    color: #C5E8C5 !important;
    font-weight: 700 !important;
}
tbody tr td {
    color: #F2EBD9 !important;
}
tbody tr:nth-child(even) td {
    background: #252238 !important;
}
tbody tr:nth-child(odd) td {
    background: #2A2640 !important;
}

/* ── Divider ─────────────────────────────────────────────── */
hr {
    border-color: #4A4560 !important;
}

/* ── Spinner ─────────────────────────────────────────────── */
.stSpinner > div {
    border-top-color: #A8D8A8 !important;
}

/* ── Caption ─────────────────────────────────────────────── */
.stCaption, [data-testid="stCaptionContainer"] p {
    color: #B8A99A !important;
    font-style: italic;
}

/* ── Form submit button ──────────────────────────────────── */
[data-testid="stFormSubmitButton"] > button {
    border-radius: 50px !important;
    border: 2px solid #6BAE7A !important;
    background: linear-gradient(135deg, #4E8C62, #3A7554) !important;
    color: #F2EBD9 !important;
    font-weight: 700 !important;
}

/* ── Sidebar (if used) ───────────────────────────────────── */
[data-testid="stSidebar"] {
    background: #2A2640 !important;
}
</style>
""", unsafe_allow_html=True)

st.title("🍃 PawPal+ 🐕🐈‍⬛🐢🐟🐹")

st.markdown(
    """
🌿 Welcome to **PawPal+** — your cozy pet care planner!

Plan your day, keep your animal companions happy, and let the Pet Co Tasker suggest what to do next.
"""
)

#st.header("🏡 About PawPal+")
with st.expander("🏡 About PawPal+",expanded=False):
    st.write(
            """
    **PawPal+** is your personal pet care planning assistant.

    Tell it about your pets, add care tasks, and let it build a cozy daily schedule — prioritized just for you and your animals. Use the AI Co-Tasker to get smart suggestions without lifting a paw. 🐾
    """
        )

st.divider()


st.subheader("🏠 Your Info")

owner_name = st.text_input("Owner name", placeholder="Enter your name")
time_available = st.number_input("Time available per day (minutes)", min_value=1, max_value=1440, placeholder="e.g. 180")

if st.button("Add New Owner"):
    if owner_name.strip():
        st.session_state.owner = Owner(owner_name.strip())
    else:
        st.warning("Please enter a name first.")

if "owner" in st.session_state:
    st.success(f"Owner: {st.session_state.owner.get_name()}")



pet_name = st.text_input("Pet name", placeholder="Enter your pet's name")
species = st.selectbox("Species", ["dog", "cat", "fish", "rabbit", "bird", "hamster", "turtle", "other"])

if "pets" not in st.session_state:
    st.session_state.pets = []

if st.button("Add New Pet"):
    if pet_name.strip() and "owner" in st.session_state:
        st.session_state.pets.append(Pet(pet_name.strip(), species))
    else:
        st.warning("Please enter a name first.")

for p in st.session_state.pets:
    st.success(f"Pet: {p.get_name()} ({p.get_type()})")


# ── Co-Tasker: AI Task Suggestions ──────────────────────────────────────────
st.divider()
st.subheader("🤖 Co-Tasker: AI Task Suggestions")
st.caption("Get personalized task suggestions for your pets — one at a time.")

if not st.session_state.pets:
    st.info("Add at least one pet above to get AI task suggestions.")
else:
    if st.button("✨ Generate Task Suggestions", key="co_tasker_generate"):
        try:
            with st.spinner("Co-Tasker is thinking..."):
                from co_tasker import generate_pet_tasks
                api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY"))
                pets_in_schedule = {task.pet for task in st.session_state.get("tasks", [])}
                recent_pet_list = [pet for pet in st.session_state.pets if pet not in pets_in_schedule]
                if not recent_pet_list:
                    st.info("All pets already have tasks in the schedule.")
                    st.stop()
                suggestions = generate_pet_tasks(recent_pet_list, api_key=api_key)
            st.session_state.co_tasker_suggestions = suggestions
            st.session_state.co_tasker_index = 0
            st.session_state.co_tasker_stats = {"accepted": 0, "edited": 0, "skipped": 0}
            st.session_state.co_tasker_editing = False
        except Exception as e:
            st.error(f"Co-Tasker error: {e}")

    if "co_tasker_suggestions" in st.session_state:
        suggestions = st.session_state.co_tasker_suggestions
        idx = st.session_state.get("co_tasker_index", 0)
        stats = st.session_state.get("co_tasker_stats", {"accepted": 0, "edited": 0, "skipped": 0})

        if idx < len(suggestions):
            s = suggestions[idx]
            pet_name = s["pet_name"]
            pet_obj = next(
                (p for p in st.session_state.pets if p.get_name() == pet_name),
                st.session_state.pets[0],
            )

            st.markdown(f"**Suggestion {idx + 1} of {len(suggestions)}** — for **{pet_name}**")

            c1, c2, c3 = st.columns(3)
            c1.metric("Task", s["description"])
            c2.metric("Duration", f"{s['duration']} min")
            c3.metric("Priority", s["priority"].upper())
            c4, c5 = st.columns(2)
            c4.metric("Date", s["date"])
            c5.metric("Start Time", s["start_time"])

            if not st.session_state.get("co_tasker_editing", False):
                btn1, btn2, btn3 = st.columns(3)
                with btn1:
                    if st.button("✓ Accept", key=f"accept_{idx}"):
                        task = PetCareTask(
                            s["description"], int(s["duration"]), s["priority"], pet_obj,
                            date=Date.fromisoformat(s["date"]),
                            start_time=Time.fromisoformat(s["start_time"]),
                        )
                        st.session_state.tasks.append(task)
                        st.session_state.co_tasker_stats["accepted"] += 1
                        st.session_state.co_tasker_index += 1
                        st.session_state.co_tasker_editing = False
                        st.rerun()
                with btn2:
                    if st.button("✏️ Edit", key=f"edit_{idx}"):
                        st.session_state.co_tasker_editing = True
                        st.rerun()
                with btn3:
                    if st.button("⏭ Skip", key=f"skip_{idx}"):
                        st.session_state.co_tasker_stats["skipped"] += 1
                        st.session_state.co_tasker_index += 1
                        st.session_state.co_tasker_editing = False
                        st.rerun()

            if st.session_state.get("co_tasker_editing", False):
                st.markdown("**Edit this suggestion:**")
                with st.form("edit_suggestion_form"):
                    edit_desc = st.text_input("Task title", value=s["description"])
                    edit_dur = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=int(s["duration"]))
                    edit_pri = st.selectbox("Priority", ["low", "med", "high"], index=["low", "med", "high"].index(s["priority"]))
                    edit_date = st.date_input("Date", value=Date.fromisoformat(s["date"]))
                    h, m = map(int, s["start_time"].split(":"))
                    edit_time = st.time_input("Start time", value=Time(h, m))
                    submitted = st.form_submit_button("Save Edited Task")
                    cancelled = st.form_submit_button("Cancel")

                if submitted:
                    task = PetCareTask(edit_desc, int(edit_dur), edit_pri, pet_obj,
                                      date=edit_date, start_time=edit_time)
                    st.session_state.tasks.append(task)
                    st.session_state.co_tasker_stats["edited"] += 1
                    st.session_state.co_tasker_index += 1
                    st.session_state.co_tasker_editing = False
                    st.rerun()
                if cancelled:
                    st.session_state.co_tasker_editing = False
                    st.rerun()

        else:
            # All suggestions reviewed — show final stats
            total = stats["accepted"] + stats["edited"] + stats["skipped"]
            if total > 0:
                rate = (stats["accepted"] + stats["edited"]) / total * 100
                st.success(f"All {total} suggestions reviewed! Acceptance rate: **{rate:.0f}%**")
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Accepted", stats["accepted"])
                m2.metric("Edited & Saved", stats["edited"])
                m3.metric("Skipped", stats["skipped"])
                m4.metric("Acceptance Rate", f"{rate:.0f}%")
                st.caption("Accepted and edited tasks have been added to your task list below.")

st.divider()

st.markdown("### 📋 Tasks")
st.caption("Add care tasks for your pets — they'll be used to build the daily schedule.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

row1_col1, row1_col2, row1_col3 = st.columns(3)
with row1_col1:
    pet_options = [p.get_name() for p in st.session_state.pets]
    selected_pet_name = st.selectbox("Pet", pet_options if pet_options else ["—"])
with row1_col2:
    task_title = st.text_input("Task title", placeholder="e.g. Feed Buddy")
with row1_col3:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, placeholder="e.g. 15")

row2_col1, row2_col2, row2_col3 = st.columns(3)
with row2_col1:
    priority = st.selectbox("Priority", ["low", "med", "high"])
with row2_col2:
    task_date = st.date_input("Date", value=Date.today())
with row2_col3:
    task_time = st.time_input("Start time", value=Time(8, 0))

if st.button("Add task"):
    selected_pet = next((p for p in st.session_state.pets if p.get_name() == selected_pet_name), None)
    if selected_pet:
        new_task = PetCareTask(task_title, int(duration), priority, selected_pet, date=task_date, start_time=task_time)
        conflict = next(
            (t for t in st.session_state.tasks if t.date == task_date and t.start_time == task_time),
            None
        )
        if conflict:
            st.error(
                f"Task not added — time conflict: '{conflict.description}' is already scheduled at "
                f"{task_time.strftime('%I:%M %p')} on {task_date.strftime('%b %d, %Y')}. "
                f"Please choose a different start time."
            )
        else:
            st.session_state.tasks.append(new_task)
            st.success(f"Task '{new_task.description}' added.")
    else:
        st.warning("Please add a pet before creating tasks.")


if st.session_state.tasks:
    st.write("Current tasks:")
    task_rows = [
        {
            "Date": task.date.strftime("%Y-%m-%d"),
            "Time": task.start_time.strftime("%I:%M %p"),
            "Pet": task.pet.get_name(),
            "Description": task.description,
            "Duration": task.get_duration_display(),
            "Priority": task.priority,
            "Status": task.status,
        }
        for task in st.session_state.tasks
    ]
    st.table(task_rows)

else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("🗓️ Build Your Schedule")

all_pet_names = [p.get_name() for p in st.session_state.pets]
filter_pets = st.multiselect("Filter by pet", all_pet_names, default=all_pet_names)

if st.button("Generate schedule"):
    if "owner" not in st.session_state or not st.session_state.tasks:
        st.warning("Please add an owner and at least one task first.")
    else:
        time_available = st.session_state.get("time_available", time_available)
        scheduler = Scheduler(st.session_state.owner, time_available)

        for task in st.session_state.tasks:
            scheduler.add_task(task)

        plan = scheduler.generate_plan()
        visible_plan = [t for t in plan if t.pet.get_name() in filter_pets]

        total_task_time = sum(task.duration for task in visible_plan)

        format_minutes = lambda m: f"{m} min" if m < 60 else f"{m//60} hr {m%60} min" if m % 60 else f"{m//60} hr"

        st.info(f"Schedule for {st.session_state.owner.get_name()} — {scheduler.get_time_available_display()} available per day — Total scheduled: {format_minutes(total_task_time)}")
        plan_rows = [
            {
                "Date": task.date.strftime("%Y-%m-%d"),
                "Time": task.start_time.strftime("%I:%M %p"),
                "Pet": task.pet.get_name(),
                "Description": task.description,
                "Duration": task.get_duration_display(),
                "Priority": task.priority,
            }
            for task in visible_plan
        ]
        st.table(plan_rows)

        excluded = [t for t in st.session_state.tasks if t not in plan]
        if excluded:
            st.warning(
                f"{len(excluded)} task(s) were excluded because they exceeded the daily time budget "
                f"({scheduler.get_time_available_display()}/day):"
            )
            excluded_rows = [
                {
                    "Date": t.date.strftime("%Y-%m-%d"),
                    "Time": t.start_time.strftime("%I:%M %p"),
                    "Pet": t.pet.get_name(),
                    "Description": t.description,
                    "Duration": t.get_duration_display(),
                    "Priority": t.priority,
                }
                for t in excluded
            ]
            st.table(excluded_rows)
