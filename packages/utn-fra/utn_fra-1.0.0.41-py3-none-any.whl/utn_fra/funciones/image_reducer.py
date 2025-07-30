# Copyright (C) 2025 <UTN FRA>
#
# Author: Facundo Falcone <f.falcone@sistemas-utnfra.com.ar>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from PIL import Image # pip install pillow
import os

class ImageReducer:
    
    def __init__(self,input_path: str):
        """
        Inicializa la clase encargada de reducir el peso de las imagenes sin perdida de calidad.
        Args:
            input_path (str): Ruta de los archivos PNG de entrada.
        """
        self.input_path = input_path
        self.paths_list = list()

    def __reducir_peso_png_pillow(self, path: str, nivel_compresion=9):
        """
        Reduce el peso de una imagen PNG usando Pillow.

        Args:
            nivel_compresion (int): Nivel de compresión de 0 (sin compresión, rápido)
                                    a 9 (máxima compresión, lento). El valor predeterminado es 9.
        """
        try:
            imagen = Image.open(path)
            imagen.save(path, optimize=True, compress_level=nivel_compresion)
            print(f"Imagen optimizada guardada en: {path}")
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo en la ruta: {path}")
        except Exception as e:
            print(f"Ocurrió un error: {e}")

    def __make_files_paths(self,root_path: str, files_path: list[str]):
        self.paths_list = list()
        for file in files_path:
            new_path = os.path.join(root_path, file)
            self.paths_list.append(f'{new_path}')

    def __create_paths(self):
        for root, dir, files in os.walk('.\\deck_test'):
            self.__make_files_paths(root, files)
    
    def reducir_peso_imagenes(self, nivel_compresion: int = 9):
        """
        Reduce el tamaño de las imagenes presentes en el directorio raíz y subdirectorios,
        guardandolas bajo su mismo nombre pero con un peso menor.
        Args:
            nivel_compresion (int): Nivel de compresión de 0 (sin compresión, rápido)
                                    a 9 (máxima compresión, lento). El valor predeterminado es 9.
        """
        self.__create_paths()
        for path in self.paths_list:
            self.__reducir_peso_png_pillow(path, nivel_compresion)