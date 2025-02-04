import os
from django.conf import settings

def get_version():
    version_file = os.path.join(settings.BASE_DIR, 'symm', 'version.txt')
    try:
        with open(version_file, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return "vUnknown"
    except Exception as e:
        print(f"Error reading version file: {e}")
        return "vUnknown"

def app_version(request):
    return {'app_version': get_version()}
