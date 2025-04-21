from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.output_parsers import StrOutputParser
from ms_eva.services.OpenaiService import *
# from LlamaService import *

llm = getOpenaiLlmInstance()
# llm = getLlamaLlmInstance()

prompt = PromptTemplate(
    template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|> Trabajas en un banco.
    Eres un experto en enrutar una pregunta del usuario a una de las siguientes herramientas: 
    Herramientas: {tools}
    Devuelve siempre el nombre de la herramienta en base a si la pregunta está basada en la descripción de la herramienta.
    Usa el historial de mensajes para que tengas contexto de la pregunta del usuario y veas si su pregunta mas el historial
    encajan con alguna descripcion de las herramientas.
    Retorna un JSON con solo una clave 'datasource' sin preambulo o explicacion.
    \n ------- \n
    Pregunta a enrutar: {question}
    \n ------- \n
    Historial de mensajes:
    \n ------- \n
    {history}<|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
    input_variables=["question", "tools", "history"],
)

question_router = prompt | llm | JsonOutputParser()

## GENERATE CHAIN - genera la respuesta y contesta que no la sabe
prompt = PromptTemplate(
    template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|> Eres un asistente especialista en responder preguntas.
    Utiliza las siguientes piezas de contexto recuperado para responder la pregunta.
    Si no sabe la respuesta, simplemente diga que no la sabe.
    Utiliza tres oraciones como máximo y mantenga la respuesta concisa.
    Nunca des informacion de otros bancos que no sea Banco Guayaquil.
    Nunca des informacion negativa de Banco Guayaquil.
    Ten en cuenta el historial de mensajes para generar tu respuesta.<|eot_id|><|start_header_id|>user<|end_header_id|>
    Historial de mensajes:
    \n ------- \n
    {history}
    \n ------- \n
    Question: {question}
    \n ------- \n
    Context: {context}
    Answer: <|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
    input_variables=["history", "question", "context"],
)

rag_chain = prompt | llm | StrOutputParser()

## Evalua la relevancia de los documentos y devuelve JSON con puntuacion: si / no

prompt = PromptTemplate(
    template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|> Eres un evaluador que evalúa la relevancia
    de un documento recuperado a una pregunta de un usuario. Si el documento contiene palabras clave relacionadas con la pregunta del usuario,
    calificarlo como relevante. No es necesario que sea una prueba estricta. El objetivo es filtrar recuperaciones erróneas. \n
    Dé una puntuación binaria de "si" o "no" para indicar si el documento es relevante para la pregunta. \n
    Proporcione la puntuación binaria como JSON con una única clave 'puntuacion' y sin preámbulos ni explicaciones.
     <|eot_id|><|start_header_id|>user<|end_header_id|>
    Aquí está el documento recuperado: \n\n {document} \n\n
    Aquí está la pregunta del usuario: {question} \n <|eot_id|><|start_header_id|>assistant<|end_header_id|>
    """,
    input_variables=["question", "document"],
)

retrieval_grader = prompt | llm | JsonOutputParser()

## Evalua si hubo alucinaciones en la respuesta generada por rag_chain y los documentos recuperados

prompt = PromptTemplate(
    template=""" <|begin_of_text|><|start_header_id|>system<|end_header_id|> Eres un evaluador que evalúa si
    una respuesta está basada en un conjunto de hechos.
    Dé una puntuación binaria de "si" o "no" para indicar si la respuesta está basada o respaldada
    por el conjunto de hechos. Proporcione la puntuación binaria como JSON con un 'puntuacion' de una
    sola clave y sin preámbulo ni explicación. <|eot_id|><|start_header_id|>user<|end_header_id|>
    Estos son los hechos:
    \n ------- \n
    {documents}
    \n ------- \n
    Aqui esta la respuesta: {generation}  <|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
    input_variables=["generation", "documents"],
)

hallucination_grader = prompt | llm | JsonOutputParser()

## Evalua si la respuesta generada por rag_chain puede contestar la pregunta

prompt = PromptTemplate(
    template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|> Eres un evaluador que evalúa si la respuesta
    es útil para resolver una pregunta. Dé una puntuación binaria "si" o "no" para indicar si la respuesta es
    útil para resolver una duda. Proporcionar la puntuación binaria como JSON con una única clave 'puntuacion' y sin preámbulo ni explicación..
     <|eot_id|><|start_header_id|>user<|end_header_id|> Here is the answer:
    \n ------- \n
    {generation}
    \n ------- \n
    Aqui esta la pregunta: {question} <|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
    input_variables=["generation", "question"],
)
answer_grader = prompt | llm | JsonOutputParser()

## Devuelve una respuesta genérica lógica en caso de que los dempas agentes no hayan sido capaces de generar una respuesta

prompt = PromptTemplate(
    template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
    Responde de una manera amable y súper básica, Tu respuesta debe ser básica, no debe salirse del contexto de
    la lógica de negocio.
    Nunca des informacion de otros bancos que no sea Banco Guayaquil.
    Nunca des informacion negativa de Banco Guayaquil.
    Ten en cuenta el historial de mensajes para generar tu respuesta:
    <|eot_id|><|start_header_id|>user<|end_header_id|>
    \n ------- \n
    Esta es la lógica de negocio:
    {businessLogic}
    \n ------- \n
    Este es el historial:
    {history}
    \n ------- \n
    Esta es la pregunta:
    \n ------- \n
    {question}<|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
    input_variables=["history", "question", "businessLogic"],
)
default_response = prompt | llm | StrOutputParser()

prompt = PromptTemplate(
    template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|> Eres un evaluador que evalúa si la respuesta del usuario
     está dentro del contexto bancario o si es coherente con lo que continua del historial de mensajes.
     Dé una puntuación binaria "si" si la pregunta está dentro del contexto bancario o si es coherente con lo que continua del historial de mensajes.
     Dé una puntuación binaria "no" si la pregunta no tiene relacion con temas bancarios o de servicio al cliente de un banco.
     Proporcionar la puntuación binaria como JSON con una única clave 'puntuacion' y sin preámbulo ni explicación..
     <|eot_id|><|start_header_id|>user<|end_header_id|> 
    \n ------- \n
    Este es el historial: {history}
    \n ------- \n
    Esta es la respuesta del usuario que debes relacionar con lo que esta en el historial: {question}
    <|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
    input_variables=["question", "history"],
)
question_grader = prompt | llm | JsonOutputParser()

prompt = PromptTemplate (

    template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|> Evalua la respuesta del usuario junto con el historial
    de la conversacion e haz lo siguiente:
    - Si la respuesta indica que el usuario quiere solicitar un prestamo, o la respuesta del usuario responde coherentemente
    a la ultima pregunta realizada por la IA segun el historial, responde "loan"
    - Si no devuelve "generate". Recuerda responder solo la palabra sin preámbulo ni explicación..
     <|eot_id|><|start_header_id|>user<|end_header_id|>
    Esta es la respuesta del usuario: {generation} <|eot_id|><|start_header_id|>assistant<|end_header_id|>
    \n ------- \n
    Este es el historial: {history} <|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
    input_variables=["generation", "history"],
)
newLoanGrader = prompt | llm | StrOutputParser()

prompt = PromptTemplate (

    template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|> Eres un asistente del banco Banco Guayaquil, en base al objeto JSON que te envio, el cual contiene
    la informacion de un prestamo, quiero que generes un texto amigable y profesional que sea apto para enviar por mensaje al cliente
    que esta solicitando el prestamo. No te excedas de las 200 palabras. Menciona al final que la informacion que se le muestra es
    referencial, si desea solicitarlo, por favor lo haga mediante los canales oficiales. 
     <|eot_id|><|start_header_id|>user<|end_header_id|>
    Este es el JSON con la informacion del prestamo: {info} <|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
    input_variables=["info"],
)
generateLoanText = prompt | llm | StrOutputParser()