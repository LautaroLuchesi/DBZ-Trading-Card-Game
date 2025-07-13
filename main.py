from modulos.juego import ejecutar_juego
import os

def install_requirements():
    if os.name in ['nt', 'dos']:
        comando = 'python '
    else:
        comando = 'python3 '
    comando += '-m pip install -r archivos/requirements.txt'
    os.system(comando)

if __name__ == '__main__':
    install_requirements()
    ejecutar_juego()