-- phpMyAdmin SQL Dump
-- version 5.2.1deb1+deb12u1
-- https://www.phpmyadmin.net/
--
-- Hôte : localhost:3306
-- Généré le : dim. 15 juin 2025 à 20:57
-- Version du serveur : 10.11.11-MariaDB-0+deb12u1
-- Version de PHP : 8.2.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `IENAC24_Alerte_reglementation_aeronautique`
--

-- --------------------------------------------------------

--
-- Structure de la table `Favoris`
--

CREATE TABLE `Favoris` (
  `user_id` int(11) NOT NULL,
  `cellar_id` varchar(255) NOT NULL,
  `nom` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `Favoris`
--

INSERT INTO `Favoris` (`user_id`, `cellar_id`, `nom`) VALUES
(17, '32025R0682', 'test');

-- --------------------------------------------------------

--
-- Structure de la table `Preferences`
--

CREATE TABLE `Preferences` (
  `user_id` int(11) NOT NULL,
  `theme_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `Preferences`
--

INSERT INTO `Preferences` (`user_id`, `theme_id`) VALUES
(4, 8),
(4, 11),
(10, 11),
(14, 11),
(16, 11),
(17, 11),
(18, 19);

-- --------------------------------------------------------

--
-- Structure de la table `Themes`
--

CREATE TABLE `Themes` (
  `theme_id` int(11) NOT NULL,
  `nom` varchar(50) NOT NULL,
  `eurvoc_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `Themes`
--

INSERT INTO `Themes` (`theme_id`, `nom`, `eurvoc_name`) VALUES
(8, 'aviation civile', '4408'),
(11, 'colza', '6042'),
(17, 'pouvoir politique', '2573'),
(19, 'aéroport', '195'),
(21, 'drone', '24'),
(22, 'contrôle aérien', '172'),
(25, 'droit public économique', '4012');

-- --------------------------------------------------------

--
-- Structure de la table `Users`
--

CREATE TABLE `Users` (
  `user_id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `nom` varchar(50) NOT NULL,
  `prenom` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `privilege` enum('user','admin') NOT NULL DEFAULT 'user'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `Users`
--

INSERT INTO `Users` (`user_id`, `username`, `password`, `nom`, `prenom`, `email`, `privilege`) VALUES
(2, 'test', 'f4f263e439cf40925e6a412387a9472a6773c2580212a4fb50d224d3a817de17', 'Nom', 'Thomas', 'z@z.com', 'user'),
(3, 'd', 'e3b98a4da31a127d4bde6e43033f66ba274cab0eb7eb1c70ec41402bf6273dd8', 'az', 'ghj', '1@5.com', 'user'),
(4, 'abc', '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08', 'abc', 'abc', 'abc@a', 'user'),
(10, 'q', '8e35c2cd3bf6641bdb0e2050b76932cbb2e6034a0ddacc1d9bea82a6ba57f7cf', 's', 'q', 'q@5.com', 'user'),
(11, 'etv', '8b1101c7d738ce75a70812bad2dd8319d74a47b63676b8eb562bd20185f4f15e', 'vidal', 'etienne', 'test@gmail.com', 'user'),
(14, 'gg', 'cbd3cfb9b9f51bbbfbf08759e243f5b3519cbf6ecc219ee95fe7c667e32c0a8d', 'gg', 'gg', 'gg@gg', 'user'),
(16, 'cc', '355b1bbfc96725cdce8f4a2708fda310a80e6d13315aec4e5eed2a75fe8032ce', 'cc', 'cc', 'cc@cc', 'admin'),
(17, 'jj', 'de3bbd0fd7945e42581643b18cdf28dd3ed61d9c3d541b7b016081564b65a3f3', 'jj', 'jj', 'jj@jj', 'user'),
(18, 'oo', 'a8c23cc814179578e3a774418ac5fc4702a66eb3b78c876df81b290465e6e334', 'oo', 'oo', 'oo@oo', 'user');

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `Favoris`
--
ALTER TABLE `Favoris`
  ADD PRIMARY KEY (`user_id`,`cellar_id`);

--
-- Index pour la table `Preferences`
--
ALTER TABLE `Preferences`
  ADD PRIMARY KEY (`user_id`,`theme_id`),
  ADD KEY `deleteonthemedelete` (`theme_id`);

--
-- Index pour la table `Themes`
--
ALTER TABLE `Themes`
  ADD PRIMARY KEY (`theme_id`);

--
-- Index pour la table `Users`
--
ALTER TABLE `Users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `Themes`
--
ALTER TABLE `Themes`
  MODIFY `theme_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT pour la table `Users`
--
ALTER TABLE `Users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `Favoris`
--
ALTER TABLE `Favoris`
  ADD CONSTRAINT `contrainte` FOREIGN KEY (`user_id`) REFERENCES `Users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Contraintes pour la table `Preferences`
--
ALTER TABLE `Preferences`
  ADD CONSTRAINT `deleteonthemedelete` FOREIGN KEY (`theme_id`) REFERENCES `Themes` (`theme_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `deleteonuserdelete` FOREIGN KEY (`user_id`) REFERENCES `Users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
