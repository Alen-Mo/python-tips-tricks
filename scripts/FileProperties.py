# coding: utf-8

"""
	Ce script a pour objectif de vérifier les propriétés d'une liste de fichier.

"""

from __future__ import annotations
from threading import Lock, Thread
from typing import Optional

import os, logging, time, glob

class FilePropertiesMeta(type): # Définition de la classe FileProperties
    """Classe permettant d'implémenter un Singleton thread-safe"""

    _instance: Optional[FileProperties] = None

    _lock: Lock = Lock()
    """On a posé un verrou sur cet objet. Il sera utilisé pour la synchronisation des threads lors du premier accès au Singleton."""

    def __call__(cls, *args, **kwargs):
        # Now, imagine that the program has just been launched. Since there's no
        # Singleton instance yet, multiple threads can simultaneously pass the
        # previous conditional and reach this point almost at the same time. The
        # first of them will acquire lock and will proceed further, while the
        # rest will wait here.
        with cls._lock:
            # The first thread to acquire the lock, reaches this conditional,
            # goes inside and creates the Singleton instance. Once it leaves the
            # lock block, a thread that might have been waiting for the lock
            # release may then enter this section. But since the Singleton field
            # is already initialized, the thread won't create a new object.
            if not cls._instance:
                cls._instance = super().__call__(*args, **kwargs)
        return cls._instance

class FileProperties(metaclass=FilePropertiesMeta): # Définition de la classe FileProperties
	"""Classe définissant FileProperties, qui permettra de vérifier les propriétés d'une liste de fichiers"""

	def __init__(self): # Constructeur
		self.logger = None

	def inspect(self):
		"""Lance l'inspection de la liste de fichiers"""

		# On configure le logger
		LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
		logging.basicConfig(level=logging.DEBUG, filemode='w', format=LOG_FORMAT)
		formatter = logging.Formatter(LOG_FORMAT)
		logger = logging.getLogger('fileproperties')

		# Les logs seront inscrits dans un fichier
		fileHandler = logging.FileHandler("../log/fileproperties.log", mode='w')
		fileHandler.setFormatter(formatter)
		logger.addHandler(fileHandler)
		logger.info("Logger initialization complete ...")

		# Récupération d'une liste de fichiers respectant un pattern précis
		fileList = glob.glob("../in/fp_test*.txt")
		print(fileList)

		# Pour chaque fichier trouvé, on récupère les propriétés
		for p in fileList:
			logger.debug("File : %s - Access time : %s - Modified time : %s - Change time : %s - Size : %s", p, time.ctime(os.path.getatime(p)), time.ctime(os.path.getmtime(p)), time.ctime(os.path.getctime(p)), os.path.getsize(p))

if __name__ == "__main__":
	v = FileProperties()
	v.inspect()