from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models, schemas
from app.services import analizar_con_ia
import os
from datetime import datetime

# Crear las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema de Cotizaciones - Capital & Farmer")

# Configurar templates
templates = Jinja2Templates(directory="app/templates")


# Dependency para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
async def form_cotizacion(request: Request):
    """Mostrar el formulario de cotización"""
    return templates.TemplateResponse("form.html", {"request": request})


@app.post("/cotizar")
async def crear_cotizacion(
    nombre: str = Form(...),
    email: str = Form(...),
    tipo_servicio: str = Form(...),
    descripcion: str = Form(...),
    db: Session = Depends(get_db),
):
    """Crear una nueva cotización"""
    try:
        # Generar número de cotización
        contador = db.query(models.Cotizacion).count()
        num_cotizacion = f"COT-2025-{contador + 1:04d}"

        # Calcular precio base según tipo de servicio
        precios_base = {
            "constitucion": 1500.0,
            "defensa_laboral": 2000.0,
            "consultoria_tributaria": 800.0,
        }
        precio_base = precios_base.get(tipo_servicio, 1000.0)

        # Analizar con IA (si está disponible)
        analisis_ia = None
        ajuste_precio = 0.0
        try:
            analisis_ia = analizar_con_ia(descripcion, tipo_servicio)
            if analisis_ia and "ajuste_precio" in analisis_ia:
                # Convertir porcentaje a valor absoluto
                porcentaje_ajuste = analisis_ia["ajuste_precio"]
                ajuste_precio = precio_base * (porcentaje_ajuste / 100)
        except Exception as e:
            print(f"Error en análisis IA: {e}")
            analisis_ia = {"error": "Servicio de IA no disponible"}

        precio_final = precio_base + ajuste_precio

        # Crear y guardar la cotización
        cotizacion = models.Cotizacion(
            num_cotizacion=num_cotizacion,
            nombre=nombre,
            email=email,
            tipo_servicio=tipo_servicio,
            descripcion=descripcion,
            precio=precio_final,
            fecha=datetime.now(),
        )

        db.add(cotizacion)
        db.commit()
        db.refresh(cotizacion)

        # Preparar respuesta
        respuesta = {
            "id": cotizacion.id,
            "num_cotizacion": cotizacion.num_cotizacion,
            "nombre": cotizacion.nombre,
            "email": cotizacion.email,
            "tipo_servicio": cotizacion.tipo_servicio,
            "descripcion": cotizacion.descripcion,
            "precio": cotizacion.precio,
            "fecha": cotizacion.fecha.isoformat(),
            "analisis_ia": analisis_ia,
        }

        return JSONResponse(content=respuesta)

    except Exception as e:
        return JSONResponse(
            content={"error": f"Error al crear cotización: {str(e)}"}, status_code=500
        )
