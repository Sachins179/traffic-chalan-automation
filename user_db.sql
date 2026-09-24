--
-- PostgreSQL database dump
--

\restrict YTZjUdvlwe3VpZWJSagMdjyla3ZSesOnmGcyVTxl9ZWkyh3wT2Rhffr94YdZ8Xo

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
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    vehicle_registration_number character varying(50) NOT NULL,
    vehicle_type character varying(50) NOT NULL,
    vehicle_number character varying(50) NOT NULL,
    mobile character varying(15) NOT NULL
);


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.users (id, name, vehicle_registration_number, vehicle_type, vehicle_number, mobile) FROM stdin;
1	Rajesh Kumar	UK06AR2131	Car	UK06AR2131	7684051736
2	Amit Sharma	TS07EK1234	Car	TS07EK1234	7684051736
3	Priya Verma	TS09EA4321	Car	TS09EA4321	7684051736
4	Sunita Devi	OD05CC9099	Scooter	OD05CC9099	7684051736
5	Rahul Patil	MH02AB1234	Bike	MH02AB1234	7684051736
6	Neha Joshi	RJ14AB4521	Bike	RJ14AB4521	7684051736
7	Vikram Singh	MH12AB3456	Car	MH12AB3456	7684051736
8	Anjali Nair	MH01AR1234	Scooter	MH01AR1234	7684051736
9	Deepak Yadav	MH01AB1234	Scooter	MH01AB1234	7684051736
10	Sanjay Gupta	TS07AZ5678	Bike	TS07AZ5678	7684051736
\.


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.users_id_seq', 10, true);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

\unrestrict YTZjUdvlwe3VpZWJSagMdjyla3ZSesOnmGcyVTxl9ZWkyh3wT2Rhffr94YdZ8Xo

