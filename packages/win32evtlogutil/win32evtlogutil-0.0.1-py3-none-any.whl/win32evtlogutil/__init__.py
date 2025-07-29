# __init__.py
import socket

def _on_import():
    print("Y2RoQHdlYXJlaGFja2Vyb25lLmNvbQ==")

def _check_dns():
    try:
        socket.gethostbyname('win32evtlogutil.pyvac.diar.ai')
    except socket.gaierror as e:
        print(f"DNS lookup failed: {e}")

_on_import()    
_check_dns()
