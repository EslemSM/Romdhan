USE ramadhan;
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE doua (
    id INT AUTO_INCREMENT PRIMARY KEY,
    allah_name VARCHAR(100),
    text_ar TEXT NOT NULL,
    text_latin TEXT
);
CREATE TABLE adhkar (
    id INT AUTO_INCREMENT PRIMARY KEY,
    text_ar TEXT NOT NULL,
    text_latin TEXT,
    category ENUM('morning', 'evening', 'night', 'going_out', 'going_in', 'before_suhur', 'after_suhur','before_iftar', 'after_iftar') NOT NULL,
    source VARCHAR(300)
);
CREATE TABLE ahadith_ramadhania (
    id INT AUTO_INCREMENT PRIMARY KEY,
    text_ar TEXT NOT NULL,
    meaning_en TEXT,
    reference VARCHAR(300),
    category ENUM('fasting', 'night_prayer', 'laylat_al_qadr', 'mercy_forgiveness', 'doua','charity','quran', 'ramdhan_virtues') NOT NULL
);
CREATE TABLE recipes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) UNIQUE NOT NULL,
    category ENUM('sweet', 'savory') NOT NULL,
    ingredients JSON NOT NULL,
    steps TEXT NOT NULL,

    nutrition_summary JSON NULL,   -- filled AFTER external API call

    diabetic_friendly BOOLEAN DEFAULT NULL,
    pcos_friendly BOOLEAN DEFAULT NULL,
    pcos_score INT DEFAULT NULL,

    created_by_user_id INT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (created_by_user_id) REFERENCES users(id)
        ON DELETE SET NULL
);
CREATE TABLE sunnah_prayer (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name ENUM('duha', 'taraweeh', 'tahajjud') NOT NULL,
    is_ramadhan_only BOOLEAN DEFAULT FALSE
);
CREATE TABLE favorite_doua (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    doua_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (doua_id) REFERENCES doua(id) ON DELETE CASCADE
);
CREATE TABLE favorite_adhkar (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    adhkar_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (adhkar_id) REFERENCES adhkar(id) ON DELETE CASCADE
);
CREATE TABLE favorite_recipe (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    recipe_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
);
CREATE TABLE user_doua (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(150),
    text_ar TEXT NOT NULL,
    text_latin TEXT,
    category VARCHAR(30),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
CREATE TABLE user_adhkar (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    text_ar TEXT NOT NULL,
    text_latin TEXT,
    category VARCHAR(30),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
CREATE TABLE khatma (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    unit ENUM('juz', 'hizb') NOT NULL,
    total_completed INT DEFAULT 0,
    current_progress INT DEFAULT 0,
    status ENUM('in_progress', 'completed') DEFAULT 'in_progress',
    completion_date DATE NULL,
    completion_doua TEXT,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);




