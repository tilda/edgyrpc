// Copyright (c) 2020 S Stewart
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

function getTabs() {
    chrome.tabs.query({}, function(t) {
        globalThis.tabs = t.length
        console.log(`number of tabs currently open: ${t.length}`)
    })
}

chrome.runtime.onInstalled.addListener(function() {
    getTabs()
    chrome.alarms.create("jsdklgjsiofjd", {
        "periodInMinutes": 1
    })
})

chrome.alarms.onAlarm.addListener(function() {
    getTabs()
    var ws = new WebSocket("ws://localhost:3233")
    ws.onopen = function () {
        ws.send(globalThis.tabs)
    }
})