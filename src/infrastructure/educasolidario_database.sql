-- ============================================
-- EDUCASOLIDARIO - Projeto Físico do Banco de Dados
-- PostgreSQL 16
-- ============================================

-- TIPOS ENUMERADOS
CREATE TYPE user_role_type AS ENUM ('donor', 'institution');
CREATE TYPE project_type_enum AS ENUM ('horta_comunitaria', 'minicurso', 'oficina', 'radio_estudantil', 'outro');
CREATE TYPE project_status_enum AS ENUM ('ativo', 'concluido', 'pausado');
CREATE TYPE material_category_enum AS ENUM ('escolar', 'tecnologia', 'ferramentas', 'livros', 'equipamentos', 'outro');
CREATE TYPE priority_enum AS ENUM ('baixa', 'media', 'alta', 'urgente');
CREATE TYPE need_status_enum AS ENUM ('pendente', 'parcialmente_atendido', 'atendido');
CREATE TYPE donation_status_enum AS ENUM ('pendente', 'confirmada', 'entregue', 'cancelada');
CREATE TYPE exchange_type_enum AS ENUM ('material', 'conhecimento', 'ambos');
CREATE TYPE exchange_status_enum AS ENUM ('proposta', 'aceita', 'em_andamento', 'concluida', 'cancelada');

-- TABELAS
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    user_role user_role_type NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    endereco TEXT NOT NULL,
    telefone VARCHAR(15) NOT NULL,
    cpf VARCHAR(14) UNIQUE,
    donor_name VARCHAR(255),
    date_birth DATE,
    cnpj VARCHAR(18) UNIQUE,
    institution_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE projects (
    project_id SERIAL PRIMARY KEY,
    institution_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    project_name VARCHAR(255) NOT NULL,
    project_description TEXT NOT NULL,
    project_type project_type_enum NOT NULL,
    status project_status_enum DEFAULT 'ativo',
    start_date DATE NOT NULL,
    end_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE materials (
    material_id SERIAL PRIMARY KEY,
    material_name VARCHAR(255) NOT NULL,
    material_category material_category_enum NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE material_needs (
    need_id SERIAL PRIMARY KEY,
    institution_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    project_id INTEGER REFERENCES projects(project_id) ON DELETE CASCADE,
    material_id INTEGER NOT NULL REFERENCES materials(material_id) ON DELETE RESTRICT,
    quantity_needed INTEGER NOT NULL DEFAULT 1 CHECK (quantity_needed > 0),
    priority priority_enum DEFAULT 'media',
    status need_status_enum DEFAULT 'pendente',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE donations (
    donation_id SERIAL PRIMARY KEY,
    donor_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    institution_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    material_id INTEGER NOT NULL REFERENCES materials(material_id) ON DELETE RESTRICT,
    quantity_donated INTEGER NOT NULL DEFAULT 1 CHECK (quantity_donated > 0),
    donation_date DATE NOT NULL DEFAULT CURRENT_DATE,
    status donation_status_enum DEFAULT 'pendente',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE institution_exchanges (
    exchange_id SERIAL PRIMARY KEY,
    institution_from_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    institution_to_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    exchange_type exchange_type_enum NOT NULL,
    description TEXT NOT NULL,
    status exchange_status_enum DEFAULT 'proposta',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CHECK (institution_from_id != institution_to_id)
);

-- ÍNDICES
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_cpf ON users(cpf);
CREATE INDEX idx_users_cnpj ON users(cnpj);
CREATE INDEX idx_users_role ON users(user_role);
CREATE INDEX idx_projects_institution ON projects(institution_id);
CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_materials_category ON materials(material_category);
CREATE INDEX idx_needs_institution ON material_needs(institution_id);
CREATE INDEX idx_needs_status ON material_needs(status);
CREATE INDEX idx_needs_priority ON material_needs(priority);
CREATE INDEX idx_donations_donor ON donations(donor_id);
CREATE INDEX idx_donations_institution ON donations(institution_id);
CREATE INDEX idx_donations_date ON donations(donation_date);
CREATE INDEX idx_donations_status ON donations(status);

-- VIEWS
CREATE VIEW view_donors AS
SELECT user_id, email, cpf, donor_name, date_birth, endereco, telefone, created_at
FROM users WHERE user_role = 'donor';

CREATE VIEW view_institutions AS
SELECT user_id, email, cnpj, institution_name, endereco, telefone, created_at
FROM users WHERE user_role = 'institution';

CREATE VIEW view_pending_needs AS
SELECT u.institution_name, m.material_name, mn.quantity_needed, mn.priority, p.project_name
FROM material_needs mn
JOIN users u ON mn.institution_id = u.user_id
JOIN materials m ON mn.material_id = m.material_id
LEFT JOIN projects p ON mn.project_id = p.project_id
WHERE mn.status IN ('pendente', 'parcialmente_atendido')
ORDER BY CASE mn.priority WHEN 'urgente' THEN 1 WHEN 'alta' THEN 2 WHEN 'media' THEN 3 ELSE 4 END;

-- TRIGGERS
CREATE FUNCTION update_updated_at_column() RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_projects_updated_at BEFORE UPDATE ON projects
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_material_needs_updated_at BEFORE UPDATE ON material_needs
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_donations_updated_at BEFORE UPDATE ON donations
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_institution_exchanges_updated_at BEFORE UPDATE ON institution_exchanges
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- DADOS DE EXEMPLO
INSERT INTO materials (material_name, material_category, description) VALUES
('Caderno universitário', 'escolar', 'Caderno de 10 matérias'),
('Lápis de cor - 12 cores', 'escolar', 'Conjunto de lápis de cor'),
('Mochila escolar', 'escolar', 'Mochila para transporte de material'),
('Livro didático - Matemática', 'livros', 'Livro de matemática ensino fundamental'),
('Livro didático - Português', 'livros', 'Livro de português ensino fundamental'),
('Computador Desktop', 'tecnologia', 'Computador completo para laboratório'),
('Tablet educacional', 'tecnologia', 'Tablet com aplicativos educacionais'),
('Ferramentas de jardinagem', 'ferramentas', 'Kit para horta comunitária'),
('Sementes diversas', 'ferramentas', 'Sementes de hortaliças'),
('Microfone USB', 'equipamentos', 'Microfone para rádio estudantil'),
('Mesa de som', 'equipamentos', 'Mesa de som para eventos'),
('Bola de futebol', 'equipamentos', 'Bola oficial de futebol'),
('Violão', 'equipamentos', 'Violão para aulas de música');

INSERT INTO users (user_role, email, password_hash, endereco, telefone, cpf, donor_name, date_birth) VALUES
('donor', 'joao.silva@email.com', '$2b$12$hash1', 'Rua das Flores, 123, Crato-CE', '85987654321', '123.456.789-00', 'João Silva', '1990-05-15'),
('donor', 'maria.santos@email.com', '$2b$12$hash2', 'Av. Principal, 456, Juazeiro-CE', '85998765432', '234.567.890-11', 'Maria Santos', '1985-08-22'),
('donor', 'pedro.oliveira@email.com', '$2b$12$hash3', 'Rua Verde, 789, Barbalha-CE', '85976543210', '345.678.901-22', 'Pedro Oliveira', '1992-03-10');

INSERT INTO users (user_role, email, password_hash, endereco, telefone, cnpj, institution_name) VALUES
('institution', 'contato@escolaesperanca.org', '$2b$12$hash4', 'Av. Educação, 456, Crato-CE', '85912345678', '12.345.678/0001-90', 'Escola Esperança'),
('institution', 'admin@institutoconhecer.edu.br', '$2b$12$hash5', 'Rua do Saber, 789, Juazeiro-CE', '85923456789', '23.456.789/0001-01', 'Instituto Conhecer'),
('institution', 'info@projetofuturo.org.br', '$2b$12$hash6', 'Av. Progresso, 321, Barbalha-CE', '85934567890', '34.567.890/0001-12', 'Projeto Futuro');

INSERT INTO projects (institution_id, project_name, project_description, project_type, status, start_date) VALUES
(4, 'Horta Comunitária Escolar', 'Projeto de horta para ensino de sustentabilidade', 'horta_comunitaria', 'ativo', '2026-01-15'),
(4, 'Rádio Escola Esperança FM', 'Criação de rádio estudantil', 'radio_estudantil', 'ativo', '2026-02-01'),
(5, 'Oficina de Leitura', 'Oficinas semanais de leitura', 'oficina', 'ativo', '2026-01-20'),
(6, 'Minicurso de Informática', 'Introdução à informática básica', 'minicurso', 'ativo', '2026-02-05');

INSERT INTO material_needs (institution_id, project_id, material_id, quantity_needed, priority, status) VALUES
(4, 1, 8, 10, 'urgente', 'pendente'),
(4, 1, 9, 20, 'alta', 'pendente'),
(4, 2, 10, 2, 'alta', 'pendente'),
(5, 3, 4, 30, 'urgente', 'pendente'),
(6, 4, 6, 10, 'alta', 'pendente'),
(6, NULL, 1, 50, 'media', 'pendente');

INSERT INTO donations (donor_id, institution_id, material_id, quantity_donated, donation_date, status, notes) VALUES
(1, 4, 1, 20, '2026-01-28', 'entregue', 'Doação de cadernos novos'),
(2, 5, 4, 15, '2026-01-27', 'confirmada', 'Livros em bom estado'),
(3, 6, 6, 3, '2026-01-26', 'pendente', 'Computadores de upgrade'),
(1, 4, 8, 5, '2026-01-25', 'entregue', 'Kit de ferramentas'),
(2, 5, 5, 10, '2026-01-24', 'entregue', 'Livros novos');

INSERT INTO institution_exchanges (institution_from_id, institution_to_id, exchange_type, description, status) VALUES
(4, 5, 'conhecimento', 'Compartilhar experiência em criar rádio estudantil', 'proposta'),
(5, 6, 'material', 'Emprestar 5 computadores temporariamente', 'aceita'),
(6, 4, 'ambos', 'Parceria para horta comunitária conjunta', 'em_andamento');
