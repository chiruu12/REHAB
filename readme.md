# 📝 REHAB - Resume Enhancement and Helping Assistance Bot

Welcome to REHAB, your comprehensive assistant for enhancing resumes, creating cover letters, and providing career advice. This interactive tool leverages advanced AI capabilities to help users optimize their resumes and professional documents.

**This repository is a standalone project** designed to offer personalized assistance in resume building and career development.

## Table of Contents

1. [Project Description](#project-description)
2. [End User](#end-user)
3. [Industry Impact](#industry-impact)
4. [Business Value](#business-value)
5. [Utilization of LLM App](#utilization-of-llm-app)
6. [Technical Implementation](#technical-implementation)
7. [Installation and Setup](#installation-and-setup)
8. [Usage Instructions](#usage-instructions)
9. [Contributing](#contributing)
10. [License](#license)

## Project Description

REHAB is designed to assist users in creating and enhancing resumes, drafting cover letters, and providing career advice. It utilizes advanced AI models to offer detailed, personalized support, making it a helpful tool for job seekers and professionals looking to improve their resumes and application materials.

### End User

- Job seekers looking to enhance their resumes and cover letters
- Professionals needing help with career development and job applications
- Students and recent graduates preparing to enter the job market

### Industry Impact

REHAB can will help people with the job application process by offering a scalable solution for resume and cover letter creation, enhancing user experience and increasing the chances of securing job opportunities.

### Business Value

Integrating REHAB into career services, online job platforms, and professional development programs can improve client satisfaction, increase engagement, and provide a competitive edge in the job market.

### Utilization of LLM App

REHAB utilizes Google Gemini GenAI for processing user queries and generating accurate, contextually relevant responses in real-time, enhancing the effectiveness of resume and cover letter optimization.

### Technical Implementation

- **Google Gemini GenAI**: Used for generating responses and processing user input.
- **Streamlit**: Used for the front-end, creating an interactive web application.
- **FAISS**: Used for efficient similarity search and retrieval of relevant information.
- **LangChain**: Utilized for integrating language models with retrieval-augmented generation (RAG) functionality.

## Installation and Setup

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/your-repository/research-assistant-bot.git
    ```

2. **Navigate to the Project Directory**:
    ```bash
    cd research-assistant-bot
    ```

3. **Install Required Packages**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Application**:
    ```bash
    streamlit run app.py
    ```


# Using Docker to Install and Run the Application

### Prerequisites
- Make sure Docker is installed on your system. If not, [install Docker](https://docs.docker.com/get-docker/) for your operating system.

### Steps to Run the Application with Docker

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/your-repository/research-assistant-bot.git
    ```

2. **Navigate to the Project Directory**:
    ```bash
    cd resume-assistant-bot
    ```

3. **Build the Docker Image**:
   Ensure that the Dockerfile is located in the root directory of your project. Build the Docker image using the following command:
    ```bash
    docker build -t rehab-app .
    ```

4. **Run the Docker Container**:
   After successfully building the image, run the container using:
    ```bash
    docker run -d -p 8501:8501 --name rehab-container rehab-app
    ```
   This command will:
   - Start the container in detached mode (`-d`).
   - Map port `8501` (Streamlit's default port) from the container to port `8501` on your host machine.

5. **Access the Application**:
   Open your web browser and go to: http://localhost:8501 


   ## Additional Docker Commands

- **Stop the Docker Container**:
```bash
docker stop rehab-container
```

- **Restart the Docker Container**:
```bash
docker start rehab-container
```

- **Remove the Docker Container**:
 ```bash
 docker rm rehab-container
 ```

- **Remove the Docker Image**:
 ```bash
 docker rmi rehab-app
 ```



## Usage Instructions

1. Open your web browser and navigate to `http://localhost:8501`.
2. Enter your Google API Key in the sidebar.
3. Upload your PDF resume file.
4. Select the type of assistance you need from the dropdown menu.
5. Enter your query or request in the chat input field and press 'Enter'.
6. REHAB will provide detailed responses based on your input.

### Sidebar Instructions

1. Enter your Google API Key and upload your resume.
2. Select the desired assistance option from the dropdown menu.
3. Type your query or request in the chat input field.
4. Click 'Enter' to receive a detailed response.

## Contributing

We welcome contributions to enhance REHAB! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
