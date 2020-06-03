-- public.customers definition

-- Drop table

-- DROP TABLE public.customers;

CREATE TABLE public.customers (
	id int4 NOT NULL,
	firstname varchar(50) NOT NULL,
	lastname varchar(50) NOT NULL,
	address varchar(200) NULL,
	cp varchar(20) NULL,
	city varchar(50) NULL,
	email varchar(200) NOT NULL,
	created_at date NOT NULL,
	subscription_id int4 NULL,
	nb_orders int4 NULL,
	nb_subscriptions int4 NULL,
	CONSTRAINT customers_pkey PRIMARY KEY (id)
);


-- public.lines definition

-- Drop table

-- DROP TABLE public.lines;

CREATE TABLE public.lines (
	order_id int4 NOT NULL,
	product_id int4 NOT NULL,
	quantity int4 NOT NULL DEFAULT 1,
	price float4 NOT NULL DEFAULT 0.00,
	CONSTRAINT lines_pk PRIMARY KEY (order_id, product_id)
);
CREATE INDEX lines_order_id_idx ON public.lines USING btree (order_id);
CREATE INDEX lines_product_id_idx ON public.lines USING btree (product_id);


-- public.order_status definition

-- Drop table

-- DROP TABLE public.order_status;

CREATE TABLE public.order_status (
	"name" text NULL
);


-- public.payement_status definition

-- Drop table

-- DROP TABLE public.payement_status;

CREATE TABLE public.payement_status (
	"name" text NULL,
	CONSTRAINT payement_status_name_key UNIQUE (name)
);


-- public.product_status definition

-- Drop table

-- DROP TABLE public.product_status;

CREATE TABLE public.product_status (
	"name" text NULL
);


-- public.products definition

-- Drop table

-- DROP TABLE public.products;

CREATE TABLE public.products (
	id int4 NOT NULL,
	"name" text NULL,
	description text NULL,
	price float4 NULL DEFAULT 0.00,
	seller_id int4 NULL,
	status text NULL,
	category text NULL,
	CONSTRAINT products_id_key UNIQUE (id)
);


-- public.sellers definition

-- Drop table

-- DROP TABLE public.sellers;

CREATE TABLE public.sellers (
	id int4 NOT NULL,
	"name" text NOT NULL,
	email text NULL,
	nb_subscriptions int4 NULL DEFAULT 0.0,
	nb_orders int4 NULL DEFAULT 0,
	CONSTRAINT sellers_pkey PRIMARY KEY (id)
);


-- public.shipping_status definition

-- Drop table

-- DROP TABLE public.shipping_status;

CREATE TABLE public.shipping_status (
	"name" text NULL
);


-- public.subscription_days definition

-- Drop table

-- DROP TABLE public.subscription_days;

CREATE TABLE public.subscription_days (
	id int4 NOT NULL,
	day_of_week int4 NULL,
	price float4 NULL,
	shipping_price float4 NULL,
	subscription_id int4 NULL,
	nb_products int4 NULL,
	CONSTRAINT subscription_days_pkey PRIMARY KEY (id)
);


-- public.subscription_lines definition

-- Drop table

-- DROP TABLE public.subscription_lines;

CREATE TABLE public.subscription_lines (
	id int4 NOT NULL,
	subscription_day_id int4 NOT NULL,
	product_id int4 NOT NULL,
	quantity int4 NOT NULL,
	price float4 NOT NULL,
	CONSTRAINT subscription_lines_pkey PRIMARY KEY (id)
);


-- public.subscriptions definition

-- Drop table

-- DROP TABLE public.subscriptions;

CREATE TABLE public.subscriptions (
	id int4 NOT NULL,
	start_dt date NULL,
	end_dt date NULL,
	customer_id int4 NULL,
	shipping_price float4 NULL,
	price float4 NULL,
	status text NULL,
	payment_status text NULL,
	promotion text NULL,
	description text NULL,
	seller_id int4 NULL,
	nb_products int4 NULL,
	nb_orders int4 NULL,
	category text NULL,
	CONSTRAINT subscriptions_pkey PRIMARY KEY (id)
);


-- public.users definition

-- Drop table

-- DROP TABLE public.users;

CREATE TABLE public.users (
	id int4 NOT NULL,
	username text NULL,
	"password" text NULL,
	email text NULL,
	joined_at date NULL,
	is_admin int4 NULL,
	CONSTRAINT users_pkey PRIMARY KEY (id)
);


-- public.orders definition

-- Drop table

-- DROP TABLE public.orders;

CREATE TABLE public.orders (
	id int4 NOT NULL,
	title varchar(150) NOT NULL,
	shipping_dt date NULL,
	created_at date NOT NULL,
	customer_id int4 NOT NULL,
	status text NOT NULL DEFAULT 'CREE'::text,
	payment_status text NULL DEFAULT 'NON_PAYEE'::text,
	subscription_id int4 NULL,
	price float4 NULL,
	shipping_price float4 NULL,
	seller_id int4 NULL,
	shipping_status varchar NULL,
	shipping_rules text NULL,
	category text NULL,
	shipping_address text NULL,
	shipping_cp text NULL,
	shipping_city text NULL,
	nb_products int4 NULL,
	CONSTRAINT orders_pkey PRIMARY KEY (id),
	CONSTRAINT orders_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES customers(id)
);

CREATE SEQUENCE customer_id_seq;

-- Use it to provide a new value for each project ID
ALTER TABLE customers 
ALTER id 
SET DEFAULT NEXTVAL('customer_id_seq');

CREATE SEQUENCE order_id_seq;

-- Use it to provide a new value for each project ID
ALTER TABLE orders 
ALTER id 
SET DEFAULT NEXTVAL('order_id_seq');

CREATE SEQUENCE product_id_seq;

-- Use it to provide a new value for each project ID
ALTER TABLE products 
ALTER id 
SET DEFAULT NEXTVAL('product_id_seq');

CREATE SEQUENCE seller_id_seq;

-- Use it to provide a new value for each project ID
ALTER TABLE sellers 
ALTER id 
SET DEFAULT NEXTVAL('seller_id_seq');

CREATE SEQUENCE subscription_day_id_seq;

-- Use it to provide a new value for each project ID
ALTER TABLE subscription_days 
ALTER id 
SET DEFAULT NEXTVAL('subscription_day_id_seq');

CREATE SEQUENCE subscription_id_seq;

-- Use it to provide a new value for each project ID
ALTER TABLE subscriptions 
ALTER id 
SET DEFAULT NEXTVAL('subscription_id_seq');

CREATE SEQUENCE user_id_seq;

-- Use it to provide a new value for each project ID
ALTER TABLE users 
ALTER id 
SET DEFAULT NEXTVAL('user_id_seq');


ALTER SEQUENCE subscription_day_id_seq RESTART 20;

