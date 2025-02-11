# 📸 Image Metadata Explorer

[English Ver.](./README_en.md)

Este projeto permite analisar metadados de imagens, extraindo informações como localização GPS, data e hora da captura, além de exibir mapas e previsões do tempo para o local onde a foto foi tirada.

## 🚀 Funcionalidades
- Upload de imagens e extração automática de metadados EXIF
- Obtenção de coordenadas GPS da imagem (se disponíveis)
- Exibição da localização em um mapa interativo
- Consulta de endereço com base nas coordenadas usando a API OpenCage
- Exibição da previsão do tempo para o local da imagem

## 🛠 Tecnologias Utilizadas
- **Python**
- **Streamlit** (interface interativa)
- **Folium** (exibição de mapas)
- **OpenCage API** (conversão de coordenadas em endereços)
- **OpenWeather API** (previsão do tempo)
- **Pillow (Exif)** (leitura de metadados de imagens)

## 📦 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/elara-mendes/exif-tool.git
cd exif-tool
```

2. Criação do ambiente virtual:

### Usando venv (Opcional)
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

### Usando Conda (Recomendado)
```bash
conda create --name meu_ambiente python=3.11
conda activate meu_ambiente
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## ▶️ Como Usar

1. Execute o programa:
```bash
streamlit run main.py
```
2. Faça o upload de uma imagem e visualize as informações extraídas!

Entendido! Aqui está a versão atualizada do README, mencionando que a chave da API do OpenWeather está no arquivo `getWeather.py` dentro da pasta `Functions`:

---

## 🔑 Configuração de APIs
Antes de rodar o projeto, configure suas **chaves de API** nas variáveis abaixo:

1. **Obter chave da API**:
   - **OpenWeather**: Obtenha uma chave em [https://openweathermap.org/](https://openweathermap.org/)
   - **OpenCage**: Obtenha uma chave em [https://opencagedata.com/](https://opencagedata.com/)

2. **Adicionar a chave no código**:
   As chaves de API estão localizadas em arquivos separados no seu projeto.

   - **OpenWeather API**: Abra o arquivo `Functions/getWeather.py` e substitua a variável `OPENWEATHER_API_KEY` pela sua chave de API:
   
     ```python
     OPENWEATHER_API_KEY = "YOUR_API_KEY_HERE"
     ```

   - **OpenCage API**: Abra o arquivo `main.py` e substitua a variável `OPENCAGE_API_KEY` pela sua chave de API:
   
     ```python
     OPENCAGE_API_KEY = "YOUR_API_KEY_HERE"
     ```

   Substitua `"YOUR_API_KEY_HERE"` pela chave que você obteve para cada API.

Com isso, o programa estará pronto para obter as informações necessárias sobre o clima e o endereço da localização das imagens.

## 🤝 Colaboradores
- [@stevopablo](https://github.com/stevopablo)

## 📜 Licença
Este projeto está sob a licença MIT. Sinta-se à vontade para contribuir! 😊