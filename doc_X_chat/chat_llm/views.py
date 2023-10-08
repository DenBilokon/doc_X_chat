# import fitz  # PyMuPDF
import os
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from dotenv import load_dotenv

from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.llms.openai import OpenAI
from langchain.callbacks import get_openai_callback
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory

from PyPDF2 import PdfReader
from .forms import PDFUploadForm, PDFUpdateForm, PDFDocumentForm2
from .models import ChatMessage, PDFDocument, UserData

load_dotenv()


def main(request):
    # avatar = Avatar.objects.filter(user_id=request.user.id).first()
    return render(request, 'chat_llm/index.html', context={})


def get_pdf_text(pdf):
    """
    Retrieves text from a PDF document.

    :param pdf: PDF file.
    :return: Extracted text from the PDF.
    """
    text = None
    if pdf:
        pdf_reader = PdfReader(pdf)
        text = ''.join(page.extract_text() for page in pdf_reader.pages)
    return text


def get_text_chunks(text):
    """
    Splits text into chunks.

    :param text: Input text.
    :return: List of text chunks.
    """
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    """
    Retrieves the vector store for text chunks.

    :param text_chunks: List of text chunks.
    :return: Knowledge base vector store.
    """
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    knowledge_base = FAISS.from_texts(text_chunks, embeddings)
    return knowledge_base


def get_conversation_chain(vectorstore):
    """
    Retrieves the conversation chain.

    :param vectorstore: Vector store.
    :return: Conversational retrieval chain.
    """
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


@login_required(login_url="/login/")
def upload_pdf(request):
    """
    Handles the PDF upload.

    :param request: HTTP request.
    :return: JSON response.
    """
    user = request.user

    try:
        user_data = UserData.objects.get(user=user)
    except UserData.DoesNotExist:
        # Обробка ситуації, коли відсутній запис UserData для користувача.
        # Можна створити запис за замовчуванням тут.
        user_data = UserData.objects.create(user=user, subscribe_plan='free', total_files_uploaded=0,
                                            total_questions_asked=0)

    # Отримати обмеження для користувача залежно від плану підписки
    max_files_allowed = user_data.max_files_allowed_for_plan()

    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_document = request.FILES['pdf_document']

            # Перевірити, чи користувач перевищив обмеження для завантажених файлів
            if user_data.total_files_uploaded >= max_files_allowed:
                return JsonResponse({'error': 'Ви досягли обмеження для завантажених файлів.'}, status=400)

            # Перевірити, чи файл з такою назвою вже існує для цього користувача
            if PDFDocument.objects.filter(user=user, title=pdf_document.name).exists():
                return JsonResponse({'error': 'Файл з такою назвою вже існує.'}, status=400)

            # Збільшити кількість завантажених файлів користувача
            user_data.total_files_uploaded += 1
            user_data.save()

            # Зберегти PDF-документ у базі даних
            pdf = PDFDocument(user=user, title=pdf_document.name)
            pdf.documentContent = get_pdf_text(pdf_document)
            pdf.save()

    else:
        form = PDFUploadForm()
    user_pdfs = PDFDocument.objects.filter(user=request.user)
    # file_context = ask_question(request)
    chat_message = ChatMessage.objects.all()
    return render(request, 'chat_llm/chat_base.html', {'form': form, 'user_pdfs': user_pdfs, 'chat_message': chat_message})


@login_required(login_url="/login/")
def ask_question(request):
    """
    Handles the user's question and generates a response.

    :param request: HTTP request.
    :return: Rendered page with the response.
    """

    # chat_history = ChatMessage.objects.filter(user=request.user).order_by(
    #     'timestamp')[:3]  # Retrieve chat history for the logged-in user
    chat_history = ChatMessage.objects.filter(user=request.user).order_by(
        'timestamp')[:10]
    chat_response = ''
    user_pdfs = PDFDocument.objects.filter(user=request.user)
    user_question = ""

    if request.method == 'POST':
        user_question = request.POST.get('user_question')
        print(f'user question:  {user_question}')
        selected_pdf_id = request.POST.get('selected_pdf')
        print(f'selected_pdf_id:  {selected_pdf_id}')
        selected_pdf = get_object_or_404(PDFDocument, id=selected_pdf_id)
        text_chunks = get_text_chunks(selected_pdf.documentContent)

        knowledge_base = get_vectorstore(text_chunks)
        conversation_chain = get_conversation_chain(knowledge_base)

        with get_openai_callback() as cb:
            # print(f'cd: {cb}')
            response = conversation_chain({'question': user_question})
            print(f'response: {response}')
            # response = cb.complete(response)

        chat_response = response["answer"]
        print(f'chat_response: {chat_response}')
        chat_message = ChatMessage(user=request.user, message=user_question, answer=chat_response)

        chat_message.save()
    # chat_history = ChatMessage.objects.filter(user=request.user).order_by(
    #     'timestamp')[:10]

    user_pdfs = PDFDocument.objects.filter(user=request.user)
    chat_message = ChatMessage.objects.all()
    context = {'chat_response': chat_response, 'chat_history': chat_history, 'user_question': user_question,
               'user_pdfs': user_pdfs, 'chat_message': chat_message}

    return render(request, 'chat_llm/chat_base.html', context)
    #return redirect(to='chat_llm:main')


@login_required(login_url="/login/")
def view_pdf(request, pdf_id):
    """
    Displays a PDF document.

    :param request: HTTP request.
    :param pdf_id: ID of the PDF document.
    :return: Rendered page with the PDF document.
    """
    pdf = PDFDocument.objects.get(id=pdf_id)
    return render(request, 'view_pdf.html', {'pdf': pdf})


@login_required(login_url="/login/")
def view_chat_history(request):
    """
    Displays the chat history for the logged-in user.

    :param request: HTTP request.
    :return: Rendered page with chat history.
    """
    chat_messages = ChatMessage.objects.filter(user=request.user)
    return render(request, 'view_chat_history.html', {'chat_messages': chat_messages})


def list_pdfs(request):
    """
    Lists PDF documents for the logged-in user.

    :param request: HTTP request.
    :return: Rendered page with the list of PDF documents.
    """
    pdfs = PDFDocument.objects.filter(user=request.user)
    return render(request, 'edit_pdf.html', {'pdfs': pdfs})


def delete_pdf(request, pdf_id):
    """
    Deletes a PDF document.

    :param request: HTTP request.
    :param pdf_id: ID of the PDF document to delete.
    :return: Redirect or error response.
    """
    try:
        pdfs = PDFDocument.objects.get(id=pdf_id)
        pdf_title = getattr(pdfs, 'document', pdfs.title)
        pdfs.delete()
        return redirect('/pdfs/')
    except PDFDocument.DoesNotExist:
        # Handle the case where the PDFDocument with the given id does not exist
        return HttpResponseNotFound("PDF not found")


def update_pdf(request, pdf_id):
    """
    Updates a PDF document.

    :param request: HTTP request.
    :param pdf_id: ID of the PDF document to update.
    :return: Rendered page with the updated PDF document.
    """
    pdf = get_object_or_404(PDFDocument, pk=pdf_id)
    if request.method == 'POST':
        form = PDFDocumentForm2(request.POST, instance=pdf)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pdf updated successfully.')
            return redirect('/pdfs/')
    else:
        form = PDFUpdateForm(instance=pdf)
    return render(request, 'update_pdf.html', {'form': form, 'pdf': pdf})
