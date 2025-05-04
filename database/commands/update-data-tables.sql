-- Update registros na tabela sessoes

UPDATE sessoes SET {', '.join(campos)} WHERE id=%s;
