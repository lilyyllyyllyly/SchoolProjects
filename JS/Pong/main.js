const WIN_W = 600
const WIN_H = 400

let entities = [];

function setup() {
	createCanvas(WIN_W, WIN_H);
}

function draw() {
	let delta = deltaTime/1000;
	background(0);

	for (const e of entities) {
		e.update(delta);
		e.draw();
	}
}

