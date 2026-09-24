--
-- PostgreSQL database dump
--

\restrict eLlvQYon9Lq2amDpS0WskgY7FtM77ZaB1zpmCZSGf0PkdwM0GWxdom3hhSBh9Fl

-- Dumped from database version 18.3
-- Dumped by pg_dump version 18.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: chalan_log; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.chalan_log (
    id integer NOT NULL,
    chalan_id integer,
    user_id integer,
    plate_number character varying(20),
    violation_name character varying(100),
    fine integer,
    image_path text,
    whatsapp_status character varying(30) DEFAULT 'PENDING'::character varying,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: chalan_log_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.chalan_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: chalan_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.chalan_log_id_seq OWNED BY public.chalan_log.id;


--
-- Name: violations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.violations (
    id integer NOT NULL,
    violation_name character varying(100) NOT NULL,
    fine integer NOT NULL
);


--
-- Name: violations_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.violations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: violations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.violations_id_seq OWNED BY public.violations.id;


--
-- Name: chalan_log id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chalan_log ALTER COLUMN id SET DEFAULT nextval('public.chalan_log_id_seq'::regclass);


--
-- Name: violations id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.violations ALTER COLUMN id SET DEFAULT nextval('public.violations_id_seq'::regclass);


--
-- Data for Name: chalan_log; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.chalan_log (id, chalan_id, user_id, plate_number, violation_name, fine, image_path, whatsapp_status, created_at) FROM stdin;
1	\N	7	MH12AB3456	No Helmet, Triple Ride	1200	C:\\Users\\sachi\\Documents\\Naresh It\\traffic-chalan-automation\\data\\input\\test9.jpg	PENDING	2026-09-18 17:28:13.109033
2	\N	7	MH12AB3456	No Helmet, Triple Ride	1200	C:\\Users\\sachi\\Documents\\Naresh It\\traffic-chalan-automation\\data\\input\\test9.jpg	PENDING	2026-09-18 17:30:26.581544
3	\N	4	OD05CC9099	No Helmet, Triple Ride	1200	C:\\Users\\sachi\\Documents\\Naresh It\\traffic-chalan-automation\\data\\input\\test4.jpg	PENDING	2026-09-18 17:34:23.556282
4	\N	4	OD05CC9099	No Helmet, Triple Ride	1200	C:\\Users\\sachi\\Documents\\Naresh It\\traffic-chalan-automation\\data\\input\\test4.jpg	PENDING	2026-09-18 17:36:17.228315
5	\N	1	UK06AR2131	No Parking	100	C:\\Users\\sachi\\Documents\\Naresh It\\traffic-chalan-automation\\data\\input\\test1.jpg	PENDING	2026-09-18 17:37:14.911128
6	\N	4	OD05CC9099	No Helmet, Triple Ride	1200	C:\\Users\\sachi\\Documents\\Naresh It\\traffic-chalan-automation\\data\\input\\test4.jpg	PENDING	2026-09-18 17:37:55.380491
7	\N	4	OD05CC9099	No Helmet, Triple Ride	1200	C:\\Users\\sachi\\Documents\\Naresh It\\traffic-chalan-automation\\data\\input\\test4.jpg	PENDING	2026-09-18 17:38:46.390708
8	\N	4	OD05CC9099	No Helmet, Triple Ride	1200	C:\\Users\\sachi\\Documents\\Naresh It\\traffic-chalan-automation\\data\\input\\test4.jpg	PENDING	2026-09-18 17:42:20.619577
9	\N	7	MH12AB3456	No Parking	100	C:\\Users\\sachi\\Documents\\Naresh It\\traffic-chalan-automation\\data\\input\\test8.jpg	PENDING	2026-09-18 17:42:57.95378
10	\N	3	TS09EA4321	No Parking	100	data/input/test3.jpg	PENDING	2026-09-18 18:07:52.625904
11	\N	3	TS09EA4321	No Parking	100	data/input/test3.jpg	PENDING	2026-09-18 19:17:40.693217
12	\N	5	MH02AB1234	No Helmet	200	C:\\Users\\sachi\\Documents\\Naresh It\\traffic-chalan-automation\\data\\input\\test5.jpg	PENDING	2026-09-18 19:20:39.298902
13	\N	4	OD05CC9099	No Helmet, Triple Ride	1200	C:\\Users\\sachi\\Documents\\Naresh It\\traffic-chalan-automation\\data\\input\\test4.jpg	PENDING	2026-09-18 19:21:13.131571
14	\N	4	OD05CC9099	No Helmet, Triple Ride	1200	/app/data/input/test4.jpg	PENDING	2026-09-20 19:36:10.790169
15	\N	3	TS09EA4321	No Parking	100	/app/data/input/test3.jpg	PENDING	2026-09-20 19:37:10.921659
16	\N	7	MH12AB3456	No Parking	100	/app/data/input/test8.jpg	PENDING	2026-09-20 19:38:14.484065
17	\N	8	MH01AR1234	No Helmet, Overspeed	1200	/app/data/input/test10.jpg	PENDING	2026-09-20 19:38:54.169052
18	\N	4	OD05CC9099	No Helmet, Triple Ride	1200	/app/data/input/test4.jpg	PENDING	2026-09-20 19:54:50.962918
\.


--
-- Data for Name: violations; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.violations (id, violation_name, fine) FROM stdin;
1	No Helmet	200
2	No Parking	100
3	Triple Ride	1000
4	Overspeed	1000
\.


--
-- Name: chalan_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.chalan_log_id_seq', 18, true);


--
-- Name: violations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.violations_id_seq', 4, true);


--
-- Name: chalan_log chalan_log_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chalan_log
    ADD CONSTRAINT chalan_log_pkey PRIMARY KEY (id);


--
-- Name: violations violations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.violations
    ADD CONSTRAINT violations_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

\unrestrict eLlvQYon9Lq2amDpS0WskgY7FtM77ZaB1zpmCZSGf0PkdwM0GWxdom3hhSBh9Fl

