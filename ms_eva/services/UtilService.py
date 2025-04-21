import re
import requests
from typing_extensions import TypedDict

class LoanData(TypedDict):
    loan_amount: float
    interest_rate: float
    duration_years: float

def successResponse(message = "Proceso realizado correctamente"):
    return {
        "status" : "OK",
        "message" : message
    }

def successResponseWithData(data = None):
    return {
        "status" : "OK",
        "message" : "Proceso realizado correctamente",
        "data" : data
    }

def failureResponse(message = "No se ha podido realizar el proceso correctamente"):
    return {
        "status" : "ERROR",
        "message" : message
    }

def extract_dni(texto: str) -> str:
    """
    Extrae el primer número de cédula válido (10 dígitos consecutivos) de un texto.
    """
    match = re.search(r"\b\d{10}\b", texto)
    return match.group() if match else ""

def extract_number(texto: str) -> int:
    match = re.search(r"\d+", texto)
    return int(match.group()) if match else None

def try_extract_field(field: str, user_input: str):
    if field == "dni":
        match = re.fullmatch(r"\d{10}", user_input.strip())
        return match.group() if match else None
    elif field in ["ammount", "deadline"]:
        match = re.search(r"\d+", user_input)
        return int(match.group()) if match else None
    return None

def calculateLoanAPI(data: LoanData):
    api_url = f'https://api.api-ninjas.com/v1/mortgagecalculator?loan_amount={data["loan_amount"]}&interest_rate=15.6&duration_years={data["duration_years"]}'
    response = requests.get(api_url, headers={'X-Api-Key': 'TyNgA2RdOpzpydOWFsoIBA==RNCUeirVlKxQyZVG'})
    return response

businessLogic = """
    La lógica de negocio de un banco incluye áreas clave como la atención financiera personalizada para resolver dudas sobre productos como cuentas,
    préstamos y tarjetas. Además, abarca la gestión de operaciones bancarias, información sobre tasas de interés, tipos de cambio y servicios asociados.
    Los clientes también pueden realizar procesos automatizados, como consultar saldos, realizar transferencias y solicitar información sobre movimientos.
    La entidad facilita consultas sobre normativas bancarias, comisiones aplicadas y políticas de seguridad financiera.
"""

infoVectorBG = """

Tarjetas de Crédito Banco Guayaquil: disponemos de 3 tarjetas de crédito: Tarjeta American Express Clásica, Tarjeta American Express Gold, Tarjeta American Express The Platinum Card

1. Tarjeta American Express Clásica
- Requisitos: Score crediticio mínimo de 750.
- Costos:
  - Mantenimiento mensual: $0.00
  - Emisión/renovación: $5.03 (único)
  - Plan Membership Rewards: $26.45 (opcional)
  - Prestaciones en el exterior: $12.65 anuales
- Beneficios:
  - Difiere compras nacionales e internacionales hasta 60 meses
  - Descuentos en Booking.com
  - Acumulación de puntos Membership Rewards: canjeables por premios, viajes, alojamientos y más
- Seguros incluidos:
  - Asistencia en Viaje Referencial: cobertura 24/7 mundial, incluye envío de médicos, reemplazo de lentes, asistencia legal y más
  - Seguro de Accidente en Viajes: hasta $25,000 en caso de muerte o desmembramiento accidental en transporte público

2. Tarjeta American Express Gold
- Requisitos: Score crediticio mínimo de 750.
- Costos:
  - Mantenimiento mensual: $0.00
  - Emisión/renovación: $5.03 (único)
  - Plan Membership Rewards: $32.20 (opcional)
  - Prestaciones en el exterior: $18.40 anuales
- Beneficios:
  - Difiere compras hasta 60 meses
  - Descuentos en Booking.com
  - Acumulación de puntos Membership Rewards
- Seguros incluidos:
  - Asistencia en Viaje Referencial (mismos beneficios que la clásica)
  - Seguro de Accidente en Viajes: cobertura hasta $50,000
  - Seguros de Inconvenientes de Viaje: por demoras, pérdida de conexión o equipaje
  - Seguro de Alquiler de Vehículos
  - Asistencia al Hogar y Vehículo

3. Tarjeta American Express The Platinum Card
- Requisitos: Score crediticio mínimo de 750.
- Costos:
  - Mantenimiento mensual: $0.00
  - Emisión/renovación: $5.03 (único)
  - Plan Membership Rewards: $50.60
  - Prestaciones en el exterior: $23.00 anuales
- Beneficios:
  - Difiere compras hasta 60 meses
  - Acceso a más de 1,600 salas VIP con Priority Pass (5 accesos gratuitos al año)
  - Acceso ilimitado a Centurion Lounge en más de 140 países
  - Salas AMEX: acceso en salidas internacionales (Quito y Guayaquil)
  - Servicio Concierge 24/7
  - Acumulación de millas Membership Rewards por cada dólar gastado
- Seguros incluidos:
  - Asistencia en Viajes Premium (cobertura mejorada)
  - Seguro de Accidente en Viajes: hasta $1,000,000
  - Seguros de Inconvenientes de Viaje: demoras, pérdida de vuelo o equipaje
  - Seguro de Alquiler de Vehículos: hasta $50,000 por incidente
  - Seguro de Compra Protegida: daños o robos en productos comprados con la tarjeta
  - Asistencia al Hogar y Vehículo (24/7)



Cuentas e Inversiones para Personas
1.  Cuenta de Ahorros:
    Una cuenta bancaria que te permite guardar tu dinero de forma segura y disponer de él cuando lo necesites. No requiere monto mínimo de apertura. Puedes pagar servicios, hacer transferencias, retirar en cajeros y realizar compras en línea. Se gestiona fácilmente desde la App del Banco Guayaquil.
    Beneficios:
    Sin costo de mantenimiento.
    Disponible en App y Web.
    Retiro de efectivo en cajeros y Banco del Barrio.
    Permite establecer Metas de ahorro.

2.  Cuenta Corriente:
    Diseñada para manejar tu dinero con cheques personales y movimientos frecuentes. Ideal para clientes con ingresos constantes o necesidades empresariales.

3.  Póliza de Inversión:
    Una opción de inversión segura a plazo fijo. Ganas intereses sobre el monto invertido con tasas competitivas del mercado, sin costo de mantenimiento.

4.  Metas:
    Permite ahorrar automáticamente todos los meses. Tú defines el objetivo, monto y tiempo. Ofrece una tasa de interés preferencial del 5.5% anual. Se administra directamente desde la app.

5.  Póliza de Inversión Banco Guayaquil:
    ¿Qué es una Póliza de Inversión?: Es un depósito a plazo fijo donde inviertes un monto durante un plazo establecido y generas intereses.
    Características Principales:
    - Monto mínimo de inversión: $100.
    - Plazo mínimo: 31 días.
    - Tasa de interés: Desde 4.05% y hasta 6.70%, ajustándose según el monto y plazo que elijas.
    - Contratación: 100% para los canales línea y sin costo.
    Beneficios:
    - Intereses desde el primer día: Comienzas a generar intereses desde el día de la contratación.
    - Flexibilidad en la recepción de intereses: Puedes recibir tus intereses en tu cuenta y en la frecuencia que elijas.
    - Renovación automática opcional: Puedes elegir si tu póliza se renueva automáticamente al vencimiento. 
    Gestión desde la App:
    - Apertura de póliza: Puedes abrir una Póliza de Inversión directamente desde la App del Banco Guayaquil.
    - Seguimiento: Revisa cuánto has generado y el plazo de vencimiento de tu póliza desde la App.
    Consideraciones Adicionales:
    - Días no laborables: Si la póliza es aperturada o renovada en un día no laborable (fines de semana o feriados), el débito de la cuenta seleccionada se hará ese mismo día, pero los intereses correrán a partir del siguiente día laborable. La fecha de apertura y vencimiento de la póliza será movida al siguiente día hábil. ​

    

Préstamos y Créditos Banco Guayaquil
1.  Multicrédito:
    Crédito personal desde $2,000 hasta $50,000. Aprobación en línea en minutos. Puedes elegir el plazo (de 6 a 60 meses) y el valor de las cuotas. El desembolso se acredita directamente a tu cuenta.

2.  Microcrédito:
    Financiamiento para pequeños negocios o emprendedores. El banco evalúa la capacidad de pago y ofrece condiciones flexibles para el pago.

3.  Casafácil:
    Crédito hipotecario para la compra de casa nueva o usada. Puedes financiar hasta el 80% para el valor del inmueble, con plazos de hasta 20 años.

4.  Autofácil:
    Crédito para vehículos nuevos o usados. El banco financia hasta el 80% para el monto total del vehículo.

5.  Educativo:
    Crédito para estudios universitarios o de posgrado. Puedes pagar cuando te gradúes. Ideal para educación local o internacional.


    
Servicios Adicionales:
1.  Pago de servicios básicos: puedes pagar luz, agua, internet, etc., desde App, Web, Banco del Barrio o cajeros.
2.  Pago de matrícula vehicular: habilitado desde canales digitales.
3.  Giros nacionales e internacionales: envío o retiro de dinero desde cualquier punto autorizado.
4.  Compra/venta de divisas: puedes adquirir dólares o monedas extranjeras desde tu cuenta.
5.  Billetera virtual Peigo: permite pagar, recibir dinero, hacer compras en línea y físicas desde tu celular.



Servicios para Empresas:
1.  Cuentas y Finanzas
2.  Cuenta corriente para manejo diario de la empresa.
3.  Tarjetas corporativas para control de gastos del equipo.
4.  Créditos para capital de trabajo, activos fijos, agricultura.
5.  Crédito Nómina: financiamiento para anticipos o sueldos de colaboradores.
6.  Facturación electrónica integrada.
7.  Confirming: financiamiento a proveedores.
8.  Comercio Exterior
9.  Transferencias internacionales.
10. Compra y venta de divisas para importaciones/exportaciones.




Políticas y Seguridad:
1.  Protección de Datos Personales:
    El Banco Guayaquil cumple con la Ley Orgánica de Protección de Datos Personales de Ecuador. Los datos de los clientes son utilizados únicamente con su consentimiento, y se garantiza su confidencialidad. El cliente puede revocar el consentimiento en cualquier momento.

2.  Sistema de Gestión Antisoborno (SGAS):
    Implementado bajo la norma ISO 37001:2016. El banco promueve la transparencia y tiene canales de denuncia seguros y confidenciales.

3.  Inclusión Financiera:
    Política activa de atención a poblaciones no bancarizadas mediante el programa Banco del Barrio, con presencia en comunidades rurales y zonas sin acceso a agencias bancarias tradicionales.


    
Canales de Atención:
1.  Presenciales: Agencias en todo el Ecuador.
2.  Puntos Banco del Barrio: corresponsales autorizados en barrios, tiendas y comunidades.
3.  Cajeros automáticos multifunción.
4.  Autobancos: cajeros en vehículos.
5.  Digitales
6.  App Banco Guayaquil (Android y iOS): operaciones, pagos, consultas y transferencias.
7.  Web: banca virtual para personas y empresas.
8.  WhatsApp: atención automatizada y transaccional.
9.  Call center y chat web.



Política de Cancelación de Tarjetas de Crédito Empresariales: Para cerrar una Tarjeta de Crédito empresarial en Banco Guayaquil, es necesario enviar una carta de autorización firmada por el representante legal al oficial de cuenta correspondiente. Este procedimiento garantiza que la cancelación sea procesada de manera formal y segura.
Procedimientos para el Bloqueo de Tarjetas: Banco Guayaquil ofrece múltiples canales para bloquear tarjetas en caso de pérdida, robo u otras razones:
1.  Aplicación Móvil: Accede a tu cuenta, selecciona la tarjeta que deseas bloquear, elige "Bloqueo Permanente", ingresa tu clave de cajero y confirma el bloqueo. Se emitirá una nueva tarjeta automáticamente
2.  Banca Virtual: Ingresa a la plataforma, selecciona "Bloqueos/Desbloqueos", elige la tarjeta, proporciona la clave del cajero y especifica el motivo del bloqueo:
3.  WhatsApp: Envía un mensaje con la palabra "bloquear" y sigue las instrucciones para seleccionar el tipo de tarjeta
4.  Banca Telefónica: Llama al 04-3730100, opción 2, y sigue las instrucciones según el tipo de tarjeta.


Políticas del Programa "Círculos": El programa "Círculos" de Banco Guayaquil permite a los usuarios acceder a servicios y funciones específicas. Aunque el registro es gratuito, el banco se reserva el derecho de cobrar cargos o comisiones por los servicios habilitados. Los usuarios pueden cancelar su registro si no están de acuerdo con los cargos establecidos.

Servicios Adicionales para Clientes:
1.  Banco Guayaquil ofrece una variedad de servicios adicionales para facilitar las operaciones financieras de sus clientes:
2.  Pago de Servicios Básicos: Permite cancelar facturas de luz, agua, teléfono, internet y más a través de la App, Banca Virtual, ventanillas y cajeros automáticos
3.  Giros Nacionales e Internacionales: Facilita el envío y recepción de dinero dentro y fuera del país de manera rápida y segura
4.  Compra y Venta de Divisas: Ofrece servicios de cambio de monedas extranjeras y operaciones relacionadas
5.  Solicitud de Citas para Visados: Permite realizar pagos para la asignación de fechas de citas para visados en oficinas del banco.
"""