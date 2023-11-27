
$(document).ready(function() {
    if ($("#citacion_select").val() === "None") {
        $(".form-control").prop("disabled", true);
        $(".form-select.aprendiz").prop("disabled", true);
        $('[name="submit"]').prop("disabled", true);
    };
    const asyn = () =>{
        if ($("#citacion_select").val() === "None") {
            $(".form-control").prop("disabled", true);
            $(".form-select.aprendiz").prop("disabled", true);
            $('[name="submit"]').prop("disabled", true);
            return false
        } else {
            $(".form-control").prop("disabled", false);
            $(".form-select.aprendiz").prop("disabled", false);
            $('[name="submit"]').prop("disabled", false);
            return true
        }
    }
    $('#aprendiz_select').change(async function() {
        var aprendizId = $(this).val();
        
        try {
            const response = await fetch('/citacion/aprendiz/obtenerDatosAprendiz/' + aprendizId, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            
            if (!response.ok) {
                throw new Error('Error en la solicitud AJAX');
            }
            
            const data = await response.json();
            $('#correo_Aprendiz').val(data.otro_campo);
        } catch (error) {
            console.error('Error en la solicitud AJAX:', error.message);
        }
    });
    
    
    
    
    $("#citacion_select").on("click",async () =>{
        asyn()
        var citacionId= document.getElementById("citacion_select");
        
        const responseCt = await fetch('/citacion/aprendiz/obtenerDatosCitaciones/' + citacionId.value, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });
        
        if (!responseCt.ok) {
            throw new Error('Error en la solicitud AJAX');
        }
        const dataCt = await responseCt.json();

        if (dataCt.error){
            $("#hora").prop("disabled", true);
        }
        var fechaObjeto = new Date(dataCt.fecha);
        if (!isNaN(fechaObjeto.getTime())) {
            $("#hora").val("12:02")
            $("#fecha").val(fechaObjeto.toISOString().slice(0,10));
        } else {
            $("#hora").val(null)
            $("#fecha").val(null);
        }
    })
});

