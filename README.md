![cover](/images/cover.jpg)

# 💬 Chatbot Bancario Inteligente con LangGraph y Generative AI

Este proyecto implementa un **agente conversacional bancario** con arquitectura RAG (Retrieval-Augmented Generation), diseñado para responder consultas de clientes, recuperar información relevante del banco y cotizar préstamos inteligentes, todo desde una interfaz web intuitiva desarrollada con Streamlit.

---

## 🚀 Tecnologías Utilizadas

| Tecnología                    | Propósito                                                                 |
|------------------------------|--------------------------------------------------------------------------|
| **LangGraph**                | Orquestador de nodos en forma de grafo para flujos conversacionales      |
| **LangChain**                | Integración de prompts, herramientas, embeddings y flujos de RAG         |
| **Redis Stack**              | Almacén de embeddings, historial de conversaciones y estado de sesiones  |
| **OpenAI GPT-4o Mini**       | Modelo generativo ligero y eficiente para respuestas precisas            |
| **OpenAIEmbeddings**         | Conversión de documentos bancarios en vectores para similitud semántica  |
| **Streamlit**                | Interfaz web tipo chat para usuarios finales                              |
| **DuckDuckGo Tool**          | Búsqueda web en caso de no encontrar respuestas en la base vectorial     |
| **API Mortgage Calculator**  | Simulador real de préstamos integrable mediante Tool                     |
| **SQLite**                   | Base de datos local para validar score Equifax antes de cotizar préstamo |

---

## 🎯 Características del Chatbot

- Consulta de información bancaria como:
  - Tarjetas de crédito, cuentas, servicios, seguros.
- Cotización de préstamos con flujo guiado:
  - Solicitud de cédula, validación de score y simulación del préstamo.
- Búsqueda web integrada para preguntas abiertas (por ejemplo, tasas actuales del dólar).
- Nodo de fallback que garantiza siempre una respuesta.

---

## 🧠 Arquitectura de Flujos (LangGraph)

![diagrama](/images/diagrama.jpg)

---

## 🛠 Instalación Rápida

```bash
# 1. Clonar repositorio
git clone https://github.com/tu_usuario/chatbot-banco.git
cd chatbot-banco

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: .\venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar interfaz web
streamlit run app.py
```

---

## 📦 Pasos para desplegar sistema

1. **Clonar repositorio**

```bash
git clone https://github.com/tu_usuario/chatbot-banco.git
cd chatbot-banco
```

2. **Crear entorno virtual**

```bash
python -m venv bg_demo_venv
.\bg_demo_venv\Scripts\activate
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

3. **Instalar las dependencias**

```bash
pip install -r .\requirements.txt
```

4. **Desplegar instancia de Redis para embeddings e historial de mensajes**

   - Instalar Docker Desktop:  
     [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)

   - Ejecutar en terminal como administrador:

```bash
docker run -d --name redis-stack-server -p 6379:6379 redis/redis-stack-server:latest
```

5. **Ejecutar el chatbot**

```bash
streamlit run .\appStreamLit.py
```

---

## ⚙️ Endpoints REST disponibles

- `/ms_eva/message`: Procesa mensaje y responde  
- `/ms_eva/clearHistory`: Limpia historial y estado  
- `/ms_eva/loadEmbedding`: Carga documentos embebidos  
- `/ms_eva/createDatabase`: Inicializa base SQLite  

---

## 🔮 Posibles Mejoras

- Incorporación de un NLP intermedio para detectar intenciones comunes sin usar el LLM.  
- Conexión a APIs bancarias reales.  
- Flujo autenticado por cédula + validación biométrica.  
- Dashboard de preguntas frecuentes y monitoreo de uso.  

---

## 👨‍💻 Autor

Edwin Veloz  
[[LinkedIn](https://www.linkedin.com/in/edwin-veloz-2153a9137/) / [GitHub](https://github.com/edwin06111998) / edwin06111998@gmail.com]

---

## 📄 Licencia

Este proyecto se entrega como parte de una evaluación técnica y puede ser reutilizado con fines educativos o de demostración.