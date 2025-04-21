from langchain.tools import Tool
from langchain_community.tools import DuckDuckGoSearchRun
from ms_eva.services.VectorStoreFEService import query_vector_store

search = DuckDuckGoSearchRun()
websearch = Tool(
    name='web_search',
    func=search.run,
    description='Útil para realizar búsquedas en internet sobre noticias del ambito financiero y bancario.'
)

# Herramienta para Embedding
def embedding_tool_func(query):
    results = query_vector_store(query)
    if results:
        return results[0].page_content
    return "No se encontró información relevante en los embeddings."

vectorstore = Tool(
    name='vectorstore',
    func=embedding_tool_func,
    description="Sirve para buscar informacion sobre los servicios, tarjetas, prestamos, polizas o politicas internas del banco"
)

loanSolicitudeFunction = {
    "name" : 'loanSolicitude',
    "description" : "Útil para calcular una prestamo de prestamo bancario"
}