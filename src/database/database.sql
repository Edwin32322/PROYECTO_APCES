DELIMITER //

CREATE PROCEDURE RegistrarLlamadoYValidar(
    p_num_Ficha,
    p_nombre_Aprendiz
    p_correo_Aprendiz
    p_num_Llamados
    p_nombre_Instructor
    p_fecha 
    p_falta 
    p_tipo_Falta
    p_art_Incumplido
    p_motivo 
    p_plan_Mejora
    p_firma_Instructor
    p_firma_Aprendiz
    p_firma_Vocero
    p_id_CasoAprendizFK 
    p_id_UsuarioFK
_
)
BEGIN
    DECLARE totalLlamados INT;

    SELECT COUNT(id_CasoAprendizFK) INTO totalLlamados
    FROM llamadoatencion
    WHERE id_CasoAprendizFK = p_id_CasoAprendizFK;

    -- Verificar si el aprendiz ha superado los dos llamados o tiene un llamado GRAVISIMO
    IF p_tipo_falta = 'GRAVISIMA' THEN
        -- Registrar el caso para citación
        INSERT INTO CasoParaCitacion (motivo_ParaCitacion, id_CasoAprendizFK)
        VALUES ('FALTA GRAVE', p_id_CasoAprendiz);

        -- Puedes realizar otras acciones aquí si es necesario
    ELSE IF 
        INSERT INTO  CasoParaCitacion (motivo_ParaCitacion, id_CasoAprendizFK)
        VALUES ('+2 LLAMADOS DE ATENCION', p_id_CasoAprendizFK);
    END IF;
    
    INSERT INTO `llamadoatencion`(`num_Ficha`, `nombre_Aprendiz`, `correo_Aprendiz`, `num_LlamadosAtencion`, `nombre_Instructor`, `fecha`, `falta`, `tipo_falta`, `art_Incumplido`, `motivo`, `plan_Mejora`, `firma_Instructor`, `firma_Aprendiz`, `firma_Vocero`, `id_CasoAprendizFK`, `id_UsuarioFK`) 
    VALUES (p_num_Ficha)

END;

//

DELIMITER ;
