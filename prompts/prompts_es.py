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

        }
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
