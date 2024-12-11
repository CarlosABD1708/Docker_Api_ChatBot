
% Permitir la adición y eliminación dinámica de hechos
:- dynamic facultad/3.
:- dynamic edificio/4.
:- dynamic oficina/4.
:- dynamic aula/4.
:- dynamic laboratorio/4.
:- dynamic lugar_interes/4.

% Regla para obtener coordenadas del facultad
coordenadas_facultad(NombreFacultad, (Lat, Long)) :- 
    facultad(NombreFacultad, _, (Lat, Long)).
% Regla para obtener coordenadas del edificio
coordenadas_edificio(NombreEdificio, (Lat, Long)) :- 
    edificio(NombreEdificio, _, _, (Lat, Long)).
% Regla para obtener coordenadas del aula
coordenadas_oficina(NombreOficina, (Lat, Long)) :- 
    oficina(NombreOficina, _, _, (Lat, Long)).
% Regla para obtener coordenadas del aula
coordenadas_aula(NombreAula, (Lat, Long)) :- 
    aula(NombreAula, _, _, (Lat, Long)).
% Regla para obtener coordenadas del laboratorio
coordenadas_laboratorio(NombreLaboratorio, (Lat, Long)) :- 
    laboratorio(NombreLaboratorio, _, _, (Lat, Long)).
% Regla para obtener coordenadas del lugar interes
coordenadas_lugar_interes(NombreLugarInteres, (Lat, Long)) :- 
    lugar_interes(NombreLugarInteres, _, _, (Lat, Long)).


% Regla para determinar el tipo de lugar
tipo_de_lugar(Nombre, Tipo) :-
    ( aula(Nombre, _, _, _) -> Tipo = 'aula'
    ; laboratorio(Nombre, _, _, _) -> Tipo = 'laboratorio'
    ; oficina(Nombre, _, _, _) -> Tipo = 'oficina'
    ; lugar_interes(Nombre, _, _, _) -> Tipo = 'lugar_interes'
    ; edificio(Nombre, _, _, _) -> Tipo = 'edificio'
    ; facultad(Nombre, _, _) -> Tipo = 'facultad'
    ; Tipo = 'desconocido'
    ).

% Regla para buscar el lugar (nombre original en caso de descripción)
buscar_lugar(Nombre, Tipo) :-
    ( 
    tipo_de_lugar(Nombre, Tipo), Tipo \= 'desconocido' 
    ; Tipo = 'no_encontrado'
    ).

% Regla para encontrar facultad, edificio y nombre original
ubicacion_lugar(Nombre, Facultad, Edificio) :-
    ( aula(Nombre, Edificio, _, _)
    ; laboratorio(Nombre, Edificio, _, _)
    ; oficina(Nombre, Edificio, _, _)
    ; lugar_interes(Nombre, Edificio, _, _)
    ),
    edificio(Edificio, Facultad, _, _), !.

