# deepseek-r1-chatbot-speech-azure

Este projeto integra o modelo de linguagem **DeepSeek-R1** da **Azure AI** com o serviço de síntese de fala **Azure Speech**. O objetivo é criar um assistente virtual que interage com o usuário em português brasileiro, respondendo a perguntas por meio de texto e voz.

## Tecnologias Utilizadas

- **Azure AI Foundry**: Para interações de processamento de linguagem natural.
- **Azure Speech**: Para conversão de texto em fala.
- **Python**: Linguagem de programação utilizada para o desenvolvimento do script.

## Funcionalidades

- **Interação com o modelo de linguagem**: O modelo **DeepSeek-R1** gera respostas com base nas entradas do usuário.
- **Síntese de fala**: A resposta gerada é convertida em fala utilizando o **Azure Speech**, com uma voz natural e clara em português brasileiro.
- **Limpeza de texto**: O texto gerado pela IA é limpo para remoção de emojis e ênfases em negrito (asteriscos).
- **Pensamentos pausados**: Se o modelo contiver uma pausa de pensamento (representada pela tag `<think>...</think>`), a resposta será falada após o término do pensamento.

## Configuração

Antes de rodar o código, você precisa configurar as chaves de API para o Azure. Substitua os seguintes valores no código pelo seu próprio:

- `ENDPOINT`: O ponto final do seu serviço de IA no Azure.
- `API_KEY`: A chave da API para autenticação no Azure AI.
- `speech_key`: A chave para autenticação no Azure Speech.
- `region`: A região do serviço **Azure Speech**.

### Exemplo de Configuração

```python
# Configurações do Azure AI Foundry
ENDPOINT = "SEU-ENDPOINT-DO-MODELO"
API_KEY = "SUA_API_KEY_AQUI"

# Configurações do Azure Speech para síntese de fala
speech_key = "SUA_SPEECH_KEY_AQUI"
region = "sua-regiao-aqui"
```

## Como Executar

Instale as depedências necessárias:

```
pip install azure-ai-inference azure-cognitiveservices-speech
```

Substitua as variáveis de configuração com suas credenciais do Azure no código.

Execute o script:
```
python app.py
```
Interaja com o assistente virtual digitando suas perguntas. O assistente responderá e falará as respostas em voz alta.

## Exemplos de uso:

```
🔹 Chat com DeepSeek-R1 iniciado! Digite 'sair' para encerrar.
Você: Como você está?
🤖 DeepSeek-R1: Estou bem, obrigado por perguntar!
🎤 Resposta falada com sucesso!

```

## Encerrando:

Digite ```sair```, ```exit``` ou ```quit``` para terminar a sessão.

## Contribuições

Sinta-se à vontade para contribuir com melhorias no código ou criar novas funcionalidades. Envie um pull request ou abra uma issue para discutir suas ideias.

## Licença
Este projeto está licenciado sob a MIT License.




