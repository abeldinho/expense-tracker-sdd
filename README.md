# 💰 Expense Tracker API (SDD + IA)

Proyecto demo desarrollado siguiendo **Spec-Driven Development (SDD)** con apoyo de IA.

## 🚀 Objetivo

Construir una API simple para:

* Registrar gastos
* Listarlos
* Obtener balance total

## 🧠 Enfoque

Este proyecto no se centra solo en código, sino en el proceso:

1. Definición del problema
2. Casos de uso (UC)
3. Modelo de dominio
4. Diagramas de secuencia
5. Implementación
6. Testing
7. Deploy

## 🛠️ Tecnologías

* Python
* Django
* Django REST Framework
* Docker
* Pytest

## 📂 Endpoints

### Crear gasto

POST /api/gastos/

### Listar gastos

GET /api/gastos/listar/

### Obtener balance

GET /api/balance/

## 🧪 Tests

```bash
docker compose run web pytest
```

## 🐳 Ejecutar proyecto

```bash
docker compose up
```

## 📌 Decisiones de diseño

* El balance no se guarda, se calcula dinámicamente
* Separación en capas (views, services)
* Validaciones en serializer + lógica en services

## 🔮 Próximas mejoras

* Autenticación (JWT)
* Multiusuario
* PostgreSQL
* Deploy en producción

---

## 👨‍💻 Autor

Proyecto desarrollado como práctica de arquitectura backend y SDD.
