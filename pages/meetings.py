import streamlit as st

from llm import summarize_meeting

from database import (
    get_projects,
    add_task,
    task_exists
)


st.title("🤖 AI Meeting Assistant")

st.write(
    "Transform meeting notes into structured "
    "project information and actionable tasks."
)


# =========================
# Meeting Notes
# =========================

notes = st.text_area(
    "Paste meeting notes here",
    height=250
)


# =========================
# Generate Summary
# =========================

if st.button(
    "Generate Summary",
    type="primary"
):

    if not notes.strip():

        st.warning(
            "Please enter meeting notes."
        )

    else:

        with st.spinner(
            "AI is analyzing..."
        ):

            result = summarize_meeting(
                notes
            )


        if (
            isinstance(result, dict)
            and "error" in result
        ):

            st.error(
                result["error"]
            )

        else:

            st.session_state[
                "meeting_result"
            ] = result


            st.success(
                "Meeting analysis completed."
            )


# =========================
# Display Result
# =========================

if "meeting_result" in st.session_state:

    result = st.session_state[
        "meeting_result"
    ]


    # Safety check

    if (
        not isinstance(result, dict)
        or "error" in result
    ):

        st.error(
            result.get(
                "error",
                "Invalid meeting result."
            )
        )

        st.stop()


    # =========================
    # Summary
    # =========================

    st.subheader(
        "📋 Summary"
    )

    st.write(
        result.get(
            "summary",
            "No summary available."
        )
    )


    st.divider()


    # =========================
    # Action Items
    # =========================

    st.subheader(
        "✅ Action Items"
    )

    action_items = result.get(
        "action_items",
        []
    )


    if not action_items:

        st.info(
            "No action items found."
        )

    else:

        for index, item in enumerate(
            action_items
        ):

            if isinstance(
                item,
                dict
            ):

                task = item.get(
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


                st.checkbox(
                    task,
                    key=f"action_{index}"
                )


                st.caption(
                    f"👤 {owner} | "
                    f"🎯 {priority} | "
                    f"📅 {deadline}"
                )

            else:

                st.checkbox(
                    str(item),
                    key=f"action_{index}"
                )


    st.divider()


    # =========================
    # Risks
    # =========================

    st.subheader(
        "⚠ Risks"
    )

    risks = result.get(
        "risks",
        []
    )


    if not risks:

        st.info(
            "No major risks identified."
        )

    else:

        for risk in risks:

            if isinstance(
                risk,
                dict
            ):

                risk_text = risk.get(
                    "risk",
                    "Unknown risk"
                )

                impact = risk.get(
                    "impact",
                    "Medium"
                )

                mitigation = risk.get(
                    "mitigation",
                    "N/A"
                )


                st.warning(
                    f"**{risk_text}**"
                )

                st.caption(
                    f"Impact: {impact} | "
                    f"Mitigation: {mitigation}"
                )

            else:

                st.warning(
                    str(risk)
                )


    st.divider()


    # =========================
    # Next Steps
    # =========================

    st.subheader(
        "➡ Next Steps"
    )

    next_steps = result.get(
        "next_steps",
        []
    )


    if not next_steps:

        st.info(
            "No next steps identified."
        )

    else:

        for step in next_steps:

            st.info(
                str(step)
            )


    st.divider()


    # =========================
    # Generate Tasks
    # =========================

    st.subheader(
        "🚀 Generate Project Tasks"
    )

    projects = get_projects()

    if not projects:

        st.warning(
            "Create a project before generating tasks."
        )

    else:

        project_options = {
            project[1]: project[0]
            for project in projects
        }

        selected_project = st.selectbox(
            "Select Project",
            list(project_options.keys()),
            key="task_project_select"
        )

        if st.button(
            "🚀 Generate Tasks",
            key="generate_tasks"
        ):

            project_id = project_options[
                selected_project
            ]

            action_items = result.get(
                "action_items",
                []
            )

            created_count = 0
            skipped_count = 0

            for item in action_items:

                if isinstance(
                    item,
                    dict
                ):

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

                task_name = task_name.strip()

                if not task_name:
                    continue

                if task_exists(
                    project_id,
                    task_name
                ):

                    skipped_count += 1

                    continue

                add_task(
                    project_id,
                    task_name,
                    owner,
                    priority,
                    "Todo",
                    deadline
                )

                created_count += 1

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

            if (
                created_count == 0
                and skipped_count == 0
            ):

                st.warning(
                    "No tasks were generated."
                )
