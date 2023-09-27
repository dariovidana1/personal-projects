-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 05-04-2022 a las 03:06:39
-- Versión del servidor: 10.4.22-MariaDB
-- Versión de PHP: 8.1.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `tienda`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tblcompra`
--

CREATE TABLE `tblcompra` (
  `idcompra` int(11) NOT NULL,
  `Nombre` varchar(50) NOT NULL,
  `Precio` varchar(20) NOT NULL,
  `Cantidad` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `tblcompra`
--

INSERT INTO `tblcompra` (`idcompra`, `Nombre`, `Precio`, `Cantidad`) VALUES
(4, 'Sudadera Reebook', '250.00', '1');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tblproductos`
--

CREATE TABLE `tblproductos` (
  `ID` int(11) NOT NULL,
  `NOMBRE` varchar(50) NOT NULL,
  `PRECIO` varchar(50) NOT NULL,
  `CANTIDAD` varchar(50) NOT NULL,
  `DESCRIPCION` varchar(500) NOT NULL,
  `IMAGEN` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `tblproductos`
--

INSERT INTO `tblproductos` (`ID`, `NOMBRE`, `PRECIO`, `CANTIDAD`, `DESCRIPCION`, `IMAGEN`) VALUES
(1, 'PLAYERA DE MUJER ', '500.00', '10', 'PLAYERA ROSA', 'imgs/MUJER1.jpg'),
(2, 'Sudadera Reebook', '250.00', '12', 'Sudadera Reebook Color Azul con Capucha Edicion Invierno 2021', 'imgs/hombre1.jpg'),
(3, 'Playera Gatos Negros', '50000.00', '5000', 'Playera Gatos Negros Edición ULTIMATE POWER', 'imgs/hombre4.jpg'),
(4, 'Playera Verde con Logo', '150.00', '20', 'Playera Verde con Logo con pequeñas manchas azuladas', 'imgs/niño1.jpg'),
(5, 'Top Deportivo', '200.00', '25', 'Top Deportivo color gris anti-calor', 'imgs/mujer3.jpg'),
(6, 'Blusa Rosa', '250.00', '10', 'Blusa Rosa ', 'imgs/mujer2.jpeg'),
(7, 'Short', '100.00', '30', 'Short Negro Refrescaste', 'imgs/niño2.jpg'),
(8, 'Sudadera Crop-Top', '300.00', '60', 'Sudadera Crop-Top Ideal para el día a día y útil para entrenar', 'imgs/mujer1.jpeg');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tblregistro`
--

CREATE TABLE `tblregistro` (
  `ID` int(11) NOT NULL,
  `CORREO` varchar(50) NOT NULL,
  `CONTRA` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `tblregistro`
--

INSERT INTO `tblregistro` (`ID`, `CORREO`, `CONTRA`) VALUES
(4, 'dario@mail.com', '123'),
(5, 'marcedelgamore@gmail.com', '123');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `tblcompra`
--
ALTER TABLE `tblcompra`
  ADD PRIMARY KEY (`idcompra`);

--
-- Indices de la tabla `tblproductos`
--
ALTER TABLE `tblproductos`
  ADD PRIMARY KEY (`ID`);

--
-- Indices de la tabla `tblregistro`
--
ALTER TABLE `tblregistro`
  ADD PRIMARY KEY (`ID`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `tblcompra`
--
ALTER TABLE `tblcompra`
  MODIFY `idcompra` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `tblproductos`
--
ALTER TABLE `tblproductos`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `tblregistro`
--
ALTER TABLE `tblregistro`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
