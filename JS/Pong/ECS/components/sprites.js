import {Entity, Component} from "../ecs.js"

export class CircleSprite extends Component {
	constructor(radius) {
		super();
		this.radius = radius;
	}

	draw() {
		circle(this.owner.x, this.owner.y, this.radius * 2)
	}
}

export class RectSprite extends Component {
	constructor(w, h) {
		super();
		this.w = w;
		this.h = h;
	}

	draw() {
		rect(this.owner.x - this.w/2, this.owner.y - this.h/2, this.w, this.h);
	}
}

