import os
from pathlib import Path

import folium


def desenhar_mapa_rotas(coordenadas_hospital, rotas_otimizadas) -> Path:
    chave_carto = os.environ.get("CARTO_BASEMAPS_KEY")
    if not chave_carto:
        raise RuntimeError(
            "Defina a variável de ambiente CARTO_BASEMAPS_KEY com sua chave "
            "de basemaps do CARTO."
        )

    mapa = folium.Map(
        location=coordenadas_hospital,
        zoom_start=13,
        tiles=None,
    )
    folium.TileLayer(
        tiles=(
            "https://basemaps.cartocdn.com/rastertiles/voyager/"
            f"{{z}}/{{x}}/{{y}}.png?key={chave_carto}"
        ),
        attr=(
            '&copy; <a href="https://www.openstreetmap.org/copyright">'
            "OpenStreetMap</a>, "
            '&copy; <a href="https://carto.com/attribution/">CARTO</a>'
        ),
        name="CARTO Voyager",
    ).add_to(mapa)
    folium.Marker(coordenadas_hospital, popup="Hospital Base", icon=folium.Icon(color="red")).add_to(mapa)
    
    cores_veiculos = ['blue', 'green', 'purple', 'orange']
    
    # Plota as rotas de cada veículo com cores diferentes
    for idx, rota in enumerate(rotas_otimizadas):
        cor = cores_veiculos[idx % len(cores_veiculos)]
        
        for ponto in rota:
            folium.Marker(ponto['coordenada'], popup=f"Entrega {ponto['id']}").add_to(mapa)
            
        
        coordenadas_rota = [coordenadas_hospital] + [p['coordenada'] for p in rota] + [coordenadas_hospital]
        folium.PolyLine(coordenadas_rota, color=cor, weight=2.5, opacity=0.8).add_to(mapa)
        
    pasta_downloads = Path.home() / "Downloads"
    pasta_downloads.mkdir(parents=True, exist_ok=True)
    arquivo_mapa = pasta_downloads / "mapa_rotas_hospital.html"
    mapa.save(str(arquivo_mapa))
    return arquivo_mapa.resolve()