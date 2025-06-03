CREATE TABLE publishers(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255),
    description VARCHAR(255),
    created_by INT,
    updated_by INT,
    created_at DATETIME,
    updated_at DATETIME,
    status ENUM('pending', 'active', 'inactive')
);