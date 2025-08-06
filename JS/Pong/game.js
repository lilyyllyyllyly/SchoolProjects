import {Entity, Component} from "./ECS/ecs.js";

import {Ball} from "./ECS/entities/ball.js";
import {Paddle} from "./ECS/entities/paddle.js";

const PADDLE_DIST = 50;

const TEXT_COLOR = 255;
const TEXT_SIZE = 16;
const TEXT_DIST = 25;

const BALL_SPAWN_TIME = 5.0;

const WINNER_SHOW_TIME = 1.0;

class Game extends Entity {
	constructor() {
		super(0, 0, []);

		this.win_condition = 10;
		this.score_l = this.score_r = 0;
		this.state = "menu"; // i hate using a string for this but its 4:28am i need to be done
		this.winner = "First to " + this.win_condition +  " wins!";
		this.winner_time = 0;
	}

	start_game() {
		this.state = "game";
		this.score_l = this.score_r = 0;

		this.paddles = [
			new Paddle(PADDLE_DIST, WIN_H/2),
			new Paddle(WIN_W - PADDLE_DIST, WIN_H/2),
		];
		for (const paddle of this.paddles) entities.push(paddle);

		this.balls = [];
		this.add_ball();

		this.ball_timer = BALL_SPAWN_TIME;
	}

	end_game() {
		this.state = "menu";
		this.winner = this.score_l > this.score_r? "P1 WINS" : "P2 WINS";
		this.winner_time = WINNER_SHOW_TIME;

		entities = [this];
		this.balls = [];
	}

	update(delta) {
		if (this.state !== "game") {
			// menu
			if (keyIsDown(32) /* Space */) {
				this.start_game();
				return;
			}

			let n = keyCode - 48; // 0
			this.win_condition = n > 0 && n < 10? n : 10;

			if (this.winner_time <= 0 && keyIsPressed) this.winner = "First to " + this.win_condition +  " wins!";
			this.winner_time -= delta;

			return;
		}

		if (keyIsDown(82) /* R */) {
			this.end_game();
			this.winner = "First to " + this.win_condition +  " wins!";
			return;
		}

		if (this.ball_timer > 0) {
			this.ball_timer -= delta;
			return;
		}

		this.add_ball();
	}

	draw() {
		fill(TEXT_COLOR);
		textSize(TEXT_SIZE);
		textFont("Monospace");

		if (this.state !== "game") {
			// menu
			textAlign(CENTER);

			text("(totally normal)", WIN_W/2, TEXT_DIST*3);

			textSize(TEXT_SIZE*4);
			text("PONG", WIN_W/2, TEXT_DIST*3 + TEXT_SIZE*3);

			textSize(TEXT_SIZE*2);
			text("> Press SPACE <", WIN_W/2, WIN_H - TEXT_DIST*3)

			text(this.winner, WIN_W/2, WIN_H/2 + TEXT_SIZE);

			return;
		}

		textAlign(LEFT);
		text(this.score_l, TEXT_DIST, TEXT_DIST);

		textAlign(RIGHT);
		text(this.score_r, WIN_W - TEXT_DIST, TEXT_DIST);

		textAlign(CENTER);
		text("DASH:\nA/D (P1)\n←/→ (P2)", WIN_W/2, TEXT_DIST)

		super.draw();
	}

	add_ball() {
		let ball = new Ball(this.paddles);
		this.balls.push(ball);
		entities.push(ball);

		ball.hit_left.register( (ball) => {this.score_r++; this.remove_ball(ball)});
		ball.hit_right.register((ball) => {this.score_l++; this.remove_ball(ball)});

		this.ball_timer = BALL_SPAWN_TIME;
	}

	remove_ball(ball) {
		if (this.score_l >= this.win_condition || this.score_r >= this.win_condition) {
			this.end_game();
			return;
		}

		this.balls = this.balls.filter(x => x !== ball);
		entities = entities.filter(x => x !== ball);

		if (this.balls.length <= 0) this.add_ball();
	}
}

let game = new Game();
entities.push(game);

