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
    "ASSOCIATION": {
        "WITH_BOTH_DESCRIPTIONS": """
                Diga-me se existe uma relação direta ou indireta entre '{term}', cuja descrição é '{term_description}',
                e '{associative_term}', cuja descrição é '{associative_term_description}'.
            """,
        "WITH_TERM_DESCRIPTION": """
                Diga-me se existe uma relação direta ou indireta entre '{term}', cuja descrição é '{term_description}',
                e '{associative_term}'.
            """,
        "WITH_ASSOCIATIVE_TERM_DESCRIPTION": """
                Diga-me se existe uma relação direta ou indireta entre '{term}' e '{associative_term}',
                cuja descrição é '{associative_term_description}'.
            """,
        "WITHOUT_DESCRIPTIONS": """
                Diga-me se existe uma relação direta ou indireta entre '{term}' e '{associative_term}'.
            """,
        "COMMON_PART": """
            Descubra se existe alguma forma de associar os termos, mesmo que não seja uma relação muito direta.

            A resposta deve estar no formato JSON, seguindo este exemplo:
            {{"term": "{term}", "associative_term": "{associative_term}", "relationship": true/false, "reason": "motivo pelo qual existe ou não relação entre {term} e {associative_term}"}}
        """,
    },
    "GENERATION": {
        "WITH_ASSOCIATIVE_TERM": {
            "WITHOUT_RELATIONSHIP_AND_DESCRIPTIONS": """
                    Gere {n} anúncios de texto com menos de {length} caracteres para o Google Ads.
                    O anúncio deve estar relacionado aos termos '{term}' e '{associative_term}'.
                    O anúncio de texto deve incentivar os potenciais clientes a comprar '{term}' porque '{associative_term}' está em alta.

                    A resposta deve estar no seguinte formato:
                    ["texto 1 aqui", "texto 2 aqui", ..., "texto {n} aqui"]
                    A resposta deve estar exatamente no formato fornecido, sem incluir quebras de linha ou espaços desnecessários.
                    Deve ser apenas uma lista de anúncios de texto separados por vírgulas e entre colchetes.
                """,
            "WITHOUT_DESCRIPTIONS": """
                    Gere {n} anúncios de texto com menos de {length} caracteres para o Google Ads.
                    O anúncio deve estar relacionado aos termos '{term}' e '{associative_term}'.
                    O anúncio de texto deve incentivar os potenciais clientes a comprar '{term}' porque '{associative_term}' está em alta.
                    Considere o seguinte motivo de associação entre ambos os termos para criar o anúncio: '{association_reason}'.
                    Se os anúncios de texto gerados forem longos, tente incluir o nome do varejista: '{company}'.

                    A resposta deve estar no seguinte formato:
                    ["texto 1 aqui", "texto 2 aqui", ..., "texto {n} aqui"]
                    A resposta deve estar exatamente no formato fornecido, sem incluir quebras de linha ou espaços desnecessários.
                    Deve ser apenas uma lista de anúncios de texto separados por vírgulas e entre colchetes.
                """,
            "WITH_TERM_DESCRIPTION": """
                    Gere {n} anúncios de texto com menos de {length} caracteres para o Google Ads.
                    O anúncio deve estar relacionado aos termos '{term}', cuja descrição é '{term_description}', e '{associative_term}'.
                    O anúncio de texto deve incentivar os potenciais clientes a comprar '{term}' porque '{associative_term}' está em alta.
                    Considere o seguinte motivo de associação entre ambos os termos para criar o anúncio: '{association_reason}'.
                    Se os anúncios de texto gerados forem longos, tente incluir o nome do varejista: '{company}'.

                    A resposta deve estar no seguinte formato:
                    ["texto 1 aqui", "texto 2 aqui", ..., "texto {n} aqui"]
                    A resposta deve estar exatamente no formato fornecido, sem incluir quebras de linha ou espaços desnecessários.
                    Deve ser apenas uma lista de anúncios de texto separados por vírgulas e entre colchetes.
                """,
            "WITH_ASSOCIATIVE_TERM_DESCRIPTION": """
                    Gere {n} anúncios de texto com menos de {length} caracteres para o Google Ads.
                    O anúncio deve estar relacionado aos termos '{term}' e '{associative_term}', cuja descrição é '{associative_term_description}'.
                    O anúncio de texto deve incentivar os potenciais clientes a comprar '{term}' porque '{associative_term}' está em alta.
                    Considere o seguinte motivo de associação entre ambos os termos para criar o anúncio: '{association_reason}'.
                    Se os anúncios de texto gerados forem longos, tente incluir o nome do varejista: '{company}'.

                    A resposta deve estar no seguinte formato:
                    ["texto 1 aqui", "texto 2 aqui", ..., "texto {n} aqui"]
                    A resposta deve estar exatamente no formato fornecido, sem incluir quebras de linha ou espaços desnecessários.
                    Deve ser apenas uma lista de anúncios de texto separados por vírgulas e entre colchetes.
                """,
            "WITH_BOTH_DESCRIPTIONS": """
                    Gere {n} anúncios de texto com menos de {length} caracteres para o Google Ads.
                    O anúncio deve estar relacionado aos termos '{term}', cuja descrição é '{term_description}', e '{associative_term}', cuja descrição é '{associative_term_description}'.
                    O anúncio de texto deve incentivar os potenciais clientes a comprar '{term}' porque '{associative_term}' está em alta.
                    Considere o seguinte motivo de associação entre ambos os termos para criar o anúncio: '{association_reason}'.
                    Se os anúncios de texto gerados forem longos, tente incluir o nome do varejista: '{company}'.

                    A resposta deve estar no seguinte formato:
                    ["texto 1 aqui", "texto 2 aqui", ..., "texto {n} aqui"]
                    A resposta deve estar exatamente no formato fornecido, sem incluir quebras de linha ou espaços desnecessários.
                    Deve ser apenas uma lista de anúncios de texto separados por vírgulas e entre colchetes.
                """,
        },
        "WITHOUT_ASSOCIATIVE_TERM": {
            "WITH_DESCRIPTION": """
                    Gere {n} anúncios de texto com menos de {length} caracteres para o Google Ads.
                    O anúncio deve estar relacionado ao termo '{term}', cuja descrição é '{term_description}'.
                    É de um varejista chamado {company} e deve incentivar os potenciais clientes a comprar '{term}'.
                    Se os anúncios de texto gerados forem longos, tente incluir o nome do varejista: '{company}'.

                    A resposta deve estar no seguinte formato:
                    ["texto 1 aqui", "texto 2 aqui", ..., "texto {n} aqui"]
                    A resposta deve estar exatamente no formato fornecido, sem incluir quebras de linha ou espaços desnecessários.
                    Deve ser apenas uma lista de anúncios de texto separados por vírgulas e entre colchetes.
                """,
            "WITHOUT_DESCRIPTION": """
                    Gere {n} anúncios de texto com menos de {length} caracteres para o Google Ads.
                    O anúncio deve estar relacionado ao termo '{term}'.
                    É de um varejista chamado {company} e deve incentivar os potenciais clientes a comprar '{term}'.
                    Se os anúncios de texto gerados forem longos, tente incluir o nome do varejista: '{company}'.

                    A resposta deve estar no seguinte formato:
                    ["texto 1 aqui", "texto 2 aqui", ..., "texto {n} aqui"]
                    A resposta deve estar exatamente no formato fornecido, sem incluir quebras de linha ou espaços desnecessários.
                    Deve ser apenas uma lista de anúncios de texto separados por vírgulas e entre colchetes.
                """,
        },
        "PATHS_WITHOUT_TERM_DESCRIPTION": """
                Será fornecido um termo, e você deve gerar um caminho de URL dividido em {n} partes para esse termo.
                O caminho deve se referir ao termo '{term}'.
                Cada parte do caminho deve ser extremamente curta, apenas uma palavra que englobe a ideia principal de '{term}'
                e que leve em conta a descrição '{term_description}'.

                Por exemplo, se o termo for 'celulares' e sua descrição for 'Samsung Galaxy S23, Samsung Galaxy S23 Plus, Samsung Galaxy S23 Ultra',
                então a parte 1 do caminho pode ser 'celulares' e a parte 2 do caminho pode ser 'galaxy-s23'.
                Este caminho será usado na URL de um site de e-commerce para que seja exibido da seguinte forma: www.ecommerce.com/CAMINHO1/CAMINHO2.
                Exemplo: www.ecommerce.com/celulares/galaxy-s23
                A primeira parte do caminho deve ser uma categoria, por exemplo 'celulares', e a segunda parte deve ser algo mais granular
                referente ao produto, por exemplo 'galaxy-s23'.
                Estes são alguns exemplos de CAMINHOS com 2 partes: 'tenis/nike-corrida', 'televisores/samsung', 'veiculos/ford-ranger'.
                IMPORTANTE: NÃO deve conter letras maiúsculas ou espaços, se houver várias palavras, elas devem estar em minúsculas e separadas por um hífen.

                A resposta deve estar no seguinte formato:
                ["parte 1 do caminho aqui", "parte 2 do caminho aqui", ..., "parte {n} do caminho aqui"]
                A resposta deve estar exatamente no formato fornecido, sem incluir quebras de linha ou espaços desnecessários.
                Deve ser apenas uma lista de partes do caminho separadas por vírgulas e entre colchetes.
            """,
        "PATHS_WITH_TERM_DESCRIPTION": """
                Será fornecido um termo e sua descrição, e você deve gerar um caminho de URL dividido em {n} partes para esse termo.
                O caminho deve se referir ao termo '{term}' e sua descrição '{term_description}'.
                Cada parte do caminho deve ser extremamente curta, apenas uma palavra que englobe a ideia principal de '{term}'
                e que leve em conta a descrição '{term_description}'.

                Por exemplo, se o termo for 'celulares' e sua descrição for 'Samsung Galaxy S23, Samsung Galaxy S23 Plus, Samsung Galaxy S23 Ultra',
                então a parte 1 do caminho pode ser 'celulares' e a parte 2 do caminho pode ser 'galaxy-s23'.
                Este caminho será usado na URL de um site de e-commerce para que seja exibido da seguinte forma: www.ecommerce.com/CAMINHO1/CAMINHO2.
                Exemplo: www.ecommerce.com/celulares/galaxy-s23
                A primeira parte do caminho deve ser uma categoria, por exemplo 'celulares', e a segunda parte deve ser algo mais granular
                referente ao produto, por exemplo 'galaxy-s23'.
                Estes são alguns exemplos de CAMINHOS com 2 partes: 'tenis/nike-corrida', 'televisores/samsung', 'veiculos/ford-ranger'.
                IMPORTANTE: NÃO deve conter letras maiúsculas ou espaços, se houver várias palavras, elas devem estar em minúsculas e separadas por um hífen.

                A resposta deve estar no seguinte formato:
                ["parte 1 do caminho aqui", "parte 2 do caminho aqui", ..., "parte {n} do caminho aqui"]
                A resposta deve estar exatamente no formato fornecido, sem incluir quebras de linha ou espaços desnecessários.
                Deve ser apenas uma lista de partes do caminho separadas por vírgulas e entre colchetes.
            """,
    },
    "SIZE_ENFORCEMENT": """
            Encurte o seguinte anúncio de texto, ele precisa ter menos de {max_length} caracteres.
            O anúncio de texto é: {copy}

            A resposta deve estar no seguinte formato:
            texto_encurtado
            A resposta deve ser apenas o texto encurtado, sem aspas, quebras de linha ou qualquer outra coisa.
        """,
    "PATH_SIZE_ENFORCEMENT": """
            Vou fornecer uma lista de textos de caminho de exibição de Anúncios Responsivos de Pesquisa para o Google Ads que podem ser muito longos,
            de uma lista de caminhos, onde cada item é individualmente chamado de parte. O caminho deve estar no formato de
            ["parte 1 do caminho", "parte 2 do caminho"], e é possível que exista apenas uma parte ou
            que o caminho esteja vazio (o que são casos válidos).
            Verifique cada parte. Encurte a parte se ela tiver mais de {max_length} caracteres, e verifique todas as partes.
            Se uma parte não precisar ser encurtada, mantenha a mesma parte na lista.
            O texto é: {copy}
            Me dê o resultado no seguinte formato (o mesmo formato do texto):
            ["escreva a parte 1 do caminho aqui", "escreva a parte 2 do caminho aqui"]
            A resposta deve ser dada exatamente no formato que eu forneci, sem adicionar
            quebras de linha ou espaços desnecessários. Deve ser apenas uma lista de textos separados por vírgulas,
            tudo entre colchetes e nada mais.
            IMPORTANTE: NÃO deve conter letras maiúsculas ou espaços, se houver várias palavras, elas devem
            estar em minúsculas e separadas por um hífen.
        """,
    "EXTRACT_MAIN_FEATURES": """
            Dada a seguinte descrição do produto:
            '{description}'
            Gere uma lista curta das principais características. O resultado deve estar no seguinte formato:
            "Característica 1", "Característica 2", ..., "Característica N"
        """,
    "KEYWORDS_GENERATION": """
            Dado o termo '{term}', forneça uma lista de até 10 palavras-chave para o Google Ads que estejam relacionadas ao termo fornecido.
            A resposta deve estar no seguinte formato:
            ["Palavra-chave 1", "Palavra-chave 2", ..., "Palavra-chave N"]
            A resposta deve estar exatamente no formato fornecido, sem adicionar quebras de linha ou espaços desnecessários.
            Deve ser apenas uma lista de palavras-chave separadas por vírgulas e entre colchetes.
        """,
}