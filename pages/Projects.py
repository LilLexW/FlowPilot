import streamlit as st

from database import (
    add_project,
    get_projects,
    get_tasks,
    project_exists,
    delete_project
)


st.title("📁 Projects")

st.write(
    "Manage your FlowPilot projects."
)


# =========================
# Create Project
# =========================

st.subheader("➕ Create Project")


with st.form(
    "create_project_form"
):

    name = st.text_input(
        "Project Name"
    )

    description = st.text_area(
        "Description"
    )

    deadline = st.date_input(
        "Deadline"
    )

    submitted = st.form_submit_button(
        "Create Project"
    )


    if submitted:

        if not name.strip():

            st.warning(
                "Please enter a project name."
            )

        elif project_exists(name.strip()):

            st.warning(
                "A project with this name already exists."
            )

        else:

            add_project(
                name.strip(),
                description,
                deadline
            )

            st.success(
                "Project created successfully!"
            )

            st.rerun()


st.divider()


# =========================
# Existing Projects
# =========================

st.subheader(
    "📂 Your Projects"
)


projects = get_projects()

tasks = get_tasks()


if not projects:

    st.info(
        "No projects yet. "
        "Create your first project above."
    )


else:

    for project in projects:

        project_id = project[0]
        project_name = project[1]
        description = project[2]
        deadline = project[3]


        # =========================
        # Project Tasks
        # =========================

        project_tasks = [
            task
            for task in tasks
            if task[1] == project_id
        ]


        total_tasks = len(
            project_tasks
        )


        completed_tasks = len(
            [
                task
                for task in project_tasks
                if task[5] == "Done"
            ]
        )


        if total_tasks > 0:

            progress = (
                completed_tasks
                / total_tasks
            )

        else:

            progress = 0


        # =========================
        # Project Card
        # =========================

        with st.container(
            border=True
        ):

            st.markdown(
                f"### 📁 {project_name}"
            )


            if description:

                st.write(
                    description
                )


            st.caption(
                f"📅 Deadline: {deadline}"
            )


            col1, col2, col3 = st.columns(3)


            with col1:

                st.metric(
                    "Tasks",
                    total_tasks
                )


            with col2:

                st.metric(
                    "Completed",
                    completed_tasks
                )


            with col3:

                st.metric(
                    "Progress",
                    f"{progress:.0%}"
                )


            st.progress(
                progress
            )


            # =========================
            # Project Tasks
            # =========================

            with st.expander(
                "📋 View Project Tasks"
            ):

                if not project_tasks:

                    st.info(
                        "No tasks for this project yet."
                    )

                else:

                    for task in project_tasks:

                        task_name = task[2]
                        owner = task[3]
                        priority = task[4]
                        status = task[5]
                        task_deadline = task[6]


                        st.markdown(
                            f"**{task_name}**"
                        )


                        st.caption(
                            f"👤 {owner} | "
                            f"🎯 {priority} | "
                            f"📌 {status} | "
                            f"📅 {task_deadline}"
                        )


                        st.divider()


            # =========================
            # Delete Project
            # =========================

            st.divider()


            if st.button(
                "🗑 Delete Project",
                key=f"delete_project_{project_id}"
            ):

                st.session_state[
                    f"confirm_delete_{project_id}"
                ] = True


            # =========================
            # Confirmation
            # =========================

            if st.session_state.get(
                f"confirm_delete_{project_id}",
                False
            ):

                st.warning(
                    "This will delete the project "
                    "and all associated tasks."
                )


                col1, col2 = st.columns(2)


                with col1:

                    if st.button(
                        "Yes, Delete",
                        key=f"confirm_{project_id}"
                    ):

                        delete_project(
                            project_id
                        )

                        del st.session_state[
                            f"confirm_delete_{project_id}"
                        ]

                        st.rerun()


                with col2:

                    if st.button(
                        "Cancel",
                        key=f"cancel_{project_id}"
                    ):

                        del st.session_state[
                            f"confirm_delete_{project_id}"
                        ]

                        st.rerun()