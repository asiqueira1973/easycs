# Easy CS

**Solução gratuita de Customer Success para pequenas empresas usando Salesforce.**

O Easy CS é um ponto de partida para pequenos times de Customer Success que utilizam o Salesforce como CRM. A solução foi construída de forma simples, usando recursos nativos e customizações básicas, sem depender de licenças adicionais ou pacotes pagos.

---

## 📦 O que está incluído

- Objeto de **Clientes** (Accounts)
- Objeto de **Engajamentos** relacionados ao cliente
- Objeto de **Tarefas** dentro de cada engajamento
- Telas personalizadas, layouts e abas de navegação
- Relacionamentos pré-configurados
- Layouts e exemplos de registros
- Código-fonte completo para instalação e personalização

---

## 🚀 Como instalar

Você precisa de uma **Salesforce Developer Edition** (ou sandbox) para testar ou personalizar a solução. Siga os passos:

### 1. Clone este repositório
```bash
git clone https://github.com/asiqueira1973/easycs.git
cd easycs

Faça login na sua org Salesforce

sf org login web --alias MinhaOrg

Use --set-default se quiser defini-la como org padrão.

Faça o deploy do código para a org

sf project deploy start --target-org MinhaOrg

Aguarde o deploy e, em seguida, acesse sua org para visualizar os objetos e abas criados.

📘 Manual do Usuário
Para orientações de uso e exemplos práticos, acesse o PDF abaixo:
👉 Manual do Easy CS – PDF
https://github.com/asiqueira1973/easycs/blob/main/docs/Easy%20CS%20%E2%80%93%20User%20Manual.pdf

✨ Sobre este projeto
Este projeto é uma iniciativa pessoal com o objetivo de contribuir com a comunidade Salesforce, oferecendo uma base simples e reutilizável para operações de Customer Success.
Não há custos


Código aberto (MIT License)


Pode ser instalado, adaptado e evoluído livremente



🤝 Contribuindo
Fique à vontade para:
Criar um fork


Propor melhorias


Adaptar a estrutura para outras áreas (ex: Suporte, Projetos, Implantação)



📄 Licença
MIT License. Veja o arquivo LICENSE para mais detalhes.
