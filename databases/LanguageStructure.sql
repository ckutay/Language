-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Aug 15, 2015 at 05:02 PM
-- Server version: 5.5.44-0ubuntu0.14.04.1
-- PHP Version: 5.5.9-1ubuntu4.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `LanguageStructure`
--

-- --------------------------------------------------------

--
-- Table structure for table `Bundjalung`
--

CREATE TABLE IF NOT EXISTS `Bundjalung` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Language_Word` varchar(200) NOT NULL,
  `Part_of_Speech` varchar(100) NOT NULL,
  `English` varchar(200) DEFAULT NULL,
  `Search_English` varchar(200) NOT NULL,
  `Category` varchar(30) NOT NULL,
  `Scientific` varchar(100) NOT NULL,
  `Comment` varchar(500) NOT NULL,
  `Gold_Coast_Tweed` varchar(500) NOT NULL,
  `Lower_Richmond` varchar(500) NOT NULL,
  `Middle_Clarence` varchar(500) NOT NULL,
  `Condamine_Upper_Clarence` varchar(500) NOT NULL,
  `Copmanhurst` varchar(500) NOT NULL,
  `RelatedWord` text NOT NULL,
  `Image` text NOT NULL,
  `SoundFile` text NOT NULL,
  `Lesson` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `BundjalungExamples`
--

CREATE TABLE IF NOT EXISTS `BundjalungExamples` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `language_id` int(10) NOT NULL,
  `Language` varchar(200) NOT NULL,
  `English` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
