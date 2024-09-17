import subprocess


def get_link() -> str:
    """gets last item in users clipboard."""
    link = subprocess.getoutput("powershell.exe -Command Get-Clipboard")
    return link

print(get_link())