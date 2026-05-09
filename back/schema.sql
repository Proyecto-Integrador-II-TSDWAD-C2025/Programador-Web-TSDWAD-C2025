-- ============================================================
-- NutriApp - Script SQL de Base de Datos
-- Motor: MySQL 8.x
-- ============================================================

CREATE DATABASE IF NOT EXISTS proyectointegrador
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE proyectointegrador;

-- ------------------------------------------------------------
-- Tabla: ROL
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS ROL (
    id_rol      INT          NOT NULL AUTO_INCREMENT,
    nombre_rol  VARCHAR(50)  NOT NULL,
    PRIMARY KEY (id_rol)
);

-- ------------------------------------------------------------
-- Tabla: USUARIO
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS USUARIO (
    id_usuario      INT          NOT NULL AUTO_INCREMENT,
    nombre          VARCHAR(100) NOT NULL,
    apellido        VARCHAR(100) NOT NULL,
    email           VARCHAR(255) NOT NULL,
    contrasena      VARCHAR(255) NOT NULL,
    fecha_registro  DATETIME     NOT NULL,
    id_rol          INT          NOT NULL,
    PRIMARY KEY (id_usuario),
    UNIQUE KEY uq_usuario_email (email),
    CONSTRAINT fk_usuario_rol FOREIGN KEY (id_rol) REFERENCES ROL (id_rol)
);

-- ------------------------------------------------------------
-- Tabla: PLAN
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS PLAN (
    id_plan           INT             NOT NULL AUTO_INCREMENT,
    nombre_plan       VARCHAR(100)    NOT NULL,
    descripcion       TEXT            NOT NULL,
    duracion_dias     INT             NOT NULL,
    calorias_objetivo DECIMAL(10, 2)  NOT NULL,
    PRIMARY KEY (id_plan)
);

-- ------------------------------------------------------------
-- Tabla: COMIDA
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS COMIDA (
    id_comida      INT            NOT NULL AUTO_INCREMENT,
    nombre         VARCHAR(100)   NOT NULL,
    calorias       DECIMAL(10, 2) NOT NULL,
    proteinas      DECIMAL(10, 2) NOT NULL,
    carbohidratos  DECIMAL(10, 2) NOT NULL,
    grasas         DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (id_comida)
);

-- ------------------------------------------------------------
-- Tabla: USUARIO_PLAN
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS USUARIO_PLAN (
    id_usuario_plan  INT         NOT NULL AUTO_INCREMENT,
    id_usuario       INT         NOT NULL,
    id_plan          INT         NOT NULL,
    fecha_inicio     DATE        NOT NULL,
    fecha_fin        DATE        NOT NULL,
    estado           VARCHAR(20) NOT NULL DEFAULT 'activo',
    PRIMARY KEY (id_usuario_plan),
    CONSTRAINT fk_up_usuario FOREIGN KEY (id_usuario) REFERENCES USUARIO (id_usuario),
    CONSTRAINT fk_up_plan    FOREIGN KEY (id_plan)    REFERENCES PLAN    (id_plan)
);

-- ------------------------------------------------------------
-- Tabla: PLAN_COMIDA
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS PLAN_COMIDA (
    id_plan_comida  INT         NOT NULL AUTO_INCREMENT,
    id_plan         INT         NOT NULL,
    id_comida       INT         NOT NULL,
    tipo_comida     VARCHAR(20) NOT NULL,
    PRIMARY KEY (id_plan_comida),
    CONSTRAINT fk_pc_plan   FOREIGN KEY (id_plan)   REFERENCES PLAN   (id_plan),
    CONSTRAINT fk_pc_comida FOREIGN KEY (id_comida) REFERENCES COMIDA (id_comida)
);

-- ------------------------------------------------------------
-- Datos iniciales
-- ------------------------------------------------------------
INSERT INTO ROL (nombre_rol) VALUES
    ('administrador'),
    ('usuario');

INSERT INTO USUARIO (nombre, apellido, email, contrasena, fecha_registro, id_rol)
VALUES ('Admin', 'Sistema', 'admin@nutriapp.com', 'admin123', NOW(), 1);
