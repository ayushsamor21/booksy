CREATE TABLE categories_books(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    category_id INT,
    FOREIGN KEY (category_id) REFERENCES categories(id),
    book_id INT,
    FOREIGN KEY (book_id) REFERENCES books(id)
);