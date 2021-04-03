# coding: utf-8

"""
	Ce script a pour objectif d'extraire le contenu VBA des fichiers Excel d'un dossier.
	Tout cela permettra d'évaluer les opérations réalisées dans ces fichiers.
"""

from __future__ import annotations
from threading import Lock, Thread
from typing import Optional

import os, logging, configparser

class OletoolsMeta(type): # Définition de la classe Oletools
    """Classe permettant d'implémenter un Singleton thread-safe"""

    _instance: Optional[Oletools] = None

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

class Oletools(metaclass=OletoolsMeta): # Définition de la classe Oletools
	"""Classe définissant Oletools, qui permettra d'inspecter le code VBA présent dans des fichiers Excel"""

	def __init__(self): # Constructeur
		self.logger = None

	def inspect(self):
		"""Lance l'inspection du code VBA"""

		# On configure le logger
		LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
		logging.basicConfig(level=logging.DEBUG, filemode='w', format=LOG_FORMAT)
		formatter = logging.Formatter(LOG_FORMAT)
		logger = logging.getLogger('oletools')

		# Les logs seront inscrits dans un fichier
		fileHandler = logging.FileHandler("../log/oletools.log", mode='w')
		fileHandler.setFormatter(formatter)
		logger.addHandler(fileHandler)
		logger.info("Logger initialization complete ...")

		# On récupère le contenu du fichier de configuration
		# La configuration de l'analyse (quoi et où)
		config = configparser.ConfigParser()
		config.sections()
		config.read("../config/oletools.ini")
		root = config['DEFAULT']['root']
		pattern = config['DEFAULT']['pattern']

		# Appel de olevba
		# -a : effectuer une analyse
		# -d : activer le mode détaillé
		# -r : activer la récursivité
		# -c : afficher le code VBA sans l'analyser
		logger.info("Scan in progress : %s%s ..." % (root,pattern))
		os.system("olevba -a -d -r -c %s%s* > ../out/result.log" % (root,pattern))
		logger.info("Scan finished !")

if __name__ == "__main__":
	v = Oletools()
	v.inspect()