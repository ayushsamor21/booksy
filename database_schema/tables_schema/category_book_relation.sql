CREATE TABLE category_book_relation(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    category_id INT,
    FOREIGN KEY (category_id) REFERENCES category_schema(category_id),
    book_id INT,
    FOREIGN KEY (book_id) REFERENCES book_schema(book_id)
);