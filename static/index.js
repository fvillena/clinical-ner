
// head.js(
//     // External libraries
//     'static/client/lib/jquery.min.js',
//     'static/client/lib/jquery.svg.min.js',
//     'static/client/lib/jquery.svgdom.min.js',

//     // brat helper modules
//     'static/client/src/configuration.js',
//     'static/client/src/util.js',
//     'static/client/src/annotation_log.js',
//     'static/client/lib/webfont.js',

//     // brat modules
//     'static/client/src/dispatcher.js',
//     'static/client/src/url_monitor.js',
//     'static/client/src/visualizer.js'
// );

$(document).ready(function() {    
    // var webFontURLs = [
    //     'fonts/Astloch-Bold.ttf',
    //     'fonts/PT_Sans-Caption-Web-Regular.ttf',
    //     'fonts/Liberation_Sans-Regular.ttf'
    // ];
    
    var collData = {
        entity_types: [ {
                type   : 'Disease',
                /* The labels are used when displaying the annotion, in this case
                    we also provide a short-hand "Per" for cases where
                    abbreviations are preferable */
                labels : ['Disease', 'Dis'],
                // Blue is a nice colour for a person?
                bgColor: '#7fa2ff',
                // Use a slightly darker version of the bgColor for the border
                borderColor: 'darken'
        } ]
    };
    
    var docData = {
        "entities": [
            // [
            //     "T1",
            //     "Disease",
            //     [
            //         [
            //             18,
            //             36
            //         ]
            //     ]
            // ]
        ],
        "labels": [
            "O",
            "O",
            "O",
            "B-Disease",
            "I-Disease",
            "I-Disease"
        ],
        "tagged_string": "el paciente tiene cáncer <B-Disease> de <I-Disease> tiroides <I-Disease>",
        "text": "",
        "tokens": [
            "el",
            "paciente",
            "tiene",
            "cáncer",
            "de",
            "tiroides"
        ]
    }
    
    var liveDispatcher = Util.embed('brat',
                collData,
                docData,
                undefined);

    
    function annotate(text) {
        $("#spinner").show();
        $("#button").addClass('disabled');
        $.ajax("https://pln.cmm.uchile.cl/clinical-ner/endpoint", {
            data : JSON.stringify({"text":text}),
            contentType : 'application/json',
            type : 'POST',
        }).success(function (data) {
            $("#spinner").hide();
            $("#button").removeClass('disabled');
            liveDispatcher.post("requestRenderData", [data]);
        })
    }
    
    $("#button").click(function () {
        annotate($("#text").val())
    })
    $("#example-medical").click(function () {
        $("#text").val("HTA DM CA COLON OPERADO ANEMIA TROMBOSIS HPB MARCAPASOS ULTIMO CONTROL DE TELEMETRIA ABRIL15 HISTOGRAMA SIN EVENTOS MCP CON BUEN SENSADO Y CAPTURA, TVP VENA AXILAR IZQUIERDA EN TACO LE DETECTARON GLAUCOMA EN TTO")
    })
    $("#example-dental").click(function () {
        $("#text").val("Se envía pieza 1.3 caries dentinaria penetrante, lesion apical compatible con granuloma periapical. Trepanada y eliminada la caries. Aun presenta remanete denario suficiente para rehabilitarlo y ser pilar de protesis.")
    })
    
});

