-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 30, 2025 at 02:37 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cinema_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `admins`
--

CREATE TABLE `admins` (
  `id` int(11) NOT NULL,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admins`
--

INSERT INTO `admins` (`id`, `username`, `password`) VALUES
(1, 'admin', 'password123');

-- --------------------------------------------------------

--
-- Table structure for table `bookings`
--

CREATE TABLE `bookings` (
  `id` int(11) NOT NULL,
  `customer_name` varchar(255) DEFAULT NULL,
  `customer_email` varchar(255) DEFAULT NULL,
  `booking_date` timestamp NOT NULL DEFAULT current_timestamp(),
  `total_amount` decimal(10,2) DEFAULT NULL,
  `status` enum('CONFIRMED','CANCELLED') DEFAULT 'CONFIRMED'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `halls`
--

CREATE TABLE `halls` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `total_rows` int(11) DEFAULT 10,
  `total_cols` int(11) DEFAULT 10
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `halls`
--

INSERT INTO `halls` (`id`, `name`, `total_rows`, `total_cols`) VALUES
(1, 'Cinema 1 (Standard)', 10, 14),
(2, 'Cinema 2 (Standard)', 10, 14),
(3, 'IMAX Theater', 14, 20),
(4, 'VIP Lounge', 5, 8);

-- --------------------------------------------------------

--
-- Table structure for table `movies`
--

CREATE TABLE `movies` (
  `id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `genre` varchar(100) DEFAULT NULL,
  `duration_minutes` int(11) DEFAULT NULL,
  `rating` varchar(50) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `poster_path` varchar(255) DEFAULT NULL,
  `status` enum('Now Showing','Coming Soon') DEFAULT 'Now Showing',
  `director` varchar(255) DEFAULT NULL,
  `cast` text DEFAULT NULL,
  `review` text DEFAULT NULL,
  `imdb_rating` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `movies`
--

INSERT INTO `movies` (`id`, `title`, `genre`, `duration_minutes`, `rating`, `description`, `poster_path`, `status`, `director`, `cast`, `review`, `imdb_rating`) VALUES
(1, 'Zootopia 2', 'Animation', 107, 'PG', 'After cracking the biggest case in Zootopia\'s history, rookie cops Judy Hopps and Nick Wilde find themselves on the twisting trail of a great mystery when Gary De’Snake arrives and turns the animal metropolis upside down. To crack the case, Judy and Nick must go undercover to unexpected new parts of town, where their growing partnership is tested like never before.', 'assets/sample_posters/oJ7g2CifqpStmoYQyaLQgEU32qO.jpg', 'Now Showing', 'Jared Bush', 'Ginnifer Goodwin, Jason Bateman, Ke Huy Quan', '\"Zootopia will be changed furrrever...\"', '★ 7.7/10'),
(2, 'The Shadow\'s Edge', 'Action', 142, 'NR', 'Macau Police brings the tracking expert police officer out of retirement to help catch a dangerous group of professional thieves.', 'assets/sample_posters/e0RU6KpdnrqFxDKlI3NOqN8nHL6.jpg', 'Now Showing', 'Larry Yang', 'Jackie Chan, Zhang Zifeng, Tony Leung Ka-fai', 'No tagline available.', '★ 6.4/10'),
(3, 'Altered', 'Science Fiction', 85, 'PG-13', 'In an alternate present, genetically enhanced humans dominate society. Outcasts Leon and Chloe fight for justice against corrupt politicians exploiting genetic disparity, risking everything to challenge the oppressive system.', 'assets/sample_posters/6QlAcGRaUrgHcZ4WTBh5lsPnzKx.jpg', 'Now Showing', 'Timo Vuorensola', 'Tom Felton, Aggy K. Adams, Elizaveta Bugulova', '\"Fight the system. Change the world.\"', '★ 6.5/10'),
(4, 'The Family Plan 2', 'Action', 106, 'PG-13', 'Now that Dan\'s assassin days are behind him, all he wants for Christmas is quality time with his kids. But when he learns his daughter has her own plans, he books a family trip to London—putting them all in the crosshairs of an unexpected enemy.', 'assets/sample_posters/semFxuYx6HcrkZzslgAkBqfJvZk.jpg', 'Now Showing', 'Simon Cellan Jones', 'Mark Wahlberg, Michelle Monaghan, Kit Harington', '\"Deck the halls, dodge the bad guys.\"', '★ 6.8/10'),
(5, 'Wildcat', 'Action', 99, 'R', 'An ex-black ops team reunite to pull off a desperate heist in order to save the life of their leader’s eight-year-old daughter.', 'assets/sample_posters/h893ImjM6Fsv5DFhKJdlZFZIJno.jpg', 'Now Showing', 'James Nunn', 'Kate Beckinsale, Lewis Tan, Alice Krige', 'No tagline available.', '★ 6.1/10'),
(6, 'Wicked: For Good', 'Fantasy', 137, 'PG', 'As an angry mob rises against the Wicked Witch, Glinda and Elphaba will need to come together one final time. With their singular friendship now the fulcrum of their futures, they will need to truly see each other, with honesty and empathy, if they are to change themselves, and all of Oz, for good.', 'assets/sample_posters/si9tolnefLSUKaqQEGz1bWArOaL.jpg', 'Now Showing', 'Jon M. Chu', 'Ariana Grande, Cynthia Erivo, Jonathan Bailey', '\"You will be changed.\"', '★ 6.8/10'),
(7, 'Frankenstein', 'Drama', 150, 'R', 'Dr. Victor Frankenstein, a brilliant but egotistical scientist, brings a creature to life in a monstrous experiment that ultimately leads to the undoing of both the creator and his tragic creation.', 'assets/sample_posters/g4JtvGlQO7DByTI6frUobqvSL3R.jpg', 'Now Showing', 'Guillermo del Toro', 'Oscar Isaac, Jacob Elordi, Christoph Waltz', '\"Only monsters play God.\"', '★ 7.8/10'),
(8, 'Dracula', 'Horror', 130, 'NR', 'When a 15th-century prince denounces God after the devastating loss of his wife, he inherits an eternal curse: he becomes Dracula. Condemned to wander the centuries, he defies fate and death itself, guided by a single hope — to be reunited with his lost love.', 'assets/sample_posters/ykyRfv7JDofLxXLAwtLXaSuaFfM.jpg', 'Now Showing', 'Luc Besson', 'Caleb Landry Jones, Zoë Bleu Sidel, Christoph Waltz', '\"He renounced his faith to become immortal. Passion, anger, vengeance, and hatred will be unleashed into the modern world.\"', '★ 7.1/10'),
(9, 'She Rides Shotgun', 'Action', 120, 'R', 'Newly released from prison and marked for death by unrelenting enemies, Nate must now protect his estranged 11-year-old daughter, Polly, at all costs. With scant resources and no one to trust, Nate and Polly forge a bond under fire as he shows her how to fight and survive—and she teaches him the true meaning of unconditional love.', 'assets/sample_posters/nvqW8mOm818QDio3GKKmPLK8kXj.jpg', 'Now Showing', 'Nick Rowland', 'Taron Egerton, Ana Sophia Heger, Odessa A\'zion', '\"All a father needs is a fighting chance.\"', '★ 7.0/10'),
(10, 'Predator: Badlands', 'Action', 107, 'PG-13', 'Cast out from his clan, a young Predator finds an unlikely ally in a damaged android and embarks on a treacherous journey in search of the ultimate adversary.', 'assets/sample_posters/ef2QSeBkrYhAdfsWGXmp0lvH0T1.jpg', 'Now Showing', 'Dan Trachtenberg', 'Elle Fanning, Dimitrius Schuster-Koloamatangi, Ravi Narayan', '\"First hunt. Last chance.\"', '★ 7.4/10'),
(11, 'A Legend', 'Action', 129, 'NR', 'An archeologist noticed that the texture of the relics discovered during the excavation of a glacier closely resembled a jade pendant seen in one of his dreams. He and his team then embark on an expedition into the depths of the glacier.', 'assets/sample_posters/qbImUt1d3itXcB81BCItPZlfbyr.jpg', 'Now Showing', 'Stanley Tong Gwai-Lai', 'Jackie Chan, Zhang Yixing, Gulnezer Bextiyar', 'No tagline available.', '★ 6.8/10'),
(12, 'One Battle After Another', 'Action', 162, 'R', 'Washed-up revolutionary Bob exists in a state of stoned paranoia, surviving off-grid with his spirited, self-reliant daughter, Willa. When his evil nemesis resurfaces after 16 years and she goes missing, the former radical scrambles to find her, father and daughter both battling the consequences of his past.', 'assets/sample_posters/m1jFoahEbeQXtx4zArT2FKdbNIj.jpg', 'Now Showing', 'Paul Thomas Anderson', 'Leonardo DiCaprio, Sean Penn, Chase Infiniti', '\"Some search for battle, others are born into it...\"', '★ 7.5/10'),
(13, 'JUJUTSU KAISEN: Execution -Shibuya Incident x The Culling Game Begins-', 'Animation', 88, 'NR', 'A veil abruptly descends over the busy Shibuya area amid the bustling Halloween crowds, trapping countless civilians inside. Satoru Gojo, the strongest jujutsu sorcerer, steps into the chaos. But lying in wait are curse users and spirits scheming to seal him away. Yuji Itadori, accompanied by his classmates and other top-tier jujutsu sorcerers, enters the fray in an unprecedented clash of curses — the Shibuya Incident. In the aftermath, ten colonies across Japan are transformed into dens of curses in a plan orchestrated by Noritoshi Kamo. As the deadly Culling Game starts, Special Grade sorcerer Yuta Okkotsu is assigned to carry out Yuji\'s execution for his perceived crimes. A compilation movie of Shibuya Incident including the first two episodes of the Culling Games arc.', 'assets/sample_posters/tc7RrVW5FGvyO2tsgW6LIN1esHI.jpg', 'Now Showing', 'Shota Goshozono', 'Junya Enoki, Megumi Ogata, Koji Yusa', 'No tagline available.', '★ 4.5/10'),
(14, 'Bugonia', 'Comedy', 119, 'R', 'Two conspiracy obsessed young men kidnap the high-powered CEO of a major company, convinced that she is an alien intent on destroying planet Earth.', 'assets/sample_posters/oxgsAQDAAxA92mFGYCZllgWkH9J.jpg', 'Now Showing', 'Yorgos Lanthimos', 'Emma Stone, Jesse Plemons, Aidan Delbis', '\"Of all the abductions, this one is different.\"', '★ 7.6/10'),
(15, 'Demon Slayer: Kimetsu no Yaiba Infinity Castle', 'Animation', 156, 'R', 'The Demon Slayer Corps are drawn into the Infinity Castle, where Tanjiro, Nezuko, and the Hashira face terrifying Upper Rank demons in a desperate fight as the final battle against Muzan Kibutsuji begins.', 'assets/sample_posters/fWVSwgjpT2D78VUh6X8UBd2rorW.jpg', 'Now Showing', 'Haruo Sotozaki', 'Natsuki Hanae, Hiro Shimono, Takahiro Sakurai', '\"It\'s time to have some fun.\"', '★ 7.6/10'),
(16, 'Now You See Me: Now You Don\'t', 'Thriller', 112, 'PG-13', 'The original Four Horsemen reunite with a new generation of illusionists to take on powerful diamond heiress Veronika Vanderberg, who leads a criminal empire built on money laundering and trafficking. The new and old magicians must overcome their differences to work together on their most ambitious heist yet.', 'assets/sample_posters/oD3Eey4e4Z259XLm3eD3WGcoJAh.jpg', 'Now Showing', 'Ruben Fleischer', 'Jesse Eisenberg, Dominic Sessa, Ariana Greenblatt', '\"Unlock the illusion.\"', '★ 6.3/10'),
(17, 'Playdate', 'Action', 93, 'PG-13', 'When out-of-work accountant Brian joins stay-at-home dad Jeff for a playdate with their sons, he expects a laid-back afternoon. Instead, they\'re chased by mercenaries, and Brian—totally unprepared—must survive one absurd obstacle after another.', 'assets/sample_posters/fGodXWqJkkkbSebPIlxLSygV8GY.jpg', 'Now Showing', 'Luke Greenfield', 'Kevin James, Alan Ritchson, Sarah Chalke', '\"Playtime just got real.\"', '★ 6.2/10'),
(18, 'Regretting You', 'Romance', 116, 'PG-13', 'Morgan Grant and her daughter Clara explore what\'s left behind after a devastating accident reveals a shocking betrayal and forces them to confront family secrets, redefine love, and rediscover each other.', 'assets/sample_posters/z4gVnxTaks3anTycwKjDmvQSuWt.jpg', 'Now Showing', 'Josh Boone', 'Mckenna Grace, Allison Williams, Dave Franco', '\"Risk everything. Regret nothing.\"', '★ 7.1/10'),
(19, 'KPop Demon Hunters', 'Fantasy', 96, 'PG', 'When K-pop superstars Rumi, Mira and Zoey aren\'t selling out stadiums, they\'re using their secret powers to protect their fans from supernatural threats.', 'assets/sample_posters/zT7Lhw3BhJbMkRqm9Zlx2YGMsY0.jpg', 'Now Showing', 'Maggie Kang', 'Arden Cho, May Hong, Ji-young Yoo', '\"They sing. They dance. They battle demons.\"', '★ 8.2/10'),
(20, 'Black Phone 2', 'Horror', 114, 'R', 'Four years after escaping The Grabber, Finney Blake is struggling with his life after captivity. When his sister Gwen begins receiving calls in her dreams from the black phone and seeing disturbing visions of three boys being stalked at a winter camp, the siblings become determined to solve the mystery and confront a killer who has grown more powerful in death and more significant to them than either could imagine.', 'assets/sample_posters/gFddBLQ8wj9M9O82iPzgX5KVNHz.jpg', 'Now Showing', 'Scott Derrickson', 'Ethan Hawke, Mason Thames, Madeleine McGraw', '\"Dead is just a word.\"', '★ 6.9/10'),
(21, 'Chainsaw Man - The Movie: Reze Arc', 'Animation', 100, 'R', 'In a brutal war between devils, hunters, and secret enemies, a mysterious girl named Reze has stepped into Denji\'s world, and he faces his deadliest battle yet, fueled by love in a world where survival knows no rules.', 'assets/sample_posters/xdzLBZjCVSEsic7m7nJc4jNJZVW.jpg', 'Now Showing', 'Tatsuya Yoshihara', 'Kikunosuke Toya, Reina Ueda, Shiori Izawa', '\"everyone’s after my chainsaw heart! what about denji’s heart?!?\"', '★ 7.8/10'),
(22, '31 Minutes: One Hot Christmas', 'Family', 91, 'PG', 'Puppeton, the town of 31 Minutes, faces such an infernally hot Christmas that Santa Claus cancels his visit! Bodoque the rabbit heroically volunteers to rescue the presents from the North Pole, while his friends improvise a disastrous Christmas show. But what they don\'t expect is Bodoque giving in to some irresistible temptations along the way.', 'assets/sample_posters/dv9UrOoicRiMGkzr2oj2YwSFY2K.jpg', 'Now Showing', 'Pedro Peirano', 'Pedro Peirano, Álvaro Díaz González, Jani Dueñas', '\"This Christmas there will be no Christmas. Unless a miracle happens. But miracles don\'t exist.\"', '★ 7.8/10'),
(23, 'Train Dreams', 'Drama', 102, 'PG-13', 'A logger leads a life of quiet grace as he experiences love and loss during an era of monumental change in early 20th-century America.', 'assets/sample_posters/l3zS4YnpOi4usyEXGJMtxSqDDyb.jpg', 'Now Showing', 'Clint Bentley', 'Joel Edgerton, Felicity Jones, Nathaniel Arcand', 'No tagline available.', '★ 7.4/10'),
(24, 'Wicked', 'Drama', 162, 'PG', 'In the land of Oz, ostracized and misunderstood green-skinned Elphaba is forced to share a room with the popular aristocrat Glinda at Shiz University, and the two\'s unlikely friendship is tested as they begin to fulfill their respective destinies as Glinda the Good and the Wicked Witch of the West.', 'assets/sample_posters/xDGbZ0JJ3mYaGKy4Nzd9Kph6M9L.jpg', 'Now Showing', 'Jon M. Chu', 'Cynthia Erivo, Ariana Grande, Michelle Yeoh', '\"Everyone deserves the chance to fly.\"', '★ 6.9/10'),
(25, 'Shelby Oaks', 'Horror', 91, 'R', 'A woman\'s obsessive search for her missing sister leads her into a terrifying mystery at the hands of an unknown evil.', 'assets/sample_posters/i3omY4P6QUzFQlEeclWY92RuXCH.jpg', 'Now Showing', 'Chris Stuckmann', 'Camille Sullivan, Sarah Durn, Brendan Sexton III', '\"Who took Riley Brennan?\"', '★ 5.7/10');

-- --------------------------------------------------------

--
-- Table structure for table `showtimes`
--

CREATE TABLE `showtimes` (
  `id` int(11) NOT NULL,
  `movie_id` int(11) DEFAULT NULL,
  `hall_id` int(11) DEFAULT NULL,
  `start_time` datetime DEFAULT NULL,
  `price_standard` decimal(10,2) DEFAULT 10.00
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `showtimes`
--

INSERT INTO `showtimes` (`id`, `movie_id`, `hall_id`, `start_time`, `price_standard`) VALUES
(1, 1, 1, '2025-11-30 12:00:00', 350.00),
(2, 1, 1, '2025-11-30 15:00:00', 350.00),
(3, 2, 1, '2025-11-30 18:00:00', 350.00),
(4, 2, 1, '2025-11-30 21:00:00', 350.00),
(5, 5, 2, '2025-11-30 12:00:00', 350.00),
(6, 6, 2, '2025-11-30 15:00:00', 350.00),
(7, 7, 2, '2025-11-30 18:00:00', 350.00),
(8, 8, 2, '2025-11-30 21:00:00', 350.00),
(9, 1, 3, '2025-11-30 12:00:00', 750.00),
(10, 1, 3, '2025-11-30 15:00:00', 750.00),
(11, 2, 3, '2025-11-30 18:00:00', 750.00),
(12, 2, 3, '2025-11-30 21:00:00', 750.00),
(13, 5, 4, '2025-11-30 12:00:00', 550.00),
(14, 6, 4, '2025-11-30 15:00:00', 550.00),
(15, 7, 4, '2025-11-30 18:00:00', 550.00),
(16, 8, 4, '2025-11-30 21:00:00', 550.00),
(17, 2, 1, '2025-12-01 12:00:00', 350.00),
(18, 9, 1, '2025-12-01 15:00:00', 350.00),
(19, 10, 1, '2025-12-01 18:00:00', 350.00),
(20, 11, 1, '2025-12-01 21:00:00', 350.00),
(21, 12, 2, '2025-12-01 12:00:00', 350.00),
(22, 1, 2, '2025-12-01 15:00:00', 350.00),
(23, 1, 2, '2025-12-01 18:00:00', 350.00),
(24, 2, 2, '2025-12-01 21:00:00', 350.00),
(25, 2, 3, '2025-12-01 12:00:00', 750.00),
(26, 9, 3, '2025-12-01 15:00:00', 750.00),
(27, 10, 3, '2025-12-01 18:00:00', 750.00),
(28, 11, 3, '2025-12-01 21:00:00', 750.00),
(29, 12, 4, '2025-12-01 12:00:00', 550.00),
(30, 1, 4, '2025-12-01 15:00:00', 550.00),
(31, 1, 4, '2025-12-01 18:00:00', 550.00),
(32, 2, 4, '2025-12-01 21:00:00', 550.00),
(33, 15, 1, '2025-12-02 12:00:00', 350.00),
(34, 16, 1, '2025-12-02 15:00:00', 350.00),
(35, 1, 1, '2025-12-02 18:00:00', 350.00),
(36, 1, 1, '2025-12-02 21:00:00', 350.00),
(37, 2, 2, '2025-12-02 12:00:00', 350.00),
(38, 2, 2, '2025-12-02 15:00:00', 350.00),
(39, 13, 2, '2025-12-02 18:00:00', 350.00),
(40, 14, 2, '2025-12-02 21:00:00', 350.00),
(41, 15, 3, '2025-12-02 12:00:00', 750.00),
(42, 16, 3, '2025-12-02 15:00:00', 750.00),
(43, 1, 3, '2025-12-02 18:00:00', 750.00),
(44, 1, 3, '2025-12-02 21:00:00', 750.00),
(45, 2, 4, '2025-12-02 12:00:00', 550.00),
(46, 2, 4, '2025-12-02 15:00:00', 550.00),
(47, 13, 4, '2025-12-02 18:00:00', 550.00),
(48, 14, 4, '2025-12-02 21:00:00', 550.00),
(49, 1, 1, '2025-12-03 12:00:00', 350.00),
(50, 2, 1, '2025-12-03 15:00:00', 350.00),
(51, 2, 1, '2025-12-03 18:00:00', 350.00),
(52, 17, 1, '2025-12-03 21:00:00', 350.00),
(53, 18, 2, '2025-12-03 12:00:00', 350.00),
(54, 19, 2, '2025-12-03 15:00:00', 350.00),
(55, 20, 2, '2025-12-03 18:00:00', 350.00),
(56, 1, 2, '2025-12-03 21:00:00', 350.00),
(57, 1, 3, '2025-12-03 12:00:00', 750.00),
(58, 2, 3, '2025-12-03 15:00:00', 750.00),
(59, 2, 3, '2025-12-03 18:00:00', 750.00),
(60, 17, 3, '2025-12-03 21:00:00', 750.00),
(61, 18, 4, '2025-12-03 12:00:00', 550.00),
(62, 19, 4, '2025-12-03 15:00:00', 550.00),
(63, 20, 4, '2025-12-03 18:00:00', 550.00),
(64, 1, 4, '2025-12-03 21:00:00', 550.00),
(65, 21, 1, '2025-12-04 12:00:00', 350.00),
(66, 22, 1, '2025-12-04 15:00:00', 350.00),
(67, 23, 1, '2025-12-04 18:00:00', 350.00),
(68, 24, 1, '2025-12-04 21:00:00', 350.00),
(69, 1, 2, '2025-12-04 12:00:00', 350.00),
(70, 1, 2, '2025-12-04 15:00:00', 350.00),
(71, 2, 2, '2025-12-04 18:00:00', 350.00),
(72, 2, 2, '2025-12-04 21:00:00', 350.00),
(73, 21, 3, '2025-12-04 12:00:00', 750.00),
(74, 22, 3, '2025-12-04 15:00:00', 750.00),
(75, 23, 3, '2025-12-04 18:00:00', 750.00),
(76, 24, 3, '2025-12-04 21:00:00', 750.00),
(77, 1, 4, '2025-12-04 12:00:00', 550.00),
(78, 1, 4, '2025-12-04 15:00:00', 550.00),
(79, 2, 4, '2025-12-04 18:00:00', 550.00),
(80, 2, 4, '2025-12-04 21:00:00', 550.00),
(81, 7, 1, '2025-12-05 12:00:00', 350.00),
(82, 1, 1, '2025-12-05 15:00:00', 350.00),
(83, 1, 1, '2025-12-05 18:00:00', 350.00),
(84, 2, 1, '2025-12-05 21:00:00', 350.00),
(85, 2, 2, '2025-12-05 12:00:00', 350.00),
(86, 25, 2, '2025-12-05 15:00:00', 350.00),
(87, 5, 2, '2025-12-05 18:00:00', 350.00),
(88, 6, 2, '2025-12-05 21:00:00', 350.00),
(89, 7, 3, '2025-12-05 12:00:00', 750.00),
(90, 1, 3, '2025-12-05 15:00:00', 750.00),
(91, 1, 3, '2025-12-05 18:00:00', 750.00),
(92, 2, 3, '2025-12-05 21:00:00', 750.00),
(93, 2, 4, '2025-12-05 12:00:00', 550.00),
(94, 25, 4, '2025-12-05 15:00:00', 550.00),
(95, 5, 4, '2025-12-05 18:00:00', 550.00),
(96, 6, 4, '2025-12-05 21:00:00', 550.00),
(97, 2, 1, '2025-12-06 12:00:00', 350.00),
(98, 2, 1, '2025-12-06 15:00:00', 350.00),
(99, 8, 1, '2025-12-06 18:00:00', 350.00),
(100, 9, 1, '2025-12-06 21:00:00', 350.00),
(101, 10, 2, '2025-12-06 12:00:00', 350.00),
(102, 11, 2, '2025-12-06 15:00:00', 350.00),
(103, 1, 2, '2025-12-06 18:00:00', 350.00),
(104, 1, 2, '2025-12-06 21:00:00', 350.00),
(105, 2, 3, '2025-12-06 12:00:00', 750.00),
(106, 2, 3, '2025-12-06 15:00:00', 750.00),
(107, 8, 3, '2025-12-06 18:00:00', 750.00),
(108, 9, 3, '2025-12-06 21:00:00', 750.00),
(109, 10, 4, '2025-12-06 12:00:00', 550.00),
(110, 11, 4, '2025-12-06 15:00:00', 550.00),
(111, 1, 4, '2025-12-06 18:00:00', 550.00),
(112, 1, 4, '2025-12-06 21:00:00', 550.00),
(113, 13, 1, '2025-12-07 12:00:00', 350.00),
(114, 14, 1, '2025-12-07 15:00:00', 350.00),
(115, 15, 1, '2025-12-07 18:00:00', 350.00),
(116, 1, 1, '2025-12-07 21:00:00', 350.00),
(117, 1, 2, '2025-12-07 12:00:00', 350.00),
(118, 2, 2, '2025-12-07 15:00:00', 350.00),
(119, 2, 2, '2025-12-07 18:00:00', 350.00),
(120, 12, 2, '2025-12-07 21:00:00', 350.00),
(121, 13, 3, '2025-12-07 12:00:00', 750.00),
(122, 14, 3, '2025-12-07 15:00:00', 750.00),
(123, 15, 3, '2025-12-07 18:00:00', 750.00),
(124, 1, 3, '2025-12-07 21:00:00', 750.00),
(125, 1, 4, '2025-12-07 12:00:00', 550.00),
(126, 2, 4, '2025-12-07 15:00:00', 550.00),
(127, 2, 4, '2025-12-07 18:00:00', 550.00),
(128, 12, 4, '2025-12-07 21:00:00', 550.00),
(129, 1, 1, '2025-12-08 12:00:00', 350.00),
(130, 1, 1, '2025-12-08 15:00:00', 350.00),
(131, 2, 1, '2025-12-08 18:00:00', 350.00),
(132, 2, 1, '2025-12-08 21:00:00', 350.00),
(133, 16, 2, '2025-12-08 12:00:00', 350.00),
(134, 17, 2, '2025-12-08 15:00:00', 350.00),
(135, 18, 2, '2025-12-08 18:00:00', 350.00),
(136, 19, 2, '2025-12-08 21:00:00', 350.00),
(137, 1, 3, '2025-12-08 12:00:00', 750.00),
(138, 1, 3, '2025-12-08 15:00:00', 750.00),
(139, 2, 3, '2025-12-08 18:00:00', 750.00),
(140, 2, 3, '2025-12-08 21:00:00', 750.00),
(141, 16, 4, '2025-12-08 12:00:00', 550.00),
(142, 17, 4, '2025-12-08 15:00:00', 550.00),
(143, 18, 4, '2025-12-08 18:00:00', 550.00),
(144, 19, 4, '2025-12-08 21:00:00', 550.00),
(145, 2, 1, '2025-12-09 12:00:00', 350.00),
(146, 20, 1, '2025-12-09 15:00:00', 350.00),
(147, 21, 1, '2025-12-09 18:00:00', 350.00),
(148, 22, 1, '2025-12-09 21:00:00', 350.00),
(149, 23, 2, '2025-12-09 12:00:00', 350.00),
(150, 1, 2, '2025-12-09 15:00:00', 350.00),
(151, 1, 2, '2025-12-09 18:00:00', 350.00),
(152, 2, 2, '2025-12-09 21:00:00', 350.00),
(153, 2, 3, '2025-12-09 12:00:00', 750.00),
(154, 20, 3, '2025-12-09 15:00:00', 750.00),
(155, 21, 3, '2025-12-09 18:00:00', 750.00),
(156, 22, 3, '2025-12-09 21:00:00', 750.00),
(157, 23, 4, '2025-12-09 12:00:00', 550.00),
(158, 1, 4, '2025-12-09 15:00:00', 550.00),
(159, 1, 4, '2025-12-09 18:00:00', 550.00),
(160, 2, 4, '2025-12-09 21:00:00', 550.00),
(161, 5, 1, '2025-12-10 12:00:00', 350.00),
(162, 6, 1, '2025-12-10 15:00:00', 350.00),
(163, 1, 1, '2025-12-10 18:00:00', 350.00),
(164, 1, 1, '2025-12-10 21:00:00', 350.00),
(165, 2, 2, '2025-12-10 12:00:00', 350.00),
(166, 2, 2, '2025-12-10 15:00:00', 350.00),
(167, 24, 2, '2025-12-10 18:00:00', 350.00),
(168, 25, 2, '2025-12-10 21:00:00', 350.00),
(169, 5, 3, '2025-12-10 12:00:00', 750.00),
(170, 6, 3, '2025-12-10 15:00:00', 750.00),
(171, 1, 3, '2025-12-10 18:00:00', 750.00),
(172, 1, 3, '2025-12-10 21:00:00', 750.00),
(173, 2, 4, '2025-12-10 12:00:00', 550.00),
(174, 2, 4, '2025-12-10 15:00:00', 550.00),
(175, 24, 4, '2025-12-10 18:00:00', 550.00),
(176, 25, 4, '2025-12-10 21:00:00', 550.00),
(177, 1, 1, '2025-12-11 12:00:00', 350.00),
(178, 2, 1, '2025-12-11 15:00:00', 350.00),
(179, 2, 1, '2025-12-11 18:00:00', 350.00),
(180, 7, 1, '2025-12-11 21:00:00', 350.00),
(181, 8, 2, '2025-12-11 12:00:00', 350.00),
(182, 9, 2, '2025-12-11 15:00:00', 350.00),
(183, 10, 2, '2025-12-11 18:00:00', 350.00),
(184, 1, 2, '2025-12-11 21:00:00', 350.00),
(185, 1, 3, '2025-12-11 12:00:00', 750.00),
(186, 2, 3, '2025-12-11 15:00:00', 750.00),
(187, 2, 3, '2025-12-11 18:00:00', 750.00),
(188, 7, 3, '2025-12-11 21:00:00', 750.00),
(189, 8, 4, '2025-12-11 12:00:00', 550.00),
(190, 9, 4, '2025-12-11 15:00:00', 550.00),
(191, 10, 4, '2025-12-11 18:00:00', 550.00),
(192, 1, 4, '2025-12-11 21:00:00', 550.00),
(193, 11, 1, '2025-12-12 12:00:00', 350.00),
(194, 12, 1, '2025-12-12 15:00:00', 350.00),
(195, 13, 1, '2025-12-12 18:00:00', 350.00),
(196, 14, 1, '2025-12-12 21:00:00', 350.00),
(197, 1, 2, '2025-12-12 12:00:00', 350.00),
(198, 1, 2, '2025-12-12 15:00:00', 350.00),
(199, 2, 2, '2025-12-12 18:00:00', 350.00),
(200, 2, 2, '2025-12-12 21:00:00', 350.00),
(201, 11, 3, '2025-12-12 12:00:00', 750.00),
(202, 12, 3, '2025-12-12 15:00:00', 750.00),
(203, 13, 3, '2025-12-12 18:00:00', 750.00),
(204, 14, 3, '2025-12-12 21:00:00', 750.00),
(205, 1, 4, '2025-12-12 12:00:00', 550.00),
(206, 1, 4, '2025-12-12 15:00:00', 550.00),
(207, 2, 4, '2025-12-12 18:00:00', 550.00),
(208, 2, 4, '2025-12-12 21:00:00', 550.00),
(209, 18, 1, '2025-12-13 12:00:00', 350.00),
(210, 1, 1, '2025-12-13 15:00:00', 350.00),
(211, 1, 1, '2025-12-13 18:00:00', 350.00),
(212, 2, 1, '2025-12-13 21:00:00', 350.00),
(213, 2, 2, '2025-12-13 12:00:00', 350.00),
(214, 15, 2, '2025-12-13 15:00:00', 350.00),
(215, 16, 2, '2025-12-13 18:00:00', 350.00),
(216, 17, 2, '2025-12-13 21:00:00', 350.00),
(217, 18, 3, '2025-12-13 12:00:00', 750.00),
(218, 1, 3, '2025-12-13 15:00:00', 750.00),
(219, 1, 3, '2025-12-13 18:00:00', 750.00),
(220, 2, 3, '2025-12-13 21:00:00', 750.00),
(221, 2, 4, '2025-12-13 12:00:00', 550.00),
(222, 15, 4, '2025-12-13 15:00:00', 550.00),
(223, 16, 4, '2025-12-13 18:00:00', 550.00),
(224, 17, 4, '2025-12-13 21:00:00', 550.00);

-- --------------------------------------------------------

--
-- Table structure for table `tickets`
--

CREATE TABLE `tickets` (
  `id` int(11) NOT NULL,
  `booking_id` int(11) DEFAULT NULL,
  `showtime_id` int(11) DEFAULT NULL,
  `seat_row_label` varchar(5) DEFAULT NULL,
  `seat_number` int(11) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admins`
--
ALTER TABLE `admins`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `bookings`
--
ALTER TABLE `bookings`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `halls`
--
ALTER TABLE `halls`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `movies`
--
ALTER TABLE `movies`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `showtimes`
--
ALTER TABLE `showtimes`
  ADD PRIMARY KEY (`id`),
  ADD KEY `movie_id` (`movie_id`),
  ADD KEY `hall_id` (`hall_id`);

--
-- Indexes for table `tickets`
--
ALTER TABLE `tickets`
  ADD PRIMARY KEY (`id`),
  ADD KEY `booking_id` (`booking_id`),
  ADD KEY `showtime_id` (`showtime_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admins`
--
ALTER TABLE `admins`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `bookings`
--
ALTER TABLE `bookings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `halls`
--
ALTER TABLE `halls`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `movies`
--
ALTER TABLE `movies`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT for table `showtimes`
--
ALTER TABLE `showtimes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=225;

--
-- AUTO_INCREMENT for table `tickets`
--
ALTER TABLE `tickets`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `showtimes`
--
ALTER TABLE `showtimes`
  ADD CONSTRAINT `showtimes_ibfk_1` FOREIGN KEY (`movie_id`) REFERENCES `movies` (`id`),
  ADD CONSTRAINT `showtimes_ibfk_2` FOREIGN KEY (`hall_id`) REFERENCES `halls` (`id`);

--
-- Constraints for table `tickets`
--
ALTER TABLE `tickets`
  ADD CONSTRAINT `tickets_ibfk_1` FOREIGN KEY (`booking_id`) REFERENCES `bookings` (`id`),
  ADD CONSTRAINT `tickets_ibfk_2` FOREIGN KEY (`showtime_id`) REFERENCES `showtimes` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
