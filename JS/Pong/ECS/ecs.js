export class Component {
	constructor() {
		this.owner = null;
	}

	update(delta) {
		return;
	}

	draw() {
		return;
	}
}

export class Entity {
	constructor(x, y, components) {
		this.x = x;
		this.y = y;

		this.components = components;
		for (let c of this.components) {
			c.owner = this;
		}
	}

	update(delta) {
		for (const c of this.components) {
			c.update(delta);
		}
		return;
	}

	draw() {
		for (const c of this.components) {
			c.draw();
		}
		return;
	}

	add_component(c) {
		this.components.push(c);
		c.owner = this;
	}
}

