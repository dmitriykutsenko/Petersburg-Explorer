ymaps.ready(function showPanorama(x, y) {

    // Для начала проверим, поддерживает ли плеер браузер пользователя.
    if (!ymaps.panorama.isSupported()) {
        // Если нет, то просто ничего не будем делать.
        return;
    }

    // Ищем панораму в переданной точке.
    ymaps.panorama.locate([x, y]).done(
        function (panoramas) {
            // Убеждаемся, что найдена хотя бы одна панорама.
            if (panoramas.length > 0) {
                // Создаем плеер с одной из полученных панорам.
                window.player = new ymaps.panorama.Player(
                    'player1',
                    // Панорамы в ответе отсортированы по расстоянию
                    // от переданной в panorama.locate точки. Выбираем первую,
                    // она будет ближайшей.
                    panoramas[0],

                    // Зададим направление взгляда, отличное от значения
                    // по умолчанию.
                    {
                        direction: [256, 16],
                        controls: []
                    }
                );
                window.panorama = player.getPanorama();
                player.events.add('panoramachange', function () {
                    window.panorama = player.getPanorama();
                });
            }
        },
        function (error) {
            // Если что-то пошло не так, сообщим об этом пользователю.
            alert(error.message);
        }
    );
    // Для добавления панорамы на страницу также можно воспользоваться
    // методом panorama.createPlayer. Этот метод ищет ближайщую панораму и
    // в случае успеха создает плеер с найденной панорамой.
});

function getCoordinates() {
    alert(panorama.getPosition()[0] + " " + panorama.getPosition()[1]);
}

function movePanorama(x, y) {
    player.moveTo([x, y]);
}