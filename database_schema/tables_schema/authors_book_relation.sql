CREATE TABLE author_book_relation(
id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
author_id INT,
FOREIGN KEY (author_id) REFERENCES authors_schema(authors_id),
book_id INT,
FOREIGN KEY (book_id) REFERENCES book_schema(book_id)
);