CREATE TABLE authors_books(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    author_id INT,
    FOREIGN KEY (author_id) REFERENCES authors(id),
    book_id INT,
    FOREIGN KEY (book_id) REFERENCES books(id)
);