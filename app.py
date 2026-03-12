import streamlit as st


from pawpal_system import Pet, Owner, PetCareTask, Scheduler


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """

At minimum, your system should:

[MermaidChart: 3c5df3d2-97cb-455e-8e47-a43e262279b1]
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()


st.subheader("Quick Demo Inputs (UI only)")

owner_name = st.text_input("Owner name", placeholder="Enter your name")

if st.button("Add New Owner"):
    if owner_name.strip():
        st.session_state.owner = Owner(owner_name.strip())
    else:
        st.warning("Please enter a name first.")

if "owner" in st.session_state:
    st.success(f"Owner: {st.session_state.owner.get_name()}")



pet_name = st.text_input("Pet name", placeholder="Enter your pet's name")
species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add New Pet"):
    if pet_name.strip() and "owner" in st.session_state:
        st.session_state.pet = Pet(pet_name.strip(), species)
    else:
        st.warning("Please enter a name first.")

if "pet" in st.session_state:
    st.success(f"Pet: {st.session_state.pet.get_name()}")



st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", placeholder="e.g. Feed Buddy")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, placeholder="e.g. 15")
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], placeholder="Select priority")

if st.button("Add task"):
    task = PetCareTask(task_title,int(duration),priority,st.session_state.pet)
    st.session_state.tasks.append(task)

# if st.session_state.tasks:
#     st.write("Current tasks:")
#     st.table(st.session_state.tasks)
if st.session_state.tasks:
    st.write("Current tasks:")
    task_rows = [
        {
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

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    st.warning(
        "Not implemented yet. Next step: create your scheduling logic (classes/functions) and call it here."
    )
    st.markdown(
        """
Suggested approach:
1. Design your UML (draft).
2. Create class stubs (no logic).
3. Implement scheduling behavior.
4. Connect your scheduler here and display results.
"""
    )
