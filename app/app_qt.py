# -*- coding: UTF-8 -*-

def main():
    '''Main function for the app.'''
    import os
    import re
    import streamlit as st 
    from langchain.llms import OpenAI
    from langchain.prompts import PromptTemplate
    from langchain.chains import LLMChain, SequentialChain 
    from langchain.memory import ConversationBufferMemory
    from langchain.utilities import WikipediaAPIWrapper 
    from bs4 import BeautifulSoup
    import requests
    from importlib import reload
    from . import utils #relative import
    utils = reload(utils)

    #Error log
    pkg_path = utils.pkg_path
    filename = re.findall('(.*).py', os.path.basename(__file__))
    utils.errorLog(pkg_path,filename)

    #OpenAI API key
    openai_apikey  = utils.loadJSON(json_name='openaiapi')['key']
    os.environ['OPENAI_API_KEY'] = openai_apikey


    #App framework
    st.title('🦜🔗 Stock Info Retreiver')
    query = st.text_input("请输入你想了解的A股股票名称或股票代码:")


    #Leveraging google search results via streamlit.
    def googleSearch(query):
        '''Return Google search results.'''
        from googlesearch import search
        results = []
        for j in search(query, num=5, start=0, stop=5, pause=2.0):
            results.append(j)
        return results
    

    #Specify search inputs and parse results with bs4.
    def queryToPrompt():
        results = googleSearch(query+'的股票代码')
        prompt = []
        for result in results:
            try:
                response = requests.get(result)
                soup = BeautifulSoup(response.text, 'html.parser')
                title = soup.title.string if soup.title else ""
                snippet = soup.find('meta', attrs={'name': 'description'})
                snippet = snippet['content'] if snippet else ""
                prompt.append(f"Title: {title}\nSnippet: {snippet}")
                #st.write(f"Title: {title}")
                #st.write(f"Snippet: {snippet}")
            #except requests.exceptions.SSLError:
            except Exception as e:
                utils.exceptionLog(pkg_path,filename,func_name=queryToPrompt.__name__,error=e,loop_item='nothing(not a loop)')
                pass
        return prompt
    

    google_search_result = queryToPrompt()
    

    #Prompt templates: combining user input(a.k.a. symbol) and google search results for specified outputs in nature syntax prompt.
    symbol_template = PromptTemplate(
        input_variables = ['symbol','google_search_result'], 
        template='''根据以下信息，告诉我 {symbol} 的股票代码是什么。 {google_search_result} 
                    另外请根据以下提示，告诉我 {symbol} 的交易所代号。提示：如果股票代码第一位数为0或者3，则交易所代号为sz；
                    如果股票代码第一位数为6或者9，则交易所代号为sh。
                    最终答案请只提供股票代码数字和交易所代号，用英文逗号分隔。'''
    )
    

    #Memory 
    symbol_memory = ConversationBufferMemory(input_key='symbol', memory_key='chat_history')


    #LLMs
    llm = OpenAI(temperature=0.9) 
    symbol_chain = LLMChain(llm=llm, prompt=symbol_template, verbose=True, memory=symbol_memory) #, output_key='title'


    #Show stuff to the screen if there's a user input query
    if query:
        
        st.write(google_search_result)

        input = {'symbol': query, 'google_search_result': google_search_result}
        title = symbol_chain.run(input)

        st.write(title)

        with st.expander('Symbol History'): 
            st.info(symbol_memory.buffer)
