CREATE SEQUENCE public.category_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE SEQUENCE public.specification_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


CREATE TABLE public.categories (
    id integer DEFAULT nextval('public.category_id_seq'::regclass) NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE public.categories OWNER TO postgres;

CREATE TABLE public.specifications (
    id integer DEFAULT nextval('public.specification_id_seq'::regclass) NOT NULL,
    name character varying(50) NOT NULL,
    subscription_id integer
);


ALTER TABLE public.specifications OWNER TO postgres;

ALTER TABLE ONLY public.categories
ADD CONSTRAINT categories_pkey PRIMARY KEY
(id);

ALTER TABLE ONLY public.specifications
ADD CONSTRAINT specifications_pkey PRIMARY KEY
(id);

ALTER TABLE ONLY public.specifications
    ADD CONSTRAINT specifications_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(id);


ALTER TABLE public.products ADD type_id integer NULL;
ALTER TABLE public.products ADD category_id integer NULL;

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(id);

ALTER TABLE public.lines ADD specifications integer[];
ALTER TABLE public.subscription_lines ADD specifications integer[];

SELECT pg_catalog.setval('public.category_id_seq', 1, true);

SELECT pg_catalog.setval('public.specification_id_seq', 1, true);