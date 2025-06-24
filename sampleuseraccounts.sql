-- Group 1: Like imrans
CREATE USER IF NOT EXISTS 'imrans'@'%' IDENTIFIED BY 'imran';
GRANT USAGE ON *.* TO 'imrans'@'%';
GRANT ALL PRIVILEGES ON `pawcache`.`animal_dat` TO 'imrans'@'%';
GRANT ALL PRIVILEGES ON `pawcache`.`food_dir` TO 'imrans'@'%';
GRANT SELECT, UPDATE ON `pawcache`.`notes_for_imrans` TO 'imrans'@'%';
GRANT SELECT, INSERT ON `pawcache`.`requests` TO 'imrans'@'%';
GRANT SELECT ON `pawcache`.`staff_dat` TO 'imrans'@'%';

CREATE USER IF NOT EXISTS 'deepikar'@'%' IDENTIFIED BY 'deepika';
GRANT USAGE ON *.* TO 'deepikar'@'%';
GRANT ALL PRIVILEGES ON `pawcache`.`animal_dat` TO 'deepikar'@'%';
GRANT ALL PRIVILEGES ON `pawcache`.`food_dir` TO 'deepikar'@'%';
GRANT SELECT, UPDATE ON `pawcache`.`notes_for_deepikar` TO 'deepikar'@'%';
GRANT SELECT, INSERT ON `pawcache`.`requests` TO 'deepikar'@'%';
GRANT SELECT ON `pawcache`.`staff_dat` TO 'deepikar'@'%';

CREATE USER IF NOT EXISTS 'raviv'@'%' IDENTIFIED BY 'ravi';
GRANT USAGE ON *.* TO 'raviv'@'%';
GRANT ALL PRIVILEGES ON `pawcache`.`animal_dat` TO 'raviv'@'%';
GRANT ALL PRIVILEGES ON `pawcache`.`food_dir` TO 'raviv'@'%';
GRANT SELECT, UPDATE ON `pawcache`.`notes_for_raviv` TO 'raviv'@'%';
GRANT SELECT, INSERT ON `pawcache`.`requests` TO 'raviv'@'%';
GRANT SELECT ON `pawcache`.`staff_dat` TO 'raviv'@'%';

-- Group 2: Like udaans
CREATE USER IF NOT EXISTS 'udaans'@'%' IDENTIFIED BY 'udaan';
GRANT USAGE ON *.* TO 'udaans'@'%';
GRANT SELECT, UPDATE ON `pawcache`.`notes_for_udaans` TO 'udaans'@'%';
GRANT SELECT, INSERT ON `pawcache`.`requests` TO 'udaans'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON `pawcache`.`shop_purchase_logs` TO 'udaans'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON `pawcache`.`shop_stock` TO 'udaans'@'%';
GRANT SELECT ON `pawcache`.`staff_dat` TO 'udaans'@'%';

-- Group 3: Like nishat
CREATE USER IF NOT EXISTS 'nishat'@'%' IDENTIFIED BY 'nisha';
GRANT USAGE ON *.* TO 'nishat'@'%';
GRANT ALL PRIVILEGES ON `pawcache`.* TO 'nishat'@'%';

CREATE USER IF NOT EXISTS 'meeraj'@'%' IDENTIFIED BY 'meera';
GRANT USAGE ON *.* TO 'meeraj'@'%';
GRANT ALL PRIVILEGES ON `pawcache`.* TO 'meeraj'@'%';

CREATE USER IF NOT EXISTS 'sandeepk'@'%' IDENTIFIED BY 'sandeep';
GRANT USAGE ON *.* TO 'sandeepk'@'%';
GRANT ALL PRIVILEGES ON `pawcache`.* TO 'sandeepk'@'%';

-- Group 4: Like mikee
CREATE USER IF NOT EXISTS 'mikee'@'%' IDENTIFIED BY 'mike';
GRANT CREATE USER ON *.* TO 'mikee'@'%';
GRANT ALL PRIVILEGES ON `pawcache`.* TO 'mikee'@'%' WITH GRANT OPTION;
GRANT GRANT OPTION ON *.* TO 'mikee'@'%';

CREATE USER IF NOT EXISTS 'mayar'@'%' IDENTIFIED BY 'maya';
GRANT CREATE USER ON *.* TO 'mayar'@'%';
GRANT ALL PRIVILEGES ON `pawcache`.* TO 'mayar'@'%' WITH GRANT OPTION;
GRANT GRANT OPTION ON *.* TO 'mayar'@'%';

-- Finalize
FLUSH PRIVILEGES;
