# Easy CS

Estrutura simples de Customer Success para pequenas empresas que usam o Salesforce, feita só com recursos nativos da plataforma, sem licenças adicionais nem pacotes pagos.

## Principais funcionalidades

- Clientes (Account) com layout e página de registro próprios para CS.
- Engajamentos (`Engagement__c`) ligados ao cliente: data, tipo (Meeting, Training, Onboarding, QBR, Incident Support, Other), status e notas.
- Tarefas de CS (`CS_Task__c`) dentro de cada engajamento: tipo, prioridade, status, prazo e notas.
- Time do engajamento (`Engagement_Team__c`) e time da conta (`AccountTeamMember__c`, com papéis como CSM, TAM, Sales, Executive Sponsor).
- Página inicial "Easy CS", abas, páginas Lightning e layouts de registro.
- Permission set `Easy_CS_Full_Access`.
- Manual do usuário em PDF: [`docs/Easy CS – User Manual.pdf`](docs/Easy%20CS%20%E2%80%93%20User%20Manual.pdf).

## Stack técnica

- Salesforce Platform: objetos e campos customizados, páginas Lightning (FlexiPages), layouts, abas e permission sets
- Salesforce DX (projeto `sfdx-project.json`, API 59.0) e Salesforce CLI (`sf`) para deploy
- Ferramentas de desenvolvimento do template Salesforce DX: ESLint, Prettier (com plugins Apex e XML), Husky + lint-staged e Jest para LWC

## Como foi construído

Projeto Salesforce DX montado a partir do template padrão do Salesforce CLI, com os metadados da org versionados em `force-app/`. Este repositório não tem especificação SDD (spec.md) nem arquivos de configuração do Claude.

- Hook de pre-commit (Husky + lint-staged) que formata os arquivos com Prettier e roda o ESLint nos componentes Aura/LWC.
- Não há testes automatizados: o Jest para LWC está configurado, mas o projeto não tem componentes LWC nem classes Apex.

## Status

Em desenvolvimento.

## Licença

O código está disponível apenas para leitura e estudo. Veja [LICENSE](LICENSE).

## Contribuições

Issues são bem-vindas; pull requests não são aceitos. Veja [CONTRIBUTING.md](CONTRIBUTING.md).

## Como rodar

Você precisa de uma Salesforce Developer Edition (ou sandbox) e do [Salesforce CLI](https://developer.salesforce.com/tools/salesforcecli).

```bash
git clone https://github.com/asiqueira1973/easycs.git
cd easycs
sf org login web --alias MinhaOrg          # use --set-default para defini-la como org padrão
sf project deploy start --target-org MinhaOrg
```

Depois do deploy, acesse a org para ver os objetos e abas criados.

---

Feito pela [Dab Lab](https://www.dablab.com.br/) — product studio de software e IA que constrói apps para pequenas empresas, startups e áreas dentro de grandes empresas, partindo de uma especificação (Spec-Driven Development) e com as disciplinas de engenharia de software robusta.
