const WIN_W = 600
const WIN_H = 400

new p5();

let entities = [];

function setup() {
	createCanvas(WIN_W, WIN_H);
	angleMode(RADIANS);
}

function draw() {
	let delta = deltaTime/1000;
	background(0);

	for (const e of entities) {
		e.update(delta);
		e.draw();
	}
}

function clamp(t, min, max) {
	return Math.min(Math.max(t, min), max);
}

