import {Entity, Component} from "/ECS/ecs.js";

import {Mover} from "/ECS/components/movement.js";
import {CircleSprite} from "/ECS/components/sprites.js";

const BALL_R = 8;
const BALL_SPEED = 350;

export class Ball extends Entity {
	constructor(x, y) {
		super(x, y, [new CircleSprite(BALL_R)]);
		this.add_component(this.mover = new Mover(BALL_SPEED, BALL_SPEED));

		this.radius = BALL_R; // so that the game entity can know
	}

	update(delta) {
		let next_x = this.x + this.mover.xvel * delta;
		let next_y = this.y + this.mover.yvel * delta;

		if (next_x + BALL_R >= WIN_W || next_x - BALL_R <= 0) {
			this.mover.xvel *= -1;
		}
		if (next_y + BALL_R >= WIN_H || next_y - BALL_R <= 0) {
			this.mover.yvel *= -1;
		}

		super.update(delta);
	}
}

