-- Sample data

INSERT INTO categories (name) VALUES
    ('Electronics'),
    ('Books'),
    ('Home & Kitchen'),
    ('Sports');

INSERT INTO products (name, description, price, image_url, stock, category_id) VALUES
('Wireless Headphones', 'Over-ear Bluetooth headphones with active noise cancellation and 30-hour battery life.', 4999.00, '/images/headphones.svg', 25, 1),
('Mechanical Keyboard', 'Compact 75% mechanical keyboard with hot-swappable switches and RGB backlight.', 3499.00, '/images/keyboard.svg', 40, 1),
('Smart Watch', 'Fitness tracker with heart-rate monitor, GPS, and 7-day battery.', 6999.00, '/images/watch.svg', 15, 1),
('Portable Power Bank', '20000 mAh power bank with 22.5W fast charging and dual USB ports.', 1799.00, '/images/powerbank.svg', 60, 1),
('Clean Code', 'A handbook of agile software craftsmanship by Robert C. Martin.', 899.00, '/images/book-clean-code.svg', 30, 2),
('Introduction to Algorithms', 'Comprehensive textbook on algorithms (CLRS), 4th edition.', 1599.00, '/images/book-algorithms.svg', 18, 2),
('Database System Concepts', 'Standard textbook on database systems by Silberschatz, Korth and Sudarshan.', 1299.00, '/images/book-dbms.svg', 22, 2),
('Stainless Steel Water Bottle', 'Insulated 1-litre bottle that keeps drinks cold for 24 hours or hot for 12.', 799.00, '/images/bottle.svg', 100, 3),
('Non-stick Frying Pan', '28 cm induction-compatible non-stick pan with a heat-resistant handle.', 1199.00, '/images/pan.svg', 35, 3),
('Electric Kettle', '1.5 litre kettle with auto shut-off and boil-dry protection.', 1099.00, '/images/kettle.svg', 50, 3),
('Yoga Mat', '6 mm anti-slip yoga mat with carrying strap.', 699.00, '/images/yogamat.svg', 70, 4),
('Badminton Racket Set', 'Pair of lightweight aluminium rackets with 3 shuttlecocks and a carry bag.', 1399.00, '/images/racket.svg', 0, 4);
