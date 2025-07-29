# DRF Protector

Secure your Django REST Framework (DRF) projects with PyArmor and Docker. This tool lets you obfuscate your source code, add licensing with PyArmor, and package everything into a Docker container for deployment.

## 🧩 Django Web + DRF Support

This tool is designed to work with **both Django REST Framework (DRF)** APIs and **traditional Django web applications**. Whether your project includes APIs, templates, or both — you can use `drf-protector` to obfuscate your backend logic, protect source code, and deploy it securely using Docker.

Just ensure the `drf_protector.json` is correctly configured for your app structure.

- ✅ Works with `urls.py`, `views.py`, models, and API views  
- ✅ Compatible with Django templates, static files, and DRF serializers  
- ✅ Obfuscation targets Python code only — static and templates are preserved as-is

## Features

- 🔐 Obfuscate Python code using PyArmor
- 🧾 License-based execution control
- 🐳 Generate secure Docker containers
- 🛠️ Easy CLI for local development and deployment

## Usage

```bash
drf-protector init        # Generate drf_protector.json config
drf-protector obfuscate   # Obfuscate code
drf-protector dockerize   # Build secure docker image
```

## ⚠️ Handling Django Migrations with PyArmor

When obfuscating your Django app, it's important to handle `migrations/` correctly to avoid runtime issues.

### ✅ Best Practices:

1. **Exclude `migrations/` from PyArmor obfuscation**:
   - These files must remain in readable Python as Django loads them dynamically.
   - Already handled in `drf_protector.json` default: `"exclude": ["migrations", "__pycache__"]`

2. **Include `migrations/` in your Docker build**:
   - Make sure to copy migration folders into the Docker image for proper deployment.

3. **Run `makemigrations` before obfuscating**:
   - Prepare all database changes before protecting the code.

4. **Run `migrate` at container runtime**:
   - Once deployed, run `python manage.py migrate` to apply changes.

### ❌ Don't Obfuscate:
Avoid obfuscating files in `migrations/` as it can break introspection, `RunPython`, or ORM model detection.

## License

MIT

---