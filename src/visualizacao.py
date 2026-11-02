import folium

def desenhar_mapa_rotas(coordenadas_hospital, rotas_otimizadas, coordenadas_destinos):
    mapa = folium.Map(location=coordenadas_hospital, zoom_start=13)
    folium.Marker(
        coordenadas_hospital, 
        popup="Hospital Base", 
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(mapa)
    
    cores_veiculos = ['blue', 'green', 'purple', 'orange']
    
    for idx, rota in enumerate(rotas_otimizadas):
        if not rota: 
            continue
            
        cor = cores_veiculos[idx % len(cores_veiculos)]
        coordenadas_trajeto = [coordenadas_hospital]
        
        for ponto_id in rota:
            coord = coordenadas_destinos[ponto_id]['coord']
            nome = coordenadas_destinos[ponto_id]['nome']
            folium.Marker(coord, popup=f"Entrega: {nome}").add_to(mapa)
            coordenadas_trajeto.append(coord)
            
        coordenadas_trajeto.append(coordenadas_hospital)
        folium.PolyLine(coordenadas_trajeto, color=cor, weight=2.5, opacity=0.8).add_to(mapa)
        
    mapa.save("mapa_rotas_hospital.html")