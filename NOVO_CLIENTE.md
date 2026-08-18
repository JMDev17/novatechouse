# Novo Cliente — Checklist Rápido

## 1. Duplicar o template
- [ ] Nunca trabalhar diretamente no `TEMPLATE_MASTER`.
- [ ] Criar uma cópia completa da pasta com o nome do novo cliente.

## 2. Alterar os dados da empresa
Editar:
- [ ] `config/site.json`
- [ ] `config/services.json`
- [ ] `config/catalog.json` (se utilizado)
- [ ] `config/areas.json`
- [ ] `config/reviews.json`
- [ ] `config/blog/posts.json`

## 3. Trocar as imagens
- [ ] `fotos/`
- [ ] Logo
- [ ] Favicon
- [ ] Imagens dos serviços
- [ ] Imagens da hero

## 4. Escrever os conteúdos SEO
- [ ] `content/services/`
- [ ] `content/areas/`
- [ ] `content/blog/`
- [ ] Demais conteúdos em `content/`

## 5. Gerar o site
```bash
python scripts/build.py
```

## 6. Validar antes da entrega
- [ ] Home abre normalmente
- [ ] Todas as páginas carregam
- [ ] WhatsApp correto
- [ ] Telefone correto
- [ ] Endereço correto
- [ ] Links internos funcionando
- [ ] Sitemap gerado
- [ ] Robots.txt correto
- [ ] Meta Title
- [ ] Meta Description
- [ ] Schema
- [ ] Responsividade
- [ ] PageSpeed
- [ ] Console sem erros

## 7. Publicação
Enviar o HTML final gerado (a pasta raiz do projeto, já com o build rodado) para a hospedagem.

---

## Boas práticas
- Nunca alterar a arquitetura do template durante um projeto de cliente.
- Sempre criar uma cópia do template para cada novo cliente.
- Melhorias estruturais devem ser feitas apenas na versão mestre (`TEMPLATE_MASTER`).
- Manter controle de versões do template (ex.: `SEO_TEMPLATE_V1`, `SEO_TEMPLATE_V2`).
- Antes de criar uma nova versão, validar a anterior em um projeto real.
