import {Entity, Component} from "../ecs.js"

export class Mover extends Component {
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

