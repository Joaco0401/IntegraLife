--
-- PostgreSQL database dump
--

\restrict fBOFIgCMaFjMI43wC9QlchUYz1Nj4dkoIDEYHIds6tCT9h1K7ZRktg9Ahq0qMCG

-- Dumped from database version 18.4
-- Dumped by pg_dump version 18.4

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
-- Data for Name: usuario_organizaciones; Type: TABLE DATA; Schema: public; Owner: postgres
--

SET SESSION AUTHORIZATION DEFAULT;

ALTER TABLE public.usuario_organizaciones DISABLE TRIGGER ALL;

COPY public.usuario_organizaciones (id, usuario_id, nombre, mi_cargo, creado_en) FROM stdin;
897eebf1-b445-4718-ae66-eff6c7d068e9	5b71b13a-2b30-4d3b-92c3-25cf394e1641	John ORyan Surveyors	Gerente General	2026-08-11 00:32:48.139465-04
7857fbf4-5196-42f7-beb0-0c6ed7ef9cec	5b71b13a-2b30-4d3b-92c3-25cf394e1641	CORMA	Presidente	2026-08-12 15:51:59.849464-04
\.


ALTER TABLE public.usuario_organizaciones ENABLE TRIGGER ALL;

--
-- Data for Name: eventos; Type: TABLE DATA; Schema: public; Owner: postgres
--

ALTER TABLE public.eventos DISABLE TRIGGER ALL;

COPY public.eventos (id, gcal_event_id, titulo, descripcion, ubicacion, inicio, fin, link_reunion, sincronizado_en, usuario_id, organizacion_id) FROM stdin;
92bc3472-3d42-441b-bff7-4b868714596d	local-2653556b-09b9-40dd-b6f2-148d66580782	Enviar informe de avance de obra	Importado desde archivo	\N	2026-08-20 10:30:00-04	\N	\N	2026-08-10 23:32:29.207596-04	9c3f64db-f158-484e-b47e-1b099af66560	\N
c328d161-fd3c-43de-bfdb-aeba12d9dbc0	mmhcf7gplcbv8j82o009rs5kd8	Revisar app con rodrigo	\N	\N	2026-08-11 01:00:00-04	2026-08-11 02:00:00-04	https://meet.google.com/nmu-oqpy-sah	2026-08-11 00:40:22.216225-04	5b71b13a-2b30-4d3b-92c3-25cf394e1641	\N
48be43b2-eaa2-492d-9177-6bccb64cc334	local-4da242cc-ccf2-4302-a1e3-805a7735e01a	Coordinar cuadrilla para faena de Antofagasta	Importado desde archivo	\N	2026-08-20 09:00:00-04	\N	\N	2026-08-13 00:24:58.19438-04	5b71b13a-2b30-4d3b-92c3-25cf394e1641	897eebf1-b445-4718-ae66-eff6c7d068e9
812a9656-bac7-4cc6-99a1-7e14bdcf39c1	local-50e11daf-a477-4ea2-86b8-781cf44c6221	Visita a terreno faena Antofagasta	Importado desde archivo	\N	2026-08-21 07:00:00-04	\N	\N	2026-08-13 00:24:58.218955-04	5b71b13a-2b30-4d3b-92c3-25cf394e1641	897eebf1-b445-4718-ae66-eff6c7d068e9
80f70f24-1b6d-442c-af36-4239b4410b97	local-9c03faf8-9457-4e59-8291-4bbfb1c27dab	Emitir facturas pendientes del mes	Importado desde archivo	\N	2026-08-22 09:00:00-04	\N	\N	2026-08-13 00:24:58.230276-04	5b71b13a-2b30-4d3b-92c3-25cf394e1641	897eebf1-b445-4718-ae66-eff6c7d068e9
3b9d8183-3102-4650-9fdd-73edf75a88b2	local-9fbc9816-415c-48bf-a8cd-bdf5a07ce47d	Entregar informe de levantamiento topografico	Importado desde archivo	\N	2026-08-25 09:00:00-04	\N	\N	2026-08-13 00:24:58.243176-04	5b71b13a-2b30-4d3b-92c3-25cf394e1641	897eebf1-b445-4718-ae66-eff6c7d068e9
3d20fa7d-2292-492d-989e-bd8646dda6bb	local-c67e35d7-a3af-4dc1-89ac-55c3749f5146	Enviar propuesta economica ampliacion planta	Importado desde archivo	\N	2026-08-28 09:00:00-04	\N	\N	2026-08-13 00:24:58.255714-04	5b71b13a-2b30-4d3b-92c3-25cf394e1641	897eebf1-b445-4718-ae66-eff6c7d068e9
3f776302-f306-43a9-9b6a-cf721009d066	local-8e2a8a12-0147-40e4-b69a-80b5013f6fa8	Cierre contable mensual	Importado desde archivo	\N	2026-08-29 16:00:00-04	\N	\N	2026-08-13 00:24:58.266645-04	5b71b13a-2b30-4d3b-92c3-25cf394e1641	897eebf1-b445-4718-ae66-eff6c7d068e9
be638a4f-ecd1-4435-9850-bc633ef3d655	local-83e01b46-c689-46bd-866d-64544e5bc0cf	Contactar Arauco Nueva Aldea (MS-01)	Importado desde archivo	\N	2026-08-10 09:00:00-04	\N	\N	2026-08-09 12:48:07.274396-04	5b71b13a-2b30-4d3b-92c3-25cf394e1641	\N
f52e82aa-59a3-4483-af95-58bb4a6dbe62	local-9c250ac0-5777-46f7-b9ff-db811e602712	Solicitar revisión legal laboral (LF-01)	Importado desde archivo	\N	2026-08-10 09:00:00-04	\N	\N	2026-08-09 12:48:07.300475-04	5b71b13a-2b30-4d3b-92c3-25cf394e1641	\N
4c9e3fc7-c4ec-4f4c-bf5f-77a3baabb36e	local-d9b08065-901e-452b-89ee-09dbce3ceea1	Definir posición licitación inventario CMPC (MS-02)	Importado desde archivo	\N	2026-08-11 09:00:00-04	\N	\N	2026-08-09 12:48:07.309301-04	5b71b13a-2b30-4d3b-92c3-25cf394e1641	\N
7f7a11c9-7b12-4f07-9b05-2931c8757b64	local-3b6e33b6-ae84-453d-a786-5f5f22205541	Reunion de coordinacion semanal	Importado desde archivo	\N	2026-08-18 09:30:00-04	\N	\N	2026-08-13 00:24:58.277087-04	5b71b13a-2b30-4d3b-92c3-25cf394e1641	897eebf1-b445-4718-ae66-eff6c7d068e9
8c8e8ce9-ba65-4a61-a3fe-cbe075e827b4	local-65302bfb-e200-4d68-afcf-37b24cd2e597	Cotizar mantencion de estaciones totales	Importado desde archivo	\N	2026-09-02 09:00:00-04	\N	\N	2026-08-13 00:24:58.288252-04	5b71b13a-2b30-4d3b-92c3-25cf394e1641	897eebf1-b445-4718-ae66-eff6c7d068e9
64dcadf6-2d38-449d-af58-21e7602bf9ba	local-772849f4-01b6-4faf-8ee1-4e0bac567e26	Reunión sector forestal sur	Reunión definida a partir de la discusión sobre la importancia del sector forestal en el sur.	\N	2026-08-24 09:00:00-04	\N	\N	2026-08-13 01:28:33.328864-04	5b71b13a-2b30-4d3b-92c3-25cf394e1641	\N
\.


ALTER TABLE public.eventos ENABLE TRIGGER ALL;

--
-- Data for Name: briefs_generados; Type: TABLE DATA; Schema: public; Owner: postgres
--

ALTER TABLE public.briefs_generados DISABLE TRIGGER ALL;

COPY public.briefs_generados (id, tipo, fecha, evento_id, contenido, modelo_usado, generado_en) FROM stdin;
b74c152a-9f8c-419d-92ae-737567c26f4c	brief_diario	2026-08-13	\N	{"saludo": "Buenos días Rodrigo, jueves despejado de reuniones: día ideal para avanzar pendientes críticos.", "resumen": "No tienes reuniones agendadas hoy. Tu semana tiene tres frentes urgentes: la propuesta a Constructora Andes vence el 28 de agosto, las facturas de julio vencen el 22 y aún no has cotizado las estaciones totales con GeoEquipos. Todos los pendientes fueron registrados ayer, así que es momento de activarlos antes de que se acumulen.", "fecha_texto": "jueves 13 de agosto de 2026", "sugerencias": ["Prioriza contactar a Carla Méndez hoy para destrabar las 4 facturas: sin ellas no entra caja de proyectos cerrados en julio.", "Agrupa los dos pendientes con Ignacio Vera (propuesta ampliación + cotización 12 há) en un solo bloque de trabajo hoy.", "Escribe a Marcelo Ríos (GeoEquipos) para solicitar información técnica: necesitas sus datos para cumplir el plazo del 2 sep."], "puntos_clave": ["Enviar propuesta económica de ampliación de planta a Ignacio Vera (Constructora Andes) — vence 28 ago.", "Emitir 4 facturas de julio con Carla Méndez — vence 22 ago, es lo más próximo.", "Preparar cotización de levantamiento de 12 hectáreas para Ignacio Vera — sin fecha límite, pero va con la propuesta.", "Cotizar mantención de 3 estaciones totales a Marcelo Ríos (GeoEquipos SpA) — vence 2 sep.", "Confirmar agenda y rol con Carla Méndez para reunión de seguimiento del 24 ago."], "total_eventos": 0, "total_pendientes": 5}	claude-sonnet-4-6	2026-08-13 13:35:33.313152-04
cd62260a-22c4-4073-b53b-baff2cdd58f1	brief_diario	2026-08-13	\N	{"saludo": "Buenos días, Rodrigo. Agenda libre hoy, pero tienes pendientes urgentes que atender.", "resumen": "No tienes reuniones agendadas para hoy. Sin embargo, acumulas cinco pendientes abiertos, todos registrados ayer, con fechas límite próximas. El más urgente es la propuesta económica para Ignacio Vera (Constructora Andes) que vence el 28 de agosto. Las facturas de julio deben emitirse antes del 22, lo que te deja solo nueve días.", "fecha_texto": "jueves 13 de agosto de 2026", "sugerencias": ["Escríbele hoy a Carla Méndez para destrabar las 4 facturas — vencen el 22/08 y dependen de su gestión conjunta.", "Agrupa ambos pendientes con Ignacio Vera (propuesta + cotización) en un solo contacto hoy para ganar tiempo.", "Llama o escribe a Marcelo Ríos (GeoEquipos SpA) para iniciar cotización de estaciones totales — aunque vence el 02/09, conviene tener margen."], "puntos_clave": ["Emitir 4 facturas de proyectos cerrados en julio antes del 22/08 — coordina con Carla Méndez hoy.", "Enviar propuesta económica de ampliación de planta a Ignacio Vera (Constructora Andes) antes del 28/08.", "Preparar cotización por levantamiento de 12 hectáreas para Ignacio Vera — sin fecha límite, no dejes que se postergue.", "Cotizar mantención y calibración de 3 estaciones totales con Marcelo Ríos (GeoEquipos SpA) antes del 02/09.", "Confirmar agenda y preparar contenidos para reunión de seguimiento con Carla Méndez el 24/08."], "total_eventos": 0, "total_pendientes": 5}	claude-sonnet-4-6	2026-08-13 13:39:01.234204-04
\.


ALTER TABLE public.briefs_generados ENABLE TRIGGER ALL;

--
-- Data for Name: empresas; Type: TABLE DATA; Schema: public; Owner: postgres
--

ALTER TABLE public.empresas DISABLE TRIGGER ALL;

COPY public.empresas (id, nombre, nicho, descripcion, sitio_web, creado_en, actualizado_en, foto_path, usuario_id, organizacion_id) FROM stdin;
8af090f3-e994-4337-a068-a03ef60ee8b9	Constructora Andes	Construcción	Empresa constructora, cliente de Integra Life.	\N	2026-08-10 23:32:29.099207-04	2026-08-10 23:32:29.099207-04	\N	9c3f64db-f158-484e-b47e-1b099af66560	\N
6b53e875-7cd5-4da4-b402-b420fa74499e	John O'Ryan Surveyors	topografia	Organizacion principal. Empresa de levantamientos topograficos.	\N	2026-08-13 00:24:57.878767-04	2026-08-13 00:24:57.878767-04	\N	5b71b13a-2b30-4d3b-92c3-25cf394e1641	897eebf1-b445-4718-ae66-eff6c7d068e9
c6f1c370-b6c3-47d6-b1f2-59665b65e233	Constructora Andes	construccion	Cliente de levantamientos topograficos en proyectos industriales del norte.	\N	2026-08-13 00:24:57.89844-04	2026-08-13 00:24:57.89844-04	\N	5b71b13a-2b30-4d3b-92c3-25cf394e1641	897eebf1-b445-4718-ae66-eff6c7d068e9
90819633-ed77-4689-9710-60c44ee25b37	GeoEquipos SpA	instrumentacion	Proveedor de estaciones totales, GPS y servicio de calibracion.	\N	2026-08-13 00:24:57.911413-04	2026-08-13 00:24:57.911413-04	\N	5b71b13a-2b30-4d3b-92c3-25cf394e1641	897eebf1-b445-4718-ae66-eff6c7d068e9
edb7183e-b57f-4963-a416-a51036b3b66a	Minera Los Pelambres	mineria	Cliente potencial. Contacto inicial en seminario de topografia 2026.	\N	2026-08-13 00:24:57.922754-04	2026-08-13 00:24:57.922754-04	\N	5b71b13a-2b30-4d3b-92c3-25cf394e1641	897eebf1-b445-4718-ae66-eff6c7d068e9
\.


ALTER TABLE public.empresas ENABLE TRIGGER ALL;

--
-- Data for Name: contactos; Type: TABLE DATA; Schema: public; Owner: postgres
--

ALTER TABLE public.contactos DISABLE TRIGGER ALL;

COPY public.contactos (id, nombre, empresa_id, cargo, nicho, telefono, linkedin_url, notas_generales, relacion_tipo, relacion_estado, creado_en, actualizado_en, foto_path, usuario_id, organizacion_id) FROM stdin;
8141a14e-6577-4cb8-96a6-d15b667b9a06	Pedro Soto	8af090f3-e994-4337-a068-a03ef60ee8b9	Gerente General	\N	\N	\N	\N	cliente	\N	2026-08-10 23:32:29.11402-04	2026-08-10 23:32:29.11402-04	\N	9c3f64db-f158-484e-b47e-1b099af66560	\N
527a2ad0-f9b6-49fa-b6d5-3228b73e0ff9	Pedro Soto	6b53e875-7cd5-4da4-b402-b420fa74499e	Jefe de Terreno	\N	\N	\N	\N	otro	\N	2026-08-13 00:24:57.936099-04	2026-08-13 00:24:57.936099-04	\N	5b71b13a-2b30-4d3b-92c3-25cf394e1641	897eebf1-b445-4718-ae66-eff6c7d068e9
cbbcfeae-a102-4d9e-9c6e-f9049e776bc6	Carla Mendez	6b53e875-7cd5-4da4-b402-b420fa74499e	Encargada Administracion	\N	\N	\N	\N	otro	\N	2026-08-13 00:24:57.972437-04	2026-08-13 00:24:57.972437-04	\N	5b71b13a-2b30-4d3b-92c3-25cf394e1641	897eebf1-b445-4718-ae66-eff6c7d068e9
7c2271da-46cb-4d57-a026-eae4205fa1bc	Ignacio Vera	c6f1c370-b6c3-47d6-b1f2-59665b65e233	Gerente de Proyectos	\N	\N	\N	\N	cliente	\N	2026-08-13 00:24:58.047034-04	2026-08-13 00:24:58.047034-04	\N	5b71b13a-2b30-4d3b-92c3-25cf394e1641	897eebf1-b445-4718-ae66-eff6c7d068e9
e8dd15d1-c7f9-4563-a836-b9c06e3c2fea	Marcelo Rios	90819633-ed77-4689-9710-60c44ee25b37	Ejecutivo Comercial	\N	\N	\N	\N	proveedor	\N	2026-08-13 00:24:58.11866-04	2026-08-13 00:24:58.11866-04	\N	5b71b13a-2b30-4d3b-92c3-25cf394e1641	897eebf1-b445-4718-ae66-eff6c7d068e9
\.


ALTER TABLE public.contactos ENABLE TRIGGER ALL;

--
-- Data for Name: contacto_emails; Type: TABLE DATA; Schema: public; Owner: postgres
--

ALTER TABLE public.contacto_emails DISABLE TRIGGER ALL;

COPY public.contacto_emails (id, contacto_id, email) FROM stdin;
56fdb413-e4a8-4967-a523-d76049933a34	8141a14e-6577-4cb8-96a6-d15b667b9a06	psoto@andes.cl
cfb3ede5-74cf-4b75-b53d-5238e0e364e8	527a2ad0-f9b6-49fa-b6d5-3228b73e0ff9	psoto@jors.cl
f3f777c4-9f20-4ef2-91f3-f24d57152208	cbbcfeae-a102-4d9e-9c6e-f9049e776bc6	cmendez@jors.cl
e2c58a73-5dc1-47fe-aa52-e4240eb7d810	7c2271da-46cb-4d57-a026-eae4205fa1bc	ivera@constructoraandes.cl
1d6767d7-3a58-4fc1-b82c-8b685c0d3305	e8dd15d1-c7f9-4563-a836-b9c06e3c2fea	mrios@geoequipos.cl
\.


ALTER TABLE public.contacto_emails ENABLE TRIGGER ALL;

--
-- Data for Name: documentos; Type: TABLE DATA; Schema: public; Owner: postgres
--

ALTER TABLE public.documentos DISABLE TRIGGER ALL;

COPY public.documentos (id, gdrive_file_id, nombre, mime_type, empresa_id, contacto_id, texto_extraido, resumen_ia, modificado_en, sincronizado_en) FROM stdin;
\.


ALTER TABLE public.documentos ENABLE TRIGGER ALL;

--
-- Data for Name: evento_asistentes; Type: TABLE DATA; Schema: public; Owner: postgres
--

ALTER TABLE public.evento_asistentes DISABLE TRIGGER ALL;

COPY public.evento_asistentes (id, evento_id, email, nombre, contacto_id) FROM stdin;
a25937d5-d1fb-4a06-a923-d588b89a2985	f52e82aa-59a3-4483-af95-58bb4a6dbe62	\N	Luis Fuentes	\N
52e69ee9-5f11-49b0-981e-d57e3e9b25f6	be638a4f-ecd1-4435-9850-bc633ef3d655	\N	Marcelo Silva	\N
cb9c57d2-5d98-4fbb-a9d7-7b67502650bb	4c9e3fc7-c4ec-4f4c-bf5f-77a3baabb36e	\N	Marcelo Silva	\N
ab812158-8991-4417-84a0-fb0b7a1b1ff0	c328d161-fd3c-43de-bfdb-aeba12d9dbc0	rodrigo.oryanblaitt@gmail.com	\N	\N
153eef63-5a17-4dba-b34c-f9792521c0cc	92bc3472-3d42-441b-bff7-4b868714596d	\N	Pedro Soto	8141a14e-6577-4cb8-96a6-d15b667b9a06
d583178e-0ca9-417c-9e81-f10a946123f6	48be43b2-eaa2-492d-9177-6bccb64cc334	\N	Pedro Soto	527a2ad0-f9b6-49fa-b6d5-3228b73e0ff9
fea8217a-a841-44e6-8d55-54daac34010f	80f70f24-1b6d-442c-af36-4239b4410b97	\N	Carla Mendez	cbbcfeae-a102-4d9e-9c6e-f9049e776bc6
667664ab-d027-4a60-8a50-ec802b49a2c7	3b9d8183-3102-4650-9fdd-73edf75a88b2	\N	Pedro Soto	527a2ad0-f9b6-49fa-b6d5-3228b73e0ff9
0bb57914-73e8-464b-a6e9-bbc6e9352332	3d20fa7d-2292-492d-989e-bd8646dda6bb	\N	Ignacio Vera	7c2271da-46cb-4d57-a026-eae4205fa1bc
65823d35-77f7-47bb-9bf8-58ad1a870faf	8c8e8ce9-ba65-4a61-a3fe-cbe075e827b4	\N	Marcelo Rios	e8dd15d1-c7f9-4563-a836-b9c06e3c2fea
cc6fb172-364a-43fd-b2ee-2d01c292758a	64dcadf6-2d38-449d-af58-21e7602bf9ba	\N	Carla Mendez	cbbcfeae-a102-4d9e-9c6e-f9049e776bc6
\.


ALTER TABLE public.evento_asistentes ENABLE TRIGGER ALL;

--
-- Data for Name: eventos_ocultos; Type: TABLE DATA; Schema: public; Owner: postgres
--

ALTER TABLE public.eventos_ocultos DISABLE TRIGGER ALL;

COPY public.eventos_ocultos (id, usuario_id, gcal_event_id, titulo, ocultado_en) FROM stdin;
00401eb6-1f0d-4498-9029-41543b05ad55	5b71b13a-2b30-4d3b-92c3-25cf394e1641	9gh6eb60ktma78gac99bhb9ats	Cena en restorán	2026-08-12 16:15:24.376432-04
a363f4fa-f186-49f1-b9f8-a1803dc2cd00	5b71b13a-2b30-4d3b-92c3-25cf394e1641	57h4q7smoig1jimpphv6vocm9c	Revisar app 2da parte	2026-08-12 16:15:26.110015-04
\.


ALTER TABLE public.eventos_ocultos ENABLE TRIGGER ALL;

--
-- Data for Name: notas_voz; Type: TABLE DATA; Schema: public; Owner: postgres
--

ALTER TABLE public.notas_voz DISABLE TRIGGER ALL;

COPY public.notas_voz (id, usuario_id, organizacion_id, audio_path, duracion_seg, transcripcion, analisis, estado, creada_en) FROM stdin;
e867a5a7-c7d6-49d8-8a4b-462d618cd217	5b71b13a-2b30-4d3b-92c3-25cf394e1641	\N	audios\\e867a5a7-c7d6-49d8-8a4b-462d618cd217.webm	6	\N	\N	pendiente	2026-08-13 00:56:33.878436-04
9617c83e-5f09-4a39-bacd-9abb099a8620	5b71b13a-2b30-4d3b-92c3-25cf394e1641	\N	audios\\9617c83e-5f09-4a39-bacd-9abb099a8620.webm	3	\N	\N	pendiente	2026-08-13 00:57:04.844805-04
defeb47b-df23-4e58-b09e-c17e7f25db25	5b71b13a-2b30-4d3b-92c3-25cf394e1641	\N	audios\\defeb47b-df23-4e58-b09e-c17e7f25db25.webm	3	\N	\N	pendiente	2026-08-13 00:57:20.495303-04
c7887441-79a0-4495-85b2-e57ce175812e	5b71b13a-2b30-4d3b-92c3-25cf394e1641	\N	audios\\c7887441-79a0-4495-85b2-e57ce175812e.webm	10	Hay que estimar mejor los presupuestos para el año que viene. Organizar una reunión con Juan para el 24 de agosto.	\N	transcrita	2026-08-13 01:15:11.695241-04
0465b360-fb14-4482-9a0e-792efb2df849	5b71b13a-2b30-4d3b-92c3-25cf394e1641	\N	audios\\0465b360-fb14-4482-9a0e-792efb2df849.webm	13	Hay que estimar una reunión con Juan para el 24 de agosto para hablar de los presupuestos. Esta tarea corresponde a María Ana Barca. Nuevo contacto.	\N	transcrita	2026-08-13 01:16:16.375959-04
1c63e0db-714a-4a94-9b2b-0a4f6130caf2	5b71b13a-2b30-4d3b-92c3-25cf394e1641	\N	audios\\1c63e0db-714a-4a94-9b2b-0a4f6130caf2.webm	14	Carla me contó sobre la importancia del sector forestal en el sur. Le dije que teníamos que agendar una reunión para el 24 de agosto, por lo que hay que tenerla.	{"eventos": [{"hora": null, "fecha": "2026-08-24", "notas": "Reunión relacionada con el sector forestal en el sur.", "titulo": "Reunión con Carla Mendez", "contacto_nombre": "Carla Mendez"}], "empresas": [], "contactos": [{"cargo": null, "nombre": "Carla Mendez", "resumen": "Carla compartió información sobre la importancia del sector forestal en el sur.", "es_nuevo": false, "id_existente": "cbbcfeae-a102-4d9e-9c6e-f9049e776bc6", "empresa_nombre": null, "nombre_existente": "Carla Mendez", "temas_pendientes": ["Confirmar reunión agendada para el 24 de agosto (responsable: asistente ejecutivo)"]}], "resumen_general": "Carla Mendez informó sobre la relevancia del sector forestal en el sur. Se acordó agendar una reunión con ella para el 24 de agosto."}	analizada	2026-08-13 01:21:32.817398-04
5c59ec7e-8b7b-42c2-af5a-99d5287017bf	5b71b13a-2b30-4d3b-92c3-25cf394e1641	\N	audios\\5c59ec7e-8b7b-42c2-af5a-99d5287017bf.webm	10	Definimos la importancia del sector forestal en el sur, por lo que definimos una reunión para el 24 de agosto.	{"eventos": [{"hora": null, "fecha": "2026-08-24", "notas": "Reunión definida a partir de la discusión sobre la importancia del sector forestal en el sur.", "titulo": "Reunión sector forestal sur", "contacto_nombre": null}], "empresas": [], "contactos": [], "resumen_general": "Se discutió la importancia del sector forestal en el sur. Se agendó una reunión para el 24 de agosto como seguimiento."}	analizada	2026-08-13 01:28:05.740292-04
\.


ALTER TABLE public.notas_voz ENABLE TRIGGER ALL;

--
-- Data for Name: interacciones; Type: TABLE DATA; Schema: public; Owner: postgres
--

ALTER TABLE public.interacciones DISABLE TRIGGER ALL;

COPY public.interacciones (id, contacto_id, evento_id, tipo, fecha, contenido_raw, resumen_ia, temas_pendientes, creado_en, usuario_id, empresa_id, nota_voz_id) FROM stdin;
60b0779e-7a3d-4b9d-acba-f1dd6ab0f754	8141a14e-6577-4cb8-96a6-d15b667b9a06	\N	nota	2026-08-10 23:32:29.131243-04	Importado desde archivo: Reunión del 9 ago. TAREA: Enviar informe de avance de obra antes del 2026-08-20 a las 10:30. Debe incluir fotos y curva S actualizada.	En la reunión del 9 de agosto con Pedro Soto quedó pendiente el envío de un informe de avance de obra. El plazo límite es el 20 de agosto de 2026 a las 10:30.	[{"hecho": false, "texto": "Enviar informe de avance de obra con fotos y curva S actualizada antes del 2026-08-20 a las 10:30 (responsable: Rodrigo)"}]	2026-08-10 23:32:29.131243-04	9c3f64db-f158-484e-b47e-1b099af66560	\N	\N
edaef2b8-3244-44cc-80da-103f7402a026	7c2271da-46cb-4d57-a026-eae4205fa1bc	\N	nota	2026-08-13 00:24:58.066319-04	Importado desde archivo: TAREA (2026-08-28): Enviar propuesta economica ampliacion planta. Solicito cotizacion por levantamiento de 12 hectareas. Urgente para su directorio.	Ignacio Vera solicitó una propuesta económica para ampliación de planta, específicamente una cotización por levantamiento de 12 hectáreas. La necesita con urgencia para presentar a su directorio antes del 28 de agosto de 2026.	[{"hecho": false, "texto": "Enviar propuesta económica de ampliación de planta (responsable: Rodrigo, fecha límite: 2026-08-28)"}, {"hecho": false, "texto": "Preparar cotización por levantamiento de 12 hectáreas (responsable: Rodrigo)"}]	2026-08-13 00:24:58.066319-04	5b71b13a-2b30-4d3b-92c3-25cf394e1641	\N	\N
bfdc87a6-6ef5-4a82-83a4-68d793e31e3e	cbbcfeae-a102-4d9e-9c6e-f9049e776bc6	\N	nota	2026-08-13 01:28:18.619188-04	Nota de voz: Se discutió la importancia del sector forestal en el sur. Se agendó una reunión para el 24 de agosto como seguimiento.	Se mantuvo una conversación con Carla Mendez sobre el sector forestal en el sur. Se acordó una reunión de seguimiento para el 24 de agosto.	[{"hecho": false, "texto": "Asistir a reunión de seguimiento el 24 de agosto (responsable: Rodrigo y Carla Mendez)"}]	2026-08-13 01:28:18.619188-04	5b71b13a-2b30-4d3b-92c3-25cf394e1641	\N	\N
ae24d57d-96b2-4fdf-8151-f83bc8b96db0	e8dd15d1-c7f9-4563-a836-b9c06e3c2fea	\N	nota	2026-08-13 00:24:58.136428-04	Importado desde archivo: TAREA (2026-09-02): Cotizar mantencion de estaciones totales. Tres equipos requieren calibracion anual antes de la temporada alta.	Tarea registrada para cotizar mantención de tres estaciones totales que requieren calibración anual antes de la temporada alta. Fecha límite: 2 de septiembre de 2026.	[{"hecho": false, "texto": "Cotizar mantención y calibración de tres estaciones totales (responsable: Rodrigo, fecha límite: 2026-09-02)"}]	2026-08-13 00:24:58.136428-04	5b71b13a-2b30-4d3b-92c3-25cf394e1641	\N	\N
e4d068c5-e8bb-4174-830d-05164f3c8b32	cbbcfeae-a102-4d9e-9c6e-f9049e776bc6	\N	nota	2026-08-13 00:24:57.986017-04	Importado desde archivo: TAREA (2026-08-22): Emitir facturas pendientes del mes. Quedaron 4 facturas por emitir de proyectos cerrados en julio.	Hay 4 facturas pendientes de emitir correspondientes a proyectos cerrados en julio. La tarea tiene fecha límite el 22 de agosto de 2026.	[{"hecho": false, "texto": "Emitir 4 facturas pendientes de proyectos cerrados en julio (responsable: Rodrigo, fecha límite: 2026-08-22)"}]	2026-08-13 00:24:57.986017-04	5b71b13a-2b30-4d3b-92c3-25cf394e1641	\N	\N
1ed016cc-002e-4801-a0ba-fc0800276b7f	527a2ad0-f9b6-49fa-b6d5-3228b73e0ff9	\N	nota	2026-08-13 00:24:57.954547-04	Importado desde archivo: TAREA 1 (2026-08-25): Entregar informe de levantamiento topografico. Incluir planos y memoria de calculo. TAREA 2 (2026-08-20): Coordinar cuadrilla para faena de Antofagasta. Confirmar equipos GPS y alojamiento.	Se importaron dos tareas relacionadas con un proyecto topográfico. Hay que entregar un informe con planos y coordinar una cuadrilla para faena en Antofagasta.	[{"hecho": true, "texto": "Entregar informe de levantamiento topográfico con planos y memoria de cálculo antes del 2026-08-25 (responsable: por definir)"}, {"hecho": true, "texto": "Coordinar cuadrilla para faena en Antofagasta antes del 2026-08-20 (responsable: por definir)"}, {"hecho": true, "texto": "Confirmar equipos GPS para faena de Antofagasta (responsable: por definir)"}, {"hecho": true, "texto": "Confirmar alojamiento para cuadrilla en Antofagasta (responsable: por definir)"}]	2026-08-13 00:24:57.954547-04	5b71b13a-2b30-4d3b-92c3-25cf394e1641	\N	\N
\.


ALTER TABLE public.interacciones ENABLE TRIGGER ALL;

--
-- Data for Name: links_linkedin; Type: TABLE DATA; Schema: public; Owner: postgres
--

ALTER TABLE public.links_linkedin DISABLE TRIGGER ALL;

COPY public.links_linkedin (id, url, contacto_id, es_propio, texto_extraido, resumen_ia, guardado_en) FROM stdin;
\.


ALTER TABLE public.links_linkedin ENABLE TRIGGER ALL;

--
-- Data for Name: noticias; Type: TABLE DATA; Schema: public; Owner: postgres
--

ALTER TABLE public.noticias DISABLE TRIGGER ALL;

COPY public.noticias (id, nicho, titulo, fuente, url, publicada_en, resumen_ia, recolectada_en) FROM stdin;
\.


ALTER TABLE public.noticias ENABLE TRIGGER ALL;

--
-- Data for Name: sync_jobs; Type: TABLE DATA; Schema: public; Owner: postgres
--

ALTER TABLE public.sync_jobs DISABLE TRIGGER ALL;

COPY public.sync_jobs (id, tipo, estado, detalle_error, inicio, fin, creado_en) FROM stdin;
\.


ALTER TABLE public.sync_jobs ENABLE TRIGGER ALL;

--
-- PostgreSQL database dump complete
--

\unrestrict fBOFIgCMaFjMI43wC9QlchUYz1Nj4dkoIDEYHIds6tCT9h1K7ZRktg9Ahq0qMCG

