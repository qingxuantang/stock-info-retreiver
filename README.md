# stock-info-retreiver
Streamlit based app intergrating Langchain for customized stock info parsing purpose.<br>

The app is combining google search and openai model via api to effectively convert a user input(typically the name of a stock as intended) into a carefully formatted results, in the case of sample code, stock symbol and exchange code seperated by comma.<br>

First, don't forget to copy-paste your openai api key into the openaiapi.json file.<br>

Then, make sure to install all the dependencies.<br>

When all set, just run:<br>

<code>streamlit run main.py</code><br>

Note: You can change the google search keywords or prompt template for openai model in app_qt.py.
