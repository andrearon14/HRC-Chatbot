serial = 0;

function submit_message(message) {
    add_loading();
    scroll_down();

    $.post( "/send_message", {message: message}, handle_response);

    function handle_response(data) {
        serial += 1;

        if (data.fotos) {
            var lista = ""
            data.fotos.forEach(function(element) {
                lista += `<div><img src="static/img/${element.foto}"><div>${element.nombre}</div><div>${element.cargo}</div></div>`
            });
            $('.chat-container').append(`
                <div class="chat-message fotos col-md-12 bot-message">
                    ${lista}
                </div>
            `);
        }
        else {
            var msg = data.message
            if (data.calendar)
                msg = "Por favor elija cuando desea tomarse su licencia";

            $('.chat-container').append(`
                <div class="chat-message col-md-5 offset-md-7 bot-message">
                    ${msg}
                </div>
            `);

            if (data.calendar) {
                $('.chat-container').append(`
                    <div id="calendar${serial}" class="chat-message col-md-5 human-message">
                        <label for="from${serial}">Desde</label>
                        <input type="text" id="from${serial}">
                        <label for="to${serial}">hasta</label>
                        <input type="text" id="to${serial}">
                        <button type="button" id="send${serial}">Enviar</button>
                        <button type="button" id="cancel${serial}">Cancelar</button>
                    </div>
                `);
                initialize_calendar(data.calendar);
            }
        }

        // remove all the loading indicator
        while (true) {
            var loading = $("#loading")
            if (loading.length)
                loading.remove()
            else
                break;
        }

        scroll_down();
    }
}

$('#target').on('submit', function(e){
    e.preventDefault();
    const input_message = $('#input_message').val()
    if (!input_message) {
        // return if the user does not enter any text
        return
    }

    $('.chat-container').append(`
        <div class="chat-message col-md-5 human-message">
            ${input_message}
        </div>
    `)

    // clear the text input 
    $('#input_message').val('');
    $( "#calendar" + serial ).remove();

    submit_message(input_message);
});

function add_loading() {
    $('.chat-container').append(`
        <div class="chat-message text-center col-md-2 offset-md-10 bot-message" id="loading">
            <b>...</b>
        </div>
    `)
}

function scroll_down() {
    var scroll=$( '#chat' );
    scroll.animate({scrollTop: scroll.prop("scrollHeight")});
}

function initialize_calendar(ocuppiedDates) {
    $( function() {
        function showDay( d ) {
            var dmy = "";
            if (d.getMonth() < 9) 
                dmy += "0";
            dmy += (d.getMonth()+1) + "/"; 

            if (d.getDate() < 10)
                dmy += "0"; 
            dmy += d.getDate() + "/"; 

            dmy += (d.getFullYear()-2000);

            if ($.inArray(dmy, ocuppiedDates) != -1)
                return [false, "", "Uma se va de joda"];  
            else
                return [true, "", ""]; 
        }

        var dateformat = "dd-mm-yy",
        from = $( "#from" + serial ).datepicker({
            dateFormat: dateformat,
            numberOfMonths: 2,
            minDate: 0,
            beforeShowDay: showDay
        })
        .on( "change", function() {
            to.datepicker( "option", "minDate", getDate( this ) );
        });
        
        var to = $( "#to" + serial ).datepicker({
            dateFormat: dateformat,
            numberOfMonths: 2,
            beforeShowDay: showDay
        })
        .on( "change", function() {
            from.datepicker( "option", "maxDate", getDate( this ) );
        });

        var calendar = $( "#calendar" + serial )

        $( "#send" + serial ).click(function() {
            calendar.html( "Quisiera pedir del " + from.val() + " al " + to.val() + "." );
            submit_message( from.val() + " y " + to.val() );
        });

        $( "#cancel" + serial ).click(function() {
            calendar.html( "Cancelar, por favor." );
            submit_message( "cancelar" );
        });

        function getDate( element ) {
            var date;
            try {
                date = $.datepicker.parseDate( dateformat, element.value );
            } catch( error ) {
                date = null;
            }
            return date;
        }
    });
}