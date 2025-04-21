#Ejecutar este archivo si se requiere probar el flujo desde Postman

import sys
from pathlib import Path

# Añadir el directorio raíz al PYTHONPATH antes de importar
sys.path.append(str(Path(__file__).resolve().parent.parent))

from ms_eva.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)