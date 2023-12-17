-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 16-12-2023 a las 17:28:49
-- Versión del servidor: 10.4.28-MariaDB
-- Versión de PHP: 8.0.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `frutilla_rosada_db`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clientes`
--

CREATE TABLE `clientes` (
  `rut_cliente` varchar(10) NOT NULL,
  `nombre` varchar(20) NOT NULL,
  `apellido` varchar(20) DEFAULT NULL,
  `region` varchar(40) NOT NULL,
  `ciudad` varchar(40) NOT NULL,
  `calle` varchar(40) DEFAULT NULL,
  `telefono` int(9) NOT NULL,
  `tipo_envio` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `clientes`
--

INSERT INTO `clientes` (`rut_cliente`, `nombre`, `apellido`, `region`, `ciudad`, `calle`, `telefono`, `tipo_envio`) VALUES
('21178329-k', 'Ramon', 'Pacheco', 'Los Rios', 'San Jose De La Mariquina', '', 1234, 'Starken');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `diseño`
--

CREATE TABLE `diseño` (
  `nombre` varchar(15) NOT NULL,
  `cantidad` varchar(6) DEFAULT '',
  `precio` int(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `diseño`
--

INSERT INTO `diseño` (`nombre`, `cantidad`, `precio`) VALUES
('Agenda', '', 3500),
('Planner', '', 5000);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `elasticos`
--

CREATE TABLE `elasticos` (
  `nombre` varchar(20) NOT NULL,
  `cantidad` int(6) NOT NULL,
  `precio` int(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `elasticos`
--

INSERT INTO `elasticos` (`nombre`, `cantidad`, `precio`) VALUES
('Elasticos Morados', 100, 400),
('Elasticos Verdes', 120, 300),
('Sin Elastico', 0, 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `encuadernacion`
--

CREATE TABLE `encuadernacion` (
  `nombre` varchar(7) NOT NULL,
  `cantidad` int(6) NOT NULL,
  `precio` int(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `encuadernacion`
--

INSERT INTO `encuadernacion` (`nombre`, `cantidad`, `precio`) VALUES
('Disco', 200, 500),
('Espiral', 200, 300);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `fechas_importantes`
--

CREATE TABLE `fechas_importantes` (
  `id_fecha` int(11) NOT NULL,
  `fecha` date NOT NULL,
  `descripción` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `fechas_importantes`
--

INSERT INTO `fechas_importantes` (`id_fecha`, `fecha`, `descripción`) VALUES
(1, '2023-07-10', 'lalalalalalalalalalalalalalala'),
(3, '2023-10-04', 'hay que ir a comer completos'),
(4, '2023-12-12', 'a');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ganancias`
--

CREATE TABLE `ganancias` (
  `fecha` date NOT NULL,
  `precio` int(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `ganancias`
--

INSERT INTO `ganancias` (`fecha`, `precio`) VALUES
('2023-11-15', 3123),
('2023-11-15', 12000),
('2023-12-15', 8550),
('2023-12-15', 12),
('2023-12-15', 12);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pedidos`
--

CREATE TABLE `pedidos` (
  `id_pedido` int(11) NOT NULL,
  `rut_cliente` varchar(10) NOT NULL,
  `fecha_ingreso` date NOT NULL,
  `fecha_salida` date DEFAULT NULL,
  `tipo_encuadernacion` varchar(7) NOT NULL,
  `tipo_diseño` varchar(15) NOT NULL,
  `tamaño_hoja` varchar(2) NOT NULL,
  `cantidad_hojas` int(3) NOT NULL,
  `elastico` varchar(20) NOT NULL,
  `termolaminado` varchar(15) NOT NULL,
  `comentarios` varchar(500) DEFAULT 'Sin comentarios',
  `precio` int(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pedidos`
--

INSERT INTO `pedidos` (`id_pedido`, `rut_cliente`, `fecha_ingreso`, `fecha_salida`, `tipo_encuadernacion`, `tipo_diseño`, `tamaño_hoja`, `cantidad_hojas`, `elastico`, `termolaminado`, `comentarios`, `precio`) VALUES
(9, '21178329-k', '2023-12-15', '2023-12-15', 'Disco', 'Agenda', 'A5', 100, 'Elasticos Morados', 'Caliente 100um', '', 8550),
(11, '21178329-k', '2023-12-15', NULL, 'Disco', 'Agenda', 'A5', 1000, 'Sin Elastico', 'Frio 120um ', '', 44100),
(22, '21178329-k', '2023-12-16', NULL, 'Espiral', 'Planner', 'A5', 100, 'Elasticos Morados', 'Caliente 100um', 'prueba', 9850),
(23, '21178329-k', '2023-12-16', NULL, 'Espiral', 'Planner', 'A5', 100, 'Elasticos Morados', 'Caliente 100um', 'prueba2222222', 9850);

--
-- Disparadores `pedidos`
--
DELIMITER $$
CREATE TRIGGER `agregar_ganancias` AFTER UPDATE ON `pedidos` FOR EACH ROW BEGIN
    IF NEW.fecha_salida IS NOT NULL AND OLD.fecha_salida IS NULL THEN
        INSERT INTO ganancias (fecha, precio)
        VALUES (NEW.fecha_salida, NEW.precio);
    END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tamaño`
--

CREATE TABLE `tamaño` (
  `nombre` varchar(2) NOT NULL,
  `cantidad` int(6) NOT NULL,
  `precio` int(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tamaño`
--

INSERT INTO `tamaño` (`nombre`, `cantidad`, `precio`) VALUES
('A5', 900, 40),
('A6', 1300, 50);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `termolaminado`
--

CREATE TABLE `termolaminado` (
  `nombre` varchar(15) NOT NULL,
  `cantidad` int(6) NOT NULL,
  `precio` int(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `termolaminado`
--

INSERT INTO `termolaminado` (`nombre`, `cantidad`, `precio`) VALUES
('Caliente 100um', 100, 150),
('Caliente 170um ', 100, 180),
('Frio 120um ', 100, 100);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `rut` varchar(10) NOT NULL,
  `nombre` varchar(20) NOT NULL,
  `hash_clave` varchar(32) NOT NULL,
  `rol` varchar(13) DEFAULT 'vendedor'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`rut`, `nombre`, `hash_clave`, `rol`) VALUES
('1', 'Vendedor', 'c4ca4238a0b923820dcc509a6f75849b', 'Vendedor'),
('2', 'Sisi Sisi', 'c4ca4238a0b923820dcc509a6f75849b', 'Administrador'),
('21178329-k', 'Ramón', '81dc9bdb52d04dc20036dbd8313ed055', 'Administrador');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`rut_cliente`);

--
-- Indices de la tabla `diseño`
--
ALTER TABLE `diseño`
  ADD PRIMARY KEY (`nombre`);

--
-- Indices de la tabla `elasticos`
--
ALTER TABLE `elasticos`
  ADD PRIMARY KEY (`nombre`);

--
-- Indices de la tabla `encuadernacion`
--
ALTER TABLE `encuadernacion`
  ADD PRIMARY KEY (`nombre`);

--
-- Indices de la tabla `fechas_importantes`
--
ALTER TABLE `fechas_importantes`
  ADD PRIMARY KEY (`id_fecha`);

--
-- Indices de la tabla `pedidos`
--
ALTER TABLE `pedidos`
  ADD PRIMARY KEY (`id_pedido`),
  ADD KEY `pedidos_rut_cliente_fk` (`rut_cliente`),
  ADD KEY `pedidos_tipo_encuadernacion_fk` (`tipo_encuadernacion`),
  ADD KEY `pedidos_tipo_diseño_fk` (`tipo_diseño`),
  ADD KEY `pedidos_tamaño_hoja_fk` (`tamaño_hoja`),
  ADD KEY `pedidos_elastico_fk` (`elastico`),
  ADD KEY `pedidos_termolaminado_fk` (`termolaminado`);

--
-- Indices de la tabla `tamaño`
--
ALTER TABLE `tamaño`
  ADD PRIMARY KEY (`nombre`);

--
-- Indices de la tabla `termolaminado`
--
ALTER TABLE `termolaminado`
  ADD PRIMARY KEY (`nombre`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`rut`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `fechas_importantes`
--
ALTER TABLE `fechas_importantes`
  MODIFY `id_fecha` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `pedidos`
--
ALTER TABLE `pedidos`
  MODIFY `id_pedido` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `pedidos`
--
ALTER TABLE `pedidos`
  ADD CONSTRAINT `pedidos_elastico_fk` FOREIGN KEY (`elastico`) REFERENCES `elasticos` (`nombre`),
  ADD CONSTRAINT `pedidos_rut_cliente_fk` FOREIGN KEY (`rut_cliente`) REFERENCES `clientes` (`rut_cliente`),
  ADD CONSTRAINT `pedidos_tamaño_hoja_fk` FOREIGN KEY (`tamaño_hoja`) REFERENCES `tamaño` (`nombre`),
  ADD CONSTRAINT `pedidos_termolaminado_fk` FOREIGN KEY (`termolaminado`) REFERENCES `termolaminado` (`nombre`),
  ADD CONSTRAINT `pedidos_tipo_diseño_fk` FOREIGN KEY (`tipo_diseño`) REFERENCES `diseño` (`nombre`),
  ADD CONSTRAINT `pedidos_tipo_encuadernacion_fk` FOREIGN KEY (`tipo_encuadernacion`) REFERENCES `encuadernacion` (`nombre`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
