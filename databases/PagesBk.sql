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
-- Database: `PagesBk`
--

-- --------------------------------------------------------

--
-- Table structure for table `auth_cas`
--

CREATE TABLE IF NOT EXISTS `auth_cas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `created_on` datetime DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `uuid` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id__idx` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `auth_event`
--

CREATE TABLE IF NOT EXISTS `auth_event` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `time_stamp` datetime DEFAULT NULL,
  `client_ip` varchar(255) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `origin` varchar(255) DEFAULT NULL,
  `description` longtext,
  PRIMARY KEY (`id`),
  KEY `user_id__idx` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role` varchar(255) DEFAULT NULL,
  `description` longtext,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `auth_membership`
--

CREATE TABLE IF NOT EXISTS `auth_membership` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `group_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id__idx` (`user_id`),
  KEY `group_id__idx` (`group_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `table_name` varchar(255) DEFAULT NULL,
  `record_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `group_id__idx` (`group_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(128) DEFAULT NULL,
  `last_name` varchar(128) DEFAULT NULL,
  `username` text NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `registration_key` varchar(255) DEFAULT NULL,
  `registration_id` int(11) NOT NULL,
  `reset_password_key` varchar(255) DEFAULT NULL,
  `Role_Name` enum('student','teacher','editor') NOT NULL DEFAULT 'student',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `comment`
--

CREATE TABLE IF NOT EXISTS `comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `slug` varchar(128) DEFAULT NULL,
  `body` longtext,
  `created_by` int(11) DEFAULT NULL,
  `created_on` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `created_by__idx` (`created_by`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `dialect`
--

CREATE TABLE IF NOT EXISTS `dialect` (
  `id` int(11) NOT NULL,
  `name` text NOT NULL,
  `color` varchar(10) NOT NULL,
  `next` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_2` (`id`),
  KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `document`
--

CREATE TABLE IF NOT EXISTS `document` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `slug` varchar(128) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `description` longtext,
  `file` varchar(255) DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `created_on` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `created_by__idx` (`created_by`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `image`
--

CREATE TABLE IF NOT EXISTS `image` (
  `id` int(6) NOT NULL AUTO_INCREMENT,
  `show` int(11) NOT NULL DEFAULT '1',
  `title` varchar(200) NOT NULL,
  `file` varchar(255) CHARACTER SET utf8 NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `plugin_wiki_attachment`
--

CREATE TABLE IF NOT EXISTS `plugin_wiki_attachment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tablename` varchar(255) DEFAULT NULL,
  `record_id` int(11) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `filename` varchar(255) DEFAULT NULL,
  `is_active` char(1) DEFAULT NULL,
  `created_on` datetime DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `modified_on` datetime DEFAULT NULL,
  `modified_by` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `created_by__idx` (`created_by`),
  KEY `modified_by__idx` (`modified_by`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `plugin_wiki_comment`
--

CREATE TABLE IF NOT EXISTS `plugin_wiki_comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tablename` varchar(255) DEFAULT NULL,
  `record_id` int(11) DEFAULT NULL,
  `body` varchar(255) DEFAULT NULL,
  `is_active` char(1) DEFAULT NULL,
  `created_on` datetime DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `modified_on` datetime DEFAULT NULL,
  `modified_by` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `created_by__idx` (`created_by`),
  KEY `modified_by__idx` (`modified_by`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `plugin_wiki_images`
--

CREATE TABLE IF NOT EXISTS `plugin_wiki_images` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `title` varchar(200) NOT NULL,
  `filename` varchar(255) DEFAULT NULL,
  `is_active` char(1) DEFAULT NULL,
  `created_on` datetime DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `modified_on` datetime DEFAULT NULL,
  `modified_by` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `created_by__idx` (`created_by`),
  KEY `modified_by__idx` (`modified_by`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `plugin_wiki_link`
--

CREATE TABLE IF NOT EXISTS `plugin_wiki_link` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tag` int(11) DEFAULT NULL,
  `table_name` varchar(255) DEFAULT NULL,
  `record_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `tag__idx` (`tag`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `plugin_wiki_page`
--

CREATE TABLE IF NOT EXISTS `plugin_wiki_page` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `slug` varchar(255) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `is_public` char(1) DEFAULT NULL,
  `worksheet` char(1) NOT NULL DEFAULT 'F',
  `summary` mediumtext NOT NULL,
  `body` longtext,
  `tags` longtext NOT NULL,
  `role` int(11) DEFAULT NULL,
  `changelog` varchar(255) DEFAULT NULL,
  `is_active` char(1) DEFAULT NULL,
  `created_on` datetime DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `modified_on` datetime DEFAULT NULL,
  `modified_by` int(11) DEFAULT NULL,
  `comments_allowed` char(1) NOT NULL DEFAULT 'F',
  PRIMARY KEY (`id`),
  KEY `role__idx` (`role`),
  KEY `created_by__idx` (`created_by`),
  KEY `modified_by__idx` (`modified_by`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `plugin_wiki_page_archive`
--

CREATE TABLE IF NOT EXISTS `plugin_wiki_page_archive` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `current_record` int(11) DEFAULT NULL,
  `slug` varchar(255) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `is_public` char(1) DEFAULT NULL,
  `worksheet` tinyint(1) NOT NULL DEFAULT '0',
  `summary` mediumtext NOT NULL,
  `body` longtext,
  `tags` varchar(200) NOT NULL,
  `role` int(11) DEFAULT NULL,
  `changelog` varchar(255) DEFAULT NULL,
  `is_active` char(1) DEFAULT NULL,
  `created_on` datetime DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `modified_on` datetime DEFAULT NULL,
  `modified_by` int(11) DEFAULT NULL,
  `comments_allowed` char(1) NOT NULL DEFAULT 'F',
  PRIMARY KEY (`id`),
  KEY `current_record__idx` (`current_record`),
  KEY `role__idx` (`role`),
  KEY `created_by__idx` (`created_by`),
  KEY `modified_by__idx` (`modified_by`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `plugin_wiki_rating`
--

CREATE TABLE IF NOT EXISTS `plugin_wiki_rating` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tablename` varchar(255) DEFAULT NULL,
  `record_id` int(11) DEFAULT NULL,
  `rating` double DEFAULT NULL,
  `counter` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `plugin_wiki_rating_aux`
--

CREATE TABLE IF NOT EXISTS `plugin_wiki_rating_aux` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `master` int(11) DEFAULT NULL,
  `rating` double DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `master__idx` (`master`),
  KEY `created_by__idx` (`created_by`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `plugin_wiki_tag`
--

CREATE TABLE IF NOT EXISTS `plugin_wiki_tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent` varchar(100) NOT NULL DEFAULT 'Index',
  `name` varchar(255) DEFAULT NULL,
  `links` int(11) DEFAULT NULL,
  `is_active` char(1) DEFAULT NULL,
  `created_on` datetime DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `modified_on` datetime DEFAULT NULL,
  `modified_by` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `created_by__idx` (`created_by`),
  KEY `modified_by__idx` (`modified_by`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `plugin_wiki_transcript`
--

CREATE TABLE IF NOT EXISTS `plugin_wiki_transcript` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `slug` varchar(255) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `is_public` char(1) DEFAULT NULL,
  `body` longtext,
  `summary` mediumtext NOT NULL,
  `role` int(11) DEFAULT NULL,
  `changelog` varchar(255) DEFAULT NULL,
  `is_active` char(1) DEFAULT NULL,
  `created_on` datetime DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `modified_on` datetime DEFAULT NULL,
  `modified_by` int(11) DEFAULT NULL,
  `comments_allowed` char(1) NOT NULL DEFAULT 'F',
  PRIMARY KEY (`id`),
  KEY `role__idx` (`role`),
  KEY `created_by__idx` (`created_by`),
  KEY `modified_by__idx` (`modified_by`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `plugin_wiki_transcript_archive`
--

CREATE TABLE IF NOT EXISTS `plugin_wiki_transcript_archive` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `current_record` int(11) DEFAULT NULL,
  `slug` varchar(255) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `summary` mediumtext NOT NULL,
  `is_public` char(1) DEFAULT NULL,
  `body` longtext,
  `tags` text NOT NULL,
  `role` int(11) DEFAULT NULL,
  `changelog` varchar(255) DEFAULT NULL,
  `is_active` char(1) DEFAULT NULL,
  `created_on` datetime DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `modified_on` datetime DEFAULT NULL,
  `modified_by` int(11) DEFAULT NULL,
  `comments_allowed` char(1) NOT NULL DEFAULT 'F',
  PRIMARY KEY (`id`),
  KEY `current_record__idx` (`current_record`),
  KEY `role__idx` (`role`),
  KEY `created_by__idx` (`created_by`),
  KEY `modified_by__idx` (`modified_by`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `profile`
--

CREATE TABLE IF NOT EXISTS `profile` (
  `user` int(11) NOT NULL,
  `ALC` tinyint(1) NOT NULL,
  `ALC_Name` int(11) NOT NULL,
  `CLW` tinyint(1) NOT NULL,
  `CLW_Name` int(11) NOT NULL,
  PRIMARY KEY (`user`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `resources`
--

CREATE TABLE IF NOT EXISTS `resources` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `slug` varchar(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `title` varchar(100) NOT NULL,
  `file` varchar(100) DEFAULT NULL,
  `Collected_by` varchar(100) NOT NULL,
  `description` text NOT NULL,
  `Public` varchar(1) NOT NULL DEFAULT 'F',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `resources_archive`
--

CREATE TABLE IF NOT EXISTS `resources_archive` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `current_record` int(10) NOT NULL,
  `slug` varchar(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `title` varchar(100) NOT NULL,
  `Collected_by` varchar(100) NOT NULL,
  `description` text NOT NULL,
  `Public` varchar(1) NOT NULL DEFAULT 'F',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `shows`
--

CREATE TABLE IF NOT EXISTS `shows` (
  `id` int(6) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `topics`
--

CREATE TABLE IF NOT EXISTS `topics` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `page_id` int(10) NOT NULL,
  `English` varchar(255) DEFAULT NULL,
  `Language` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `web2py_session_Bundjalung`
--

CREATE TABLE IF NOT EXISTS `web2py_session_Bundjalung` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `locked` char(1) DEFAULT NULL,
  `client_ip` varchar(64) DEFAULT NULL,
  `created_datetime` datetime DEFAULT NULL,
  `modified_datetime` datetime DEFAULT NULL,
  `unique_key` varchar(64) DEFAULT NULL,
  `session_data` longblob,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
