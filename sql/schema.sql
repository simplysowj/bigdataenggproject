/* Create the database if it doesn't exist */
CREATE DATABASE IF NOT EXISTS FRAUDSDB;

/* Use the FRAUDSDB database */
USE FRAUDSDB;

/* Drop existing table if it exists */
DROP TABLE IF EXISTS fraudtrans;

/* Create the fraudtrans table with transaction and sentiment columns */
CREATE TABLE fraudtrans (
  id INT AUTO_INCREMENT PRIMARY KEY,
  transaction VARCHAR(500),
  sentiment VARCHAR(20) -- Adjust the size based on your needs
);

