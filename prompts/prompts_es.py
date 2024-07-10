# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

prompts_es = {
    'ASSOCIATION': {
        'WITH_BOTH_DESCRIPTIONS': "Dime si encuentras una relación directa o indirecta entre '{term}', cuya descripcion es '{term_description}', y '{associative_term}', cuya descripcion es '{associative_term_description}'.",
        'WITH_TERM_DESCRIPTION': "Dime si encuentras una relación directa o indirecta entre '{term}', cuya descripcion es '{term_description}', y '{associative_term}'.",
        'WITH_ASSOCIATIVE_TERM_DESCRIPTION': "Dime si encuentras una relación directa o indirecta entre '{term}', cuya descripcion es '{term_description}', y '{associative_term}'.",
        'WITHOUT_DESCRIPTIONS': "Dime si encuentras una relación directa o indirecta entre '{term}' y '{associative_term}'.",
        'COMMON_PART':  """
                        Con tal de que exista algún motivo para asociarlos, sea cual sea, ya cuenta como que hay una relación entre ambos.

                        La respuesta tiene que estar en formato JSON, siguiendo este ejemlpo:
                        {{"term": "{term}", "associative_term": "{associative_term}", "relationship": true/false, "reason": "motivo por el cuál hay o no relación entre {term} y {associative_term}"}}
                        """,
    },
    'GENERATION': {
        'WITH_ASSOCIATIVE_TERM': {
            'WITHOUT_RELATIONSHIP_AND_DESCRIPTIONS':    """
                                                        Genera {n} textos de menos de {length} caracteres para un anuncio de Google Ads.
                                                        Este anuncio tiene que estar relacionado con los términos '{term}' y '{associative_term}'.
                                                        Los textos deben incentivar al lector a comprar '{term}' debido a que es tendencia '{associative_term}'.

                                                        Finalmente, dame el resultado en el siguiente formato:
                                                        ["escribe aqui el texto 1", "escribe aqui el texto 2", ..., "escribe aqui el texto {n}"]
                                                        La respuesta debes darmela exactamente en el formato que te he pasado, sin agregar saltos de linea ni espacios innecesarios. Solo debe ser una lista de textos separados por comas, todo entre corchetes y nada mas.
                                                        """,
            'WITHOUT_DESCRIPTIONS': """
                                Genera {n} textos de menos de {length} caracteres para un anuncio de Google Ads.
                                Este anuncio tiene que estar relacionado con los términos '{term}' y '{associative_term}'.
                                Los textos deben incentivar al lector a comprar '{term}' debido a que es tendencia '{associative_term}'.
                                Considera el siguiente motivo de asociacion entre ambos términos: '{association_reason}'.
                                Si los textos a generar son largos, intenta incluir el nombre del minorista, que es '{company}', en ellos.

                                Finalmente, dame el resultado en el siguiente formato:
                                ["escribe aqui el texto 1", "escribe aqui el texto 2", ..., "escribe aqui el texto {n}"]
                                La respuesta debes darmela exactamente en el formato que te he pasado, sin agregar saltos de linea ni espacios innecesarios. Solo debe ser una lista de textos separados por comas, todo entre corchetes y nada mas.
                                """,
            'WITH_TERM_DESCRIPTION':    """
                                        Genera {n} textos de menos de {length} caracteres para un anuncio de Google Ads.
                                        Este anuncio tiene que estar relacionado con los términos '{term}', cuya descripción es '{term_description}' y '{associative_term}'.
                                        Los textos deben incentivar al lector a comprar '{term}' debido a que es tendencia '{associative_term}'.
                                        Considera el siguiente motivo de asociacion entre ambos términos: '{association_reason}'.
                                        Si los textos a generar son largos, intenta incluir el nombre del minorista, que es '{company}', en ellos.

                                        Finalmente, dame el resultado en el siguiente formato:
                                        ["escribe aqui el texto 1", "escribe aqui el texto 2", ..., "escribe aqui el texto {n}"]
                                        La respuesta debes darmela exactamente en el formato que te he pasado, sin agregar saltos de linea ni espacios innecesarios. Solo debe ser una lista de textos separados por comas, todo entre corchetes y nada mas.
                                        """,
            'WITH_ASSOCIATIVE_TERM_DESCRIPTION':    """
                                                    Genera {n} textos de menos de {length} caracteres para un anuncio de Google Ads.
                                                    Este anuncio tiene que estar relacionado con los términos '{term}' y '{associative_term}, cuya descripción es '{associative_term_description}'.
                                                    Los textos deben incentivar al lector a comprar '{term}' debido a que es tendencia '{associative_term}'.
                                                    Considera el siguiente motivo de asociacion entre ambos términos: '{association_reason}'.
                                                    Si los textos a generar son largos, intenta incluir el nombre del minorista, que es '{company}', en ellos.

                                                    Finalmente, dame el resultado en el siguiente formato:
                                                    ["escribe aqui el texto 1", "escribe aqui el texto 2", ..., "escribe aqui el texto {n}"]
                                                    La respuesta debes darmela exactamente en el formato que te he pasado, sin agregar saltos de linea ni espacios innecesarios. Solo debe ser una lista de textos separados por comas, todo entre corchetes y nada mas.
                                                    """,
            'WITH_BOTH_DESCRIPTIONS':   """
                                        Genera {n} textos de menos de {length} caracteres para un anuncio de Google Ads.
                                        Este anuncio tiene que estar relacionado con los términos '{term}', cuya descripción es '{term_description}' y '{associative_term}, cuya descripción es '{associative_term_description}'.
                                        Los textos deben incentivar al lector a comprar '{term}' debido a que es tendencia '{associative_term}'.
                                        Considera el siguiente motivo de asociacion entre ambos términos: '{association_reason}'.
                                        Si los textos a generar son largos, intenta incluir el nombre del minorista, que es '{company}', en ellos.

                                        Finalmente, dame el resultado en el siguiente formato:
                                        ["escribe aqui el texto 1", "escribe aqui el texto 2", ..., "escribe aqui el texto {n}"]
                                        La respuesta debes darmela exactamente en el formato que te he pasado, sin agregar saltos de linea ni espacios innecesarios. Solo debe ser una lista de textos separados por comas, todo entre corchetes y nada mas.
                                        """
        },
        'WITHOUT_ASSOCIATIVE_TERM': {
            'WITH_DESCRIPTION': """
                                Genera {n} textos de menos de {length} caracteres para un anuncio de Google Ads.
                                Este anuncio tiene que estar relacionado con el término '{term}', cuya descripción es '{term_description}'.
                                Es de un minorista llamado {company} y debe invitar al cliente a '{term}'.
                                Si los textos a generar son largos, intenta incluir el nombre del minorista, que es {company}, en ellos.

                                Dame el resultado en el siguiente formato:
                                ["escribe aqui el texto 1", "escribe aqui el texto 2", ..., "escribe aqui el texto {n}"]
                                La respuesta debes darmela exactamente en el formato que te he pasado, sin agregar saltos de linea ni espacios innecesarios. Solo debe ser una lista de textos separados por comas, todo entre corchetes y nada mas.
                                """,
            'WITHOUT_DESCRIPTION':  """
                                    Genera {n} textos de menos de {length} caracteres para un anuncio de Google Ads.
                                    Este anuncio tiene que estar relacionado con el término '{term}'.
                                    Es de un minorista llamado {company} y debe invitar al cliente a '{term}'.
                                    Si los textos a generar son largos, intenta incluir el nombre del minorista, que es {company}, en ellos.

                                    Dame el resultado en el siguiente formato:
                                    ["escribe aqui el texto 1", "escribe aqui el texto 2", ..., "escribe aqui el texto {n}"]
                                    La respuesta debes darmela exactamente en el formato que te he pasado, sin agregar saltos de linea ni espacios innecesarios. Solo debe ser una lista de textos separados por comas, todo entre corchetes y nada mas.
                                    """,

        },
        'PATHS_WITHOUT_TERM_DESCRIPTION': """
                                          Te daré un término y su descripción, y debes obtener un path de una url dividido en {n} partes para ese término.
                                          El path debe referirse al término, en este caso '{term}', y a su descripción, en este caso '{term_description}'.
                                          Cada parte del path debe ser extremadamente corta, una sola palabras que englobe la idea principal de '{term}' y que tengan en cuenta la descripción '{term_description}'.
                                          Por ejemplo, si el término es 'celulares' y su descripción es 'Samsung Galaxy S23, Samsung Galaxy S23 Plus, Samsung Galaxy S23 Ultra', entonces la parte 1 del path puede ser 'celulares' y la parte 2 del path puede ser 'galaxy-s23'.
                                          Este path será usado en la url de un ecommerce de manera tal que se mostrará así: www.ecommerce.com/PATH1/PATH2. Ejemplo: www.ecommerce.com/zapatillas/nike-running
                                          La primera parte del path debe ser una categoría, como por ejemplo 'celulares', y la segunda parte algo más granular referido al producto, como por ejemplo 'galaxy-s23'.
                                          Algunos ejemplos de PATHs para que te inspires, con sus dos partes, son: 'zapatillas/nike-running', 'televisores/samsung', 'vehículos/ford-ranger'.
                                          IMPORTANTE: NO debe contener mayusculas ni espacios, si son varias palabras deben estar en minúscula y separadas por guion medio.

                                          Dame el resultado en el siguiente formato:
                                          ["escribe aqui la parte 1 del path", "escribe aqui la parte 2 del path"]
                                          La respuesta debes darmela exactamente en el formato que te he pasado, sin agregar saltos de linea ni espacios innecesarios. Solo debe ser una lista de textos separados por comas, todo entre corchetes y nada mas.
                                          """,
        'PATHS_WITH_TERM_DESCRIPTION':  """
                                        Te daré un término y debes obtener un path de una url dividido en {n} partes para ese término.
                                        El path debe referirse al término, en este caso '{term}'.
                                        Cada parte del path debe ser extremadamente corta, una sola palabras que englobe la idea principal de '{term}'.
                                        Por ejemplo, si el término es 'celulares Samsung S23', entonces la parte 1 del path puede ser 'celulares' y la parte 2 del path puede ser 'galaxy-s23'.
                                        Este path será usado en la url de un ecommerce de manera tal que se mostrará así: www.ecommerce.com/PATH1/PATH2. Ejemplo: www.ecommerce.com/zapatillas/nike-running
                                        La primera parte del path debe ser una categoría, como por ejemplo 'celulares', y la segunda parte algo más granular referido al producto, como por ejemplo 'galaxy-s23'.
                                        Algunos ejemplos de PATHs para que te inspires, con sus dos partes, son: 'zapatillas/nike-running', 'televisores/samsung', 'vehículos/ford-ranger'.
                                        IMPORTANTE: NO debe contener mayusculas ni espacios, si son varias palabras deben estar en minúscula y separadas por guion medio.

                                        Dame el resultado en el siguiente formato:
                                        ["escribe aqui la parte 1 del path", "escribe aqui la parte 2 del path"]
                                        La respuesta debes darmela exactamente en el formato que te he pasado, sin agregar saltos de linea ni espacios innecesarios. Solo debe ser una lista de textos separados por comas, todo entre corchetes y nada mas.
                                        """
    },
    'SIZE_ENFORCEMENT': """
                        Te daré un texto de anuncio de Google ads que tengo que es demasiado largo.
                        Hazlo más corto, no debe tener mas de {max_length} caracteres.
                        El texto es: "{copy}"

                        Proporciona la respuesta en este formato:
                        texto_acortado
                        Solamente escribe como respuesta el texto acortado, sin comillas, saltos de linea ni nada adicional.
                        """
}
