<div align="center">
  <img src="https://raw.githubusercontent.com/DenBilokon/doc_X_chat/main/doc_X_chat/chat_llm/static/chat_llm/img/allXlogo.gif" width="700" height="300" alt="DocsXchat">
</div>

# DocsXchat Web App (GoIT final Project)

### DocsXchat is a web application coded on Django framework and Python, that allows you upload your own documents and address questions based on these materials, using the powerful capabilities of LLM models to provide context-sensitive answers.

## DocsXchat Features:
- Allows users to upload PDF files, making them available for content-based queries.
- Provides real-time chatbot responses to user requests about the content of downloaded PDF documents.
- Implements a responsive user interface that provides smooth operation on various devices and enhanced accessibility.
- The chat history function was developed and implemented, allowing users to return to previous conversations with the chatbot, which contributes to a more convenient interaction.
- 
## How to install project:

1. Clone the repository to your computer:

```sh
$ git clone https://github.com/DenBilokon/doc_X_chat.git

```
2. Navigate to the project directory: `cd doc_X_chat`

3. Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv2 --no-site-packages env
$ source env/bin/activate
```
4. Create your **.env file** using env.example:
- Create **Postgres** database to storage data and fill the neccessary fields in **.env file** ( DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_PORT ).
- Use your email account credentials to fill the neccessary fields in **.env file** ( EMAIL_PORT,EMAIL_HOST_USER, EMAIL_HOST_PASSWORD ).
- Create your **Cloudinary account** ( https://cloudinary.com/ ) in order to obtain credentials for **.env file** ( CLOUD_NAME, CLOUD_API_KAY, CLOUD_API_SECRET ). On your **Cloudinary** account **Dashboard** use data from variables **Cloud Name**, **API Key**, **API Secret**.
- Create your **OPEN AI** account ( https://openai.com/blog/openai-api ) and find API Key in order to obtain credentials for **.env file** ( OPENAI_KEY ).

5. Install the dependencies `pip install -r requirements.txt`
6. Make Migrations `python manage.py migrate`
7. Create a superuser `python manage.py createsuperuser`
8. Run the program `python manage.py runserver`
9. Follow the link  `http://127.0.0.1:8000/`.
10. Enjoy!




## Used technologies:
- Python 3.10
- Django 4.2.6
- Langchain (*gpt-3.5-turbo, OpenAIEmbeddings, ChatOpenAI, ConversationBufferMemory, FAISS, RecursiveCharacterTextSplitter*)
- PostgreSQL
- OpenAI API
- Cloudinary
- Bootswatch
- HTML5
- CSS3
- Docker
- Github




# Developers:
1. Denis Bilokon
2. Oleksand Vasylyna
3. Denis Zaitsev
4. Oleksii Latypov

