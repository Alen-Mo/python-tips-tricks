# coding: utf-8

"""
	Ce script a pour objectif de parser un fichier XML en utilisant BeautifulSoup.
"""

from __future__ import annotations
from threading import Lock, Thread
from typing import Optional
from bs4 import BeautifulSoup as bs

import os, logging

class XmlParserMeta(type): # Définition de la classe XmlParser
    """Classe permettant d'implémenter un Singleton thread-safe"""

    _instance: Optional[XmlParser] = None

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

class XmlParser(metaclass=XmlParserMeta): # Définition de la classe XmlParser
	"""Classe définissant XmlParser, qui permettra de parser le contenu d'un fichier XML"""

	def __init__(self): # Constructeur
		self.logger = None

	def inspect(self):
		"""Lance l'inspection du fichier XML"""

		# On configure le logger
		LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
		logging.basicConfig(level=logging.DEBUG, filemode='w', format=LOG_FORMAT)
		formatter = logging.Formatter(LOG_FORMAT)
		logger = logging.getLogger('xmlparser')

		# Les logs seront inscrits dans un fichier
		fileHandler = logging.FileHandler("../log/xmlparser.log", mode='w')
		fileHandler.setFormatter(formatter)
		logger.addHandler(fileHandler)
		logger.info("Logger initialization complete ...")

		content = []

		# Lecture du fichier XML
		with open("../sample/food_menu.xml", "r") as file:
			# Lecture de chaque ligne du fichier
			content = file.readlines()
			content = "".join(content)
			bs_content = bs(content,"lxml")
			logger.info("Parse finished !")

			# Rechercher des tags
			result = bs_content.find("food")
			logger.debug("Food : %s", result)

			result = bs_content.find_all("food")
			logger.debug("All Food : %s", result)

if __name__ == "__main__":
	v = XmlParser()
	v.inspect()