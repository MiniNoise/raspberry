#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name             = 'Fenix API',
    description      = u'Communication between FenixOS and several APIs',
    author           = u'Rodolphe Asséré',
    author_email     = 'rodolphe.assere@gmail.com',
    version          = '0.1.1',
    packages         = ['fenix_api'],
    platforms        = ['Linux'],
    license          = 'GNU GPLv3',
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Environment :: Console',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: French',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Communications',
        'Topic :: Software Development :: Libraries',
        'Topic :: Terminals :: Serial',
    ],
    long_description = """
        PyMinitel est une bibliothèque Python permettant de pilor un Minitel
        depuis un PC sous Linux. Pour cela, la bibliothèque PySerial est
        nécessaire car elle est utilisée pour dialoguer avec le Minitel, en
        émission comme en réception.

        Le module de base utilise deux threads (émission + réception) offrant
        ainsi une communication asynchrone. Cette particularité permet au
        script de ne pas être tenu à une grande réactivité vis-à-vis du
        Minitel.

        En plus du module de base, PyMinitel est livrée avec une interface
        utilisateur basique.
    """
)

