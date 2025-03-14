--
-- PostgreSQL database dump
--

-- Dumped from database version 17.2
-- Dumped by pg_dump version 17.2

-- Started on 2025-03-14 10:40:27

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

--
-- TOC entry 851 (class 1247 OID 24680)
-- Name: game_result; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.game_result AS ENUM (
    'draw',
    'player1_win',
    'player2_win'
);


ALTER TYPE public.game_result OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 220 (class 1259 OID 24698)
-- Name: game; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.game (
    id integer NOT NULL,
    player1id integer NOT NULL,
    player2id integer NOT NULL,
    board text NOT NULL,
    is_finished boolean DEFAULT false,
    result text
);


ALTER TABLE public.game OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 24697)
-- Name: game_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.game_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.game_id_seq OWNER TO postgres;

--
-- TOC entry 4880 (class 0 OID 0)
-- Dependencies: 219
-- Name: game_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.game_id_seq OWNED BY public.game.id;


--
-- TOC entry 218 (class 1259 OID 24688)
-- Name: queue; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.queue (
    id integer NOT NULL,
    playerip character varying(50) NOT NULL,
    port integer NOT NULL,
    pseudo character varying(50) NOT NULL,
    entrance_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    isingame boolean DEFAULT false
);


ALTER TABLE public.queue OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 24687)
-- Name: queue_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.queue_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.queue_id_seq OWNER TO postgres;

--
-- TOC entry 4881 (class 0 OID 0)
-- Dependencies: 217
-- Name: queue_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.queue_id_seq OWNED BY public.queue.id;


--
-- TOC entry 222 (class 1259 OID 24719)
-- Name: round; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.round (
    id integer NOT NULL,
    game_id integer NOT NULL,
    move character varying(50) NOT NULL,
    player_turn integer NOT NULL
);


ALTER TABLE public.round OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 24718)
-- Name: round_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.round_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.round_id_seq OWNER TO postgres;

--
-- TOC entry 4882 (class 0 OID 0)
-- Dependencies: 221
-- Name: round_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.round_id_seq OWNED BY public.round.id;


--
-- TOC entry 4711 (class 2604 OID 24701)
-- Name: game id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game ALTER COLUMN id SET DEFAULT nextval('public.game_id_seq'::regclass);


--
-- TOC entry 4708 (class 2604 OID 24691)
-- Name: queue id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.queue ALTER COLUMN id SET DEFAULT nextval('public.queue_id_seq'::regclass);


--
-- TOC entry 4713 (class 2604 OID 24722)
-- Name: round id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.round ALTER COLUMN id SET DEFAULT nextval('public.round_id_seq'::regclass);


--
-- TOC entry 4872 (class 0 OID 24698)
-- Dependencies: 220
-- Data for Name: game; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.game (id, player1id, player2id, board, is_finished, result) FROM stdin;
\.


--
-- TOC entry 4870 (class 0 OID 24688)
-- Dependencies: 218
-- Data for Name: queue; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.queue (id, playerip, port, pseudo, entrance_date, isingame) FROM stdin;
\.


--
-- TOC entry 4874 (class 0 OID 24719)
-- Dependencies: 222
-- Data for Name: round; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.round (id, game_id, move, player_turn) FROM stdin;
\.


--
-- TOC entry 4883 (class 0 OID 0)
-- Dependencies: 219
-- Name: game_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.game_id_seq', 90636, true);


--
-- TOC entry 4884 (class 0 OID 0)
-- Dependencies: 217
-- Name: queue_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.queue_id_seq', 259, true);


--
-- TOC entry 4885 (class 0 OID 0)
-- Dependencies: 221
-- Name: round_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.round_id_seq', 455, true);


--
-- TOC entry 4717 (class 2606 OID 24707)
-- Name: game game_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game
    ADD CONSTRAINT game_pkey PRIMARY KEY (id);


--
-- TOC entry 4715 (class 2606 OID 24694)
-- Name: queue queue_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.queue
    ADD CONSTRAINT queue_pkey PRIMARY KEY (id);


--
-- TOC entry 4719 (class 2606 OID 24724)
-- Name: round round_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.round
    ADD CONSTRAINT round_pkey PRIMARY KEY (id);


--
-- TOC entry 4720 (class 2606 OID 24746)
-- Name: game game_player1id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game
    ADD CONSTRAINT game_player1id_fkey FOREIGN KEY (player1id) REFERENCES public.queue(id) ON DELETE CASCADE;


--
-- TOC entry 4721 (class 2606 OID 24751)
-- Name: game game_player2id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game
    ADD CONSTRAINT game_player2id_fkey FOREIGN KEY (player2id) REFERENCES public.queue(id) ON DELETE CASCADE;


--
-- TOC entry 4722 (class 2606 OID 24756)
-- Name: round round_game_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.round
    ADD CONSTRAINT round_game_id_fkey FOREIGN KEY (game_id) REFERENCES public.game(id) ON DELETE CASCADE;


--
-- TOC entry 4723 (class 2606 OID 24761)
-- Name: round round_player_turn_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.round
    ADD CONSTRAINT round_player_turn_fkey FOREIGN KEY (player_turn) REFERENCES public.queue(id) ON DELETE CASCADE;


-- Completed on 2025-03-14 10:40:27

--
-- PostgreSQL database dump complete
--

