-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 16 Nov 2023 pada 03.10
-- Versi server: 10.4.28-MariaDB
-- Versi PHP: 8.0.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `civia`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `lowongan`
--

CREATE TABLE `lowongan` (
  `id` int(11) NOT NULL,
  `company` varchar(100) NOT NULL,
  `job_name` varchar(100) NOT NULL,
  `salary` int(11) NOT NULL,
  `last_date` date NOT NULL,
  `skills` varchar(300) NOT NULL,
  `job_description` varchar(5000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `lowongan`
--

INSERT INTO `lowongan` (`id`, `company`, `job_name`, `salary`, `last_date`, `skills`, `job_description`) VALUES
(1, 'company1', 'marketing', 20000, '2023-11-15', 'media sosial', 'Halo ini deskripsi untuk mengetes job deskripsi');

-- --------------------------------------------------------

--
-- Struktur dari tabel `resume`
--

CREATE TABLE `resume` (
  `id` int(11) NOT NULL,
  `awards` varchar(500) NOT NULL,
  `certification` varchar(500) NOT NULL,
  `college name` varchar(500) NOT NULL,
  `companies worked at` varchar(500) NOT NULL,
  `contact` varchar(500) NOT NULL,
  `degree` varchar(500) NOT NULL,
  `designation` varchar(500) NOT NULL,
  `email address` varchar(500) NOT NULL,
  `language` varchar(500) NOT NULL,
  `linkedin link` varchar(500) NOT NULL,
  `location` varchar(500) NOT NULL,
  `name` varchar(500) NOT NULL,
  `skills` varchar(500) NOT NULL,
  `university` varchar(500) NOT NULL,
  `unlabelled` varchar(500) NOT NULL,
  `worked as` varchar(500) NOT NULL,
  `year of graduation` varchar(500) NOT NULL,
  `years of experience` varchar(500) NOT NULL,
  `job_name` varchar(50) NOT NULL,
  `file` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `resume`
--

INSERT INTO `resume` (`id`, `awards`, `certification`, `college name`, `companies worked at`, `contact`, `degree`, `designation`, `email address`, `language`, `linkedin link`, `location`, `name`, `skills`, `university`, `unlabelled`, `worked as`, `year of graduation`, `years of experience`, `job_name`, `file`) VALUES
(3, '<built-in method lower of str object at 0x00007FF9375AE6E0>', '<built-in method lower of str object at 0x00007FF9375AE6E0>', '<built-in method lower of str object at 0x00007FF9375AE6E0>', '<built-in method lower of str object at 0x00007FF9375AE6E0>', '<built-in method lower of str object at 0x00007FF9375AE6E0>', '<built-in method lower of str object at 0x00007FF9375AE6E0>', '<built-in method lower of str object at 0x00007FF9375AE6E0>', '<built-in method lower of str object at 0x00000193D4556830>', '<built-in method lower of str object at 0x00007FF9375AE6E0>', '<built-in method lower of str object at 0x00000193DCEDFDB0>', '<built-in method lower of str object at 0x00007FF9375AE6E0>', '<built-in method lower of str object at 0x00000193D5B65480>', '<built-in method lower of str object at 0x00007FF9375AE6E0>', '<built-in method lower of str object at 0x00000193F361CAD0>', '<built-in method lower of str object at 0x00007FF9375AE6E0>', '<built-in method lower of str object at 0x00007FF9375AE6E0>', '<built-in method lower of str object at 0x00007FF9375AE6E0>', '<built-in method lower of str object at 0x00007FF9375AE6E0>', 'marketing', 'c1ce4965b2796ab2.pdf'),
(4, '', '', '', '', '', '', '', 'hendriyantofendy07@gmail.com', '', 'linkedin.com/in/fendy-hendriyanto/', '', 'FENDY HENDRIYANTO', '', 'TANRI ABENG UNIVERSITY – Jakarta, Indonesia', '', '', '', '', 'marketing', '1a3defd84b071a08.pdf'),
(5, '', '', 'Bandung Institute of Technology | Mathematics | GPA: 3.92/4.00 (Cumlaude)', '', '', '', '', '', '', '', 'Jakarta, Indonesia|', 'Louis Owen', '', '', '', '', '', '', 'marketing', 'e47a497f38584f65.pdf'),
(6, '', '', 'bandung institute of technology | mathematics | gpa: 3.92/4.00 (cumlaude)', '', '', '', '', '', '', '', 'jakarta, indonesia|', 'louis owen', '', '', '', '', '', '', 'marketing', 'f250e9c6e8272e40.pdf');

-- --------------------------------------------------------

--
-- Struktur dari tabel `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(40) NOT NULL,
  `username` varchar(40) NOT NULL,
  `password` varchar(40) NOT NULL,
  `date_of_birth` date NOT NULL,
  `email` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `users`
--

INSERT INTO `users` (`id`, `name`, `username`, `password`, `date_of_birth`, `email`) VALUES
(3, 'bb', 'bb', '21ad0bd836b90d08f4cf640b4c298e7c', '2023-11-15', 'a@a.cmo');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `lowongan`
--
ALTER TABLE `lowongan`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `resume`
--
ALTER TABLE `resume`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `lowongan`
--
ALTER TABLE `lowongan`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT untuk tabel `resume`
--
ALTER TABLE `resume`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT untuk tabel `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
