import mysql.connector
from mysql.connector import Error
import streamlit as st


def connect():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            database="social_media",
            user="root",
            password="Sanjeev$88"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        st.error(f"Error: {e}")
        return None


def authenticate_user(username, password):
    # Implement your user authentication logic here
    # You may check credentials against a database or any other authentication method
    return username == "admin" and password == "admin"


def run_query(query, connection):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        connection.commit()
        return result
    except Error as e:
        st.error(f"Error executing query: {e}")
        return None
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()


def create_post(user_id, caption, location, photo_url, video_url, hashtags):
    connection = connect()
    if connection:
        try:
            cursor = connection.cursor()

            # Call the stored procedure to create a post
            cursor.callproc('CreatePost', (user_id, caption,
                            location, photo_url, video_url, hashtags))

            # Commit the changes
            connection.commit()
            st.success("Post created successfully!")
        except Exception as e:
            st.error(f"Error creating post: {str(e)}")
        finally:
            cursor.close()
            connection.close()


def add_comment(user_id, post_id, comment_text):
    connection = connect()
    if connection:
        try:
            cursor = connection.cursor()

            # Call the stored procedure to add a comment
            cursor.callproc('AddComment', (user_id, post_id, comment_text))

            # Commit the changes
            connection.commit()
            st.success("Comment added successfully!")
        except Exception as e:
            st.error(f"Error adding comment: {str(e)}")
        finally:
            cursor.close()
            connection.close()


def like_post(user_id, post_id):
    connection = connect()
    if connection:
        try:
            cursor = connection.cursor()

            # Call the stored procedure to like a post
            cursor.callproc('LikePost', (user_id, post_id))

            # Commit the changes
            connection.commit()
            st.success("Post liked successfully!")
        except Exception as e:
            st.error(f"Error liking post: {str(e)}")
        finally:
            cursor.close()
            connection.close()


def follow_user(follower_id, followee_id):
    connection = connect()
    if connection:
        try:
            cursor = connection.cursor()

            # Call the stored procedure to follow a user
            cursor.callproc('FollowUser', (follower_id, followee_id))

            # Commit the changes
            connection.commit()
            st.success("User followed successfully!")
        except Exception as e:
            st.error(f"Error following user: {str(e)}")
        finally:
            cursor.close()
            connection.close()


def bookmark_post(user_id, post_id):
    connection = connect()
    if connection:
        try:
            cursor = connection.cursor()

            # Call the stored procedure to bookmark a post
            cursor.callproc('BookmarkPost', (user_id, post_id))

            # Commit the changes
            connection.commit()
            st.success("Post bookmarked successfully!")
        except Exception as e:
            st.error(f"Error bookmarking post: {str(e)}")
        finally:
            cursor.close()
            connection.close()


def add_hashtag(hashtag_name):
    connection = connect()
    if connection:
        try:
            cursor = connection.cursor()

            # Call the stored procedure to add a hashtag
            cursor.callproc('AddHashtag', (hashtag_name,))

            # Commit the changes
            connection.commit()
            st.success("Hashtag added successfully!")
        except Exception as e:
            st.error(f"Error adding hashtag: {str(e)}")
        finally:
            cursor.close()
            connection.close()


def add_hashtags_to_post(hashtags, post_id):
    connection = connect()
    if connection:
        try:
            cursor = connection.cursor()

            # Call the stored procedure to add hashtags to a post
            cursor.callproc('AddHashtagsToPost', (hashtags, post_id))

            # Commit the changes
            connection.commit()
            st.success("Hashtags added to post successfully!")
        except Exception as e:
            st.error(f"Error adding hashtags to post: {str(e)}")
        finally:
            cursor.close()
            connection.close()


def main():
    st.title("Social Media Admin Panel")

    # Add login functionality
    username = st.sidebar.text_input("Username", key="username")
    password = st.sidebar.text_input(
        "Password", key="password", type="password")
    login_button = st.sidebar.button("Login")

    if login_button:
        if authenticate_user(username, password):
            st.success("Login successful")
            display_admin_panel()
        else:
            st.error("Invalid username or password")


def display_admin_panel():
    connection = connect()

    if connection:
        st.success("Connected to the database")

        st.sidebar.header("Admin Configuration")

        # Interface to create a post
        st.sidebar.subheader("Create Post")
        user_id = st.sidebar.number_input("User ID", min_value=1)
        caption = st.sidebar.text_input("Caption")
        location = st.sidebar.text_input("Location")
        photo_url = st.sidebar.text_input("Photo URL")
        video_url = st.sidebar.text_input("Video URL")
        hashtags = st.sidebar.text_input("Hashtags")

        if st.sidebar.button("Create Post"):
            create_post(user_id, caption, location,
                        photo_url, video_url, hashtags)

        # Interface to add a comment
        st.sidebar.subheader("Add Comment")
        user_id_comment = st.sidebar.number_input("User ID", min_value=1)
        post_id_comment = st.sidebar.number_input("Post ID", min_value=1)
        comment_text = st.sidebar.text_input("Comment Text")

        if st.sidebar.button("Add Comment"):
            add_comment(user_id_comment, post_id_comment, comment_text)

        # Interface to like a
