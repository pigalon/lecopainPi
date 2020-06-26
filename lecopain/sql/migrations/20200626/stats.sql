-- Table: public.stats

-- DROP TABLE public.stats;

CREATE TABLE public.stats
(
    id integer NOT NULL DEFAULT 1,
    updated_at timestamp without time zone
)

TABLESPACE pg_default;

ALTER TABLE public.stats
    OWNER to postgres;

INSERT INTO public.stats(
	id, updated_at)
	VALUES (1, '2020-06-26 19:41:00');