import {Entity, Component} from "../ecs.js";

import {Mover} from "../components/movement.js";
import {RectSprite} from "../components/sprites.js";

const PADDLE_SPEED =  300;
const PADDLE_MAX_ACCEL = 3000;

const PADDLE_DASH_SPEED = 1000;
const PADDLE_DASH_DELAY = 1.0;

const PADDLE_W = 10;
const PADDLE_H = 80;

const PADDLEL_SCHEMES = [
	{up:   87,  // W
	 down: 83,  // S
	 dash: 65}, // A

	{dash: 68}, // D
];

const PADDLER_SCHEMES = [
	{up:   73,  // I
	 down: 75,  // K
	 dash: 74}, // J

	{up:   38,  // UP_ARROW
	 down: 40,  // DOWN_ARROW
	 dash: 76}, // L

	{dash: 37}, // LEFT_ARROW

	{dash: 39}, // RIGHT_ARROW
];

export class Paddle extends Entity {
	constructor(x, y) {
		super(x, y, [new RectSprite(PADDLE_W, PADDLE_H)]);
		this.add_component(this.mover = new Mover(0, 0));

		// so that the game entity can know
		this.w = PADDLE_W;
		this.h = PADDLE_H;

		this.dash_delay = 0;
	}

	update(delta) {
		this.dash_delay -= delta;
		let goal_vel = 0;
		let dir = 0;

		let schemes = (this.x < WIN_W/2) ? PADDLEL_SCHEMES : PADDLER_SCHEMES;
		for (const scheme of schemes) {
			// dash
			if (this.dash_delay <= 0 && keyIsDown(scheme.dash)) {
				this.mover.yvel += Math.sign(this.mover.yvel) * PADDLE_DASH_SPEED;
				this.dash_delay = PADDLE_DASH_DELAY;
			}

			// movement
			if (scheme.down === undefined || scheme.up === undefined) continue;

			if ((dir = (+keyIsDown(scheme.down)) - (+keyIsDown(scheme.up))) === 0) {
				continue;
			}

			goal_vel = dir * PADDLE_SPEED;
		}

		let max_move = PADDLE_MAX_ACCEL * delta * ((goal_vel != 0 && Math.sign(goal_vel) != Math.sign(this.mover.yvel))? 2 : 1)
		this.mover.yvel += clamp(goal_vel - this.mover.yvel, -max_move, max_move);

		// collide
		let ref;
		let next_y = this.y + this.mover.yvel * delta;
		if (next_y > (ref = WIN_H - PADDLE_H/2) || next_y < (ref = PADDLE_H/2)) {
			this.mover.yvel = (ref - this.y) / delta;
		}

		super.update(delta);
	}
}

