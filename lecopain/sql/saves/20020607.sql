--
-- PostgreSQL database dump
--

-- Dumped from database version 12.3
-- Dumped by pg_dump version 12.3

-- Started on 2020-06-06 22:26:58 CEST

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 3 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO postgres;

--
-- TOC entry 3050 (class 0 OID 0)
-- Dependencies: 3
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA public IS 'standard public schema';


--
-- TOC entry 215 (class 1259 OID 24576)
-- Name: customer_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.customer_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.customer_id_seq OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 202 (class 1259 OID 16385)
-- Name: customers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.customers (
    id integer DEFAULT nextval('public.customer_id_seq'::regclass) NOT NULL,
    firstname character varying(50) NOT NULL,
    lastname character varying(50) NOT NULL,
    address character varying(200),
    cp character varying(20),
    city character varying(50),
    email character varying(200) NOT NULL,
    created_at date NOT NULL,
    subscription_id integer,
    nb_orders integer,
    nb_subscriptions integer
);


ALTER TABLE public.customers OWNER TO postgres;

--
-- TOC entry 203 (class 1259 OID 16393)
-- Name: lines; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.lines (
    order_id integer NOT NULL,
    product_id integer NOT NULL,
    quantity integer DEFAULT 1 NOT NULL,
    price real DEFAULT 0.00 NOT NULL
);


ALTER TABLE public.lines OWNER TO postgres;

--
-- TOC entry 216 (class 1259 OID 24579)
-- Name: order_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.order_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.order_id_seq OWNER TO postgres;

--
-- TOC entry 204 (class 1259 OID 16402)
-- Name: order_status; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.order_status (
    name text
);


ALTER TABLE public.order_status OWNER TO postgres;

--
-- TOC entry 214 (class 1259 OID 16473)
-- Name: orders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orders (
    id integer DEFAULT nextval('public.order_id_seq'::regclass) NOT NULL,
    title character varying(150) NOT NULL,
    shipping_dt date,
    created_at date NOT NULL,
    customer_id integer NOT NULL,
    status text DEFAULT 'CREE'::text NOT NULL,
    payment_status text DEFAULT 'NON_PAYEE'::text,
    subscription_id integer,
    price real,
    shipping_price real,
    seller_id integer,
    shipping_status character varying,
    shipping_rules text,
    category text,
    shipping_address text,
    shipping_cp text,
    shipping_city text,
    nb_products integer,
    updated_at date
);


ALTER TABLE public.orders OWNER TO postgres;

--
-- TOC entry 205 (class 1259 OID 16408)
-- Name: payement_status; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.payement_status (
    name text
);


ALTER TABLE public.payement_status OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 24582)
-- Name: product_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.product_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.product_id_seq OWNER TO postgres;

--
-- TOC entry 206 (class 1259 OID 16416)
-- Name: product_status; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.product_status (
    name text
);


ALTER TABLE public.product_status OWNER TO postgres;

--
-- TOC entry 207 (class 1259 OID 16422)
-- Name: products; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.products (
    id integer DEFAULT nextval('public.product_id_seq'::regclass) NOT NULL,
    name text,
    description text,
    price real DEFAULT 0.00,
    seller_id integer,
    status text,
    category text
);


ALTER TABLE public.products OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 24585)
-- Name: seller_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.seller_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.seller_id_seq OWNER TO postgres;

--
-- TOC entry 208 (class 1259 OID 16431)
-- Name: sellers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sellers (
    id integer DEFAULT nextval('public.seller_id_seq'::regclass) NOT NULL,
    name text NOT NULL,
    email text,
    nb_subscriptions integer DEFAULT 0.0,
    nb_orders integer DEFAULT 0
);


ALTER TABLE public.sellers OWNER TO postgres;

--
-- TOC entry 209 (class 1259 OID 16441)
-- Name: shipping_status; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.shipping_status (
    name text
);


ALTER TABLE public.shipping_status OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 24588)
-- Name: subscription_day_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.subscription_day_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.subscription_day_id_seq OWNER TO postgres;

--
-- TOC entry 210 (class 1259 OID 16447)
-- Name: subscription_days; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.subscription_days (
    id integer DEFAULT nextval('public.subscription_day_id_seq'::regclass) NOT NULL,
    day_of_week integer,
    price real,
    shipping_price real,
    subscription_id integer,
    nb_products integer
);


ALTER TABLE public.subscription_days OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 24591)
-- Name: subscription_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.subscription_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.subscription_id_seq OWNER TO postgres;

--
-- TOC entry 211 (class 1259 OID 16452)
-- Name: subscription_lines; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.subscription_lines (
    subscription_day_id integer NOT NULL,
    product_id integer NOT NULL,
    quantity integer NOT NULL,
    price real NOT NULL
);


ALTER TABLE public.subscription_lines OWNER TO postgres;

--
-- TOC entry 212 (class 1259 OID 16457)
-- Name: subscriptions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.subscriptions (
    id integer DEFAULT nextval('public.subscription_id_seq'::regclass) NOT NULL,
    start_dt date,
    end_dt date,
    customer_id integer,
    shipping_price real,
    price real,
    status text,
    payment_status text,
    promotion text,
    description text,
    seller_id integer,
    nb_products integer,
    nb_orders integer,
    category text
);


ALTER TABLE public.subscriptions OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 24594)
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_id_seq OWNER TO postgres;

--
-- TOC entry 213 (class 1259 OID 16465)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer DEFAULT nextval('public.user_id_seq'::regclass) NOT NULL,
    username text,
    password text,
    email text,
    joined_at date,
    is_admin integer
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 3025 (class 0 OID 16385)
-- Dependencies: 202
-- Data for Name: customers; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.customers VALUES (2, 'Pierre', 'Dujardin', '35, allée des jardins', '30120', 'Langlade', 'mail2@gmail.com', '2019-02-17', NULL, 0, 0);
INSERT INTO public.customers VALUES (3, 'Jean', 'Delatour', '54, rue de la madeleine', '30430', 'Caveirac', 'mail3@gmail.com', '2019-02-20', NULL, 2, 0);
INSERT INTO public.customers VALUES (4, 'Simone', 'Dupont', '11, allée des colibris', '30120', 'Langlade', 'mail4@gmail.com', '2019-02-22', NULL, 4, 0);
INSERT INTO public.customers VALUES (6, 'David', 'C.', '24, rue des pétunias', '13000', 'Marseille', 'dc@gmail.com', '2019-05-15', NULL, 3, 1);
INSERT INTO public.customers VALUES (5, 'Dan', 'Delarue', '1 place de moulin', '30120', 'Langlade', 'mail5@gmail.com', '2019-02-28', NULL, 24, 1);
INSERT INTO public.customers VALUES (7, 'Anouk', 'Sanglion', '8 rue des poupoux', '30000', 'NIMES', 'pio@noukey.com', '2019-05-18', NULL, 13, 1);


--
-- TOC entry 3026 (class 0 OID 16393)
-- Dependencies: 203
-- Data for Name: lines; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.lines VALUES (14, 5, 1, 0.6);
INSERT INTO public.lines VALUES (15, 2, 1, 2.35);
INSERT INTO public.lines VALUES (15, 3, 2, 1.1);
INSERT INTO public.lines VALUES (15, 5, 3, 0.6);
INSERT INTO public.lines VALUES (16, 5, 1, 0);
INSERT INTO public.lines VALUES (17, 5, 1, 0.6);
INSERT INTO public.lines VALUES (18, 5, 1, 0.6);
INSERT INTO public.lines VALUES (18, 4, 2, 1.3);
INSERT INTO public.lines VALUES (19, 3, 1, 1.1);
INSERT INTO public.lines VALUES (19, 4, 2, 1.3);
INSERT INTO public.lines VALUES (20, 4, 1, 1.3);
INSERT INTO public.lines VALUES (20, 3, 2, 1.1);
INSERT INTO public.lines VALUES (21, 3, 1, 1.1);
INSERT INTO public.lines VALUES (23, 5, 2, 0.6);
INSERT INTO public.lines VALUES (23, 2, 1, 2.35);
INSERT INTO public.lines VALUES (24, 5, 2, 0.6);
INSERT INTO public.lines VALUES (24, 2, 1, 2.35);
INSERT INTO public.lines VALUES (25, 5, 1, 0.6);
INSERT INTO public.lines VALUES (27, 5, 2, 0.6);
INSERT INTO public.lines VALUES (26, 5, 1, 0.6);
INSERT INTO public.lines VALUES (28, 3, 4, 1.1);
INSERT INTO public.lines VALUES (28, 4, 1, 9);
INSERT INTO public.lines VALUES (28, 5, 3, 1.3);
INSERT INTO public.lines VALUES (13, 2, 1, 2.36);
INSERT INTO public.lines VALUES (22, 4, 2, 1.3);
INSERT INTO public.lines VALUES (22, 5, 1, 0.6);
INSERT INTO public.lines VALUES (22, 2, 1, 2.36);
INSERT INTO public.lines VALUES (30, 5, 1, 0.6);
INSERT INTO public.lines VALUES (31, 8, 1, 14.9);
INSERT INTO public.lines VALUES (32, 8, 1, 14.9);
INSERT INTO public.lines VALUES (12, 3, 4, 1.1);
INSERT INTO public.lines VALUES (12, 4, 3, 1.3);
INSERT INTO public.lines VALUES (12, 5, 5, 0.6);
INSERT INTO public.lines VALUES (12, 2, 1, 2.36);
INSERT INTO public.lines VALUES (35, 5, 1, 0.6);
INSERT INTO public.lines VALUES (40, 4, 1, 1.3);
INSERT INTO public.lines VALUES (41, 1, 1, 0.65);
INSERT INTO public.lines VALUES (42, 2, 1, 2.36);
INSERT INTO public.lines VALUES (43, 4, 1, 1.3);
INSERT INTO public.lines VALUES (43, 5, 1, 0.6);
INSERT INTO public.lines VALUES (44, 5, 1, 0.6);
INSERT INTO public.lines VALUES (44, 3, 1, 1.1);
INSERT INTO public.lines VALUES (45, 1, 1, 0.65);
INSERT INTO public.lines VALUES (45, 3, 2, 1.1);
INSERT INTO public.lines VALUES (46, 1, 1, 0.65);
INSERT INTO public.lines VALUES (47, 1, 1, 0.65);
INSERT INTO public.lines VALUES (48, 1, 1, 0.65);
INSERT INTO public.lines VALUES (50, 1, 1, 0.95);
INSERT INTO public.lines VALUES (51, 4, 2, 1.3);
INSERT INTO public.lines VALUES (51, 1, 1, 0.95);
INSERT INTO public.lines VALUES (52, 3, 2, 1.1);
INSERT INTO public.lines VALUES (55, 4, 2, 1.3);
INSERT INTO public.lines VALUES (55, 1, 1, 0.95);
INSERT INTO public.lines VALUES (56, 3, 2, 1.1);
INSERT INTO public.lines VALUES (57, 4, 2, 1.3);
INSERT INTO public.lines VALUES (57, 1, 1, 0.95);
INSERT INTO public.lines VALUES (58, 3, 2, 1.1);
INSERT INTO public.lines VALUES (59, 4, 2, 1.3);
INSERT INTO public.lines VALUES (59, 1, 1, 0.95);
INSERT INTO public.lines VALUES (60, 3, 2, 1.1);
INSERT INTO public.lines VALUES (53, 4, 1, 1.3);
INSERT INTO public.lines VALUES (53, 1, 1, 0.95);
INSERT INTO public.lines VALUES (54, 3, 2, 1.1);
INSERT INTO public.lines VALUES (54, 1, 10, 0.95);
INSERT INTO public.lines VALUES (61, 5, 4, 0.6);
INSERT INTO public.lines VALUES (62, 5, 3, 0.6);
INSERT INTO public.lines VALUES (63, 10, 1, 0);
INSERT INTO public.lines VALUES (64, 1, 1, 0.95);


--
-- TOC entry 3027 (class 0 OID 16402)
-- Dependencies: 204
-- Data for Name: order_status; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.order_status VALUES ('ANNULEE');
INSERT INTO public.order_status VALUES ('LIVREE');
INSERT INTO public.order_status VALUES ('DEFAUT');
INSERT INTO public.order_status VALUES ('CREE');
INSERT INTO public.order_status VALUES ('PAYEE');


--
-- TOC entry 3037 (class 0 OID 16473)
-- Dependencies: 214
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.orders VALUES (12, 'Cmd urgente', '2019-04-01', '2020-05-09', 3, 'CREE', 'NON', NULL, NULL, NULL, 1, 'OUI', NULL, 'ARTICLE', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.orders VALUES (13, 'Commande express', '2019-03-13', '2019-06-15', 4, 'CREE', 'OUI', NULL, NULL, NULL, 1, 'OUI', NULL, 'ARTICLE', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.orders VALUES (14, 'test', '2019-03-22', '2019-03-05', 3, 'CREE', 'NON', NULL, NULL, NULL, 1, 'OUI', NULL, 'ARTICLE', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.orders VALUES (15, 'test-today', '2019-03-18', '2019-03-10', 5, 'ANNULEE', 'NON', NULL, NULL, NULL, 1, 'OUI', NULL, 'ARTICLE', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.orders VALUES (16, 'test', '2019-05-24', '2019-05-11', 5, 'CREE', 'NON', NULL, NULL, NULL, 1, 'OUI', NULL, 'ARTICLE', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.orders VALUES (17, 'test', '2019-05-24', '2019-05-11', 5, 'CREE', 'NON', NULL, NULL, NULL, 1, 'OUI', NULL, 'ARTICLE', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.orders VALUES (18, 'opop', '2019-05-14', '2019-05-12', 5, 'CREE', 'NON', NULL, NULL, NULL, 1, 'OUI', NULL, 'ARTICLE', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.orders VALUES (19, 'opop', '2019-05-14', '2019-05-12', 5, 'CREE', 'NON', NULL, NULL, NULL, 1, 'OUI', NULL, 'ARTICLE', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.orders VALUES (20, 'opop', '2019-05-14', '2019-05-12', 5, 'CREE', 'NON', NULL, NULL, NULL, 1, 'OUI', NULL, 'ARTICLE', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.orders VALUES (21, 'opop', '2019-05-14', '2019-05-12', 5, 'CREE', 'NON', NULL, NULL, NULL, 1, 'OUI', NULL, 'ARTICLE', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.orders VALUES (22, 'patato', '2019-06-06', '2019-06-15', 5, 'CREE', 'OUI', NULL, NULL, NULL, 1, 'NON', NULL, 'ARTICLE', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.orders VALUES (23, 'test_order', '2019-05-22', '2019-05-12', 5, 'CREE', 'NON', NULL, NULL, NULL, 1, 'OUI', NULL, 'ARTICLE', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.orders VALUES (24, 'test_order', '2019-05-22', '2019-05-12', 5, 'CREE', 'NON', NULL, NULL, NULL, 1, 'OUI', NULL, 'ARTICLE', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.orders VALUES (25, 'bofi', '2019-05-30', '2019-05-12', 5, 'CREE', 'NON', NULL, NULL, NULL, 1, 'OUI', NULL, 'ARTICLE', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.orders VALUES (26, 'bofu', '2019-06-07', '2019-05-12', 5, 'CREE', 'NON', NULL, NULL, NULL, 1, 'NON', NULL, 'ARTICLE', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.orders VALUES (27, 'la commande à tata', '2019-05-22', '2019-05-13', 5, 'CREE', 'NON', NULL, NULL, NULL, 1, 'NON', NULL, 'ARTICLE', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.orders VALUES (28, 'prout', '2019-06-12', '2019-06-08', 7, 'TERMINEE', 'NON', NULL, NULL, NULL, 1, 'OUI', NULL, 'ARTICLE', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.orders VALUES (30, 'test', '2019-06-21', '2020-05-03', 7, 'TERMINEE', 'NON', NULL, NULL, NULL, 1, 'OUI', NULL, 'ARTICLE', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.orders VALUES (31, 'test', '2020-05-03', '2020-05-03', 7, 'CREE', 'OUI', NULL, NULL, NULL, 1, 'OUI', NULL, 'ARTICLE', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.orders VALUES (32, 'testr', '2020-05-06', '2020-05-06', 7, 'CREE', 'OUI', NULL, NULL, NULL, 1, 'OUI', NULL, 'ARTICLE', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.orders VALUES (34, 'Anouk ette', '2020-05-09', '2020-05-09', 7, 'CREE', 'OUI', NULL, NULL, NULL, 1, 'OUI', NULL, 'ARTICLE', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.orders VALUES (35, 'testo', '2020-05-10', '2020-05-10', 4, 'CREE', 'OUI', NULL, NULL, NULL, 1, 'OUI', NULL, 'ARTICLE', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.orders VALUES (40, 'test', '2020-05-23', '2020-05-10', 7, 'CREE', 'OUI', NULL, NULL, NULL, 1, 'NON', NULL, 'ARTICLE', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.orders VALUES (41, 'tout', '2020-05-12', '2020-05-12', 7, 'CREE', 'OUI', NULL, NULL, NULL, 1, 'NON', NULL, 'ARTICLE', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.orders VALUES (42, 'toutou', '2020-05-13', '2020-05-13', 7, 'CREE', 'OUI', NULL, NULL, NULL, 1, 'NON', NULL, 'ARTICLE', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.orders VALUES (43, 'testr', '2020-05-17', '2020-05-16', 7, 'CREE', 'NON', NULL, NULL, NULL, 1, 'NON', NULL, 'ARTICLE', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.orders VALUES (44, 'haha', '2020-05-16', '2020-05-16', 7, 'CREE', 'NON', NULL, NULL, NULL, 1, 'NON', NULL, 'ARTICLE', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.orders VALUES (45, 'benelux', '2020-05-19', '2020-05-19', 7, 'CREE', 'NON', NULL, 2.85, 1.75, 1, 'NON', 'article_non-local_3', 'ARTICLE', '8 rue des poupoux', '30000', 'NIMES', 3, NULL);
INSERT INTO public.orders VALUES (46, 'testr', '2020-05-22', '2020-05-22', 4, 'CREE', 'NON', NULL, 0.65, 0.6, 1, 'NON', 'article_local_1', 'ARTICLE', '11, allée des colibris', '30120', 'Langlade', 1, NULL);
INSERT INTO public.orders VALUES (47, 'pouf', '2020-05-25', '2020-05-25', 6, 'CREE', 'OUI', NULL, 0.65, 0.65, 1, 'NON', 'article_non-local_1', 'ARTICLE', '24, rue des pétunias', '13000', 'Marseille', 1, NULL);
INSERT INTO public.orders VALUES (48, 'abo 1 - 1/6', '2020-05-25', '2020-05-26', 7, 'CREE', 'NON', 1, 0.65, 0.65, 1, 'NON', 'article_non-local_1', 'ARTICLE', '8 rue des poupoux', '30000', 'NIMES', 1, NULL);
INSERT INTO public.orders VALUES (50, 'trt', '2020-05-26', '2020-05-29', 6, 'CREE', 'NON', NULL, 0.95, 0.65, 1, 'NON', 'article_non-local_1', 'ARTICLE', '24, rue des pétunias', '13000', 'Marseille', 1, NULL);
INSERT INTO public.orders VALUES (57, 'abo 5 - 22/29', '2020-06-22', '2020-06-04', 5, 'CREE', 'NON', 5, 3.55, 1.62, 1, 'NON', 'article_local_3', 'ARTICLE', '1 place de moulin', '30120', 'Langlade', 3, NULL);
INSERT INTO public.orders VALUES (51, 'abo 5 - 1/29', '2020-06-01', '2020-06-04', 5, 'CREE', 'NON', 5, 3.55, 1.62, 1, 'NON', 'article_local_3', 'ARTICLE', '1 place de moulin', '30120', 'Langlade', 3, NULL);
INSERT INTO public.orders VALUES (62, 'pain langlade', '2020-06-04', '2020-06-04', 6, 'CREE', 'NON', NULL, 1.8, 1.75, 1, 'NON', 'article_non-local_3', 'ARTICLE', '24, rue des pétunias', '13000', 'Marseille', 3, NULL);
INSERT INTO public.orders VALUES (52, 'abo 5 - 2/29', '2020-06-02', '2020-06-04', 5, 'CREE', 'NON', 5, 2.2, 1.16, 1, 'NON', 'article_local_2', 'ARTICLE', '1 place de moulin', '30120', 'Langlade', 2, NULL);
INSERT INTO public.orders VALUES (58, 'abo 5 - 23/29', '2020-06-23', '2020-06-04', 5, 'CREE', 'NON', 5, 2.2, 1.16, 1, 'NON', 'article_local_2', 'ARTICLE', '1 place de moulin', '30120', 'Langlade', 2, NULL);
INSERT INTO public.orders VALUES (59, 'abo 5 - 29/29', '2020-06-29', '2020-06-04', 5, 'CREE', 'NON', 5, 3.55, 1.62, 1, 'NON', 'article_local_3', 'ARTICLE', '1 place de moulin', '30120', 'Langlade', 3, NULL);
INSERT INTO public.orders VALUES (55, 'abo 5 - 15/29', '2020-06-15', '2020-06-04', 5, 'CREE', 'NON', 5, 3.55, 1.62, 1, 'NON', 'article_local_3', 'ARTICLE', '1 place de moulin', '30120', 'Langlade', 3, NULL);
INSERT INTO public.orders VALUES (56, 'abo 5 - 16/29', '2020-06-16', '2020-06-04', 5, 'CREE', 'NON', 5, 2.2, 1.16, 1, 'NON', 'article_local_2', 'ARTICLE', '1 place de moulin', '30120', 'Langlade', 2, NULL);
INSERT INTO public.orders VALUES (60, 'abo 5 - 30/29', '2020-06-30', '2020-06-04', 5, 'CREE', 'NON', 5, 2.2, 1.16, 1, 'NON', 'article_local_2', 'ARTICLE', '1 place de moulin', '30120', 'Langlade', 2, NULL);
INSERT INTO public.orders VALUES (63, '', '2020-06-04', '2020-06-04', 5, 'ANNULEE', 'OUI', NULL, 0, 0.6, 5, 'NON', 'article_local_1', 'COURSETTE', '1 place de moulin', '30120', 'Langlade', 1, NULL);
INSERT INTO public.orders VALUES (53, 'abo 5 - 8/29', '2020-06-08', '2020-06-04', 5, 'CREE', 'NON', 5, 2.25, 1.16, 1, 'NON', 'article_local_2', 'ARTICLE', '1 place de moulin', '30120', 'Langlade', 2, NULL);
INSERT INTO public.orders VALUES (54, 'abo 5 - 9/29', '2020-06-09', '2020-06-04', 5, 'CREE', 'NON', 5, 11.7, 5, 1, 'NON', 'article_local_12', 'ARTICLE', '1 place de moulin', '30120', 'Langlade', 12, NULL);
INSERT INTO public.orders VALUES (61, '', '2020-06-10', '2020-06-04', 4, 'CREE', 'NON', NULL, 2.4, 2.05, 1, 'NON', 'article_local_4', 'ARTICLE', '11, allée des colibris', '30120', 'Langlade', 4, NULL);
INSERT INTO public.orders VALUES (64, '', '2020-06-05', '2020-06-05', 7, 'CREE', 'NON', NULL, 0.95, 0.65, 1, 'NON', 'article_non-local_1', 'ARTICLE', '8 rue des poupoux', '30000', 'NIMES', 1, NULL);


--
-- TOC entry 3028 (class 0 OID 16408)
-- Dependencies: 205
-- Data for Name: payement_status; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3029 (class 0 OID 16416)
-- Dependencies: 206
-- Data for Name: product_status; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.product_status VALUES ('DISPONIBLE');
INSERT INTO public.product_status VALUES ('INDISPONIBLE');


--
-- TOC entry 3030 (class 0 OID 16422)
-- Dependencies: 207
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.products VALUES (1, 'croissant', '', 0.95, 1, 'DISPONIBLE', 'ARTICLE');
INSERT INTO public.products VALUES (2, 'tarte tatin', 'test', 2.36, 1, 'DISPONIBLE', 'ARTICLE');
INSERT INTO public.products VALUES (3, 'baguette', '', 1.1, 1, NULL, 'ARTICLE');
INSERT INTO public.products VALUES (4, 'banette', NULL, 1.3, 1, NULL, 'ARTICLE');
INSERT INTO public.products VALUES (5, 'pain au chocolat', NULL, 0.6, 1, NULL, 'ARTICLE');
INSERT INTO public.products VALUES (8, 'poupée pop', '', 14.9, 2, 'DISPONIBLE', 'ARTICLE');
INSERT INTO public.products VALUES (10, 'Village', '', 0, 5, 'DISPONIBLE', 'COURSETTE');


--
-- TOC entry 3031 (class 0 OID 16431)
-- Dependencies: 208
-- Data for Name: sellers; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.sellers VALUES (2, 'Epicerie de Caveirac', 'test@test.comu', 0, 0);
INSERT INTO public.sellers VALUES (5, 'lecopain', 'lecopains@gmail.com', 0, 1);
INSERT INTO public.sellers VALUES (1, 'Boulanger Langlade', 'boubou@lange.fr', 3, 15);


--
-- TOC entry 3032 (class 0 OID 16441)
-- Dependencies: 209
-- Data for Name: shipping_status; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.shipping_status VALUES ('NON_LIVREE');
INSERT INTO public.shipping_status VALUES ('LIVREE');
INSERT INTO public.shipping_status VALUES ('ANNULEE');
INSERT INTO public.shipping_status VALUES ('EN_DEFAULT');


--
-- TOC entry 3033 (class 0 OID 16447)
-- Dependencies: 210
-- Data for Name: subscription_days; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.subscription_days VALUES (1, 1, 0.65, 0.65, 1, 1);
INSERT INTO public.subscription_days VALUES (2, 2, 0, 0, 1, 0);
INSERT INTO public.subscription_days VALUES (3, 3, 0, 0, 1, 0);
INSERT INTO public.subscription_days VALUES (4, 4, 0, 0, 1, 0);
INSERT INTO public.subscription_days VALUES (5, 5, 0, 0, 1, 0);
INSERT INTO public.subscription_days VALUES (6, 6, 0, 0, 1, 0);
INSERT INTO public.subscription_days VALUES (7, 7, 0, 0, 1, 0);
INSERT INTO public.subscription_days VALUES (8, 1, 0, 0, 2, 0);
INSERT INTO public.subscription_days VALUES (9, 2, 0, 0, 2, 0);
INSERT INTO public.subscription_days VALUES (10, 3, 0, 0, 2, 0);
INSERT INTO public.subscription_days VALUES (11, 4, 0, 0, 2, 0);
INSERT INTO public.subscription_days VALUES (12, 5, 0, 0, 2, 0);
INSERT INTO public.subscription_days VALUES (13, 6, 0, 0, 2, 0);
INSERT INTO public.subscription_days VALUES (14, 7, 0, 0, 2, 0);
INSERT INTO public.subscription_days VALUES (20, 1, 0, 0, 4, 0);
INSERT INTO public.subscription_days VALUES (21, 2, 0, 0, 4, 0);
INSERT INTO public.subscription_days VALUES (22, 3, 0, 0, 4, 0);
INSERT INTO public.subscription_days VALUES (23, 4, 0, 0, 4, 0);
INSERT INTO public.subscription_days VALUES (24, 5, 0, 0, 4, 0);
INSERT INTO public.subscription_days VALUES (25, 6, 0, 0, 4, 0);
INSERT INTO public.subscription_days VALUES (26, 7, 0, 0, 4, 0);
INSERT INTO public.subscription_days VALUES (29, 3, 0, 0, 5, 0);
INSERT INTO public.subscription_days VALUES (30, 4, 0, 0, 5, 0);
INSERT INTO public.subscription_days VALUES (31, 5, 0, 0, 5, 0);
INSERT INTO public.subscription_days VALUES (32, 6, 0, 0, 5, 0);
INSERT INTO public.subscription_days VALUES (33, 7, 0, 0, 5, 0);
INSERT INTO public.subscription_days VALUES (27, 1, 3.55, 1.62, 5, 3);
INSERT INTO public.subscription_days VALUES (28, 2, 2.2, 1.16, 5, 2);


--
-- TOC entry 3034 (class 0 OID 16452)
-- Dependencies: 211
-- Data for Name: subscription_lines; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.subscription_lines VALUES (1, 1, 1, 0.65);
INSERT INTO public.subscription_lines VALUES (27, 4, 2, 1.3);
INSERT INTO public.subscription_lines VALUES (27, 1, 1, 0.95);
INSERT INTO public.subscription_lines VALUES (28, 3, 2, 1.1);


--
-- TOC entry 3035 (class 0 OID 16457)
-- Dependencies: 212
-- Data for Name: subscriptions; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.subscriptions VALUES (1, '2020-05-25', '2020-05-31', 7, 0.65, 0.65, 'CREE', NULL, NULL, NULL, 1, 1, 1, 'ARTICLE');
INSERT INTO public.subscriptions VALUES (2, '2020-04-01', '2020-04-30', 6, 0, 0, 'CREE', NULL, NULL, NULL, 2, 0, 0, 'ARTICLE');
INSERT INTO public.subscriptions VALUES (4, '2020-05-25', '2020-05-31', 6, 0, 0, 'CREE', NULL, NULL, NULL, 1, 0, 0, 'ARTICLE');
INSERT INTO public.subscriptions VALUES (5, '2020-06-01', '2020-06-30', 5, 17.28, 36.95, 'CREE', NULL, NULL, NULL, 1, 34, 10, 'ARTICLE');


--
-- TOC entry 3036 (class 0 OID 16465)
-- Dependencies: 213
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.users VALUES (1, 'lecopain', 'pbkdf2:sha256:150000$12kz7VyS$caa1e8c354f3d1d5e04f488449ab06039bc0ed8af503ddf59ccdc588841af1a7', 'pigalon@gmail.com', NULL, 1);
INSERT INTO public.users VALUES (2, NULL, NULL, NULL, NULL, NULL);


--
-- TOC entry 3051 (class 0 OID 0)
-- Dependencies: 215
-- Name: customer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.customer_id_seq', 8, false);


--
-- TOC entry 3052 (class 0 OID 0)
-- Dependencies: 216
-- Name: order_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.order_id_seq', 64, true);


--
-- TOC entry 3053 (class 0 OID 0)
-- Dependencies: 217
-- Name: product_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.product_id_seq', 10, true);


--
-- TOC entry 3054 (class 0 OID 0)
-- Dependencies: 218
-- Name: seller_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.seller_id_seq', 5, true);


--
-- TOC entry 3055 (class 0 OID 0)
-- Dependencies: 219
-- Name: subscription_day_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.subscription_day_id_seq', 33, true);


--
-- TOC entry 3056 (class 0 OID 0)
-- Dependencies: 220
-- Name: subscription_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.subscription_id_seq', 5, true);


--
-- TOC entry 3057 (class 0 OID 0)
-- Dependencies: 221
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_id_seq', 5, false);


--
-- TOC entry 2877 (class 2606 OID 16392)
-- Name: customers customers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_pkey PRIMARY KEY (id);


--
-- TOC entry 2880 (class 2606 OID 16399)
-- Name: lines lines_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lines
    ADD CONSTRAINT lines_pk PRIMARY KEY (order_id, product_id);


--
-- TOC entry 2897 (class 2606 OID 16482)
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id);


--
-- TOC entry 2883 (class 2606 OID 16415)
-- Name: payement_status payement_status_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payement_status
    ADD CONSTRAINT payement_status_name_key UNIQUE (name);


--
-- TOC entry 2885 (class 2606 OID 16430)
-- Name: products products_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_id_key UNIQUE (id);


--
-- TOC entry 2887 (class 2606 OID 16440)
-- Name: sellers sellers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sellers
    ADD CONSTRAINT sellers_pkey PRIMARY KEY (id);


--
-- TOC entry 2889 (class 2606 OID 16451)
-- Name: subscription_days subscription_days_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subscription_days
    ADD CONSTRAINT subscription_days_pkey PRIMARY KEY (id);


--
-- TOC entry 2891 (class 2606 OID 24606)
-- Name: subscription_lines subscription_lines_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subscription_lines
    ADD CONSTRAINT subscription_lines_pk PRIMARY KEY (product_id, subscription_day_id);


--
-- TOC entry 2893 (class 2606 OID 16464)
-- Name: subscriptions subscriptions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subscriptions
    ADD CONSTRAINT subscriptions_pkey PRIMARY KEY (id);


--
-- TOC entry 2895 (class 2606 OID 16472)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 2878 (class 1259 OID 16400)
-- Name: lines_order_id_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX lines_order_id_idx ON public.lines USING btree (order_id);


--
-- TOC entry 2881 (class 1259 OID 16401)
-- Name: lines_product_id_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX lines_product_id_idx ON public.lines USING btree (product_id);


--
-- TOC entry 2898 (class 2606 OID 16483)
-- Name: orders orders_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(id);


-- Completed on 2020-06-06 22:27:01 CEST

--
-- PostgreSQL database dump complete
--

