const manifest = (() => {
function __memo(fn) {
	let value;
	return () => value ??= (value = fn());
}

return {
	appDir: "_app",
	appPath: "_app",
	assets: new Set([]),
	mimeTypes: {},
	_: {
		client: {"start":"_app/immutable/entry/start.D65rAvI6.js","app":"_app/immutable/entry/app.Kcny67sR.js","imports":["_app/immutable/entry/start.D65rAvI6.js","_app/immutable/chunks/client.D5aGrkoG.js","_app/immutable/entry/app.Kcny67sR.js","_app/immutable/chunks/preload-helper.DpQnamwV.js"],"stylesheets":[],"fonts":[],"uses_env_dynamic_public":false},
		nodes: [
			__memo(() => import('./chunks/0-56XYbDH8.js')),
			__memo(() => import('./chunks/1-Cmi1gKpK.js')),
			__memo(() => import('./chunks/2-DWmO7qBD.js').then(function (n) { return n.aD; }))
		],
		routes: [
			{
				id: "/[...catchall]",
				pattern: /^(?:\/(.*))?\/?$/,
				params: [{"name":"catchall","optional":false,"rest":true,"chained":true}],
				page: { layouts: [0,], errors: [1,], leaf: 2 },
				endpoint: null
			}
		],
		matchers: async () => {
			
			return {  };
		},
		server_assets: {}
	}
}
})();

const prerendered = new Set([]);

const base = "";

export { base, manifest, prerendered };
//# sourceMappingURL=manifest.js.map
