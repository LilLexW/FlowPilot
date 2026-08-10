import streamlit as st

from llm import summarize_meeting

from database import (
    add_task,
    task_exists,
    get_projects
)


st.title("🤖 AI Meeting Assistant")


notes = st.text_area(
    "Paste meeting notes here",
    height=250
)


# =========================
# Generate AI Summary
# =========================

if st.button("Generate Summary"):

    if notes.strip() == "":
        st.warning("Please enter meeting notes.")

    else:

        with st.spinner("AI is analyzing..."):

            result = summarize_meeting(notes)

            if isinstance(result, dict) and "error" in result:

                st.error(
                    result["error"]
                )

            else:

                st.session_state["meeting_result"] = result


# =========================
# Display AI Result
# =========================

if "meeting_result" in st.session_state:

    result = st.session_state["meeting_result"]
    
if "error" in result:

    st.error(
        result["error"]
    )

    st.stop()


    # =========================
    # Summary
    # =========================

    st.subheader("📋 Summary")

    st.write(
        result["summary"]
    )


    st.divider()


    # =========================
    # Action Items
    # =========================

    st.subheader("✅ Action Items")

    for item in result["action_items"]:

        if isinstance(item, dict):

            st.write(
                f"**{item.get('task', 'Untitled Task')}**"
            )

            st.caption(
                f"Owner: {item.get('owner', 'N/A')} | "
                f"Priority: {item.get('priority', 'N/A')} | "
                f"Deadline: {item.get('deadline', 'N/A')}"
            )

        else:

            st.write(
                f"☐ {item}"
            )


    st.divider()


    # =========================
    # Risks
    # =========================

    st.subheader("⚠ Risks")

    for risk in result["risks"]:

        if isinstance(risk, dict):

            st.warning(
                risk.get(
                    "risk",
                    "Unknown risk"
                )
            )

            st.caption(
                f"Impact: {risk.get('impact', 'N/A')} | "
                f"Mitigation: {risk.get('mitigation', 'N/A')}"
            )

        else:

            st.warning(
                str(risk)
            )


    st.divider()


    # =========================
    # Next Steps
    # =========================

    st.subheader("➡ Next Steps")

    for step in result["next_steps"]:

        st.info(
            str(step)
        )


    st.divider()


    # =========================
    # Generate Tasks
    # =========================

    st.subheader(
        "🚀 Convert Action Items into Tasks"
    )


    projects = get_projects()


    if len(projects) == 0:

        st.warning(
            "No projects found. Please create a project first."
        )

    else:

        project_options = {
            project[1]: project[0]
            for project in projects
        }


        selected_project = st.selectbox(
            "Select Project",
            list(project_options.keys())
        )


        if st.button("Generate Tasks"):

            project_id = project_options[
                selected_project
            ]

            created_count = 0
            skipped_count = 0


            for item in result["action_items"]:

                # -------------------------
                # Extract task information
                # -------------------------

                if isinstance(item, dict):

                    task_name = item.get(
                        "task",
                        "Untitled Task"
                    )

                    owner = item.get(
                        "owner",
                        "N/A"
                    )

                    priority = item.get(
                        "priority",
                        "Medium"
                    )

                    deadline = item.get(
                        "deadline",
                        "N/A"
                    )

                else:

                    task_name = str(item)

                    owner = "N/A"

                    priority = "Medium"

                    deadline = "N/A"


                # -------------------------
                # Duplicate check
                # -------------------------

                if task_exists(
                    project_id,
                    task_name
                ):

                    skipped_count += 1

                    continue


                # -------------------------
                # Create task
                # -------------------------

                add_task(
                    project_id,
                    task_name,
                    owner,
                    priority,
                    "Todo",
                    deadline
                )

                created_count += 1


            # -------------------------
            # Result message
            # -------------------------

            if created_count > 0:

                st.success(
                    f"Successfully created "
                    f"{created_count} new tasks."
                )


            if skipped_count > 0:

                st.info(
                    f"{skipped_count} duplicate "
                    f"tasks were skipped."
                )


            if created_count == 0 and skipped_count == 0:

                st.warning(
                    "No tasks were generated."
                )