CREATE TABLE books(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    publisher_id INT NOT NULL,
    FOREIGN KEY (publisher_id) REFERENCES publisher(id),
    description VARCHAR(255),
    isAudio BOOLEAN NULL DEFAULT 0,
    price INT NOT NULL,
    published_date DATETIME NOT NULL,
    created_by INT,
    updated_by INT,
    created_at DATETIME,
    updated_at DATETIME,
    status ENUM('pending', 'active', 'inactive')
);
