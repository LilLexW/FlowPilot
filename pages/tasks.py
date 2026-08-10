import streamlit as st

from database import (
    get_tasks,
    update_task_status,
    delete_task,
    update_task
)


st.title("📋 Tasks")

tasks = get_tasks()


if not tasks:

    st.info("No tasks yet.")

else:

    # =========================
    # Filters
    # =========================

    st.subheader("🔎 Filter Tasks")

    owners = sorted(
        set(
            task[3]
            for task in tasks
            if task[3]
        )
    )

    owner_options = ["All"] + owners

    priority_options = [
        "All",
        "High",
        "Medium",
        "Low"
    ]

    status_options = [
        "All",
        "Todo",
        "In Progress",
        "Done"
    ]

    col1, col2, col3 = st.columns(3)

    with col1:

        selected_owner = st.selectbox(
            "Owner",
            owner_options
        )

    with col2:

        selected_priority = st.selectbox(
            "Priority",
            priority_options
        )

    with col3:

        selected_status = st.selectbox(
            "Status",
            status_options
        )


    # =========================
    # Apply Filters
    # =========================

    filtered_tasks = tasks

    if selected_owner != "All":

        filtered_tasks = [
            task
            for task in filtered_tasks
            if task[3] == selected_owner
        ]

    if selected_priority != "All":

        filtered_tasks = [
            task
            for task in filtered_tasks
            if task[4] == selected_priority
        ]

    if selected_status != "All":

        filtered_tasks = [
            task
            for task in filtered_tasks
            if task[5] == selected_status
        ]


    st.divider()

    st.subheader(
        f"📋 {len(filtered_tasks)} Tasks"
    )


    # =========================
    # Display Tasks
    # =========================

    if not filtered_tasks:

        st.info(
            "No tasks match the selected filters."
        )

    else:

        for task in filtered_tasks:

            task_id = task[0]
            project_id = task[1]
            task_name = task[2]
            owner = task[3]
            priority = task[4]
            status = task[5]
            deadline = task[6]


            with st.container(border=True):

                st.markdown(
                    f"### {task_name}"
                )

                if priority == "High":

                    priority_label = "🔴 High"

                elif priority == "Medium":

                    priority_label = "🟡 Medium"

                else:

                    priority_label = "🟢 Low"


                if priority == "High":
                    priority_label = "🔴 High"
                elif priority == "Medium":
                    priority_label = "🟡 Medium"
                else:
                    priority_label = "🟢 Low"

                if deadline == "N/A" or deadline == "":
                    deadline_label = "📅 No deadline"
                else:
                    deadline_label = f"📅 {deadline}"

                st.caption(
                    f"👤 {owner}   |   "
                    f"🎯 {priority_label}   |   "
                    f"{deadline_label}"
                )


                # =========================
                # Status
                # =========================

                new_status = st.selectbox(
                    "Status",
                    [
                        "Todo",
                        "In Progress",
                        "Done"
                    ],
                    index=[
                        "Todo",
                        "In Progress",
                        "Done"
                    ].index(status)
                    if status in [
                        "Todo",
                        "In Progress",
                        "Done"
                    ]
                    else 0,
                    key=f"status_{task_id}"
                )


                if new_status != status:

                    update_task_status(
                        task_id,
                        new_status
                    )

                    st.rerun()


                # =========================
                # Edit
                # =========================

                with st.expander("✏️ Edit Task"):

                    edited_task_name = st.text_input(
                        "Task",
                        value=task_name,
                        key=f"edit_task_{task_id}"
                    )

                    edited_owner = st.text_input(
                        "Owner",
                        value=owner,
                        key=f"edit_owner_{task_id}"
                    )

                    edited_priority = st.selectbox(
                        "Priority",
                        [
                            "High",
                            "Medium",
                            "Low"
                        ],
                        index=[
                            "High",
                            "Medium",
                            "Low"
                        ].index(priority)
                        if priority in [
                            "High",
                            "Medium",
                            "Low"
                        ]
                        else 1,
                        key=f"edit_priority_{task_id}"
                    )

                    edited_deadline = st.text_input(
                        "Deadline",
                        value=deadline,
                        key=f"edit_deadline_{task_id}"
                    )


                    if st.button(
                        "Save Changes",
                        key=f"save_{task_id}"
                    ):

                        update_task(
                            task_id,
                            edited_task_name,
                            edited_owner,
                            edited_priority,
                            edited_deadline
                        )

                        st.success(
                            "Task updated successfully."
                        )

                        st.rerun()


                # =========================
                # Delete
                # =========================

                if st.button(
                    "🗑 Delete",
                    key=f"delete_{task_id}"
                ):

                    delete_task(
                        task_id
                    )

                    st.rerun()