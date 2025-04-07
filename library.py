import streamlit as st
import json
import os

data_file = 'library.txt'

def load_library():
    if os.path.exists(data_file):
        with open(data_file, 'r') as file:
            return json.load(file)
    return []

def save_library(library):
    with open(data_file, 'w') as file:
        json.dump(library, file, indent=4)

def add_book_form():
    st.subheader("Add a New Book")
    with st.form("add_book_form", clear_on_submit=True):
        title = st.text_input("Title")
        author = st.text_input("Author")
        year = st.text_input("Year")
        genre = st.text_input("Genre")
        read = st.selectbox("Have you read this book?", ["No", "Yes"])
        submitted = st.form_submit_button("Add Book")

        if submitted:
            if title and author and year and genre:
                new_book = {
                    'title': title,
                    'author': author,
                    'year': year,
                    'genre': genre,
                    'read': read.lower() == 'yes'
                }
                library = load_library()
                library.append(new_book)
                save_library(library)
                st.success(f"✅ Book '{title}' added successfully!")
            else:
                st.warning("Please fill in all the fields.")

def remove_book_section():
    st.subheader("Remove a Book")
    library = load_library()
    titles = [book['title'] for book in library]
    if titles:
        selected = st.selectbox("Select a book to remove", titles)
        if st.button("Remove Book"):
            library = [book for book in library if book['title'] != selected]
            save_library(library)
            st.success(f"❌ Book '{selected}' removed successfully.")
    else:
        st.info("Library is empty. Nothing to remove.")

def search_library_section():
    st.subheader("Search Library")
    library = load_library()
    search_by = st.radio("Search by", ["title", "author"])
    query = st.text_input(f"Enter the {search_by} to search")
    if query:
        results = [book for book in library if query.lower() in book[search_by].lower()]
        if results:
            st.success(f"Found {len(results)} result(s):")
            for book in results:
                status = "✅ Read" if book['read'] else "📖 Unread"
                st.markdown(f"- **{book['title']}** by {book['author']} ({book['year']}) - *{book['genre']}* - {status}")
        else:
            st.warning("No matching books found.")

def display_all_books_section():
    st.subheader("All Books in Library")
    library = load_library()
    if library:
        for book in library:
            status = "✅ Read" if book['read'] else "📖 Unread"
            st.markdown(f"- **{book['title']}** by {book['author']} ({book['year']}) - *{book['genre']}* - {status}")
    else:
        st.info("The library is currently empty.")

def display_statistics_section():
    st.subheader("Library Statistics")
    library = load_library()
    total_books = len(library)
    read_books = len([book for book in library if book['read']])
    percentage_read = (read_books / total_books) * 100 if total_books else 0

    col1, col2 = st.columns(2)
    col1.metric("📚 Total Books", total_books)
    col2.metric("✅ Read (%)", f"{percentage_read:.2f}%")

def main():
    st.set_page_config(page_title="📖 Library Manager", layout="centered", page_icon="📚")
    st.title("📚 Personal Library Manager")

    tabs = st.tabs(["📘 Add Book", "🗑️ Remove Book", "🔍 Search", "📂 All Books", "📊 Statistics"])

    with tabs[0]:
        add_book_form()
    with tabs[1]:
        remove_book_section()
    with tabs[2]:
        search_library_section()
    with tabs[3]:
        display_all_books_section()
    with tabs[4]:
        display_statistics_section()

if __name__ == '__main__':
    main()
