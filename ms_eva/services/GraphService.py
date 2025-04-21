#Dependencias externas
import requests
from pprint import pprint
from typing_extensions import TypedDict, List
from langgraph.graph import END, StateGraph
from langchain.docstore.document import Document

#Dependencias locales
from ms_eva.prompts import *
from ms_eva.tools import *
from ms_eva.db.serviceDb import consultar_score
from ms_eva.services.VectorStoreFEService import retriever, get_redis_history, load_state, save_state, clear_state
from ms_eva.services.UtilService import *

class LoanData(TypedDict, total=False):
    dni: str
    deadline: int
    ammount: str

### State
class GraphState(TypedDict, total=False):
    question : str
    generation : str
    web_search : str
    documents : List[str]
    chatHistory : str
    sessionId : str
    data: LoanData
    flow: str

def retrieve(state):
    """
    Recupera documentos del vectorstore
    Args:
        state (dict): El estado actual del grafico
    Returns:
        state (dict): Nueva clave agregada al estado, documentos, que contiene documentos recuperados
    """
    print("--- RECUPERANDO DOCUMENTOS DEL EMBEDDING ---")
    question = state["question"]

    # Retrieval
    documents = retriever.invoke(question)
    documents = None if documents is [] else documents[:2]
    return {"documents": documents, "question": question}

def generate(state):
    """
    Generar respuesta usando RAG en documentos recuperados
    Args:
        state (dict): El estado actual del grafico
    Returns:
        state (dict): Nueva clave agregada al estado, generación, que contiene generación de LLM
    """
    print("--- GENERANDO RESPUESTA A PARTIR DE DOCUMENTOS ---")
    question = state["question"]
    documents = state["documents"]
    history = get_redis_history(state["sessionId"])

    # RAG generation
    generation = rag_chain.invoke({"context": documents, "question": question, "history": history})
    return {"documents": documents, "question": question, "generation": generation}

def grade_documents(state):
    """
    Determina si los documentos recuperados son relevantes para la pregunta.
    Si algún documento no es relevante, estableceremos una marca para ejecutar la búsqueda web.

    Args:
        state (dict): El estado actual del grafico

    Returns:
        state (dict): Se filtraron documentos irrelevantes y se actualizó el estado web_search.
    """

    print("--- VERIFICANDO RELEVANCIA DE DOCUMENTO ---")
    question = state["question"]
    documents = state["documents"]

    filtered_docs = []
    web_search = "si"
    for d in documents:
        score = retrieval_grader.invoke({"question": question, "document": d.page_content})
        grade = score['puntuacion']
        # Documento relevante
        if grade.lower() == "si" or grade.lower() == "sí":
            print("--- CALIFICACION: DOCUMENTO RELEVANTE ---")
            filtered_docs.append(d)
            web_search = "no"
        # Documento no relevante
        else:
            print("--- CALIFICACION: DOCUMENTO NO RELEVANTE ---")
            continue
    return {"documents": filtered_docs, "question": question, "web_search": web_search}

def web_search(state):
    """
    Búsqueda web basada en la pregunta

    Args:
        state (dict): El estado actual del grafico

    Returns:
        state (dict): Resultados web añadidos a documentos
    """

    print("--- BUSQUEDA WEB ---")
    question = state["question"]
    documents = state.get("documents", [])

    # Web search
    docs = search.invoke({"query": question})
    web_results = Document(page_content=docs)
    if documents is not None:
        documents.append(web_results)
    else:
        documents = [web_results]
    return {"documents": documents, "question": question}

def route_question(state):
    """
    Dirigir la pregunta a una de las herramientas

    Args:
        state (dict): El estado actual del grafico

    Returns:
        str: Siguiente nodo a llamar
    """
    if state.get("flow") == "loanSolicitude":
        return "loanSolicitude"
    question = state["question"]
    history = get_redis_history(state["sessionId"])
    grade = question_grader.invoke({"question": question, "history":history})
    if(grade["puntuacion"] == "no"):
        return "handle_default_response"
    tools = [vectorstore, websearch, loanSolicitudeFunction]
    source = question_router.invoke({"question": question, "tools": tools,  "history":history})
    print(source)

    if source['datasource'] == 'web_search':
        return "websearch"
    elif source['datasource'] == 'vectorstore':
        return "vectorstore"
    elif source["datasource"] == "loanSolicitude":
        state["flow"] = "loanSolicitude"
        save_state(state["sessionId"], state)
        return "loanSolicitude"
    else:
        return "handle_default_response"

def decide_to_generate(state):
    """
    Determina si se genera una respuesta o se hace una búsqueda web

    Args:
        state (dict): El estado actual del grafico

    Returns:
        str: Decisión binaria para llamar al siguiente nodo
    """

    print("--- EVALUANDO DOCUMENTOS CALIFICADOS ---")
    web_search = state["web_search"]

    if web_search == "si":
        print("--- DECISION: TODOS LOS DOCUMENTOS NO SON RELEVANTES, EJECUTANDO WEB SEARCH ---")
        return "websearch"
    else:
        print("--- DECISION: GENERAR DOCUMENTO CON LLM ---")
        return "generate"

def grade_generation_v_documents_and_question(state):
  """
  Determina si la generación está fundamentada en el documento y responde la pregunta.

  Args:
      state (dict): El estado actual del grafico

  Returns:
      str: Decisión sobre el siguiente nodo a llamar
  """

  print("--- VERIFICANDO ALUCINACIONES ---")
  question = state["question"]
  documents = state["documents"]
  generation = state["generation"]

  score = hallucination_grader.invoke({"documents": documents, "generation": generation})
  grade = score['puntuacion']

  # Verificar alucinaciones
  if grade == "si":
      print("--- DECISION: LA RESPUESTA GENERADA SE BASA EN LOS DOCUMENTOS ---")
      print("--- VERIFICANDO RESPUESTA VS PREGUNTA DEL USUARIO ---")
      score = answer_grader.invoke({"question": question,"generation": generation})
      grade = score['puntuacion']
      if grade == "si":
          print("--- DECISION: LA RESPUESTA SATISFACE LA PREGUNTA ---")
          return "useful"
      else:
          print("--- DECISION: LA RESPUESTA NO SATISFACE LA PREGUNTA ---")
          return "not useful"
  else:
      print("--- DECISION: LA RESPUESTA GENERADA NO SE BASA EN LOS DOCUMENTOS, REINTENTANDO ---")
      return "not supported"

def handle_default_response(state):
    print("--- GENERANDO RESPUESTA DE FALLBACK ---")
    question = state["question"]
    history = get_redis_history(state["sessionId"])
    generation = default_response.invoke({"history": history, "question": question, "businessLogic" : businessLogic})
    return {"question": question, "generation": generation}

# NUEVO: Flujo préstamo

def loanSolicitude(state):
    userInput = state["question"]

    if "data" not in state:
        state["data"] = {}

    if state["data"].get("dni") == None:
        dni = extract_dni(userInput)
        if dni:
            score = consultar_score(dni)
            if score == None: #Se valida score crediticio
                # state["flow"] = None
                save_state(state["sessionId"], state)
                return {
                    "generation": f'El # de cédula {dni} no se encuentra registrado en nuestra base de datos. Por favor intente con una cédula diferente'
                }
            if score < 700: #Se valida score crediticio
                # state["flow"] = None
                save_state(state["sessionId"], state)
                return {
                    "generation": f'Lastimosamente no cumple con los requisitos para solicitar el préstamo por este canal, por favor, acérquese a una de nuestras agencias bancarias'
                }
            state["data"]["dni"] = dni
            save_state(state["sessionId"], state)
            return {
                "generation": f'Por favor, ingrese la cantidad solicitada para el préstamo'
            }
        return {
            "generation": f'Por favor, ingrese el # de cédula de 10 dígitos'
        }
    if state["data"].get("ammount") == None:
        ammount = extract_number(userInput)
        if ammount:
            state["data"]["ammount"] = ammount
            save_state(state["sessionId"], state)
            return {
                "generation": f'Por favor, ingrese el plazo en meses para el préstamo'
            }
        return {
            "generation": f'Por favor, ingrese la cantidad solicitada para el préstamo'
        }
    if state["data"].get("deadline") == None:
        deadline = extract_number(userInput)
        if deadline:
            state["data"]["deadline"] = deadline
            save_state(state["sessionId"], state)
            return {
                "generation": "Ya tengo todos los datos. Procesando...",
                "next": "generateLoan"
            }
        return {
            "generation": f'Por favor, ingrese el plazo en meses para el préstamo'
        }

    state["flow"] = None
    return {
        "generation": "Ya tengo todos los datos. Procesando...",
        "next": "generateLoan"
    }

def LoanDecision(state):
    return state.get("next", "returnMessage")

def generateLoan(state):
    form = state["data"]
    ammount = float(form["ammount"])
    deadline = float(int(form["deadline"])/12)
    data = {
        "loan_amount": ammount,
        "duration_years": deadline
    }
    response = calculateLoanAPI(data)
    dataResponse = {}
    if response.status_code != requests.codes.ok:
        return {
            "No hemos podido obtener la informacion del prestamo, por favor, intente nuevamente"
        }
    dataResponse = response.text
    print(f'Respuesta del webservice de prestamo: {dataResponse}')
    loanText = generateLoanText.invoke({"info": dataResponse})
    clear_state(state["sessionId"])
    return {
        "generation": loanText
    }

# Declaracion de grafo -----------------------------------------------

workflow = StateGraph(GraphState)

workflow.add_node("retrieve", retrieve)
workflow.add_node("websearch", web_search)
workflow.add_node("handle_default_response", handle_default_response)
workflow.add_node("grade_documents", grade_documents)
workflow.add_node("generate", generate)
workflow.add_node("loanSolicitude", loanSolicitude)
workflow.add_node("generateLoan", generateLoan)
        
workflow.set_conditional_entry_point(
    route_question,
    {
        "loanSolicitude": "loanSolicitude",
        "websearch": "websearch",
        "vectorstore": "retrieve",
        "handle_default_response" : "handle_default_response"
    },
)

workflow.add_conditional_edges(
    "loanSolicitude",
    LoanDecision,
    {
        "generateLoan": "generateLoan",
        "returnMessage": END
    }
)

workflow.add_edge("generateLoan", END)

workflow.add_edge("retrieve", "grade_documents")
workflow.add_conditional_edges(
    "grade_documents",
    decide_to_generate,
    {
        "websearch": "websearch",
        "generate": "generate",
    },
)

workflow.add_edge("websearch", "generate")
workflow.add_conditional_edges(
    "generate",
    grade_generation_v_documents_and_question,
    {
        "not supported": "handle_default_response",
        "useful": END,
        "not useful": "handle_default_response",
    },
)

app = workflow.compile()

def processQuery(query : str, sessionId: str):
    state = load_state(sessionId)
    
    # Añadir la nueva pregunta
    state.update({
        "question": query,
        "sessionId": sessionId
    })
    for output in app.stream(state, {"recursion_limit": 10}):
        for key, value in output.items():
            pprint(f"Finished running: {key}:")
    pprint(value["generation"])
    return successResponseWithData(value["generation"])