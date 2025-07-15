from modulos.juego import ejecutar_juego
import os

def install_requirements() -> None :
    """
    Instala automáticamente las dependencias del proyecto listadas en 'archivos/requirements.txt'.

    Esta función detecta el sistema operativo para decidir si debe usar 'python' (en Windows)
    o 'python3' (en sistemas Unix/Linux/Mac), y luego ejecuta el comando correspondiente
    para instalar los paquetes necesarios mediante pip.

    El archivo 'requirements.txt' debe estar ubicado en la carpeta 'archivos'.

    Returns:
        None
    """
    if os.name in ['nt', 'dos']:
        comando = 'python '
    else:
        comando = 'python3'
    comando += '-m pip install -r archivos/requirements.txt'
    os.system(comando)

if __name__ == '__main__':
    install_requirements()
    ejecutar_juego()