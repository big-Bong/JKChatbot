#Calls ChatGPT API using langchain for prompt and context chaining

from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    SystemMessagePromptTemplate)

from VectorStore import create_vectorstore


def askgpt(query):
    system_template="""Use the following pieces of context to answer the users question. 
    In case the context provided does not contain the necessary information, then use your existing knowledge to answer the question.
    If you don't know the answer, just say that "I don't know", don't try to make up an answer.----------------{summaries}"""
    messages = [
        SystemMessagePromptTemplate.from_template(system_template),
        HumanMessagePromptTemplate.from_template("{question}")
    ]
    prompt = ChatPromptTemplate.from_messages(messages)

    chain_type_kwargs = {"prompt": prompt}
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, max_tokens=256)  # Modify model_name if you have access to GPT-4
    chain = RetrievalQAWithSourcesChain.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=create_vectorstore().as_retriever(),
        return_source_documents=False,
        chain_type_kwargs=chain_type_kwargs
    )

    result = chain(query)
    print(result['answer'])
    return result['answer']