import {Entity, Component} from "../ecs.js";

import {Mover} from "../components/movement.js";
import {RectSprite} from "../components/sprites.js";

const PADDLE_SPEED = 300;

const PADDLE_W = 10;
const PADDLE_H = 80;

const PADDLEL_UP   = 87; // W
const PADDLEL_DOWN = 83; // S

const PADDLER_UP   = 38; // UP_ARROW
const PADDLER_DOWN = 40; // DOWN_ARROW

export class Paddle extends Entity {
	constructor(x, y) {
		super(x, y, [new RectSprite(PADDLE_W, PADDLE_H)]);

		// so that the game entity can know
		this.w = PADDLE_W;
		this.h = PADDLE_H;
	}

	update(delta) {
		let next_y;
		if (this.x < WIN_W/2) {
			// left paddle (i hate this)
			if (keyIsDown(PADDLEL_UP)   && (next_y = this.y - PADDLE_SPEED * delta) - PADDLE_H/2 > 0 ||
			    keyIsDown(PADDLEL_DOWN) && (next_y = this.y + PADDLE_SPEED * delta) + PADDLE_H/2 < WIN_H) {
				this.y = next_y;
			}

			return;
		}
		// right paddle
		if (keyIsDown(PADDLER_UP)   && (next_y = this.y - PADDLE_SPEED * delta) - PADDLE_H/2 > 0 ||
		    keyIsDown(PADDLER_DOWN) && (next_y = this.y + PADDLE_SPEED * delta) + PADDLE_H/2 < WIN_H) {
			this.y = next_y;
		}
	}
}

