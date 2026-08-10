import streamlit as st

st.set_page_config(
    page_title="FlowPilot",
    page_icon="🚀",
    layout="wide"
)

from database import (
    create_tables,
    get_task_count,
    get_task_status_counts,
    get_project_count
)

create_tables()


st.title("🚀 FlowPilot")

st.write(
    "AI-powered project management platform"
)


# Get statistics

project_count = get_project_count()

task_count = get_task_count()

status_counts = get_task_status_counts()

status_dict = dict(status_counts)

todo_count = status_dict.get("Todo", 0)

in_progress_count = status_dict.get("In Progress", 0)

done_count = status_dict.get("Done", 0)


# Metrics

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Projects",
        project_count
    )

with col2:
    st.metric(
        "Total Tasks",
        task_count
    )

with col3:
    st.metric(
        "In Progress",
        in_progress_count
    )

with col4:
    st.metric(
        "Completed",
        done_count
    )


st.divider()


# Task Progress

st.subheader("📊 Task Progress")

if task_count > 0:

    progress = done_count / task_count

    st.progress(progress)

    st.write(
        f"{done_count} of {task_count} tasks completed "
        f"({progress:.0%})"
    )
    
    if task_count > 0:

        st.success(
            f"Completion rate: {progress:.0%}"
        )

else:

    st.info(
        "No tasks yet. Create a project and generate tasks from a meeting."
    )


# Task Status

st.subheader("📋 Task Status")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Todo",
        todo_count
    )

with col2:
    st.metric(
        "In Progress",
        in_progress_count
    )

with col3:
    st.metric(
        "Done",
        done_count
    )