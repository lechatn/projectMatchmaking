--
-- PostgreSQL database dump
--

-- Dumped from database version 17.2
-- Dumped by pg_dump version 17.2

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
-- Name: game_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.game_id_seq OWNED BY public.game.id;


--
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
-- Name: queue_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.queue_id_seq OWNED BY public.queue.id;


--
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
-- Name: round_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.round_id_seq OWNED BY public.round.id;


--
-- Name: game id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game ALTER COLUMN id SET DEFAULT nextval('public.game_id_seq'::regclass);


--
-- Name: queue id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.queue ALTER COLUMN id SET DEFAULT nextval('public.queue_id_seq'::regclass);


--
-- Name: round id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.round ALTER COLUMN id SET DEFAULT nextval('public.round_id_seq'::regclass);


--
-- Data for Name: game; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.game (id, player1id, player2id, board, is_finished, result) FROM stdin;
90611	229	230	XNOXOXXNO	t	winX
62154	217	218	XOXXOXOXO	t	draw
62155	219	220	XOOXXXNON	t	winX
62156	221	222	NNNNNNNNN	f	null
90612	231	232	XONXONXNN	t	winX
66043	224	225	NNNNNNNNN	f	null
82644	227	228	NNNNNNNNN	f	null
\.


--
-- Data for Name: queue; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.queue (id, playerip, port, pseudo, entrance_date, isingame) FROM stdin;
217	127.0.0.1	13377	Noe	2025-03-13 14:30:42.011355	t
218	127.0.0.1	13386	Noa	2025-03-13 14:30:47.020765	t
219	127.0.0.1	13440	dazdaz	2025-03-13 14:33:27.203608	t
220	127.0.0.1	13449	zfez	2025-03-13 14:33:32.217223	t
221	127.0.0.1	13579		2025-03-13 14:36:57.382698	t
222	127.0.0.1	13592	dazd	2025-03-13 14:37:06.558362	t
224	127.0.0.1	13635	zafaz	2025-03-13 14:37:45.837762	t
225	127.0.0.1	13630	aaa	2025-03-13 14:37:53.798625	t
227	127.0.0.1	13669	dzadz	2025-03-13 14:38:38.808015	t
228	127.0.0.1	13664	sadazdza	2025-03-13 14:38:46.67001	t
229	127.0.0.1	13706	noe	2025-03-13 14:40:11.32707	t
230	127.0.0.1	13714	noa	2025-03-13 14:40:15.704439	t
231	127.0.0.1	13739	dazdza	2025-03-13 14:40:55.337435	t
232	127.0.0.1	13744	thrj	2025-03-13 14:40:57.143618	t
\.


--
-- Data for Name: round; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.round (id, game_id, move, player_turn) FROM stdin;
335	62154	0	217
336	62154	4	218
337	62154	3	217
338	62154	6	218
339	62154	2	217
340	62154	1	218
341	62154	5	217
342	62154	8	218
343	62154	7	217
344	62155	0	219
345	62155	1	220
346	62155	4	219
347	62155	7	220
348	62155	3	219
349	62155	2	220
350	62155	5	219
351	90611	0	229
352	90611	4	230
353	90611	6	229
354	90611	2	230
355	90611	5	229
356	90611	8	230
357	90611	3	229
358	90612	0	231
359	90612	1	232
360	90612	3	231
361	90612	4	232
362	90612	6	231
\.


--
-- Name: game_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.game_id_seq', 90612, true);


--
-- Name: queue_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.queue_id_seq', 232, true);


--
-- Name: round_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.round_id_seq', 362, true);


--
-- Name: game game_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game
    ADD CONSTRAINT game_pkey PRIMARY KEY (id);


--
-- Name: queue queue_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.queue
    ADD CONSTRAINT queue_pkey PRIMARY KEY (id);


--
-- Name: round round_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.round
    ADD CONSTRAINT round_pkey PRIMARY KEY (id);


--
-- Name: game game_player1id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game
    ADD CONSTRAINT game_player1id_fkey FOREIGN KEY (player1id) REFERENCES public.queue(id) ON DELETE CASCADE;


--
-- Name: game game_player2id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game
    ADD CONSTRAINT game_player2id_fkey FOREIGN KEY (player2id) REFERENCES public.queue(id) ON DELETE CASCADE;


--
-- Name: round round_game_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.round
    ADD CONSTRAINT round_game_id_fkey FOREIGN KEY (game_id) REFERENCES public.game(id) ON DELETE CASCADE;


--
-- Name: round round_player_turn_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.round
    ADD CONSTRAINT round_player_turn_fkey FOREIGN KEY (player_turn) REFERENCES public.queue(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

