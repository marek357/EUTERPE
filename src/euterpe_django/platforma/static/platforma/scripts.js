let address="http://127.0.0.1:8000/endpoint/";
function help() {
    Swal.fire({
        title: "Witamy na platformie EUTERPE!",
        customClass: "opis",
        showConfirmButton: false,
        html: "<div style='font-size: 1.1em; text-align: left;'>" +
            "<br><b> Co to jest?</b><br><br>" +
            "Jest to rewolucyjna plaforma, dzięki której już za chwilę bedziesz mógł cieszyć się " +
            "muzyką wygenerowaną specjalnie dla ciebie!<br><br>" +
            "<b>Jak to działa?</b><br><br>" +
            "Po prostu określ parametry dla swojej wymarzonej piosenki, a nasze algorytmy zajmą się resztą.<br><br>" +
            "<b>Jakie parametry mogę określić?</b><br><br>" +
            "W polu znajdującym się na środku strony wybierz R, jeśli chcesz posłuchać " +
            "muzyki z parametrami losowymi lub gatunek muzyki, który chcesz posłuchać.<br><br>" +
            "<b>Jakie gatunki mogę wpisać?</b><br><br>" +
            "Obecnie wspieranymi gatunkami są: Country<br><br>" +
            "<b>Gdzie mogę odsłuchać wygenerowanych utworów?</b><br><br>" +
            "Kliknij logo historii, znajdujące się w prawym górnym rogu strony" +
            "</div>"
    });
}
function generate(csrf_token) {
    Swal.fire({
        icon: 'info',
        title: 'Utwór w trakcie generowania',
        text: 'Prosimy o cierpliwość',
        onBeforeOpen: () => {
            Swal.showLoading()
        }
    });
    $.ajax({
        url: address,
        method: "post",
        dataType: "json",
        data: {
            genre: $("#wybor-gatunku").val(),
            csrfmiddlewaretoken: csrf_token
        },
        success: function(data) {
            Swal.fire({
                icon: 'success',
                title: 'Udało się!',
                showConfirmButton: true,
                showCancelButton: true,
                confirmButtonText: 'Przejdź do wygenerowanego utworu',
                cancelButtonText: 'Wygeneruj kolejny utwór',
                position: 'top-end',
            }).then((result) => {
                if (result["isConfirmed"]) {
                    window.location.href = "http://127.0.0.1:8000/list/";
                }
            });
        }
    });
}
function music_history() {
    window.location.href = "http://127.0.0.1:8000/list/";
}