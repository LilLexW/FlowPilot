import sqlite3

DB_NAME = "flowpilot.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        description TEXT,
        deadline TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER,
        task_name TEXT,
        owner TEXT,
        priority TEXT,
        status TEXT,
        deadline TEXT
    )
    """)

    conn.commit()
    conn.close()
    
def add_project(name, description, deadline):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO projects(name,description,deadline)
        VALUES(?,?,?)
        """,
        (
            name,
            description,
            str(deadline)
        )
    )

    conn.commit()

    conn.close()


def get_projects():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM projects"
    )

    rows = cursor.fetchall()

    conn.close()

    return rows

def add_task(project_id, task_name, owner, priority, status, deadline):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO tasks(
            project_id,
            task_name,
            owner,
            priority,
            status,
            deadline
        )
        VALUES(?,?,?,?,?,?)
        """,
        (
            project_id,
            task_name,
            owner,
            priority,
            status,
            str(deadline)
        )
    )

    conn.commit()
    conn.close()

def get_tasks():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks")

    rows = cursor.fetchall()

    conn.close()

    return rows

def update_task_status(task_id, status):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE tasks
        SET status = ?
        WHERE id = ?
        """,
        (
            status,
            task_id
        )
    )

    conn.commit()
    conn.close()
    
def update_task(
    task_id,
    task_name,
    owner,
    priority,
    deadline
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE tasks
        SET task_name = ?,
            owner = ?,
            priority = ?,
            deadline = ?
        WHERE id = ?
        """,
        (
            task_name,
            owner,
            priority,
            str(deadline),
            task_id
        )
    )

    conn.commit()
    conn.close()
    
def get_task_count():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM tasks"
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count

def get_task_status_counts():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT status, COUNT(*)
        FROM tasks
        GROUP BY status
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows

def get_project_count():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM projects"
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count

def delete_task(task_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM tasks
        WHERE id = ?
        """,
        (task_id,)
    )

    conn.commit()
    conn.close()
    
def task_exists(project_id, task_name):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM tasks
        WHERE project_id = ?
        AND task_name = ?
        """,
        (
            project_id,
            task_name
        )
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count > 0

def project_exists(name):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM projects
        WHERE name = ?
        """,
        (name,)
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count > 0