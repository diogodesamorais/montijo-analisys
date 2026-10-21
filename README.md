# montijo-analisys

Análise Montijo / Portalegre — mapas, HTML e PPTX gerados pelos scripts `make_*.py`.

## Projectos

### Montijo / Portalegre (análise territorial)
Mapas de satélite, fichas de abandono e mudança de função, PPTX e páginas HTML.
Geradores: `make_images.py`, `make_pptx.py`, `make_site_pptx.py`, `make_ribeirinha_v2.py`,
`make_sat.py`, `make_website_pptx.py`, `make_edificios_pptx.py`.

### Sagrada Família — geologia das pedras
`make_sf_site.py` gera `sagrada-familia-geologia/index.html`: trabalho de geologia
sobre as **13 pedras** usadas na construção da basílica — tipos de rocha, idade
absoluta, pedreira de origem, textura, composição mineralógica e aplicação no templo.

Conteúdo do site:
- Enquadramento geológico de Barcelona (Collserola, Montjuïc, Zona Volcânica Catalana)
- As 13 pedras, agrupadas em sedimentares / ígneas / metamórficas, com ficha técnica
- Linha do tempo geológica (escala com quebra: linear 300→1 Ma, logarítmica abaixo)
- Gráfico comparativo de resistência à compressão
- Tabela-síntese, cinco temas de leitura crítica, roteiro de trabalho de campo
- Método de análise, notas e limitações, bibliografia

**46 fotografias** obtidas da Wikimedia Commons, com atribuição e licença de cada uma
(marcadas no rodapé). Duas distinções usadas nas legendas:
`Local de origem` (fotografia do local de extracção) e `Tipo de rocha`
(fotografia do tipo petrográfico equivalente).

Regenerar:

```bash
python make_sf_images.py   # descarrega imagens + img-manifest.json
python make_sf_site.py      # gera sagrada-familia-geologia/index.html
python check_sf_site.py     # valida referencias, estrutura HTML e SVG
```

## Licença

CC BY-SA 4.0.
