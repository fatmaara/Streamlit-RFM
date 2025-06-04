import streamlit as st

# Set up page configuration
st.set_page_config(page_title="Portfolio")

# Sidebar Navigation
st.sidebar.title('Homepage')
page = st.sidebar.radio('Pilih halaman:', ['Home', 'Project', 'About Me'])

# Home Page
if page == 'Home':
    st.markdown("<h1 style='text-align: center; font-size: 36px;'>Welcome to My Data Science Portfolio</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; font-size: 24px;'>🚀 Data Science Enthusiast | Storyteller with Data</h3>", unsafe_allow_html=True)

    st.markdown("---")

    # About Me Section (No quote, more about you)
    st.markdown("""  
    <div style='text-align: justify; font-size: 18px;'>
        Welcome to my data science portfolio! I am passionate about using data to tell compelling stories and drive business decisions. 
        Whether it's through predictive modeling, data visualization, or statistical analysis, I strive to make data actionable. 
        In my work, I focus on extracting valuable insights from raw data, transforming it into meaningful narratives that can guide decision-making. 
        I'm always eager to learn new skills and explore innovative data science techniques. 
        Feel free to browse through my projects and see how I tackle complex problems using data.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Closing statement (no quote, just an invitation)
    st.markdown("""  
    <div style='text-align: center; font-size: 16px;'>
        Explore my work and reach out if you'd like to collaborate or learn more!
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")

    # Centered Image Section using st.image
    image_path = "images/images.webp"  # Ensure the correct relative path
    st.image(image_path, width=300, use_container_width=False)  # Set the width to a fixed size

# Project Page
elif page == 'Project':
    import main
    main.project()

# About Me Page
elif page == 'About Me':
    import kontak
    kontak.user()
