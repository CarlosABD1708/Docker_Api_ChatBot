
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
    oficina(NombreOficina, _, _, (Lat, Long)); oficina(_, _, Descripcion, _), sub_string(Descripcion, _, _, _, NombreOficina).
% Regla para obtener coordenadas del aula
coordenadas_aula(NombreAula, (Lat, Long)) :- 
    aula(NombreAula, _, _, (Lat, Long)).
% Regla para obtener coordenadas del laboratorio
coordenadas_laboratorio(NombreLaboratorio, (Lat, Long)) :- 
    laboratorio(NombreLaboratorio, _, _, (Lat, Long)) ; laboratorio(_, _, Descripcion, _), sub_string(Descripcion, _, _, _, NombreLaboratorio).
% Regla para obtener coordenadas del lugar interes
coordenadas_lugar_interes(NombreLugarInteres, (Lat, Long)) :- 
    lugar_interes(NombreLugarInteres, _, _, (Lat, Long)).


% Reglas para determinar el tipo de un lugar dado su nombre exacto
tipo_de_lugar(Nombre, Tipo) :-
    ( aula(Nombre, _, _, _) -> Tipo = 'aula'
    ; laboratorio(Nombre, _, _, _) -> Tipo = 'laboratorio'
    ; oficina(Nombre, _, _, _) -> Tipo = 'oficina'
    ; lugar_interes(Nombre, _, _, _) -> Tipo = 'lugar_interes'
    ; edificio(Nombre, _, _, _) -> Tipo = 'edificio'
    ; facultad(Nombre, _, _) -> Tipo = 'facultad'
    ; Tipo = 'desconocido'  % Si no coincide con ninguno, retornar 'desconocido'
    ).

% Regla para buscar un lugar, aplicando búsqueda en descripciones solo para laboratorios y oficinas
buscar_lugar(Nombre, Tipo) :-
    ( tipo_de_lugar(Nombre, Tipo), Tipo \= 'desconocido' -> true
    ; oficina(_, _, Descripcion, _), sub_string(Descripcion, _, _, _, Nombre) -> Tipo = 'oficina'
    ; laboratorio(_, _, Descripcion, _), sub_string(Descripcion, _, _, _, Nombre) -> Tipo = 'laboratorio'
    ; Tipo = 'no_encontrado'  % Si no coincide con ninguno, retornar 'no_encontrado'
    ).

% Regla para encontrar la facultad y edificio de un lugar específico por nombre exacto
ubicacion_lugar(Nombre, Facultad, Edificio) :-
    ( aula(Nombre, Edificio, _, _)
    ; laboratorio(Nombre, Edificio, _, _)
    ; oficina(Nombre, Edificio, _, _)
    ; lugar_interes(Nombre, Edificio, _, _)
    ),
    edificio(Edificio, Facultad, _, _), !.

% Búsqueda en la descripción de laboratorios si el nombre no coincide exactamente
ubicacion_lugar(Nombre, Facultad, Edificio) :-
    laboratorio(_, Edificio, Descripcion, _),
    sub_string(Descripcion, _, _, _, Nombre),  % Verifica si el nombre está en la descripción del laboratorio
    edificio(Edificio, Facultad, _, _), !.

% Búsqueda en la descripción de oficinas si el nombre no coincide exactamente
ubicacion_lugar(Nombre, Facultad, Edificio) :-
    oficina(_, Edificio, Descripcion, _),
    sub_string(Descripcion, _, _, _, Nombre),  % Verifica si el nombre está en la descripción de la oficina
    edificio(Edificio, Facultad, _, _), !.

