# RecipeLib Backend

**Importante: Se necesita tener Docker Desktop activado (Windows + WSL2) o el servicio de Docker activo (Linux)**

Para el uso del backend es necesario activar pre-commits, para ello:

Instalar pre-commit de forma local: 

```bash
pip install pre-commit
```

Luego es necesario instalar pre-commit en el repositorio:

```bash
pre-commit install
```

Ejecutar los siguientes comandos:

```bash
docker-compose build
docker-compose up
```
Si no tienen permisos para editar los archivos del proyecto utilicen:

```bash
sudo chown -R $USER:$USER project_folder_name
```
El backend estará corriendo en [http://localhost:8000](http://localhost:8000)
