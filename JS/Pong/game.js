import {Entity, Component} from "/ECS/ecs.js";

import {Ball} from "/ECS/entities/ball.js";
import {Paddle} from "/ECS/entities/paddle.js";

const PADDLE_DIST = 50;

class Game extends Entity {
	constructor() {
		super(0, 0, []);

		this.ball = new Ball(WIN_W/2, WIN_H/2);
		entities.push(this.ball);

		this.paddle_l = new Paddle(PADDLE_DIST, WIN_H/2);
		entities.push(this.paddle_l);

		this.paddle_r = new Paddle(WIN_W - PADDLE_DIST, WIN_H/2);
		entities.push(this.paddle_r);
	}

	update(delta) {
		// ball collide
		for (const paddle of [this.paddle_l, this.paddle_r])
		if (this.ball.x - this.ball.radius < paddle.x + paddle.w/2 &&
		    this.ball.x + this.ball.radius > paddle.x - paddle.w/2 &&
		    this.ball.y - this.ball.radius < paddle.y + paddle.h/2 &&
		    this.ball.y + this.ball.radius > paddle.y - paddle.h/2) {
			this.ball.mover.xvel *= -1;
		}
	}
}

let game = new Game();
entities.push(game);

