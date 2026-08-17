# Template White-Label — Documentação

Este projeto é um **gerador de site estático** reutilizável para qualquer negócio. Você edita arquivos de configuração (JSON) e conteúdo (HTML), roda um script Python, e ele gera o site final em HTML + CSS + JS puro — sem frameworks, sem Tailwind, sem dependências de build em produção.

O site gerado funciona como qualquer site estático: basta subir a pasta raiz (com `index.html`, `style.css`, `script.js` e as pastas de páginas) para qualquer hospedagem.

---

## 1. Visão geral da arquitetura

```
config/          → dados do negócio (JSON): identidade, contato, cores, serviços, produtos, bairros, avaliações, blog
content/         → textos longos de cada página (HTML), um arquivo por serviço/produto/bairro/post
templates/       → estrutura HTML compartilhada (navbar, rodapé, layout de cada tipo de página)
scripts/
  templating.py  → motor de templates (sem dependências) — sintaxe {{variavel}}, {{#each lista}}, {{#if condição}}
  build.py       → lê config/ + content/ + templates/, gera o HTML final
fotos/           → imagens locais (as que não vêm do Unsplash)
script.js        → JS puro do site (animações GSAP, menus, carrosséis)
style.css        → CSS final gerado pelo build (não edite direto — veja seção 4)

index.html, servicos/, produtos/, areas/, blog/, sitemap.xml
                 → SAÍDA gerada pelo build.py. Não edite esses arquivos direto:
                   qualquer edição manual é perdida no próximo build.
```

**Regra de ouro:** tudo que aparece no site final vem de `config/` + `content/` + `templates/`. Os arquivos de saída (`index.html`, `servicos/*/index.html`, `produtos/*/index.html`, `areas/*/index.html`, `blog/*/index.html`, `style.css`, `sitemap.xml`) são sempre **regenerados do zero** a cada build.

### Módulos do site

O site é dividido em módulos, cada um pode ser ligado/desligado em `config/site.json → modules`:

| Módulo | O que é | Chave em `modules` |
|---|---|---|
| Serviços | Página inicial + páginas individuais de cada serviço | `services` |
| Produtos/Catálogo | Carrossel de produtos + página individual de cada um | `catalog` |
| Áreas Atendidas | Páginas de bairros/regiões atendidas (SEO local) | `areas` |
| Blog | Índice + posts | `blog` |
| Avaliações | Carrossel de depoimentos na home | `reviews` |

Desligar um módulo (`false`) remove suas páginas, links de menu e seção da home automaticamente no próximo build.

---

## 2. Como gerar o HTML final

```bash
python scripts/build.py
```

Isso regenera **todas** as páginas, `style.css` e `sitemap.xml` a partir do estado atual de `config/` e `content/`. Rode sempre que editar qualquer arquivo dessas duas pastas.

Não precisa de `npm install`, Node, ou qualquer dependência — só Python 3 padrão.

---

## 3. O que editar para um novo cliente

### 3.1 Identidade, contato, redes sociais — `config/site.json`

```jsonc
"business": {
  "name": "...",          // nome do negócio
  "name_upper": "...",    // nome em caixa alta (logo/navbar)
  "industry": "...",      // usado no título da hero da home
  "tagline": "...",       // sufixo do <title> da home
  "description": "...",   // meta description da home + parágrafo da hero
  "city": "...",
  "region_label": "...",  // ex: "Cidade e região" (textos genéricos de cobertura)
  "copyright_year": "..."
},
"contact": {
  "phone_display": "...",       // telefone formatado (exibido)
  "whatsapp_number": "...",     // só dígitos, com DDI (ex: 5511999999999)
  "address": { "street", "neighborhood", "city", "state", "zip", "line1/2/3", "footer_line" },
  "hours_highlight": "...",     // ex: "Atendimento 24h"
  "hours_detail": "...",
  "maps_query": "...",          // usado no link "Ver no Google Maps"
  "maps_embed_src": "..."       // URL do iframe do Google Maps (Google Maps → Compartilhar → Incorporar mapa)
},
"social": {
  "instagram_handle", "instagram_url", "facebook_handle", "facebook_url"
}
```

Esses valores alimentam **todas** as páginas automaticamente (navbar, rodapé, botões de WhatsApp, seção de contato da home).

### 3.2 Cores — `config/site.json → branding.colors`

```jsonc
"colors": {
  "primary": "#050505",           // fundo geral do site
  "accent": "#E63B2E",            // cor de destaque (botões, links, ícones)
  "accent_hover": "#ff5f53",       // cor do destaque no hover
  "surface": "#0D0D12",            // fundo de cards/painéis
  "surface_hover": "#16161A",
  "text_main": "#ffffff",          // texto principal
  "text_muted": "#a1a1aa"          // texto secundário
}
```

Troque só os valores hex — os campos `*_rgb` e `*_rgb_sp` (mesma cor em formato "R, G, B" e "R G B") são recalculados manualmente também; **se mudar uma cor, atualize o hex e os dois campos rgb correspondentes** para manter gradientes e sombras consistentes. Rode o build depois — todas as páginas, botões, hovers e sombras usam essas variáveis automaticamente.

Logo: `branding.logo.icon` é o nome de um ícone [Lucide](https://lucide.dev/icons) usado como logo (ex: `"cpu"`). Se quiser uma imagem de logo real em vez de ícone, isso exige editar os templates de navbar/rodapé (veja seção 5).

Favicon: `branding.favicon` aponta para o caminho do arquivo (ex: `/favicon.ico`) — copie seu arquivo de favicon para a raiz do projeto com esse nome.

### 3.3 Serviços — `config/services.json` + `content/services/*.html`

Cada item da lista em `services.json` é um serviço, com:
- `slug` → define a URL (`/servicos/{slug}/`) e o nome do arquivo de conteúdo esperado em `content/services/{slug}.html`
- `nav_label`, `card_title`, `footer_label` → nomes usados no menu, no card da home e no rodapé (podem ser diferentes entre si)
- `card_category` → selo pequeno no card da home (ex: "Apple", "Laboratório")
- `nav_order`, `card_order`, `footer_order` → controla a ordem em cada lugar
- `footer_group` → `"col1"`, `"col2"` ou `null` (define em qual coluna do rodapé aparece, ou se não aparece)
- `show_in_compact_mobile_menu` → `true`/`false` (aparece no menu mobile resumido das páginas de "Áreas Atendidas")
- `image` → `{"type":"unsplash","id":"...","alt":"..."}` (foto do Unsplash) ou `{"type":"local","type_is_local":true,"avif":"fotos/x.avif","fallback":"fotos/x.png","alt":"..."}` (foto local)
- `meta_title`, `meta_description` → SEO da página do serviço
- `footer_blurb` → texto curto no rodapé dessa página

**Para adicionar um serviço novo:** adicione um item em `services.json` e crie `content/services/{slug}.html` com o corpo da página (copie um arquivo existente como ponto de partida e reescreva o texto).

**Para remover um serviço:** apague o item de `services.json` (o arquivo de conteúdo pode ficar, só não será usado).

### 3.4 Produtos/Catálogo — `config/catalog.json` + `content/catalog/*.html`

Mesma lógica dos serviços. Campos principais:
- `slug`, `name`, `tagline`, `image` (URL da imagem do produto)
- `badge` → selo tipo "Top de Linha" (ou `null`)
- `highlighted` → `true` deixa o card em destaque no carrossel (borda colorida)
- `cta_label` → texto do botão (ex: "Ver Estoque", "Consultar")
- `whatsapp_message` → mensagem pré-preenchida do WhatsApp ao clicar
- `nav_order` → ordem no menu dropdown

### 3.5 Áreas Atendidas / bairros — `config/areas.json` + `content/areas/**/*.html`

Estrutura de duas camadas — **região** (cidade) e **bairro**:

```jsonc
[
  {
    "slug": "cidade-a", "name": "Cidade A",
    "meta_title": "...", "meta_description": "...",
    "neighborhoods": [
      { "slug": "centro", "name": "Centro", "meta_title": "...", "meta_description": "..." },
      ...
    ]
  }
]
```

Arquivos de conteúdo esperados:
- `content/areas/index.html` → texto da página geral "Áreas Atendidas" (`config/areas_hub_meta.json` tem o `meta_title`/`meta_description` dela)
- `content/areas/{regiao}/index.html` → texto da página da região/cidade
- `content/areas/{regiao}/{bairro}.html` → texto de cada bairro

**Para adicionar uma cidade ou bairro novo:** adicione a entrada em `areas.json` e crie o(s) arquivo(s) de conteúdo correspondente(s).

### 3.6 Avaliações — `config/reviews.json`

Lista simples: `{"initial": "C", "name": "...", "text": "..."}`. Adicione, remova ou reordene itens livremente.

### 3.7 Blog — `config/blog/*.json` + `content/blog/*.html`

- `config/blog/posts.json` → um item por post, com `slug`, `title`, `headline`, `category`/`category_label`, datas, imagens (`image_avif`/`image_fallback` em 3 variantes de profundidade de pasta), `excerpt`, `meta_description`, `og_image`, `data_categorias` (tags usadas no filtro), `data_search` (texto usado na busca do blog).
- `config/blog/categories.json` → categorias do filtro do blog (`{"tag": "...", "label": "..."}`). O botão "Todos" é automático.
- `config/blog/index_meta.json` → `meta_title`/`meta_description` da página `/blog/`.
- `content/blog/{slug}.html` → corpo do artigo.

**Para publicar um post novo:** adicione a entrada em `posts.json`, crie `content/blog/{slug}.html`, e garanta que as tags em `data_categorias` existam em `categories.json` (ou adicione uma categoria nova lá).

### 3.8 Imagens

- Fotos hospedadas no Unsplash: use o `id` da foto (a parte depois de `/photo-` na URL do Unsplash) nos campos `image`/`hero_image_id`/etc.
- Fotos locais: coloque o arquivo em `fotos/`. Prefira gerar uma versão `.avif` (menor) com fallback `.jpeg`/`.png` — veja `convert_to_avif.py` como referência de como isso foi feito para as fotos existentes.
- Imagens da home (hero e seção "Diferenciais"): `config/site.json → media`.

### 3.9 SEO

- **Domínio**: `config/site.json → seo.domain` e `seo.base_url` — usado para gerar as URLs absolutas do `sitemap.xml`.
- **Título/descrição por página**: cada módulo tem seus próprios campos `meta_title`/`meta_description` (veja seções 3.3 a 3.7).
- **Sitemap**: `sitemap.xml` é 100% gerado pelo build a partir das páginas ativas — nunca precisa editar à mão.
- **Favicon**: veja seção 3.2.

### 3.10 URLs e rótulos de menu

`config/site.json`:
```jsonc
"url_slugs": { "services": "servicos", "catalog": "produtos", "areas": "areas", "blog": "blog" },
"labels": {
  "catalog_nav": "Produtos",         // texto do menu para o módulo de catálogo
  "areas_nav": "Áreas Atendidas",
  "differentiators_nav": "Diferenciais",
  "header_cta": "Fale Conosco",       // botão principal do cabeçalho
  "footer_services_col1": "Serviços", // título das colunas de serviço no rodapé
  "footer_services_col2": "Mais Opções"
}
```

Trocar `url_slugs` muda o caminho das URLs (ex.: `produtos` → `catalogo`); o build cria as pastas novas automaticamente — só é preciso apagar as pastas antigas manualmente se o nome mudar (elas não se autodeletam).

---

## 4. Sobre o `style.css`

`style.css` é **gerado automaticamente** a partir de `templates/partials/style.css.tmpl` a cada build. Ele contém:
1. Um reset básico de navegador (equivalente ao Preflight do Tailwind, mas em CSS puro).
2. Classes semânticas reutilizáveis (`.btn-cta-lg`, `.card`, `.dropdown-link`, `.icon-4`, etc.) que substituem o que antes eram classes utilitárias do Tailwind.
3. Os componentes visuais originais do site (glass-panel, hero, cards, animações).

**Não edite `style.css` diretamente** — edite `templates/partials/style.css.tmpl` (que usa `{{colors.X}}` para puxar as cores de `config/site.json`) e rode o build.

O site **não usa mais Tailwind**: sem CDN, sem `tailwind.config`, sem dependência de build externo. É HTML + CSS + JS puro.

---

## 5. Mexendo na estrutura (avançado)

Isso normalmente **não é necessário** para atender um novo cliente — só se quiser mudar o layout, adicionar uma seção nova, ou mudar como uma página é montada.

- `templates/partials/` → navbar (3 variantes: home, páginas internas, páginas de área), rodapé (2 variantes), menu mobile, botão flutuante do WhatsApp.
- `templates/pages/` → estrutura de cada tipo de página (home, serviço, produto, blog, área).
- `scripts/build.py` → orquestra tudo: lê os JSON, monta o contexto de cada página, chama o motor de templates, escreve os arquivos finais.
- `scripts/templating.py` → motor de templates próprio (sem dependência), sintaxe:
  - `{{variavel}}` / `{{objeto.campo}}`
  - `{{#each lista}} ... {{/each}}` (dentro do loop, os campos do item viram variáveis diretas)
  - `{{#if condição}} ... {{else}} ... {{/if}}`

---

## 6. Limitações conhecidas

- A conversão de Tailwind para CSS puro foi feita a partir dos valores reais compilados pelo Tailwind (não "adivinhados"), mas **não há navegador neste ambiente para conferência visual pixel a pixel** — recomendável abrir o site localmente e navegar antes de publicar para um cliente novo.
- Os textos longos em `content/**/*.html` ainda contêm exemplos de redação (do negócio original que deu origem a este template) — são o conteúdo "de exemplo" que deve ser reescrito por cliente/nicho.
