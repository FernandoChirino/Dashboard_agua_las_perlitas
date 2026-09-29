-- Este es el schema de la base de datos en MySQL nombrada electropura antes de correr este archivo 
-- se necesita crear una base de datos en MySQL llamada electropura 

DROP TABLE IF EXISTS lectura_valores;
DROP TABLE IF EXISTS lecturas;
DROP TABLE IF EXISTS limites;
DROP TABLE IF EXISTS parametros;
DROP TABLE IF EXISTS puntos_muestreo;
DROP TABLE IF EXISTS usuarios;

CREATE TABLE usuarios (
	id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL, 
    nombre_completo VARCHAR(100) NOT NULL, 
    rol ENUM('analista', 'operador') NOT NULL,
    fecha_creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
); 

-- Puntos de muestreo dentro de la planta
CREATE TABLE puntos_muestreo(
	id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL UNIQUE, 
    descripcion VARCHAR(255)
);

-- Parametros medidos (PH, TDS, sabor, olor, color, verificacion de sello)
CREATE TABLE parametros (
	id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(80) NOT NULL UNIQUE, 
    tipo ENUM('numerico', 'binario') NOT NULL, 
    unidad VARCHAR(20)
);

-- Limites de especificacion por parametro y punto de muestreo.
CREATE TABLE limites(
	id INT AUTO_INCREMENT PRIMARY KEY,
    parametro_id INT NOT NULL,
    punto_muestreo_id INT NOT NULL,
    valor_min DOUBLE NOT NULL, 
    valor_max DOUBLE NOT NULL, 
    FOREIGN KEY (parametro_id) REFERENCES parametros(id), 
    FOREIGN KEY (punto_muestreo_id) REFERENCES puntos_muestreo(id), 
    CONSTRAINT unique_parametro_punto UNIQUE (parametro_id, punto_muestreo_id)
);

-- Encabezado de una lectura: cuando, donde, quien, numero de lote
CREATE TABLE lecturas(
	id INT AUTO_INCREMENT PRIMARY KEY,
    punto_muestreo_id INT NOT NULL, 
    tecnico_id INT NOT NULL, 
    fecha DATE NOT NULL, 
    hora TIME NOT NULL, 
    lote VARCHAR(50), 
    observaciones TEXT, 
    dentro_de_rango BOOLEAN NOT NULL DEFAULT TRUE, 
    FOREIGN KEY (punto_muestreo_id) REFERENCES puntos_muestreo(id), 
    FOREIGN KEY (tecnico_id) REFERENCES usuarios(id)
);

-- Valores individuales por parametro para cada lectura
CREATE TABLE lectura_valores (
	id INT AUTO_INCREMENT PRIMARY KEY, 
    lectura_id INT NOT NULL, 
    parametro_id INT NOT NULL, 
    valor DOUBLE NOT NULL, 
    dentro_de_rango BOOLEAN NOT NULL DEFAULT TRUE, 
    FOREIGN KEY (lectura_id) REFERENCES lecturas(id),
    FOREIGN KEY (parametro_id) REFERENCES parametros(id),
    CONSTRAINT unique_lectura_parametro UNIQUE (lectura_id, parametro_id)
);


