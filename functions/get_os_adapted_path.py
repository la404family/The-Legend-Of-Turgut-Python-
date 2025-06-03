import os
# Cette fonction permet d'adapter un chemin de fichier en fonction du système d'exploitation.
# Elle retourne  :chemin = os.path.join(".", dossier, fichier)  # => './assets/favicon.png' (adapté à l'OS)


def get_os_adapted_path(folder, file):
    """
    Adapt a file path to the current operating system.

    :param folder: The folder name.
    :param file: The file name.
    :return: A path string adapted to the current OS.
    """
    # Utiliser os.path.join pour créer un chemin adapté à l'OS
    chemin = os.path.join(".", folder, file)
    return chemin
