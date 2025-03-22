# import streamlit as st
# from scrape import (
#     scrape_website,
#     extract_body_content,
#     clean_body_content,
#     split_dom_content,
# )
# from parse import parse_with_ollama

# # Streamlit UI
# st.title("AI Web Scraper")
# url = st.text_input("Enter Website URL")

# url = "https://gshow.globo.com/?utm_source=globo.com&utm_medium=header"

# # Step 1: Scrape the Website
# if st.button("Scrape Website"):
#     if url:
#         st.write("Scraping the website...")

#         # Scrape the website
#         dom_content = scrape_website(url)
#         body_content = extract_body_content(dom_content)
#         cleaned_content = clean_body_content(body_content)

#         # Store the DOM content in Streamlit session state
#         st.session_state.dom_content = cleaned_content

#         # Display the DOM content in an expandable text box
#         with st.expander("View DOM Content"):
#             st.text_area("DOM Content", cleaned_content, height=300)


# # Step 2: Ask Questions About the DOM Content
# if "dom_content" in st.session_state:
#     parse_description = st.text_area("Describe what you want to parse")

#     if st.button("Parse Content"):
#         if parse_description:
#             st.write("Parsing the content...")

#             # Parse the content with Ollama
#             dom_chunks = split_dom_content(st.session_state.dom_content)
#             parsed_result = parse_with_ollama(dom_chunks, parse_description)
#             st.write(parsed_result)





from scrape import (
    scrape_website,
    get_html,
    extract_body_content,
    clean_body_content,
    split_dom_content,
)
from parse import parse_with_ollama

def main():
    url = "https://www.tiktok.com/@anitta"

    # Print starting the scraping process
    print("Scraping the website...")

    # Scrape the website
    #dom_content = scrape_website(url)
    dom_content = get_html(url)
    
    # body_content = extract_body_content(dom_content)
    # cleaned_content = clean_body_content(body_content)

    # # Print DOM content
    # print("body_content:")
    # print(body_content)

    # # Define what to parse (this should be dynamic based on your needs or hardcoded as needed)
    # parse_description = "Summary in 20 words"  # Update this as needed

    # print("Parsing the content...")

    # # Parse the content with Ollama
    # dom_chunks = split_dom_content(cleaned_content)
    # parsed_result = parse_with_ollama(dom_chunks, parse_description)
    # print("Parsed Result:")
    # print(parsed_result)

if __name__ == "__main__":
    main()
