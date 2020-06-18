CREATE TABLE public.categories (
    id integer DEFAULT nextval('public.category_id_seq'::regclass) NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE public.categories OWNER TO postgres;

CREATE TABLE public.specifications (
    id integer DEFAULT nextval('public.category_id_seq'::regclass) NOT NULL,
    name character varying(50) NOT NULL
    subscription_id integer,
);


ALTER TABLE public.specifications OWNER TO postgres;

ALTER TABLE ONLY public.specifications
    ADD CONSTRAINT specifications_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(id);


ALTER TABLE public.products ADD type_id varchar NULL;
ALTER TABLE public.products ADD category_id varchar NULL;

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(id);

