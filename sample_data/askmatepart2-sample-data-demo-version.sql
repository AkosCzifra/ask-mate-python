--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.6
-- Dumped by pg_dump version 9.5.6

ALTER TABLE IF EXISTS ONLY public.question DROP CONSTRAINT IF EXISTS pk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.answer DROP CONSTRAINT IF EXISTS pk_answer_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.answer DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS pk_comment_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS fk_answer_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS pk_question_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.tag DROP CONSTRAINT IF EXISTS pk_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS fk_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.answer DROP CONSTRAINT IF EXISTS fk_user_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question DROP CONSTRAINT IF EXISTS fk_user_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS fk_user_id CASCADE;



DROP TABLE IF EXISTS public.question;
DROP SEQUENCE IF EXISTS public.question_id_seq;
CREATE TABLE question (
    id serial NOT NULL,
    submission_time timestamp without time zone,
    view_number integer,
    vote_number integer,
    title text,
    message text,
    image text,
    user_id integer
);

DROP TABLE IF EXISTS public.answer;
DROP SEQUENCE IF EXISTS public.answer_id_seq;
CREATE TABLE answer (
    id serial NOT NULL,
    submission_time timestamp without time zone,
    vote_number integer,
    question_id integer,
    message text,
    image text,
    user_id integer
);

DROP TABLE IF EXISTS public.comment;
DROP SEQUENCE IF EXISTS public.comment_id_seq;
CREATE TABLE comment (
    id serial NOT NULL,
    question_id integer,
    answer_id integer,
    message text,
    submission_time timestamp without time zone,
    edited_count integer,
    user_id integer
);

DROP TABLE IF EXISTS public.userdata;
DROP SEQUENCE IF EXISTS public.userdata_id_seq;
CREATE TABLE userdata (
    id serial NOT NULL,
    user_name text,
    password text,
    registration_date timestamp without time zone,
    unique (user_name)
);

DROP TABLE IF EXISTS public.question_tag;
CREATE TABLE question_tag (
    question_id integer NOT NULL,
    tag_id integer NOT NULL
);

DROP TABLE IF EXISTS public.tag;
DROP SEQUENCE IF EXISTS public.tag_id_seq;
CREATE TABLE tag (
    id serial NOT NULL,
    name text,
    unique (name)
);

ALTER TABLE ONLY userdata
    ADD CONSTRAINT pk_userdata_id PRIMARY KEY (id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES userdata(id);

ALTER TABLE ONLY answer
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES userdata(id);

ALTER TABLE ONLY question
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES userdata(id);

ALTER TABLE ONLY answer
    ADD CONSTRAINT pk_answer_id PRIMARY KEY (id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT pk_comment_id PRIMARY KEY (id);

ALTER TABLE ONLY question
    ADD CONSTRAINT pk_question_id PRIMARY KEY (id);

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT pk_question_tag_id PRIMARY KEY (question_id, tag_id);

ALTER TABLE ONLY tag
    ADD CONSTRAINT pk_tag_id PRIMARY KEY (id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_answer_id FOREIGN KEY (answer_id) REFERENCES answer(id) ON DELETE CASCADE;

ALTER TABLE ONLY answer
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id) ON DELETE CASCADE;

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id) ON DELETE CASCADE;

ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id) ON DELETE CASCADE;

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT fk_tag_id FOREIGN KEY (tag_id) REFERENCES tag(id);

INSERT INTO userdata VALUES (1,'admin','$2b$12$RPuFU0GJX7lT.H.xWWsFd.DqDCkk2yN2.mgEoNddyoilN0FI.eU6q','0001-01-01 12:00:00');
INSERT INTO userdata VALUES (2,'alexadmin','$2b$12$SPYguIxuNd0XOHeAS/Q3FOA/hiIvjMvF.ye1x7DItWYZEYqYXhqFG','1994-09-26 08:30:15');
INSERT INTO userdata VALUES (3,'markadmin','$2b$12$4Q7C46iPJnOHj81ohppq2eKGVEn70GAXqUYWDQIsSY0gbn3PpDlUO','1998-01-14 20:38:53');
INSERT INTO userdata VALUES (4,'akosadmin','$2b$12$i0VnCZuf.yOt7IsMVTqhAu.EQH1aYAvgw/sZfWPZz8yEwN3NcJn2G','1994-04-16 13:42:41');
INSERT INTO userdata VALUES (5,'zoliadmin','$2b$12$pSiCtGgef.dZbBSdn4mGAOwIHWPLKATsu7vA592cw4CEIZhpBMrqW','1980-02-02 12:00:00');
SELECT pg_catalog.setval('userdata_id_seq', 5, true);

INSERT INTO question VALUES (0, '2017-04-28 08:29:00', 8, 123, 'Fusion M8s, Assemble!', 'Let me introduce you the team!', 'https://upload.wikimedia.org/wikipedia/commons/9/9a/M8_autopalya.png', 1);
INSERT INTO question VALUES (1, '2019-05-15 16:50:00', 15, 9, 'Git Workflow', 'The image is small, huh? Well, let''s see what can we do about it... ', 'http://www.kepfeltoltes.eu/images/2019/03/925Screenshot_from_2019_0.png',2);
INSERT INTO question VALUES (2, '2017-05-01 10:41:00', 1364, 57, 'Drawing canvas with an image picked with Cordova Camera Plugin', 'I''m getting an image from device and drawing a canvas with filters using Pixi JS. It works all well using computer to get an image. But when I''m on IOS, it throws errors such as cross origin issue, or that I''m trying to use an unknown format.
', NULL, NULL);
INSERT INTO question VALUES (3, '2017-04-28 08:29:00', 14, 6, 'Hello Trello!', 'We used Trello. We felt like we could have used a more advanced project tracking application this is why we choose Trello.', 'https://upload.wikimedia.org/wikipedia/commons/a/a5/Trello_logo.png', 4);
SELECT pg_catalog.setval('question_id_seq', 3, true);

INSERT INTO answer VALUES (1, '2017-04-28 16:49:00', 8, 0, 'List your name here fast and let''s get this going!',null, 1);
INSERT INTO answer VALUES (2, '2017-04-25 14:42:00', -4, 0, 'Sorry m8s, I gotta go :(', 'https://www.thestampmaker.com/stock_rubber_stamp_images/SSS2_SAD_FACE.jpg',5);
INSERT INTO answer VALUES (3, '2019-05-15 16:49:00', 0, 1, 'Thank god we only took a few User Stories!',null, 4);
INSERT INTO answer VALUES (4, '2019-05-15 16:49:00', 0, 3, 'We finished with 7300/5700.','https://fowmedia.com/wp-content/uploads/2014/08/win-1024x1024.jpg', 4);
INSERT INTO answer VALUES (5, '2019-05-15 16:48:00', 0, 3, 'Also we did some extras: stabilized the website (caught all known errors with excepts), handled invalid links! Also handled all previous SQL deletes with DELETE ON CASCADE.',null, 4);
SELECT pg_catalog.setval('answer_id_seq', 5, true);

INSERT INTO comment VALUES (1, NULL, 1, 'Hey it''s me Alex!', '2017-05-02 16:55:00', NULL, 2);
INSERT INTO comment VALUES (2, NULL, 1, 'Mark ready for duty!', '2017-05-02 16:55:00', NULL, 3);
INSERT INTO comment VALUES (3, NULL, 1, 'Hey folks, Ákos here!', '2017-05-02 16:55:00', NULL, 4);
INSERT INTO comment VALUES (4, NULL, 1, 'Zoli here!', '2017-05-02 16:55:00', NULL, 5);
INSERT INTO comment VALUES (5, NULL, 2, ':(', '2017-05-02 16:55:00', NULL, 2);
INSERT INTO comment VALUES (6, 1, NULL, 'Branches helped us a lot, they made merges so much simpler! We divided the tasks and made them all by wednesday, we even had time for extras and memes.', '2019-05-15 16:55:00', 1, 2);
INSERT INTO comment VALUES (7, NULL, 4, 'Accepted User Stories were: ' ||
                                        'user registration - 1000 | ' ||
                                        'user login - 1000 | ' ||
                                        'bind questions to user - 700 | ' ||
                                        'bind answers to user - 700 | ' ||
                                        'tag page - 600 | ' ||
                                        'user page - 900 | ' ||
                                        'list users - 800 | ', '2019-05-15 16:55:00', NULL, 4);
INSERT INTO comment VALUES (8, NULL, 4, 'Extra User Stories were: ' ||
                                        'bind the comment to user - 300 (600/2) | ' ||
                                        'delete comments - 400 (800/2) | ' ||
                                        'edit answer - 500 (1000/2) | ' ||
                                        'edit comments - 400 (800/2) | ', '2019-05-15 16:54:00', NULL, 4);
SELECT pg_catalog.setval('comment_id_seq', 8, true);

INSERT INTO tag VALUES (1, 'intro');
INSERT INTO tag VALUES (2, 'sql');
INSERT INTO tag VALUES (3, 'git');
INSERT INTO tag VALUES (4, 'trello');
SELECT pg_catalog.setval('tag_id_seq', 4, true);

INSERT INTO question_tag VALUES (0, 1);
INSERT INTO question_tag VALUES (1, 3);
INSERT INTO question_tag VALUES (2, 3);
INSERT INTO question_tag VALUES (3, 1);
INSERT INTO question_tag VALUES (3, 4);
INSERT INTO question_tag VALUES (3, 2);



