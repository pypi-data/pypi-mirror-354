import os
import json
import subprocess

def generate_dockerfile(tag):
    with open('drf_protector.json') as f:
        config = json.load(f)

    docker_base = config.get('docker_base', 'python:3.10-slim')

    dockerfile_content = f"""
FROM {docker_base}
WORKDIR /app
COPY dist/obfuscated /app
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]
"""

    with open('Dockerfile', 'w') as f:
        f.write(dockerfile_content)

    subprocess.run(['docker', 'build', '-t', tag, '.'], check=True)
    print(f"✅ Docker image '{tag}' built successfully.")
