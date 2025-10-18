# Enunciado del Proyecto - Aplicación Web con Flask

## Descripción General del Proyecto

Los estudiantes deben desarrollar una aplicación web utilizando el framework Flask y un stack tecnológico específico. Cada estudiante es **libre de elegir el tema o dominio** de su aplicación (gestión de tareas, blog, tienda, biblioteca, eventos, recetas, portfolio, foro, etc.), pero debe cumplir estrictamente con los requisitos técnicos establecidos en este documento.

La aplicación debe incluir autenticación de usuarios, persistencia en base de datos PostgreSQL, y operaciones CRUD sobre al menos una entidad principal del dominio elegido.

## Requisitos Técnicos Obligatorios

### 1. Stack Tecnológico

Los estudiantes **DEBEN** utilizar las siguientes tecnologías con sus versiones mínimas especificadas:

- **Python**: 3.12 o superior
- **Flask**: 3.1.2 o superior (Framework web)
- **Flask-WTF**: 1.2.2 o superior (Manejo y validación de formularios)
- **Flask-Login**: 0.6.3 o superior (Gestión de sesiones de usuario)
- **Flask-SQLAlchemy**: 3.1.1 o superior (ORM para operaciones de base de datos)
- **PostgreSQL**: Motor de base de datos (usando psycopg 3.2.10+)
- **python-slugify**: 8.0.4 o superior (Generación de slugs amigables para URLs)
- **email-validator**: 2.3.0 o superior (Validación de correos electrónicos)
- **Werkzeug**: Para hash de contraseñas (incluido con Flask)

**Gestor de Paquetes**: Los estudiantes deben usar **Rye** o similar para la gestión de dependencias.

### 2. Configuración de Base de Datos

- Motor: **PostgreSQL**
- Conexión vía Flask-SQLAlchemy
- Formato de conexión: `postgresql+psycopg://usuario:contraseña@host:puerto/nombre_base_datos`
- Configurar `SQLALCHEMY_TRACK_MODIFICATIONS = False`

### 3. Modelos de Datos (Mínimo 2 Modelos)

#### Modelo User (Usuario) - OBLIGATORIO

**Campos mínimos requeridos**:
- `id` (Integer, Primary Key)
- `name` o `username` (String, Not Null)
- `email` (String, Unique, Not Null)
- `password` (String, Not Null, hasheado)
- Campos adicionales según el dominio (ej: `is_admin`, `role`, `phone`, etc.)

**Métodos Requeridos**:
- `set_password(password)`: Hashear y almacenar contraseña usando Werkzeug
- `check_password(password)`: Verificar contraseña contra el hash almacenado
- `save()`: Persistir usuario en base de datos
- `get_by_id(id)`: Método estático para obtener usuario por ID
- `get_by_email(email)`: Método estático para obtener usuario por email

**Importante**: Debe heredar de `UserMixin` (Flask-Login)

#### Modelo de Entidad Principal - OBLIGATORIO

Cada estudiante debe crear un modelo para la entidad principal de su dominio elegido:
- **Ejemplos**: Post, Product, Task, Book, Event, Recipe, Project, Topic, Ad, Business, etc.

**Campos mínimos requeridos**:
- `id` (Integer, Primary Key)
- `user_id` (Integer, Foreign Key al modelo User con CASCADE delete)
- Al menos 2-3 campos relevantes al dominio
- `slug` (String, Unique, Not Null) - Para URLs amigables
- Al menos un campo de tipo Text o String largo para contenido

**Métodos Requeridos**:
- `save()`: Persistir registro con generación automática de slug
- `public_url()`: Generar URL para ver el registro
- `get_by_slug(slug)`: Método estático para obtener registro por slug
- `get_all()`: Método estático para obtener todos los registros

**Generación de Slugs (OBLIGATORIO)**:
- Generar automáticamente slugs desde un campo de texto usando `python-slugify`
- Manejar slugs duplicados añadiendo números (ej., `mi-item-1`, `mi-item-2`)
- Capturar excepciones `IntegrityError` para manejo de duplicados

### 4. Formularios con Flask-WTF (Mínimo 3)

#### SignupForm (Registro) - OBLIGATORIO
- Campo para nombre/username: StringField con validadores (DataRequired, Length)
- `email`: StringField con validadores (DataRequired, Email)
- `password`: PasswordField con validador (DataRequired)
- `submit`: SubmitField

#### LoginForm - OBLIGATORIO
- `email`: StringField con validador (DataRequired)
- `password`: PasswordField con validador (DataRequired)
- `remember_me`: BooleanField (checkbox para sesión persistente)
- `submit`: SubmitField

#### Formulario de Entidad Principal - OBLIGATORIO
- Al menos 2-3 campos StringField o TextAreaField
- Al menos un campo con validador DataRequired
- Al menos un campo con validador Length
- `submit`: SubmitField
- Los campos deben ser relevantes al dominio elegido

**Ejemplos según dominio**:
- Blog: `title`, `content`, `category`
- Tienda: `product_name`, `description`, `price`
- Tareas: `task_name`, `description`, `due_date`

### 5. Rutas (Mínimo 6 Rutas)

#### Rutas Públicas (sin autenticación)

**1. Página de Inicio (`/`) - OBLIGATORIO**
- Método: GET
- Mostrar listado de registros de la entidad principal
- Información resumida con enlaces a vista detallada

**2. Vista Detalle (`/<entidad>/<slug>/`) - OBLIGATORIO**
- Método: GET
- Mostrar registro individual por slug
- Retornar 404 si no existe
- Ejemplos: `/post/<slug>/`, `/product/<slug>/`, `/task/<slug>/`

**3. Login (`/login`) - OBLIGATORIO**
- Métodos: GET, POST
- Redirigir usuarios autenticados a inicio
- Validar credenciales usando modelo User
- Soportar "recordarme"
- Manejar parámetro `next` con validación de seguridad (usar `urlparse`)

**4. Registro (`/signup/`) - OBLIGATORIO**
- Métodos: GET, POST
- Redirigir usuarios autenticados a inicio
- Verificar si email ya existe y mostrar error
- Auto-login después de registro exitoso
- Hashear contraseña antes de almacenar

**5. Logout (`/logout`) - OBLIGATORIO**
- Método: GET
- Cerrar sesión del usuario actual
- Redirigir a página de inicio

#### Rutas Protegidas (@login_required)

**6. Crear Registro - OBLIGATORIO**
- Ejemplos de rutas: `/admin/post/`, `/admin/product/`, `/admin/task/`
- Métodos: GET, POST
- Decorador: `@login_required`
- Crear nuevo registro asociado con `current_user.id`
- Redirigir después de creación exitosa

### 6. Autenticación con Flask-Login

**Configuración obligatoria**:
- Configurar `login_manager.login_view = 'login'`
- Implementar función callback `user_loader`
- Usar decorador `@login_required` en rutas protegidas
- `current_user` accesible en templates y views
- Hash de contraseñas con `generate_password_hash`
- Verificación con `check_password_hash`

### 7. Seguridad

**Requisitos obligatorios**:
- Configurar Flask `SECRET_KEY` (string criptográficamente seguro)
- Validar URLs de redirección (parámetro `next`) usando `urlparse`
- Protección CSRF habilitada (automática con Flask-WTF)
- Validación de email con librería `email-validator`
- Manejo de excepciones `IntegrityError` en operaciones de BD

### 8. Plantillas Jinja2 (Mínimo 5)

**Plantilla Base - OBLIGATORIO**:
- Definir bloques para extensión (`{% block content %}`, etc.)
- Navegación condicional según autenticación
- Opciones diferentes para usuarios logueados vs anónimos
- Enlazar archivos CSS estáticos
- Mostrar info del usuario actual cuando esté logueado

**Plantillas mínimas**:
1. Plantilla base con estructura HTML
2. index.html - Lista de registros
3. Vista detalle del registro individual
4. login_form.html
5. signup_form.html
6. Formulario de creación de entidad

**Características**:
- Usar macros de WTForms para renderizado
- Incluir token CSRF en todos los formularios
- Mostrar errores de validación
- Navegación condicional (autenticado/anónimo)

### 9. Archivos Estáticos

- Al menos un archivo CSS Basico
- Organizados en directorio `static/`
- Usar `url_for('static', filename='...')` para referencias

### 10. Estructura del Proyecto

```
raiz_proyecto/
├── pyproject.toml           # Dependencias y configuración
├── README.md                # Documentación (en inglés)
├── requirements.lock        # Dependencias bloqueadas (Rye)
├── requirements-dev.lock    # Dev dependencies
└── src/
    └── nombre_proyecto/     # Nombre elegido por estudiante
        ├── run.py           # Aplicación principal con rutas
        ├── models.py        # Modelos de BD (User, Entidad, etc.)
        ├── forms.py         # Definiciones WTForms
        ├── static/
        │   └── *.css        # Archivos CSS
        └── templates/
            ├── base_template.html
            ├── index.html
            ├── [entidad]_view.html
            ├── login_form.html
            └── admin/
                ├── signup_form.html
                └── [entidad]_form.html
```

## Elección del Dominio del Proyecto

### Ejemplos de Dominios Sugeridos

1. **Blog/Publicaciones**: Sistema de posts con autores
2. **Gestión de Tareas**: Todo list con usuarios
3. **Tienda/Catálogo**: Productos con vendedores
4. **Biblioteca**: Libros y préstamos
5. **Eventos**: Gestión de eventos con organizadores
6. **Recetas**: Recetas de cocina con autores
7. **Portfolio**: Proyectos de usuarios
8. **Foro**: Temas y mensajes
9. **Clasificados**: Anuncios clasificados
10. **Directorio**: Listado de negocios o servicios

**Los estudiantes pueden proponer otros dominios** siempre que cumplan con los requisitos técnicos.

### Criterios para la Elección

- Debe permitir implementar todas las funcionalidades técnicas requeridas
- Debe tener sentido una relación User -> Entidad (usuario crea/posee registros)
- Los registros deben poder tener "título" o "nombre" para generar slugs
- Debe ser posible mostrar registros en lista y vista detallada

## Documentación Requerida

### README.md (en inglés) debe incluir:

1. **Descripción del proyecto**: Qué hace la aplicación y qué problema resuelve
2. **Dominio elegido**: Breve justificación de la elección
3. **Instrucciones de instalación**: Configuración de Rye y dependencias
4. **Configuración de base de datos**: Cómo crear la BD PostgreSQL
5. **Variables de entorno**: Qué configurar antes de ejecutar
6. **Cómo ejecutar la aplicación**: Comandos específicos
7. **Rutas disponibles**: Tabla o lista de endpoints
8. **Características implementadas**: Lista de funcionalidades
9. **Modelos de datos**: Descripción de modelos y relaciones
10. **Estructura del proyecto**: Explicación de organización de archivos

### Código

- **Todo el código y comentarios en inglés**
- Docstrings en funciones y clases importantes
- Nombres descriptivos para variables, funciones y clases

## Entregables

### 1. Repositorio Git Publico con:
- Código fuente completo organizado según estructura especificada
- `pyproject.toml` con todas las dependencias
- README.md con documentación completa (en inglés)
- `.gitignore` apropiado (excluir `.venv/`, `__pycache__/`, etc.)

### 2. Aplicación funcionando que:
- Se conecte exitosamente a PostgreSQL
- Permita registro de nuevos usuarios
- Permita login y logout
- Permita a usuarios autenticados crear registros
- Muestre todos los registros en página de inicio
- Muestre detalles individuales por slug
- Maneje errores apropiadamente (404, emails duplicados)

## Criterios de Evaluación

### 1. Uso correcto de librerías requeridas
- Configuración apropiada de Flask
- Implementación correcta de formularios Flask-WTF
- Integración apropiada de Flask-Login
- Definiciones correctas de modelos SQLAlchemy

### 2. Implementación de base de datos
- Relaciones de modelos correctas
- Uso apropiado de ORM SQLAlchemy
- Generación de slugs con manejo de colisiones
- Hash de contraseñas

### 3. Seguridad
- Protección CSRF
- Hash de contraseñas
- Validación de redirecciones seguras
- Uso apropiado del decorador login_required

### 4. Funcionalidad
- Todas las rutas funcionando correctamente
- Validación de formularios
- Manejo de errores (404, emails duplicados)
- Gestión de sesiones

### 5. Calidad de código y documentación
- Organización del código
- Completitud del README
- Comentarios de código en inglés
- Estructura apropiada del proyecto


## Recursos de Apoyo

- Flask: https://flask.palletsprojects.com/
- Flask-WTF: https://flask-wtf.readthedocs.io/
- Flask-Login: https://flask-login.readthedocs.io/
- Flask-SQLAlchemy: https://flask-sqlalchemy.palletsprojects.com/
- SQLAlchemy: https://www.sqlalchemy.org/

## Consejos para los Estudiantes

### Planificación
1. **Define tu dominio primero**: Elige un tema que te interese
2. **Diseña tus modelos**: Dibuja el esquema de BD antes de codificar
3. **Lista tus rutas**: Define qué URLs necesitarás

### Desarrollo
4. **Comienza con la configuración**: Instala dependencias y configura BD
5. **Desarrolla incrementalmente**:
   - Primero: Modelos y base de datos
   - Segundo: Autenticación (User, login, signup)
   - Tercero: CRUD de tu entidad principal
   - Cuarto: Plantillas y estilos
6. **Prueba frecuentemente**: Verifica cada funcionalidad
7. **Usa el debugger**: `flask run --debug`

### Buenas Prácticas
8. **Lee la documentación** de las librerías
9. **Maneja errores apropiadamente**
10. **Seguridad primero**: Nunca guardes contraseñas en texto plano
11. **Commits frecuentes**: Usa Git desde el inicio
12. **Código limpio**: Nombres descriptivos

## Checklist de Verificación

### Configuración
- [ ] Todas las dependencias en `pyproject.toml`
- [ ] Proyecto usa gestor de dependencias
- [ ] Existe `.gitignore`
- [ ] PostgreSQL configurado

### Modelos y BD
- [ ] Modelo User con todos los campos y métodos requeridos
- [ ] Modelo User hereda de UserMixin
- [ ] Modelo de entidad principal con relación a User
- [ ] Generación automática de slugs implementada
- [ ] Manejo de slugs duplicados funciona
- [ ] Foreign key con CASCADE delete

### Formularios
- [ ] SignupForm con validadores apropiados
- [ ] LoginForm con campo remember_me
- [ ] Formulario de entidad con validadores
- [ ] Todos los formularios tienen submit button

### Rutas
- [ ] Ruta `/` muestra listado
- [ ] Ruta de detalle por slug funciona
- [ ] Ruta `/login` implementada correctamente
- [ ] Ruta `/signup/` con verificación de email duplicado
- [ ] Ruta `/logout` funciona
- [ ] Ruta protegida para crear registros con @login_required
- [ ] Validación de parámetro `next` implementada

### Autenticación
- [ ] Flask-Login configurado correctamente
- [ ] login_manager.login_view configurado
- [ ] user_loader implementado
- [ ] Contraseñas se hashean antes de guardar
- [ ] Login funciona con validación de credenciales
- [ ] Logout cierra sesión correctamente
- [ ] Remember me funciona

### Seguridad
- [ ] SECRET_KEY configurada
- [ ] Protección CSRF activa
- [ ] Validación de email con email-validator
- [ ] Redirecciones seguras (urlparse)
- [ ] IntegrityError manejado

### Plantillas
- [ ] Plantilla base con bloques
- [ ] Todas las plantillas extienden de base
- [ ] Navegación condicional (logueado/anónimo)
- [ ] current_user accesible en templates
- [ ] Formularios muestran errores de validación
- [ ] Tokens CSRF en formularios

### Estáticos y Estilo
- [ ] Al menos un archivo CSS
- [ ] CSS vinculado correctamente con url_for
- [ ] Aplicación tiene estilo básico

### Documentación
- [ ] README.md completo en inglés
- [ ] Descripción del proyecto clara
- [ ] Instrucciones de instalación
- [ ] Instrucciones de configuración de BD
- [ ] Lista de rutas disponibles
- [ ] Código y comentarios en inglés

### Funcionalidad General
- [ ] Aplicación ejecuta sin errores
- [ ] Se puede registrar nuevo usuario
- [ ] Se puede hacer login
- [ ] Se puede crear nuevo registro
- [ ] Lista de registros se muestra
- [ ] Detalle de registro se muestra
- [ ] 404 se maneja apropiadamente
- [ ] Email duplicado muestra error
- [ ] Usuario debe estar logueado para crear

### Git
- [ ] Repositorio Git inicializado
- [ ] Commits descriptivos
- [ ] .gitignore apropiado

---

**Fecha límite de entrega**: [A determinar por el instructor]

**Importante**: Este es un proyecto individual. Los estudiantes deben escribir su propio código. El plagio resultará en una calificación de cero.

## Notas Finales

- **Todos los requisitos técnicos son obligatorios** independientemente del dominio elegido
- **El dominio es libre** pero debe permitir implementar todos los requisitos
- **Prueba exhaustivamente**: Una aplicación que no funciona no puede ser evaluada
- **Documenta bien**: Un buen README facilita la evaluación
- **Pregunta si tienes dudas**: Es mejor aclarar antes que entregar algo incorrecto
