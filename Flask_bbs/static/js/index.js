var e = function (sel) {
    return document.querySelector(sel)
}

var es = function (sel) {
    return document.querySelectorAll(sel)
}

var markContents = function () {
    // markdown -> html 的处理放在高亮前面
    // 因为高亮是针对 html 格式的
    // lang -> language 不需要转 prism 自动转了
    var contentDivs = es('.markdown-text')
    for (var i = 0; i < contentDivs.length; i++) {
        var contentDiv = contentDivs[i]
        console.log('pre marked', contentDiv.textContent)
        var content = marked(contentDiv.textContent)
        console.log('after marked', content)
        contentDiv.innerHTML = content
    }
}

var highlight = function () {
    // 自动加载对应的语言 不然要手动加入各个语言的 js
    Prism.plugins.autoloader.languages_path = 'https://cdn.bootcss.com/prism/1.13.0/components/'
}
var update_time = function () {
    var times = es('.created-time')
    for (var i = 0; i < times.length; i++) {
        var t = times[i]
        var time = Number(t.dataset.created_time)
        var now = Math.floor(new Date() / 1000)
        var delta = now - time
        var s = ''
        if (delta > 31536000) {
            year = Math.floor(delta / 31536000)
            s = ` ${year} 年前`
        } else if (delta > 2592000) {
            year = Math.floor(delta / 2592000)
            s = ` ${year} 个月前`
        } else if (delta > 2592000) {
            year = Math.floor(delta / 2592000)
            s = ` ${year} 个月前`
        } else if (delta > 84600) {
            year = Math.floor(delta / 86400)
            s = ` ${year} 天前`
        } else if (delta > 3600) {
            year = Math.floor(delta / 3600)
            s = ` ${year} 小时前`
        } else if (delta > 60) {
            year = Math.floor(delta / 60)
            s = ` ${year} 分钟前`
        } else {
            s = ` 几秒前`
        }

        t.innerText = s
    }
}
var registerTimer = function () {
    setInterval(update_time, 1000)
}

function footer() {
    ($(document.body).height() + $("#footer").height()) < $(window).height() ? $("#footer").addClass("fix-bottom") : $("#footer").removeClass("fix-bottom")
}

$(document).ready(function () {
    footer()
})

var __main = function () {
    update_time()
    markContents()
    highlight()
    registerTimer()

}

__main()
