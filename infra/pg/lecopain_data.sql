INSERT INTO public.customers
(id, firstname, lastname, address, cp, city, email, created_at, subscription_id, nb_orders, nb_subscriptions)
VALUES(0, '', '', '', '', '', '', '', 0, 0, 0);
INSERT INTO public.lines
(order_id, product_id, quantity, price)
VALUES(0, 0, 1, 0.00);
INSERT INTO public.order_status
("name")
VALUES('');
INSERT INTO public.orders
(id, title, shipping_dt, created_at, customer_id, status, payment_status, subscription_id, price, shipping_price, seller_id, shipping_status, shipping_rules, category, shipping_address, shipping_cp, shipping_city, nb_products)
VALUES(0, '', '', '', 0, 'CREE'::text, 'NON_PAYEE'::text, 0, 0, 0, 0, '', '', '', '', '', '', 0);
INSERT INTO public.payement_status
("name")
VALUES('');
INSERT INTO public.product_status
("name")
VALUES('');
INSERT INTO public.products
(id, "name", description, price, seller_id, status, category)
VALUES(0, '', '', 0.00, 0, '', '');
INSERT INTO public.sellers
(id, "name", email, nb_subscriptions, nb_orders)
VALUES(0, '', '', 0.0, 0);
INSERT INTO public.shipping_status
("name")
VALUES('');
INSERT INTO public.subscription_days
(id, day_of_week, price, shipping_price, subscription_id, nb_products)
VALUES(0, 0, 0, 0, 0, 0);
INSERT INTO public.subscription_lines
(id, subscription_day_id, product_id, quantity, price)
VALUES(0, 0, 0, 0, 0);
INSERT INTO public.subscriptions
(id, start_dt, end_dt, customer_id, shipping_price, price, status, payment_status, promotion, description, seller_id, nb_products, nb_orders, category)
VALUES(0, '', '', 0, 0, 0, '', '', '', '', 0, 0, 0, '');
INSERT INTO public.users
(id, username, "password", email, joined_at, is_admin)
VALUES(0, '', '', '', '', 0);

