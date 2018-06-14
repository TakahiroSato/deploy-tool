"use strict";
const electron = require("electron");
const app = electron.app;
const BrowserWindow = electron.BrowserWindow;
let mainWindow;

app.on("window-all-closed", function() {
	app.quit();
});

app.on("ready", function() {
	var rq = require("request-promise");
	var mainAddr = "http://localhost:8080";

	var openWindow = function() {
		mainWindow = new BrowserWindow({ width: 800, height: 600 });
		mainWindow.loadURL(mainAddr);
		mainWindow.on("closed", function() {
			mainWindow = null;
		});
	};

	var startUp = function() {
		rq(mainAddr)
			.then(function(htmlString) {
				console.log("server started");
				openWindow();
			})
			.catch(function(err) {
				startUp();
			});
	};
	startUp();
});
