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

prompts_pt = {
    'GOOGLE_TRENDS': {
        'FIND_RELATIONSHIP':  """
                              Quero que você me diga se encontra uma relação clara entre dois conceitos que lhe darei.
                              O primeiro é {brand} e o segundo é {trend}.

                              A resposta deve estar no formato JSON, seguindo este exemplo:
                              {{"trend": "{trend}", "brand": "{brand}", "relationship": true/false, "reason": "razão pela qual existe ou não relacionamento entre {brand} e {trend}"}}
                              """,
        'COPIES_GENERATION':    """
                                Quero gerar {n} textos com menos de {length} caracteres para um anúncio do Google Ads.
                                Este anúncio deve estar relacionado a um trending topic, neste caso {trend}, e com a marca {brand}.
                                Considere que o motivo pelo qual a marca e o trending topic estão relacionados é: {association_reason}.
                                É extremamente importante que sejam o mais curtos possível, devem ter menos de {length} caracteres.
                                Procure incluir palavras-chave relacionadas ao trending topic nos textos.
                                Se os textos gerados forem longos, procure incluir o nome do varejista, que é {company}, nos textos.

                                Aqui você tem alguns exemplos que você pode usar como inspiração para criar os novos textos que você vai me dar:

                                {examples}

                                Certifique-se de que os textos estejam em conformidade com as políticas descritas aqui: https://support.google.com/adspolicy/answer/6008942?hl=en#con

                                A resposta deve estar exatamente no seguinte formato:
                                ["escreva aqui o texto 1", "escreva aqui o texto 2", ..., "escreva aqui o texto {n}"]
                                A resposta deve seguir exatamente esse formato. Não precisa conter vírgulas, espaços em branco ou quebras de linha adicionais. Deve ser apenas uma lista de textos separados por vírgulas entre colchetes e pronto.
                                """
    }, 
    'CLIENT_TRENDS': {
        'COPIES_GENERATION':    """
                                Quero gerar {n} textos com menos de {length} caracteres para um anúncio do Google Ads.
                                Este anúncio deve estar relacionado a um produto, neste caso {title}.
                                É de um varejista chamado {company} e deve convidar o cliente a comprar porque o produto está de alguma forma na moda.
                                É extremamente importante que sejam o mais curtos possível, devem ter menos de {length} caracteres.
                                Procure incluir no texto palavras-chave relacionadas ao produto.
                                Se os textos gerados forem longos, procure incluir o nome do varejista, que é {company}, nos textos.

                                Aqui você tem alguns exemplos que você pode usar como inspiração para criar os novos textos que você vai me dar:

                                {examples}

                                Certifique-se de que os textos estejam em conformidade com as políticas descritas aqui: https://support.google.com/adspolicy/answer/6008942?hl=en#con

                                A resposta deve estar exatamente no seguinte formato:
                                ["escreva aqui o texto 1", "escreva aqui o texto 2", ..., "escreva aqui o texto {n}"]
                                A resposta deve seguir exatamente esse formato. Não precisa conter vírgulas, espaços em branco ou quebras de linha adicionais. Deve ser apenas uma lista de textos separados por vírgulas entre colchetes e pronto.
                                """
    },
    'SIZE_ENFORCEMENT': """
                        Darei a você um texto para um anúncio do Google Ads que é muito longo.
                        Torne-o mais curto, deve ter menos de {max_length} caracteres.
                        O texto é: {copy}

                        Dê-me a resposta assim:
                        texto_abreviado
                        Basta me dar como resposta o texto abreviado sem aspas, quebras de linha ou qualquer outra coisa.
                        """
}