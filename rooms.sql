-- phpMyAdmin SQL Dump
-- version 4.9.0.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 01, 2019 at 05:32 AM
-- Server version: 10.3.16-MariaDB
-- PHP Version: 7.3.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `bookingsdb`
--

-- --------------------------------------------------------

--
-- Table structure for table `rooms`
--

CREATE TABLE `rooms` (
  `room_id` varchar(10) NOT NULL,
  `room_type` varchar(20) NOT NULL,
  `detail` varchar(255) NOT NULL,
  `price` int(11) NOT NULL,
  `picture` varchar(255) NOT NULL,
  `status` int(11) NOT NULL DEFAULT 0,
  `create_timestamp` datetime NOT NULL DEFAULT current_timestamp(),
  `update_timestamp` datetime NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `rooms`
--

INSERT INTO `rooms` (`room_id`, `room_type`, `detail`, `price`, `picture`, `status`, `create_timestamp`, `update_timestamp`) VALUES
('A01', 'A', '', 1000, '', 0, '2019-10-01 09:48:57', '0000-00-00 00:00:00'),
('A02', 'A', '', 1000, '', 0, '2019-10-01 09:48:57', '0000-00-00 00:00:00'),
('A03', 'A', '', 1000, '', 0, '2019-10-01 09:48:57', '0000-00-00 00:00:00'),
('A04', 'A', '', 1000, '', 0, '2019-10-01 09:48:57', '0000-00-00 00:00:00'),
('A05', 'A', '', 1000, '', 0, '2019-10-01 09:48:57', '0000-00-00 00:00:00'),
('A06', 'A', '', 1000, '', 0, '2019-10-01 09:48:57', '0000-00-00 00:00:00'),
('A07', 'A', '', 1000, '', 0, '2019-10-01 09:48:57', '0000-00-00 00:00:00'),
('A08', 'A', '', 1000, '', 0, '2019-10-01 09:48:57', '0000-00-00 00:00:00'),
('A09', 'A', '', 1000, '', 0, '2019-10-01 09:48:57', '0000-00-00 00:00:00'),
('A10', 'A', '', 1000, '', 0, '2019-10-01 09:48:57', '0000-00-00 00:00:00'),
('B01', 'B', '', 500, '', 0, '2019-10-01 09:54:28', '0000-00-00 00:00:00'),
('B02', 'B', '', 500, '', 0, '2019-10-01 09:54:28', '0000-00-00 00:00:00'),
('B03', 'B', '', 500, '', 0, '2019-10-01 09:54:28', '0000-00-00 00:00:00'),
('B04', 'B', '', 500, '', 0, '2019-10-01 09:54:28', '0000-00-00 00:00:00'),
('B05', 'B', '', 500, '', 0, '2019-10-01 09:54:28', '0000-00-00 00:00:00'),
('C01', 'C', '', 300, '', 0, '2019-10-01 09:56:25', '0000-00-00 00:00:00'),
('C02', 'C', '', 300, '', 0, '2019-10-01 09:56:25', '0000-00-00 00:00:00'),
('C03', 'C', '', 300, '', 0, '2019-10-01 09:56:25', '0000-00-00 00:00:00'),
('C04', 'C', '', 300, '', 0, '2019-10-01 09:56:25', '0000-00-00 00:00:00'),
('C05', 'C', '', 300, '', 0, '2019-10-01 09:56:25', '0000-00-00 00:00:00');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `rooms`
--
ALTER TABLE `rooms`
  ADD PRIMARY KEY (`room_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
