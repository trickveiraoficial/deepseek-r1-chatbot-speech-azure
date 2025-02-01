import os
import re
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.inference.models import SystemMessage, UserMessage
import azure.cognitiveservices.speech as speechsdk

# Configurações do Azure AI Foundry
ENDPOINT = "ENDPOINT-HERE"
API_KEY = "API-KEY-HERE"

# Configurações do Azure Speech para síntese de fala
speech_key = "SPEECH-KEY-HERE"
region = "REGION-HERE"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=region)
speech_config.speech_synthesis_voice_name = "pt-BR-LeilaNeural" # Você pode alterar a voz aqui


# Criar cliente do Azure AI
client = ChatCompletionsClient(
    endpoint=ENDPOINT,
    credential=AzureKeyCredential(API_KEY),
)

# Histórico de mensagens
messages = [
    SystemMessage(content="Você é uma assistente útil. Responda em português-brasileiro"),
]

print("🔹 Chat com DeepSeek-R1 iniciado! Digite 'sair' para encerrar.")

# Criar o sintetizador de fala
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

# Função para remover emojis e substituir asteriscos por ênfase
def clean_text_for_speech(text):
    # Remover emojis
    emoji_pattern = re.compile(
        "[\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F700-\U0001F77F"
        "\U0001F780-\U0001F7FF"
        "\U0001F800-\U0001F8FF"
        "\U0001F900-\U0001F9FF"
        "\U0001FA00-\U0001FA6F"
        "\U0001FA70-\U0001FAFF"
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    
    # Silenciar ênfases
    text = re.sub(r'\*(.*?)\*', r'\1', text)  # "silencio" ao invés de asteriscos ou ênfase
    
    # Remover emojis
    text = emoji_pattern.sub(r'', text)
    
    return text

while True:
    # Solicita a entrada do usuário
    user_input = input("\nVocê: ")
    
    # Se o usuário quiser sair
    if user_input.lower() in ["sair", "exit", "quit"]:
        print("👋 Encerrando o chat. Até mais!")
        break
    
    # Adiciona a entrada do usuário ao histórico
    messages.append(UserMessage(content=user_input))

    # Envia a requisição ao modelo
    response = client.complete(
        messages=messages,
        model="DeepSeek-R1"
    )

    # Obtém a resposta do modelo
    assistant_response = response.choices[0].message.content

    # Exibe a resposta no console
    print(f"\n🤖 DeepSeek-R1: {assistant_response}")

    # Se o conteúdo contiver <think>... </think>, não falar até o fim do pensamento
    if "<think>" in assistant_response and "</think>" in assistant_response:
        # Se houver conteúdo após </think>, vamos extrair e falar isso
        after_think_content = assistant_response.split("</think>", 1)[-1].strip()

        # Limpar o conteúdo de emojis e caracteres indesejados
        after_think_content = clean_text_for_speech(after_think_content)

        # Se houver conteúdo após a tag </think>, falar
        if after_think_content:
            try:
                result = speech_synthesizer.speak_text_async(after_think_content).get()
                if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                    print("🎤 Resposta falada com sucesso após o pensamento!")
                else:
                    print(f"Erro ao sintetizar fala: {result.reason}")
                    if result.error_details:
                        print(f"Detalhes do erro: {result.error_details}")
            except Exception as e:
                print(f"Erro ao chamar o serviço de síntese de fala: {str(e)}")
    else:
        # Caso contrário, falar a resposta normalmente
        # Limpar o conteúdo de emojis e caracteres indesejados
        assistant_response = clean_text_for_speech(assistant_response)

        try:
            result = speech_synthesizer.speak_text_async(assistant_response).get()
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                print("🎤 Resposta falada com sucesso!")
            else:
                print(f"Erro ao sintetizar fala: {result.reason}")
                if result.error_details:
                    print(f"Detalhes do erro: {result.error_details}")
        except Exception as e:
            print(f"Erro ao chamar o serviço de síntese de fala: {str(e)}")

    # Adiciona a resposta ao histórico para manter o contexto
    messages.append(response.choices[0].message)
