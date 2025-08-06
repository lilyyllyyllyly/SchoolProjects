export class Event {
	constructor() {
		this.callbacks = [];
	}

	register(f) {
		this.callbacks.push(f);
	}

	unregister(f) {
		this.callbacks = this.callbacks.filter(x => x !== f);
	}

	raise(arg) {
		for (const f of this.callbacks) f(arg);
	}
}

