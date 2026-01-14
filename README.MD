# Inventario Casa Central – Prototipo

## Requisitos previos
- Python 3.9+
- pip
- Git

## Pasos para clonar y ejecutar

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/daveprogramer404/inventarioCasaCentral.git
   cd inventarioCasaCentral
   ```

2. **Crear y activar entorno virtual (recomendado)**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **(Opcional) Configurar variables de entorno**  
   Copia `.env.example` a `.env` y ajusta los valores.

5. **Inicializar la base de datos**
   ```bash
   python manage.py migrate
   ```

6. **Crear superusuario**
   ```bash
   python manage.py createsuperuser
   ```

7. **Ejecutar el servidor de desarrollo**
   ```bash
   python manage.py runserver
   ```
   Abre http://127.0.0.1:8000 en tu navegador.


## Comandos útiles

# 🏢 Casa Central Inventario

**Casa Central Inventario** es una aplicación web desarrollada con **Python Django + Bootstrap**, diseñada para gestionar y registrar artículos informáticos de hardware, periféricos y monitores.

Permite registrar productos con información detallada como:
- Categoría  
- Modelo y número de serie  
- Fechas de ingreso, cambio y entrega  
- Remitente y destinatario  
- Estado del producto  
- Imágenes antes y después del cambio  

---

## 🚀 Tecnologías utilizadas

- **Python 3**
- **Django 5**
- **Bootstrap 5**
- **SQLite3**
- **Pillow** (para gestión de imágenes)

---

## ⚙️ Instalación y configuración

### 1️⃣ Clona este repositorio

```bash
git clone https://github.com/<TU_USUARIO>/casa-central-inventario.git
cd casa-central-inventario
