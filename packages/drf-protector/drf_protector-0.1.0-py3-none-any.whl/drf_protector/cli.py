import click
from drf_protector.obfuscator import obfuscate_project
from drf_protector.dockerizer import generate_dockerfile
from drf_protector.utils import init_config

@click.group()
def main():
    """DRF Protector CLI - Secure your Django apps with PyArmor & Docker"""
    pass

@main.command()
def init():
    """Initialize drf_protector.json config"""
    init_config()

@main.command()
@click.option('--license', default=None, help='Path to PyArmor license file')
def obfuscate(license):
    """Obfuscate Django project with PyArmor"""
    obfuscate_project(license)

@main.command()
@click.option('--tag', default='secure-drf:latest', help='Docker image tag')
def dockerize(tag):
    """Generate Dockerfile and build image"""
    generate_dockerfile(tag)

if __name__ == '__main__':
    main()
