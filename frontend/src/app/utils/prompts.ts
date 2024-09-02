export function getPrompts() {
  const prompts: { [id: string]: any } = {
    EN: {
      ASSOCIATION: {
        WITHOUT_DESCRIPTIONS: `
                                        I want you to tell me if you find a clear relationship between '{term}' and '{associative_term}'.
                                        If there is a reason to associate them, even if it is not direct, it counts as a relationship.

                                        Response must be in JSON format, following this example:
                                        {{"term": "{term}", "associative_term": "{associative_term}", "relationship": true/false, "reason": "reason why there is or isn't relationship between {term} and {associative_term}"}}
                                        """,
            'WITH_TERM_DESCRIPTION':    """
                                        I want you to tell me if you find a clear relationship between '{term}', which is '{term_description}', and '{associative_term}'.
                                        If there is a reason to associate them, even if it is not direct, it counts as a relationship.

                                        Response must be in JSON format, following this example:
                                        {{"term": "{term}", "associative_term": "{associative_term}", "relationship": true/false, "reason": "reason why there is or isn't relationship between {term} and {associative_term}"}}
                                        `,
      },
      GENERATION: {
        WITHOUT_ASSOCIATIVE_TERM: {
          WITH_DESCRIPTION: `
                                        Generate {n} text of less than {length} characters for a Google Ads ad.
                                        This ad has to be related with the term '{term}', and its description is '{term_description}'.
                                        It is for a retailer called '{company}' and must incentive the reader to buy '{term}'.

                                        Response must be in exactly the following format:
                                        ["write here the text 1", "write here the text 2", ..., "write here the text {n}"]
                                        The response must follow exactly that format. It does not have to contain any additional commas, whitespaces or line breaks. It must be just a comma-separated list of text between square brackets and that's it.
                                        `,
        },
        WITH_ASSOCIATIVE_TERM: {
          WITHOUT_DESCRIPTIONS: {
            HEADLINES: {
              WITHOUT_BLOCK_LIST: `
                                        Generate {n} headlines of less than 30 characters for a Google Ads ad.
                                        This ad has to be related with the terms '{term}' and '{associative_term}'.
                                        They must incentive the reader to buy '{term}' because '{association_reason}' is trending.
                                        It is extremely important that they are as short as possible, they must be shorter than 30 characters.
                                        Try to include key words related with the trending topic in the text.
                                        If the generated text are long, try to include the retailer's name, which is {company}, in the text.

                                        <br>Response must be in exactly the following format:
                                        ["write here the text 1", "write here the text 2", ..., "write here the text {n}"]
                                        The response must follow exactly that format. It does not have to contain any additional commas, whitespaces or line breaks. It must be just a comma-separated list of text between square brackets and that's it.
                                        `,
              WITH_BLOCK_LIST: `
                                        Generate {n} headlines of less than 30 characters for a Google Ads ad.
                                        This ad has to be related with the terms '{term}' and '{associative_term}'.
                                        They must incentive the reader to buy '{term}' because '{association_reason}' is trending.
                                        It is extremely important that they are as short as possible, they must be shorter than 30 characters.
                                        Try to include key words related with the trending topic in the text.
                                        If the generated text are long, try to include the retailer's name, which is {company}, in the text.

                                        <br><span class="highlight">Do not include the following list of terms in the generated headlines: {headlines_block_list}.</span>

                                        <br>Response must be in exactly the following format:
                                        ["write here the text 1", "write here the text 2", ..., "write here the text {n}"]
                                        The response must follow exactly that format. It does not have to contain any additional commas, whitespaces or line breaks. It must be just a comma-separated list of text between square brackets and that's it.
                                        `,
            },
            DESCRIPTIONS: {
              WITHOUT_BLOCK_LIST: `
                                        Generate {n} descriptions of less than 90 characters for a Google Ads ad.
                                        This ad has to be related with the terms '{term}' and '{associative_term}'.
                                        They must incentive the reader to buy '{term}' because '{association_reason}' is trending.
                                        It is extremely important that they are as short as possible, they must be shorter than 90 characters.
                                        Try to include key words related with the trending topic in the text.
                                        If the generated text are long, try to include the retailer's name, which is {company}, in the text.

                                        <br>Response must be in exactly the following format:
                                        ["write here the text 1", "write here the text 2", ..., "write here the text {n}"]
                                        The response must follow exactly that format. It does not have to contain any additional commas, whitespaces or line breaks. It must be just a comma-separated list of text between square brackets and that's it.
                                        `,

              WITH_BLOCK_LIST: `
                                        Generate {n} descriptions of less than 90 characters for a Google Ads ad.
                                        This ad has to be related with the terms '{term}' and '{associative_term}'.
                                        They must incentive the reader to buy '{term}' because '{association_reason}' is trending.
                                        It is extremely important that they are as short as possible, they must be shorter than 90 characters.
                                        Try to include key words related with the trending topic in the text.
                                        If the generated text are long, try to include the retailer's name, which is {company}, in the text.

                                        <br><span class="highlight">Do not include the following list of terms in the generated descriptions: {descriptions_block_list}.</span>

                                        <br>Response must be in exactly the following format:
                                        ["write here the text 1", "write here the text 2", ..., "write here the text {n}"]
                                        The response must follow exactly that format. It does not have to contain any additional commas, whitespaces or line breaks. It must be just a comma-separated list of text between square brackets and that's it.
                                        `,
            },
          },
        },
      },
      SIZE_ENFORCEMENT: `
                            I will give you one text for a Google Ads ad that is too long.
                            Make it shorter, it has to be shorter than {max_length} characters.
                            The text is: {copy}

                            Give me the response like this:
                            shortened_text
                            Just give me as a response the shortened text without quotation marks, line breaks or anything else.
                            `,
    },

    ES: {
      ASSOCIATION: {
        WITH_BOTH_DESCRIPTIONS:
          "Dime si encuentras una relación directa o indirecta entre '{term}', cuya descripcion es '{term_description}', y '{associative_term}', cuya descripcion es '{associative_term_description}'.",
        WITH_TERM_DESCRIPTION:
          "Dime si encuentras una relación directa o indirecta entre '{term}', cuya descripcion es '{term_description}', y '{associative_term}'.",
        WITH_ASSOCIATIVE_TERM_DESCRIPTION:
          "Dime si encuentras una relación directa o indirecta entre '{term}', cuya descripcion es '{term_description}', y '{associative_term}'.",
        WITHOUT_DESCRIPTIONS:
          "Dime si encuentras una relación directa o indirecta entre '{term}' y '{associative_term}'.",
        COMMON_PART: `
                        Con tal de que exista algún motivo para asociarlos, sea cual sea, ya cuenta como que hay una relación entre ambos.

                        La respuesta tiene que estar en formato JSON, siguiendo este ejemlpo:
                        {{"term": "{term}", "associative_term": "{associative_term}", "relationship": true/false, "reason": "motivo por el cuál hay o no relación entre {term} y {associative_term}"}}
                        `,
      },
      GENERATION: {
        WITH_ASSOCIATIVE_TERM: {
          WITHOUT_RELATIONSHIP_AND_DESCRIPTIONS: `
                                                        Genera {n} textos de menos de {length} caracteres para un anuncio de Google Ads.
                                                        Este anuncio tiene que estar relacionado con los términos '{term}' y '{associative_term}'.
                                                        Los textos deben incentivar al lector a comprar '{term}' debido a que es tendencia '{associative_term}'.

                                                        Finalmente, dame el resultado en el siguiente formato:
                                                        ["escribe aqui el texto 1", "escribe aqui el texto 2", ..., "escribe aqui el texto {n}"]
                                                        La respuesta debes darmela exactamente en el formato que te he pasado, sin agregar saltos de linea ni espacios innecesarios. Solo debe ser una lista de textos separados por comas, todo entre corchetes y nada mas.
                                                        `,

          WITHOUT_DESCRIPTIONS: {
            HEADLINES: {
              WITHOUT_BLOCK_LIST: `Genera {n} encabezados de menos de 30 caracteres para un anuncio de Google Ads.
                                Este anuncio tiene que estar relacionado con los términos '{term}' y '{associative_term}'.
                                Los textos deben incentivar al lector a comprar '{term}' debido a que es tendencia '{associative_term}'.
                                Considera el siguiente motivo de asociacion entre ambos términos: '{association_reason}'.
                                Si los textos a generar son largos, intenta incluir el nombre del minorista, que es '{company}', en ellos.

                                <br>Finalmente, dame el resultado en el siguiente formato:
                                ["escribe aqui el texto 1", "escribe aqui el texto 2", ..., "escribe aqui el texto {n}"]
                                La respuesta debes darmela exactamente en el formato que te he pasado, sin agregar saltos de linea ni espacios innecesarios. Solo debe ser una lista de textos separados por comas, todo entre corchetes y nada mas.
                                `,
              WITH_BLOCK_LIST: `Genera {n} encabezados de menos de 30 caracteres para un anuncio de Google Ads.
                                Este anuncio tiene que estar relacionado con los términos '{term}' y '{associative_term}'.
                                Los textos deben incentivar al lector a comprar '{term}' debido a que es tendencia '{associative_term}'.
                                Considera el siguiente motivo de asociacion entre ambos términos: '{association_reason}'.
                                Si los textos a generar son largos, intenta incluir el nombre del minorista, que es '{company}', en ellos.

                                <br><span class="highlight">No incluyas la siguiente lista de términos en los encabezados generados: {headlines_block_list}</span>

                                <br>Finalmente, dame el resultado en el siguiente formato:
                                ["escribe aqui el texto 1", "escribe aqui el texto 2", ..., "escribe aqui el texto {n}"]
                                La respuesta debes darmela exactamente en el formato que te he pasado, sin agregar saltos de linea ni espacios innecesarios. Solo debe ser una lista de textos separados por comas, todo entre corchetes y nada mas.
                                `,
            },
            DESCRIPTIONS: {
              WITHOUT_BLOCK_LIST: `Genera {n} descripciones de menos de 90 caracteres para un anuncio de Google Ads.
                                Este anuncio tiene que estar relacionado con los términos '{term}' y '{associative_term}'.
                                Los textos deben incentivar al lector a comprar '{term}' debido a que es tendencia '{associative_term}'.
                                Considera el siguiente motivo de asociacion entre ambos términos: '{association_reason}'.
                                Si los textos a generar son largos, intenta incluir el nombre del minorista, que es '{company}', en ellos.

                                <br>Finalmente, dame el resultado en el siguiente formato:
                                ["escribe aqui el texto 1", "escribe aqui el texto 2", ..., "escribe aqui el texto {n}"]
                                La respuesta debes darmela exactamente en el formato que te he pasado, sin agregar saltos de linea ni espacios innecesarios. Solo debe ser una lista de textos separados por comas, todo entre corchetes y nada mas.
                                `,

              WITH_BLOCK_LIST: `Genera {n} descripciones de menos de 90 caracteres para un anuncio de Google Ads.
                                Este anuncio tiene que estar relacionado con los términos '{term}' y '{associative_term}'.
                                Los textos deben incentivar al lector a comprar '{term}' debido a que es tendencia '{associative_term}'.
                                Considera el siguiente motivo de asociacion entre ambos términos: '{association_reason}'.
                                Si los textos a generar son largos, intenta incluir el nombre del minorista, que es '{company}', en ellos.

                                <br><span class="highlight">No incluyas la siguiente lista de términos en las descripciones generadas: {descriptions_block_list}</span>

                                <br>Finalmente, dame el resultado en el siguiente formato:
                                ["escribe aqui el texto 1", "escribe aqui el texto 2", ..., "escribe aqui el texto {n}"]
                                La respuesta debes darmela exactamente en el formato que te he pasado, sin agregar saltos de linea ni espacios innecesarios. Solo debe ser una lista de textos separados por comas, todo entre corchetes y nada mas.
                                `,
            },
          },

          WITH_TERM_DESCRIPTION: `
                                        Genera {n} textos de menos de {length} caracteres para un anuncio de Google Ads.
                                        Este anuncio tiene que estar relacionado con los términos '{term}', cuya descripción es '{term_description}' y '{associative_term}'.
                                        Los textos deben incentivar al lector a comprar '{term}' debido a que es tendencia '{associative_term}'.
                                        Considera el siguiente motivo de asociacion entre ambos términos: '{association_reason}'.
                                        Si los textos a generar son largos, intenta incluir el nombre del minorista, que es '{company}', en ellos.

                                        Finalmente, dame el resultado en el siguiente formato:
                                        ["escribe aqui el texto 1", "escribe aqui el texto 2", ..., "escribe aqui el texto {n}"]
                                        La respuesta debes darmela exactamente en el formato que te he pasado, sin agregar saltos de linea ni espacios innecesarios. Solo debe ser una lista de textos separados por comas, todo entre corchetes y nada mas.
                                        `,
          WITH_ASSOCIATIVE_TERM_DESCRIPTION: `
                                                    Genera {n} textos de menos de {length} caracteres para un anuncio de Google Ads.
                                                    Este anuncio tiene que estar relacionado con los términos '{term}' y '{associative_term}, cuya descripción es '{associative_term_description}'.
                                                    Los textos deben incentivar al lector a comprar '{term}' debido a que es tendencia '{associative_term}'.
                                                    Considera el siguiente motivo de asociacion entre ambos términos: '{association_reason}'.
                                                    Si los textos a generar son largos, intenta incluir el nombre del minorista, que es '{company}', en ellos.

                                                    Finalmente, dame el resultado en el siguiente formato:
                                                    ["escribe aqui el texto 1", "escribe aqui el texto 2", ..., "escribe aqui el texto {n}"]
                                                    La respuesta debes darmela exactamente en el formato que te he pasado, sin agregar saltos de linea ni espacios innecesarios. Solo debe ser una lista de textos separados por comas, todo entre corchetes y nada mas.
                                                    `,
          WITH_BOTH_DESCRIPTIONS: `
                                        Genera {n} textos de menos de {length} caracteres para un anuncio de Google Ads.
                                        Este anuncio tiene que estar relacionado con los términos '{term}', cuya descripción es '{term_description}' y '{associative_term}, cuya descripción es '{associative_term_description}'.
                                        Los textos deben incentivar al lector a comprar '{term}' debido a que es tendencia '{associative_term}'.
                                        Considera el siguiente motivo de asociacion entre ambos términos: '{association_reason}'.
                                        Si los textos a generar son largos, intenta incluir el nombre del minorista, que es '{company}', en ellos.

                                        Finalmente, dame el resultado en el siguiente formato:
                                        ["escribe aqui el texto 1", "escribe aqui el texto 2", ..., "escribe aqui el texto {n}"]
                                        La respuesta debes darmela exactamente en el formato que te he pasado, sin agregar saltos de linea ni espacios innecesarios. Solo debe ser una lista de textos separados por comas, todo entre corchetes y nada mas.
                                        `,
        },
        WITHOUT_ASSOCIATIVE_TERM: {
          WITH_DESCRIPTION: `
                                Genera {n} textos de menos de {length} caracteres para un anuncio de Google Ads.
                                Este anuncio tiene que estar relacionado con el término '{term}', cuya descripción es '{term_description}'.
                                Es de un minorista llamado {company} y debe invitar al cliente a '{term}'.
                                Si los textos a generar son largos, intenta incluir el nombre del minorista, que es {company}, en ellos.

                                Dame el resultado en el siguiente formato:
                                ["escribe aqui el texto 1", "escribe aqui el texto 2", ..., "escribe aqui el texto {n}"]
                                La respuesta debes darmela exactamente en el formato que te he pasado, sin agregar saltos de linea ni espacios innecesarios. Solo debe ser una lista de textos separados por comas, todo entre corchetes y nada mas.
                                `,
          WITHOUT_DESCRIPTION: `
                                    Genera {n} textos de menos de {length} caracteres para un anuncio de Google Ads.
                                    Este anuncio tiene que estar relacionado con el término '{term}'.
                                    Es de un minorista llamado {company} y debe invitar al cliente a '{term}'.
                                    Si los textos a generar son largos, intenta incluir el nombre del minorista, que es {company}, en ellos.

                                    Dame el resultado en el siguiente formato:
                                    ["escribe aqui el texto 1", "escribe aqui el texto 2", ..., "escribe aqui el texto {n}"]
                                    La respuesta debes darmela exactamente en el formato que te he pasado, sin agregar saltos de linea ni espacios innecesarios. Solo debe ser una lista de textos separados por comas, todo entre corchetes y nada mas.
                                    `,
        },
        PATHS_WITHOUT_TERM_DESCRIPTION: `
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
                                          `,
        PATHS_WITH_TERM_DESCRIPTION: `
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
                                        `,
      },
      SIZE_ENFORCEMENT: `
                        Te daré un texto de anuncio de Google ads que tengo que es demasiado largo.
                        Hazlo más corto, no debe tener mas de {max_length} caracteres.
                        El texto es: "{copy}"

                        Proporciona la respuesta en este formato:
                        texto_acortado
                        Solamente escribe como respuesta el texto acortado, sin comillas, saltos de linea ni nada adicional.
                        `,
    },
  };

  return prompts;
}
