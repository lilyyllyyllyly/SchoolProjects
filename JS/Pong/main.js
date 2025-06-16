const WIN_W = 600
const WIN_H = 400
const BALLR = 15

class Component {
	constructor() {
		this.owner = null;
	}

	update(delta) {
		return;
	}

	draw(delta) {
		return;
	}
}

class GameObject {
	constructor(x, y, components) {
		this.x = x;
		this.y = y;

		this.components = components;
		for (let c of this.components) {
			c.owner = this;
		}
	}

	update(delta) {
		for (let c of this.components) {
			c.update(delta);
		}
		return;
	}

	draw() {
		for (let c of this.components) {
			c.draw(delta);
		}
		return;
	}
}

class Mover extends Component {
	constructor(xvel, yvel) {
		super();
		this.xvel = xvel;
		this.yvel = yvel;
	}

	update(delta) {
		this.owner.x += this.xvel * delta;
		this.owner.y += this.yvel * delta;
	}
}

let ball = new GameObject(WIN_W/2, WIN_H/2, [new Mover(200, 200)]);

function setup() {
	createCanvas(WIN_W, WIN_H);
}

function draw() {
	let delta = deltaTime/1000;
	background(0);

	//let newx = ball.x + ball.xvel * delta;
	//let newy = ball.y + ball.yvel * delta;
	//if (newx + BALLR >= WIN_W || newx - BALLR <= 0) {
	//	ball.xvel *= -1;
	//}
	//if (newy + BALLR >= WIN_H || newy - BALLR <= 0) {
	//	ball.yvel *= -1;
	//}
	ball.update(delta)

	circle(ball.x, ball.y, BALLR*2);
}

