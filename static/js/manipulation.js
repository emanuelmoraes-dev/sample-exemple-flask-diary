// Autor: Emanuel Moraes de Almeida
// email: emanuelmoraes297@gmail.com

var ready = function (fn) {
    if (document.attachEvent ? document.readyState === "complete" : document.readyState !== "loading") {
        fn();
    } else {
        document.addEventListener('DOMContentLoaded', fn);
    }
}

var setCenter = function (element, superelement, position, isready, onresize) {

    if (position === undefined)
        position = 'absolute'

    if (isready === undefined)
        isready = true

    if (onresize === undefined)
        onresize = true
    
    if (!superelement)
        superelement = window
    else if(typeof (superelement) == 'string')
        superelement = document.getElementById(superelement)

    var go = function () {

        if (superelement === window) {
            var widthScreen = superelement.innerWidth
            var heightScreen = superelement.innerHeight
        } else {
            var widthScreen = superelement.offsetWidth
            var heightScreen = superelement.offsetHeight
        }

        if (!element) {
            element = document.getElementById('center')
        } else if (typeof (element) == 'string') {
            element = document.getElementById(element)
        }

        if (!element)
            return

        var width = element.offsetWidth
        var height = element.offsetHeight

        console.log(width, widthScreen)
        console.log(height, heightScreen)

        element.style.position = position
        element.style.left = ((widthScreen - width) / 2) + 'px'
        element.style.top = ((heightScreen - height) / 2) + 'px'
    }

    if (onresize) {
        window.onresize = go;
    }

    if (isready) {
        ready(go);
    } else {
        go();
    }
}

/*
    Instruções:
    Para centralizar um componente, basta chamar a função setCenter:
        1º Argumento: componente a ser centralizado (Pode ser o id ou o elemento retornado via javascript. Por padrão o valor é o id "center")
        2º Argumento: componente pai do componente a ser centralizado (pode ser o id ou um elemento retornado via javascript. Por padrão o pai é a própria janela)
        3º Argumento: position do elemento a ser centralizado (absolute é o padrão)
        4º Argumento: se for true, o código será executado somente depois de toda a página ser recarregada (true é o padrão)
        5º Argumento: se for true, o componente será centralizado mesmo depois da tela ser redimencionada (true por padrão)

    Os valores padrões são passados caso os argumentos não sejam passados.
*/