-- DROP TABLE IF EXISTS campi CASCADE;
CREATE TABLE IF NOT EXISTS campi(
    id smallint NOT NULL,
    abbrev character(3) NOT NULL,
    name text,
    CONSTRAINT campi_pk PRIMARY KEY (id),
    CONSTRAINT campi_uniq UNIQUE (abbrev)
);

-- DROP TABLE IF EXISTS programs CASCADE;
CREATE TABLE IF NOT EXISTS programs(
    id smallint NOT NULL,
    campus_id smallint NOT NULL,
    name text NOT NULL,
    CONSTRAINT programs_pk PRIMARY KEY (id),
    CONSTRAINT campi_fk FOREIGN KEY (campus_id) REFERENCES campi (id) ON DELETE RESTRICT ON UPDATE RESTRICT
);

-- DROP TABLE IF EXISTS courses CASCADE;
CREATE TABLE IF NOT EXISTS courses(
    id character(7) NOT NULL,
    campus_id smallint NOT NULL,
    name text NOT NULL,
    load smallint NOT NULL,
    CONSTRAINT courses_pk PRIMARY KEY (id),
    CONSTRAINT campi_fk FOREIGN KEY (campus_id) REFERENCES campi (id) ON DELETE RESTRICT ON UPDATE RESTRICT
);

-- DROP TABLE IF EXISTS professors CASCADE;
CREATE TABLE IF NOT EXISTS professors(
    id bigint NOT NULL,
    name text,
    CONSTRAINT professors_pk PRIMARY KEY (id)
);

-- DROP TABLE IF EXISTS classes CASCADE;
CREATE TABLE IF NOT EXISTS classes(
    id serial NOT NULL,
    name character varying(6) NOT NULL,
    term character(5) NOT NULL,
    course_id character(7) NOT NULL,
    capacity smallint NOT NULL,
    enrolled smallint NOT NULL,
    special smallint NOT NULL,
    pending smallint NOT NULL,
    remaining smallint NOT NULL,
    CONSTRAINT classes_pk PRIMARY KEY (id),
    CONSTRAINT classes_uniq UNIQUE (name,term,course_id),
    CONSTRAINT courses_fk FOREIGN KEY (course_id) REFERENCES courses (id) ON DELETE RESTRICT ON UPDATE CASCADE
);

-- DROP TABLE IF EXISTS classes_professors CASCADE;
CREATE TABLE IF NOT EXISTS classes_professors(
    professor_id bigint NOT NULL,
    class_id integer NOT NULL,
    CONSTRAINT classes_professors_pk PRIMARY KEY (professor_id,class_id),
    CONSTRAINT professors_fk FOREIGN KEY (professor_id) REFERENCES professors (id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT classes_fk FOREIGN KEY (class_id) REFERENCES classes (id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- DROP TABLE IF EXISTS performance CASCADE;
CREATE TABLE IF NOT EXISTS performances(
    program_id smallint NOT NULL,
    class_id integer NOT NULL,
    approved smallint NOT NULL,
    disapproved smallint NOT NULL,
    attendance smallint NOT NULL,
    CONSTRAINT performances_pk PRIMARY KEY (program_id,class_id),
    CONSTRAINT classes_fk FOREIGN KEY (class_id) REFERENCES classes (id) ON DELETE CASCADE ON UPDATE CASCADE
);
