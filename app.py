import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains import create_retrieval_chain
from langchain.chains.question_answering import load_qa_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
import PyPDF2
import os


# Streamlit page configuration
st.set_page_config(page_title='Resume Evaluator RAG Application', layout='wide', initial_sidebar_state='expanded')

# Custom CSS styling
st.markdown("""
    <style>
        body {
            font-family: 'Roboto', sans-serif;
            background-color: #000000; /* Black background */
            color: #E0E0E0; /* Light grey text */
        }

        .stSidebar {
            background-color: #2C2C2C; /* Dark grey sidebar */
        }
        .stSidebar>div>div>div>h1 {
            font-size: 28px;
            color: #FF4C4C; /* Red color */
        }

        .main-container {
            background-color: #211d21; /* Dark grey background */
            border: 2px solid #a50113; /* Red border */
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            position: relative;
            top: -20px; /* Adjust this value to move the box up */
        }

        .heading-title {
            font-size: 32px; /* Increase font size for the title */
            font-weight: bold;
            color: #c10206; /* Red color for the title */
            text-align: left;
            margin-bottom: 10px;
        }

        .instructions {
            font-size: 16px;
            color: #E8E8E8; /* Light grey color for the text */
            line-height: 1.6; /* Spacing between lines */
        }
    </style>
""", unsafe_allow_html=True)


#combined heading and instructions box
st.markdown('''
    <div class="main-container">
        <div class="heading-title">REHAB : Resume Enhancement and Helping Assistance Bot</div>
        <div class="instructions">
            <h3>Instructions:</h3>
            <ul>
                <li>Enter your Google API Key in the sidebar.</li>
                <li>Upload your PDF resume file.</li>
                <li>Select the option from the dropdown to specify what assistance you need (e.g., Resume Enhancement, Cover Letter Creation, etc.).</li>
                <li>Type your query or request in the chat input field.</li>
                <li>To clear the conversation, click the 'Clear Chat' button in the sidebar.</li>
            </ul>
        </div>
    </div>
''', unsafe_allow_html=True)

st.sidebar.header("REHAB 📝")
api_key = st.sidebar.text_input("Enter your Google API Key", type="password")
if "messages" not in st.session_state:
    st.session_state.messages = []
    
if 'option' not in st.session_state:
    st.session_state['option'] = 'none'
    
if st.sidebar.button("Clear Chat", key="clear_chat", help="Clear conversation history"):
    st.session_state.messages = []
    
st.session_state.option=st.sidebar.selectbox("select option", ["Default","Resume Enhancement","Cover Letter Creation","Career Advice","Skills Assessment","Keyword Optimization"])
    
def get_prompt(option):
    # using different system prompts based on user-selected options
    if option=="Default":
        system_prompt=(
            "You are a helpful assistant and I have a general query regarding my resume  "
            "Before you provide a solution, please ask for any specific details or context that might help you better understand my situation."
            "you need to fully understand my question. Ensure your response is clear, concise, and tailored to address my concern effectively."
            "suggest the best approach based on my goals or requirements.\n"
        "{context}"
        )
    elif option=="Resume Enhancement":
        system_prompt=(
            "You are an assistant for evaluating resumes based on the provided query. "
            "enhance my resume. Before you proceed, ask me for any additional information you might need, such as specific skills, "
            "experiences, achievements, or career goals that could improve the resume"
            "be concise and make sure to look over every detail like college tier,skills and how relevant they are to industry\n"
            "{context}"
        )       
    elif option=="Cover Letter Creation":
        system_prompt=(
            "Create a personalized cover letter for my job application. "
            "Before you proceed, ask me for additional information, such as the target job role, company details,"
            "key skills, and experiences I should highlight. Make sure the cover letter is concise, tailored to the job,"
            "and demonstrates how my skills and background align with the company’s goals.\n"
            "{context}"
        )
    elif option=="Career Advice":
        system_prompt=(
            "I’m seeking career advice to align my skills and experiences with my long-term goals."
            "Please ask for any specific information you need, such as my current role, career aspirations, strengths,"
            "weaknesses, and areas for improvement. Provide guidance on how I can enhance my skill set,"
            "gain relevant experience, and stay competitive in the job market.\n"
            "{context}"
        )
    elif option=="Skills Assessment":
        system_prompt=(
            "Please assess my current skill set and identify strengths, weaknesses, and areas for improvement."
            "Before proceeding, ask me for details about my career goals, industry, and any specific technical or soft skills"
            "I want to focus on. Provide feedback on how my skills align with industry standards and suggest ways to enhance them "
            "for career growth\n"
            "{context}"
        )
    else:
        system_prompt=(
            "Optimize my resume/cover letter with relevant industry keywords. "
            "Before proceeding, ask me for details about the job role, industry, and specific skills or experiences I want to highlight."
            "Ensure the keywords align with the job description and industry standards to improve my chances of passing Applicant Tracking Systems (ATS).\n"
            "{context}"
        )
    return system_prompt
def pdf_to_text(file):
    """Convert the PDF file to text."""
    pdf_reader = PyPDF2.PdfReader(file)  # Creates a PDF reader object
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()  # Extracts text from each page
    return text

def load_and_process_pdf(file):
    """Load the PDF, split text, and prepare the RAG chain."""
    content = pdf_to_text(file)  # Extracts text from PDF using the pdf_to_text function 
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)  # Initializes the text splitter
    splits = text_splitter.split_text(content)  # Splits text into chunks
    documents = [Document(page_content=chunk) for chunk in splits]  # Converts chunks to Document objects

    if not api_key:
        st.error("Google API Key is required.")  # Shows an error if API key is missing
        return None
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")  # Initializes embedding model
    vectorstore = FAISS.from_documents(documents=documents, embedding=embeddings)  # Creates a FAISS vector store
    retriever = vectorstore.as_retriever()  # Create a retriever from vector store
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key)  # Initializes generative AI model in this case its a google gemini
    system_prompt = get_prompt(st.session_state.option)  # Get system prompt based on user option
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ]) 
    question_answer_chain = load_qa_chain(llm, chain_type="stuff", prompt=prompt)  # Load QA chain
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)  # Creates a RAG chain which will be used to invoke queries 
    return rag_chain, documents
def main():
    if api_key:
        os.environ['GOOGLE_API_KEY'] = api_key
    # File uploader in the sidebar
    uploaded_file = st.sidebar.file_uploader("Upload a PDF resume", type="pdf")
    if st.session_state.option:
        if uploaded_file :
            rag_chain,documents = load_and_process_pdf(uploaded_file) # File uploader in the sidebar
        else :
            rag_chain,documents= None,None
    # displaying messages in the session
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if query := st.chat_input("Enter your query"):
        st.session_state.messages.append({"role": "user", "content": query}) # adding user query to session state(messages)
        with st.chat_message("user"):
            st.markdown(query)# Displaying user query
        if uploaded_file:       
            if api_key and rag_chain:
                with st.spinner('Processing...'):
                    try:
                        response = rag_chain.invoke({"input": query, "input_documents": documents}) # Invoke RAG chain for the query
                        answer = response["answer"]["output_text"] #extracting the required text form the response received 
                        st.write(answer)
                        st.session_state.messages.append({"role": "assistant", "content": answer})# Add assistant's answer to session state(messages)
                    except Exception as e:
                        st.error(f"An error occurred: {e}")  # Show error if something goes wrong
                              
            else:
                st.warning("Please enter a query") # show warning if no query is entered 
        else:
            st.warning("Please upload your resume")  # Show warning if no resume is uploaded

if __name__ == "__main__":
    main()
