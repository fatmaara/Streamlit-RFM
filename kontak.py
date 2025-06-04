import streamlit as st

def user():
    st.title("👋 Hi, I'm Fatma Ramadianti")

    st.markdown("""  
        <div style='text-align: justify; font-size: 18px;'>
            I am a graduate in Statistics with a strong passion for Data Science. I have hands-on experience in data analysis, visualization, and machine learning. 
            I have worked with large datasets, performing data cleaning, feature engineering, and developing predictive models to generate actionable insights. 
            My expertise lies in Python, SQL, and Power BI, and I’m passionate about using data storytelling to drive business decisions. With a strong foundation in statistics and mathematics, I enjoy creating compelling data visualizations, designing interactive dashboards, 
            and leveraging machine learning techniques to solve problems. I'm always eager to expand my knowledge and apply my skills to tackle new challenges.
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("")

    st.markdown("Feel free to explore my projects to see how I use data to turn complex questions into clear answers.")

    st.markdown("")

    st.write("📫 Let's connect!")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("[📧 Email](mailto:fatmaramadianti6@gmail.com)", unsafe_allow_html=True)  # Replace with your actual email
    with col2:
        st.markdown("[💼 LinkedIn](www.linkedin.com/in/fatmaramadian)", unsafe_allow_html=True)  # Replace with your actual LinkedIn URL
    with col3:
        st.markdown("[✍️ Medium](https://medium.com/@fatmaramadianti6)", unsafe_allow_html=True)  # Replace with your actual Medium URL

if __name__ == "__main__":
    user()
