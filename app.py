import streamlit as st
from mydatabase_scripts import connect, run_query, create_post, like_post, add_comment, add_hashtag, add_hashtags_to_post, bookmark_post, follow_user, authenticate_user


def main():
    st.title("Social Media Admin Panel")

    # Get or create session state to store persistent data
    session_state = st.session_state
    if 'login_successful' not in session_state:
        session_state.login_successful = False

    # Add login functionality
    username = st.sidebar.text_input("Username", key="username")
    password = st.sidebar.text_input(
        "Password", key="password", type="password")
    login_button = st.sidebar.button("Login")

    if login_button:
        if authenticate_user(username, password):
            session_state.login_successful = True
            st.success("Login successful")
        else:
            session_state.login_successful = False
            st.error("Invalid username or password")

    # Check if the user is logged in before displaying the admin panel
    if session_state.login_successful:
        display_admin_panel()


def display_admin_panel():
    connection = connect()

    if connection:
       # st.success("Connected to the database")

        st.sidebar.header("Admin Configuration")

        if st.sidebar.button("Run Custom Query"):
            custom_query = st.text_area("Enter your query:")
            if custom_query:
                result = run_query(custom_query, connection)
                if result is not None:
                    st.table(result)

        st.sidebar.header("Display Tables")

        tables = ["users", "photos", "videos", "post", "comments", "post_likes",
                  "comment_likes", "follows", "hashtags", "hashtag_follow",
                  "post_tags", "bookmarks", "login"]

        selected_table = st.sidebar.selectbox("Select a table", tables)
        if st.sidebar.button("Show Table"):
            query = f"SELECT * FROM {selected_table}"
            result = run_query(query, connection)
            if result is not None:
                st.table(result)

        st.sidebar.header("Execute Stored Procedures")

        # Placeholder for dynamic input fields
        input_placeholder = st.empty()

        # Get the selected operation
        selected_operation = st.sidebar.selectbox("Select Operation", [
            "Add Comment", "Like Post", "Follow User", "Bookmark Post", "Add Hashtag", "Add Hashtags to Post"])

        # Based on the selected operation, display relevant input fields
        if selected_operation == "Add Comment":
            add_comment_input(input_placeholder)
        elif selected_operation == "Like Post":
            like_post_input(input_placeholder)
        elif selected_operation == "Follow User":
            follow_user_input(input_placeholder)
        elif selected_operation == "Bookmark Post":
            bookmark_post_input(input_placeholder)
        elif selected_operation == "Add Hashtag":
            add_hashtag_input(input_placeholder)
        elif selected_operation == "Add Hashtags to Post":
            add_hashtags_to_post_input(input_placeholder)

        connection.close()


def add_comment_input(placeholder):
    user_id_comment = st.text_input(
        "Add Comment: User ID", key="add_comment_user_id")
    post_id_comment = st.text_input(
        "Add Comment: Post ID", key="add_comment_post_id")
    comment_text = st.text_input(
        "Add Comment: Comment Text", key="add_comment_text")

    if st.button("Add Comment"):
        add_comment(user_id_comment, post_id_comment, comment_text)


def like_post_input(placeholder):
    user_id_like = st.text_input("Like Post: User ID", key="like_post_user_id")
    post_id_like = st.text_input("Like Post: Post ID", key="like_post_post_id")

    if st.button("Like Post"):
        like_post(user_id_like, post_id_like)


def follow_user_input(placeholder):
    follower_id = st.text_input(
        "Follow User: Follower ID", key="follow_user_follower_id")
    followee_id = st.text_input(
        "Follow User: Followee ID", key="follow_user_followee_id")

    if st.button("Follow User"):
        follow_user(follower_id, followee_id)


def bookmark_post_input(placeholder):
    user_id_bookmark = st.text_input(
        "Bookmark Post: User ID", key="bookmark_post_user_id")
    post_id_bookmark = st.text_input(
        "Bookmark Post: Post ID", key="bookmark_post_post_id")

    if st.button("Bookmark Post"):
        bookmark_post(user_id_bookmark, post_id_bookmark)


def add_hashtag_input(placeholder):
    hashtag_name = st.text_input(
        "Add Hashtag: Hashtag Name", key="add_hashtag_name")

    if st.button("Add Hashtag"):
        add_hashtag(hashtag_name)


def add_hashtags_to_post_input(placeholder):
    hashtags_to_post = st.text_input(
        "Add Hashtags to Post: Hashtags", key="add_hashtags_to_post_hashtags")
    post_id_hashtags = st.text_input(
        "Add Hashtags to Post: Post ID", key="add_hashtags_to_post_post_id")

    if st.button("Add Hashtags to Post"):
        add_hashtags_to_post(hashtags_to_post, post_id_hashtags)


if __name__ == "__main__":
    main()
