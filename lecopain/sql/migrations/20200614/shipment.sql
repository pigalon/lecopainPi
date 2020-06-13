ALTER TABLE public.customers DROP nb_orders;
ALTER TABLE public.customers ADD nb_shipments int4 NULL;

ALTER TABLE public.orders DROP shipping_status;
ALTER TABLE public.orders DROP shipping_rules;
ALTER TABLE public.orders DROP category;
ALTER TABLE public.orders DROP shipping_address;
ALTER TABLE public.orders DROP shipping_cp;
ALTER TABLE public.orders DROP shipping_city;
ALTER TABLE public.orders DROP shipping_price;

ALTER TABLE public.orders DROP subscription_id;
ALTER TABLE public.orders ADD shipment_id text NULL;

ALTER TABLE public.subscription_lines ADD seller_id int4 NULL;

ALTER TABLE public.subscriptions ADD nb_shipments int4 NULL;




-- public.shipments definition

-- Drop table

-- DROP TABLE public.shipments;

CREATE TABLE public.shipments (
	id serial NOT NULL,
	title varchar(150) NOT NULL,
	shipping_dt date NULL,
	created_at date NOT NULL,
	customer_id int4 NOT NULL,
	status text NOT NULL DEFAULT 'CREE'::text,
	payment_status text NULL DEFAULT 'NON_PAYEE'::text,
	subscription_id int4 NULL,
	price float4 NULL,
	shipping_price float4 NULL,
	shipping_status varchar NULL,
	shipping_rules text NULL,
	category text NULL,
	shipping_address text NULL,
	shipping_cp text NULL,
	shipping_city text NULL,
	nb_products int4 NULL,
	updated_at date NULL,
	nb_orders int4 NULL,
	CONSTRAINT shipments_pkey PRIMARY KEY (id)
);


-- public.shipments foreign keys

ALTER TABLE public.shipments ADD CONSTRAINT shipments_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES customers(id);