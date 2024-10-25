DROP TABLE IF EXISTS agenda;

CREATE TABLE agenda (
    id INT AUTO_INCREMENT PRIMARY KEY,   -- Id auto incrementable
    user_id BIGINT NOT NULL,             -- L'ID de l'utilisateur Discord
    matiere VARCHAR(255) NOT NULL,       -- Nom du module
    libelle VARCHAR(255) NOT NULL,       -- Libelle du devoir
    jour_semaine VARCHAR(20) NOT NULL,        -- Jour de la semaine en toutes lettres
    date_devoir DATETIME NOT NULL       -- Date du devoir
);