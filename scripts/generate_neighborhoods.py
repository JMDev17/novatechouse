#!/usr/bin/env python3
"""Script to generate unique, rich neighborhood HTML files for Volta Redonda and Resende."""

from pathlib import Path

ROOT = Path(__file__).parent.parent
CONTENT_AREAS = ROOT / "content" / "areas"

# Volta Redonda Neighborhoods (20)
VR_NEIGHBORHOODS = [
    ("vila-santa-cecilia", "Vila Santa Cecília", "bairro-sede", "notebooks e computadores de alta performance", "upgrade-de-ssd", "conserto-de-notebook"),
    ("aterrado", "Aterrado", "bairro comercial vizinho à Vila Santa Cecília", "atendimento a escritórios, comércios e residentes", "formatacao", "conserto-de-computador"),
    ("retiro", "Retiro", "um dos maiores polos habitacionais de Volta Redonda", "soluções rápidas para computadores lentos e notebooks com defeito", "limpeza-interna", "upgrade-de-ssd"),
    ("jardim-amalia", "Jardim Amália", "região residencial tradicional de fácil acesso", "manutenção de notebooks escolares e computadores de trabalho", "troca-de-pasta-termica", "instalacao-do-windows"),
    ("jardim-belvedere", "Jardim Belvedere", "bairro residencial de ritmo intenso de home office", "otimização de PCs e upgrades de memória para alta produtividade", "upgrade-de-memoria-ram", "otimizacao-de-computador"),
    ("laranjal", "Laranjal", "bairro central próximo ao polo comercial da Vila", "conserto ágil de notebooks com falhas na carcaça ou tela", "conserto-de-notebook", "reparo-de-placa-mae"),
    ("sao-joao", "São João", "região bem conectada às vias principais da cidade", "recuperação de sistema e remoção de vírus para PCs domésticos", "remocao-de-virus", "formatacao"),
    ("sessenta", "Sessenta", "bairro vizinho à Vila Santa Cecília", "atendimento ágil a poucos minutos de distância da nossa loja física", "conserto-de-computador", "limpeza-interna"),
    ("agua-limpa", "Água Limpa", "bairro populoso com grande demanda por manutenção de notebooks", "reparos de hardware e substituição de discos danificados", "troca-de-hd", "recuperacao-de-dados"),
    ("voldac", "Voldac", "região residencial com fácil acesso ao centro da cidade", "backup preventivo de arquivos e formatação com preservação de dados", "backup", "instalacao-de-drivers"),
    ("conforto", "Conforto", "bairro tradicional vizinho ao setor comercial", "manutenção preventiva para notebooks corporativos e de estudos", "manutencao-preventiva", "limpeza-interna"),
    ("niteroi", "Niterói", "bairro populoso de Volta Redonda", "diagnóstico de placas-mãe em curto e computadores que não ligam", "reparo-de-placa-mae", "conserto-de-notebook"),
    ("santo-agostinho", "Santo Agostinho", "região residencial com uso constante de computadores", "troca de HD por SSD e otimização para navegação rápida", "upgrade-de-ssd", "formatacao"),
    ("santa-cruz", "Santa Cruz", "bairro dinâmico de Volta Redonda", "remoto suporte de orientação e substituição de memórias RAM", "upgrade-de-memoria-ram", "conserto-de-computador"),
    ("roma", "Roma", "extensa área residencial de Volta Redonda", "manutenção de notebooks com superaquecimento e ruído de ventoinhas", "troca-de-pasta-termica", "limpeza-interna"),
    ("ponte-alta", "Ponte Alta", "bairro residencial com fácil deslocamento", "recuperação de arquivos importantes e cópias de segurança", "recuperacao-de-dados", "backup"),
    ("sao-geraldo", "São Geraldo", "bairro tradicional com demanda por serviços de informática", "instalação e configuração de sistemas operacionais atualizados", "instalacao-do-windows", "instalacao-de-drivers"),
    ("vila-mury", "Vila Mury", "região bem localizada com acesso rápido à Vila Santa Cecília", "otimização de notebooks antigos para trabalho diário", "otimizacao-de-computador", "upgrade-de-ssd"),
    ("jardim-paraiba", "Jardim Paraíba", "bairro próximo a clubes e áreas comerciais centrais", "conserto estrutural de carcaças e telas de notebooks", "conserto-de-notebook", "manutencao-preventiva"),
    ("monte-castelo", "Monte Castelo", "bairro residencial com ótimo acesso", "manutenção de fontes de alimentação e placas de computadores de mesa", "conserto-de-computador", "reparo-de-placa-mae"),
]

# Resende Neighborhoods (15) - Region served only
RESENDE_NEIGHBORHOODS = [
    ("centro", "Centro", "polo histórico e comercial de Resende", "atendimento de informática focado em empresas e moradores da área central", "conserto-de-notebook", "upgrade-de-ssd"),
    ("campos-eliseos", "Campos Elíseos", "principal centro comercial e financeiro de Resende", "suporte para manutenção de computadores de trabalho e notebooks corporativos", "formatacao", "conserto-de-computador"),
    ("manejo", "Manejo", "bairro movimentado e residencial de Resende", "soluções para notebooks superaquecendo ou travando durante o uso", "limpeza-interna", "troca-de-pasta-termica"),
    ("jardim-jalisco", "Jardim Jalisco", "região nobre e residencial de Resende", "otimização de PCs de alta exigência e upgrades de velocidade com SSD", "upgrade-de-ssd", "otimizacao-de-computador"),
    ("liberdade", "Liberdade", "bairro tradicional da cidade de Resende", "recuperação de sistemas com erro ao iniciar o Windows e reinstalações", "instalacao-do-windows", "formatacao"),
    ("paraiso", "Paraíso", "área residencial com expressivo número de usuários de notebooks", "remoção de vírus e proteção de dados sensíveis", "remocao-de-virus", "backup"),
    ("morada-da-colina", "Morada da Colina", "bairro residencial de ritmo tranquilo em Resende", "expansão de memória RAM para notebooks e computadores de estudos", "upgrade-de-memoria-ram", "conserto-de-notebook"),
    ("jardim-brasilia", "Jardim Brasília", "bairro residencial próximo a vias de acesso", "troca de discos rígidos danificados e prevenção de perda de dados", "troca-de-hd", "recuperacao-de-dados"),
    ("cidade-alegria", "Cidade Alegria", "um dos maiores bairros de Resende", "atendimento técnico especializado em reparo eletrônico de placas-mãe", "reparo-de-placa-mae", "conserto-de-computador"),
    ("itapuca", "Itapuca", "bairro residencial de Resende", "manutenção preventiva completa para aumentar a durabilidade do notebook", "manutencao-preventiva", "limpeza-interna"),
    ("toyota", "Toyota", "região residencial com forte presença de famílias e estudantes", "instalação correta de drivers e solução de conflitos de periféricos", "instalacao-de-drivers", "formatacao"),
    ("cabral", "Cabral", "bairro tradicional com comércios locais", "recuperação de arquivos deletados ou partições inacessíveis", "recuperacao-de-dados", "backup"),
    ("alvorada", "Alvorada", "área residencial de Resende", "upgrade de performance para acelerar inicialização do Windows em PCs antigos", "upgrade-de-ssd", "otimizacao-de-computador"),
    ("monet", "Monet", "bairro residencial moderno em Resende", "substituição de pasta térmica ressecada e desobstrução de coolers", "troca-de-pasta-termica", "limpeza-interna"),
    ("jardim-primavera", "Jardim Primavera", "região residencial bem localizada", "conserto de notebooks que não ligam ou apresentam problemas de imagem", "conserto-de-notebook", "reparo-de-placa-mae"),
]

def render_vr_neighborhood(slug, name, context_desc, main_focus, primary_service, secondary_service):
    is_sede = (slug == "vila-santa-cecilia")
    sede_text = "onde está localizada a nossa sede física na Rua 16, 109 - Sala 8" if is_sede else "com acesso direto à nossa sede física na Vila Santa Cecília (Rua 16, 109 - Sala 8)"
    
    return f"""<!-- HEADER SEO -->
<section class="relative-19 hero-bg">
<div class="flex-col-center-5 flex">
<h1 class="heading-5xl-3">
Assistência Técnica para {name} em Volta Redonda
</h1>
<p class="text-lg-muted">
Conserto de notebooks e computadores para moradores e empresas do bairro {name} em Volta Redonda - RJ. Atendimento técnico especializado.
</p>
</div>
</section>

<!-- CONTENT -->
<section class="relative-25">
<div class="maxw4xl-mdpx12-2">

<div class="mb16">
<h2 class="heading-3xl-7">Manutenção de computadores e notebooks para o bairro {name}</h2>
<p class="text-lg-muted-3">
Se você está no bairro {name}, em Volta Redonda, conta com a proximidade da <strong>Nova Techouse</strong>, {sede_text}.
</p>
<p class="text-lg-muted-3">
Nossa equipe é especializada em resolver problemas de hardware e software, focando em {main_focus}. Atendemos desde situações de travamento constante e superaquecimento até computadores que não ligam.
</p>
<p class="text-lg-muted-4">
Realizamos diagnósticos transparentes e manutenções eficientes para garantir que seu equipamento volte a funcionar com velocidade e estabilidade.
</p>
</div>

<div class="mb16">
<h2 class="heading-3xl-7">Serviços mais procurados por moradores do {name}</h2>
<p class="text-lg-muted-3">
Oferecemos soluções completas para notebooks e computadores de mesa. Entre as principais especialidades solicitadas por clientes da região destacam-se:
</p>
<ul class="text-base-muted-3 space-y-2 mb6">
<li>• <strong>Conserto de Notebook:</strong> Reparo de telas, dobradiças da carcaça, teclados e circuitos elétricos.</li>
<li>• <strong>Conserto de Computador:</strong> Diagnóstico de fontes de alimentação, placas de vídeo e placas-mãe.</li>
<li>• <strong>Upgrade de SSD & RAM:</strong> Instalação de armazenamento ultra-rápido e ampliação de memória.</li>
<li>• <strong>Formatação com Backup:</strong> Restauração limpa do sistema com proteção total aos seus arquivos.</li>
<li>• <strong>Limpeza Interna & Pasta Térmica:</strong> Higienização completa para evitar desligamentos por calor.</li>
</ul>
</div>

<div class="mb16">
<h2 class="heading-3xl-7">Por que escolher a Nova Techouse em Volta Redonda?</h2>
<p class="text-lg-muted-3">
Nossa localização estratégica na Vila Santa Cecília facilita a entrega e retirada de equipamentos para quem reside ou trabalha no {name}.
</p>
<p class="text-lg-muted-4">
Trabalhamos com agilidade e compromisso técnico para que você não fique parado por falhas no computador.
</p>
</div>

<div class="flex flex mt8 mb8">
<a href="/{{{{url_slugs.areas}}}}/volta-redonda/" class="text-sm-7">Voltar para Bairros de Volta Redonda</a>
<span class="textwhite20">|</span>
<a href="/{{{{url_slugs.areas}}}}/" class="text-sm-7">Regiões Atendidas</a>
</div>

</div>
</section>

<!-- CTA FINAL -->
<section class="relative-28 hero-bg">
<div class="maxw3xl">
<h2 class="heading-4xl-2">Precisa de assistência técnica no {name}?</h2>
<p class="text-lg-muted-5">Fale com a Nova Techouse no WhatsApp e traga seu equipamento para avaliação em Volta Redonda.</p>
<div class="flex-col-center-6 flex">
<a href="https://wa.me/{{{{contact.whatsapp_number}}}}?text=Olá! Vim pelo site da Nova Techouse. Moro no bairro {name} em Volta Redonda e preciso de assistência técnica." class="btn-cta-lg magnetic-btn flex">
<i data-lucide="message-square" class="icon-4"></i> Falar no WhatsApp
</a>
<a href="https://maps.google.com/?q={{{{contact.maps_query}}}}" target="_blank" class="btn-outline-10 magnetic-btn flex">
<i data-lucide="map-pin" class="icon-4"></i> Ver localização da loja
</a>
</div>
</div>
</section>
"""

def render_resende_neighborhood(slug, name, context_desc, main_focus, primary_service, secondary_service):
    return f"""<!-- HEADER SEO -->
<section class="relative-19 hero-bg">
<div class="flex-col-center-5 flex">
<h1 class="heading-5xl-3">
Assistência Técnica para {name} em Resende - RJ
</h1>
<p class="text-lg-muted">
Atendimento de assistência técnica especializada em notebooks e computadores para moradores e empresas do bairro {name} em Resende - RJ.
</p>
</div>
</section>

<!-- CONTENT -->
<section class="relative-25">
<div class="maxw4xl-mdpx12-2">

<div class="mb16">
<h2 class="heading-3xl-7">Suporte técnico de informática para a região do {name} em Resende</h2>
<p class="text-lg-muted-3">
A <strong>Nova Techouse</strong> presta atendimento especializado para clientes localizados no bairro {name}, em Resende - RJ.
</p>
<p class="text-lg-muted-3">
Oferecemos soluções de qualidade para quem necessita de {main_focus}. Nossos técnicos avaliam detalhadamente cada equipamento para determinar a solução mais eficiente e segura.
</p>
<p class="text-lg-muted-4">
Nossa sede física está localizada na Vila Santa Cecília, em Volta Redonda - RJ, e atendemos com total dedicação os clientes de Resende que buscam um serviço confiável de manutenção.
</p>
</div>

<div class="mb16">
<h2 class="heading-3xl-7">Principais serviços disponíveis para clientes de Resende</h2>
<p class="text-lg-muted-3">
Moradores do bairro {name} encontram na Nova Techouse suporte completo para diversas demandas de hardware e software:
</p>
<ul class="text-base-muted-3 space-y-2 mb6">
<li>• <strong>Conserto de Notebook:</strong> Diagnósticos de tela, teclado, bateria e reparo de carcaça.</li>
<li>• <strong>Conserto de Computador:</strong> Reparos em desktops de escritório e computadores pessoais.</li>
<li>• <strong>Upgrade de SSD & Memória RAM:</strong> Aceleramento expressivo de leitura e capacidade multitarefa.</li>
<li>• <strong>Formatação & Reinstalação do Windows:</strong> Limpeza do sistema operacional e atualização de drivers.</li>
<li>• <strong>Manutenção Preventiva & Limpeza Térmica:</strong> Higienização para evitar o superaquecimento do processador.</li>
</ul>
</div>

<div class="mb16">
<h2 class="heading-3xl-7">Atendimento ágil via WhatsApp</h2>
<p class="text-lg-muted-3">
Você pode esclarecer suas dúvidas sobre o funcionamento do seu equipamento diretamente com nossa equipe de suporte.
</p>
<p class="text-lg-muted-4">
Oferecemos orientação clara e transparente antes da realização de qualquer manutenção.
</p>
</div>

<div class="flex flex mt8 mb8">
<a href="/{{{{url_slugs.areas}}}}/resende/" class="text-sm-7">Voltar para Atendimento em Resende</a>
<span class="textwhite20">|</span>
<a href="/{{{{url_slugs.areas}}}}/" class="text-sm-7">Regiões Atendidas</a>
</div>

</div>
</section>

<!-- CTA FINAL -->
<section class="relative-28 hero-bg">
<div class="maxw3xl">
<h2 class="heading-4xl-2">Mora no {name} em Resende e precisa de ajuda técnica?</h2>
<p class="text-lg-muted-5">Converse com a equipe da Nova Techouse pelo WhatsApp para tirar dúvidas sobre seu computador ou notebook.</p>
<div class="flex-col-center-6 flex">
<a href="https://wa.me/{{{{contact.whatsapp_number}}}}?text=Olá! Vim pelo site da Nova Techouse. Sou do bairro {name} em Resende e preciso de assistência técnica." class="btn-cta-lg magnetic-btn flex">
<i data-lucide="message-square" class="icon-4"></i> Falar no WhatsApp
</a>
</div>
</div>
</section>
"""

def main():
    vr_dir = CONTENT_AREAS / "volta-redonda"
    resende_dir = CONTENT_AREAS / "resende"
    vr_dir.mkdir(parents=True, exist_ok=True)
    resende_dir.mkdir(parents=True, exist_ok=True)

    print("Generating Volta Redonda neighborhood files...")
    for item in VR_NEIGHBORHOODS:
        slug = item[0]
        html = render_vr_neighborhood(*item)
        (vr_dir / f"{slug}.html").write_text(html, encoding="utf-8")
        print(f"  created content/areas/volta-redonda/{slug}.html")

    print("Generating Resende neighborhood files...")
    for item in RESENDE_NEIGHBORHOODS:
        slug = item[0]
        html = render_resende_neighborhood(*item)
        (resende_dir / f"{slug}.html").write_text(html, encoding="utf-8")
        print(f"  created content/areas/resende/{slug}.html")

    print("Neighborhood files generation complete.")

if __name__ == "__main__":
    main()
