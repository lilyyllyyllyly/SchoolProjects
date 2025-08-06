import {Entity, Component} from "../ecs.js";

import {Mover} from "../components/movement.js";
import {CircleSprite} from "../components/sprites.js";

import {Event} from "../../event.js";

const BALL_R = 8;
const BALL_SPEED = 350;

const BALL_DELAY = 1.0;

const BALL_ANGLE_RANGE = 130;
const BALL_MIN_ANGLE = 25;

export class Ball extends Entity {
	constructor(paddles) {
		super(WIN_W/2, random(BALL_R, WIN_H - BALL_R), [new CircleSprite(BALL_R)]);

		let r = random(radians(BALL_ANGLE_RANGE)) + radians(BALL_MIN_ANGLE);
		let dirx = sin(r) * ((random([0, 1]) === 0)? 1 : -1);
		let diry = cos(r);
		this.add_component(this.mover = new Mover(BALL_SPEED * dirx, BALL_SPEED * diry));

		this.radius = BALL_R; // so that the game entity can know
		this.paddles = paddles;

		this.hit_left  = new Event();
		this.hit_right = new Event();

		this.delay = BALL_DELAY;
	}

	update(delta) {
		if (this.delay > 0) {
			this.delay -= delta;
			return;
		}

		let next_x = this.x + this.mover.xvel * delta;
		let next_y = this.y + this.mover.yvel * delta;

		// sides collide
		if (next_x + BALL_R >= WIN_W) {
			this.hit_right.raise(this);
			this.mover.xvel *= -1;
		}
		if (next_x - BALL_R <= 0) {
			this.hit_left.raise(this);
			this.mover.xvel *= -1;
		}

		// top/bottom collide
		if (next_y + BALL_R >= WIN_H || next_y - BALL_R <= 0) {
			this.mover.yvel *= -1;
		}

		// paddle collide
		for (const paddle of this.paddles) {
			if (next_x - BALL_R <= paddle.x + paddle.w/2 &&
			    next_x + BALL_R >= paddle.x - paddle.w/2 &&
			    next_y - BALL_R <= paddle.y + paddle.h/2 &&
			    next_y + BALL_R >= paddle.y - paddle.h/2) {
				this.mover.xvel = (this.x < WIN_W/2) ? abs(this.mover.xvel) : -abs(this.mover.xvel);
			}
		}

		super.update(delta);
	}
}

