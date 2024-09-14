-- Таблица с вопросами (ticket)
CREATE TABLE ticket
(
    id                INTEGER PRIMARY KEY,
    correct_answer_id INTEGER NOT NULL,
    img_source        TEXT    NULL,
    FOREIGN KEY (correct_answer_id) REFERENCES answer (id)
);

-- Таблица с ответами (answer)
CREATE TABLE answer
(
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id INTEGER NOT NULL,
    number    INTEGER NOT NULL CHECK (number >= 1 AND number <= 4), -- Номер ответа (от 1 до 4)
    FOREIGN KEY (ticket_id) REFERENCES ticket (id),
    UNIQUE (ticket_id, number)                                      -- Уникальность ответа в рамках одного вопроса
);

-- Таблица с языками (language)
CREATE TABLE language
(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    code        TEXT NOT NULL, -- Код языка, например 'en', 'ru'
    description TEXT NOT NULL  -- Название языка
);

-- Таблица с переводами вопросов (ticket_translation)
CREATE TABLE ticket_translation
(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id   INTEGER NOT NULL,
    language_id INTEGER NOT NULL,
    text        TEXT NOT NULL,      -- Текст перевода вопроса
    FOREIGN KEY (ticket_id) REFERENCES ticket (id),
    FOREIGN KEY (language_id) REFERENCES language (id),
    UNIQUE (ticket_id, language_id) -- Уникальность перевода вопроса для языка
);

CREATE UNIQUE INDEX ticket_translation__ticket_id_language_id ON ticket_translation (ticket_id, language_id);

-- Таблица с переводами ответов (answer_translation)
CREATE TABLE answer_translation
(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    answer_id   INTEGER NOT NULL,
    language_id INTEGER NOT NULL,
    text        TEXT NOT NULL,      -- Текст перевода ответа
    FOREIGN KEY (answer_id) REFERENCES answer (id),
    FOREIGN KEY (language_id) REFERENCES language (id),
    UNIQUE (answer_id, language_id) -- Уникальность перевода ответа для языка
);

CREATE UNIQUE INDEX answer_translation__answer_id_language_id ON answer_translation (answer_id, language_id);

-- Таблица с темами вопросов (topic)
CREATE TABLE topic
(
    id          INTEGER PRIMARY KEY,
    description TEXT NULL
);

-- Таблица с переводами тем (topic_translation)
CREATE TABLE topic_translation
(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_id    INTEGER NOT NULL,
    language_id INTEGER NOT NULL,
    text        TEXT NOT NULL,     -- Текст перевода темы
    FOREIGN KEY (topic_id) REFERENCES topic (id),
    FOREIGN KEY (language_id) REFERENCES language (id),
    UNIQUE (topic_id, language_id) -- Уникальность перевода темы
);

CREATE UNIQUE INDEX topic_translation__topic_id_language_id ON topic_translation (topic_id, language_id);

-- Таблица для связи вопросов и тем (ticket_topic)
CREATE TABLE ticket_topic
(
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id INTEGER NOT NULL,
    topic_id  INTEGER NOT NULL,
    FOREIGN KEY (ticket_id) REFERENCES ticket (id),
    FOREIGN KEY (topic_id) REFERENCES topic (id)
);

CREATE INDEX ticket_topic__topic_id ON ticket_topic (topic_id);

-- Таблица с категориями прав --
CREATE TABLE category
(
    id   INTEGER PRIMARY KEY,
    code TEXT NOT NULL -- Код категории
);

-- Таблица с переводами категорий прав (topic_translation)
CREATE TABLE category_translation
(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL,
    language_id INTEGER NOT NULL,
    text        TEXT NOT NULL,        -- Текст перевода описания категории
    FOREIGN KEY (category_id) REFERENCES topic (id),
    FOREIGN KEY (language_id) REFERENCES language (id),
    UNIQUE (category_id, language_id) -- Уникальность перевода темы
);

CREATE UNIQUE INDEX category_translation__category_id_language_id ON category_translation (category_id, language_id);

-- Таблица для связи вопросов и категорий (ticket_category)
CREATE TABLE ticket_category
(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id   INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    FOREIGN KEY (ticket_id) REFERENCES ticket (id),
    FOREIGN KEY (category_id) REFERENCES category (id)
);

CREATE INDEX ticket_category__category_id ON ticket_category (category_id);
