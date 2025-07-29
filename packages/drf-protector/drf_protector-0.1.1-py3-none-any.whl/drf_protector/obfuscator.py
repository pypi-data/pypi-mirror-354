import os
import subprocess
import json

def obfuscate_project(license_path=None):
    with open('drf_protector.json') as f:
        config = json.load(f)

    app_path = config.get('app_path', '.')
    exclude = config.get('exclude', [])

    exclude_args = []
    for ex in exclude:
        exclude_args.extend(['--exclude', ex])

    cmd = [
        'pyarmor', 'gen',
        '--recursive',
        '--output', 'dist/obfuscated',
        *exclude_args,
        app_path
    ]

    if license_path:
        cmd += ['--with-license', license_path]

    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)

    print("✅ Obfuscation complete. Output at dist/obfuscated/")
