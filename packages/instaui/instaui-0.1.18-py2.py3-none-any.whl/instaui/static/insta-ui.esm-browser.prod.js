var Un = Object.defineProperty;
var Kn = (e, t, n) => t in e ? Un(e, t, { enumerable: !0, configurable: !0, writable: !0, value: n }) : e[t] = n;
var B = (e, t, n) => Kn(e, typeof t != "symbol" ? t + "" : t, n);
import * as Gn from "vue";
import { toRaw as qn, customRef as je, toValue as q, unref as L, watch as G, nextTick as Ie, isRef as Ht, ref as Z, shallowRef as J, watchEffect as zt, computed as K, readonly as Hn, provide as Ne, inject as ee, shallowReactive as zn, defineComponent as F, reactive as Jn, h as A, getCurrentInstance as Jt, normalizeStyle as Qn, normalizeClass as Ye, toDisplayString as Qt, onUnmounted as Ce, Fragment as xe, vModelDynamic as Yn, vShow as Xn, resolveDynamicComponent as ft, normalizeProps as Zn, withDirectives as er, onErrorCaptured as tr, openBlock as he, createElementBlock as ke, createElementVNode as nr, createVNode as rr, withCtx as or, renderList as sr, createBlock as ir, TransitionGroup as Yt, KeepAlive as ar } from "vue";
let Xt;
function cr(e) {
  Xt = e;
}
function Xe() {
  return Xt;
}
function ye() {
  const { queryPath: e, pathParams: t, queryParams: n } = Xe();
  return {
    path: e,
    ...t === void 0 ? {} : { params: t },
    ...n === void 0 ? {} : { queryParams: n }
  };
}
class ur extends Map {
  constructor(t) {
    super(), this.factory = t;
  }
  getOrDefault(t) {
    if (!this.has(t)) {
      const n = this.factory();
      return this.set(t, n), n;
    }
    return super.get(t);
  }
}
function _e(e) {
  return new ur(e);
}
function St(e, t) {
  Object.entries(e).forEach(([n, r]) => t(r, n));
}
function De(e, t) {
  return Zt(e, {
    valueFn: t
  });
}
function Zt(e, t) {
  const { valueFn: n, keyFn: r } = t;
  return Object.fromEntries(
    Object.entries(e).map(([o, s], i) => [
      r ? r(o, s) : o,
      n(s, o, i)
    ])
  );
}
function en(e, t, n) {
  if (Array.isArray(t)) {
    const [o, ...s] = t;
    switch (o) {
      case "!":
        return !e;
      case "+":
        return e + s[0];
      case "~+":
        return s[0] + e;
    }
  }
  const r = tn(t, n);
  return e[r];
}
function tn(e, t) {
  if (typeof e == "string" || typeof e == "number")
    return e;
  if (!Array.isArray(e))
    throw new Error(`Invalid path ${e}`);
  const [n, ...r] = e;
  switch (n) {
    case "bind":
      if (!t)
        throw new Error("No bindable function provided");
      return t(r[0]);
    default:
      throw new Error(`Invalid flag ${n} in array at ${e}`);
  }
}
function be(e, t, n) {
  return t.reduce(
    (r, o) => en(r, o, n),
    e
  );
}
function Ze(e, t, n, r) {
  t.reduce((o, s, i) => {
    if (i === t.length - 1)
      o[tn(s, r)] = n;
    else
      return en(o, s, r);
  }, e);
}
function nn(e) {
  return JSON.parse(JSON.stringify(e));
}
class lr {
  toString() {
    return "";
  }
}
const we = new lr();
function Ee(e) {
  return qn(e) === we;
}
function Ot(e, t, n) {
  const { paths: r, getBindableValueFn: o } = t, { paths: s, getBindableValueFn: i } = t;
  return r === void 0 || r.length === 0 ? e : je(() => ({
    get() {
      try {
        return be(
          q(e),
          r,
          o
        );
      } catch {
        return;
      }
    },
    set(u) {
      Ze(
        q(e),
        s || r,
        u,
        i
      );
    }
  }));
}
function ht(e) {
  return je((t, n) => ({
    get() {
      return t(), e;
    },
    set(r) {
      !Ee(e) && JSON.stringify(r) === JSON.stringify(e) || (e = r, n());
    }
  }));
}
function de(e) {
  return typeof e == "function" ? e() : L(e);
}
typeof WorkerGlobalScope < "u" && globalThis instanceof WorkerGlobalScope;
const et = () => {
};
function tt(e, t = !1, n = "Timeout") {
  return new Promise((r, o) => {
    setTimeout(t ? () => o(n) : r, e);
  });
}
function nt(e, t = !1) {
  function n(a, { flush: f = "sync", deep: d = !1, timeout: v, throwOnTimeout: p } = {}) {
    let g = null;
    const _ = [new Promise((S) => {
      g = G(
        e,
        (R) => {
          a(R) !== t && (g ? g() : Ie(() => g == null ? void 0 : g()), S(R));
        },
        {
          flush: f,
          deep: d,
          immediate: !0
        }
      );
    })];
    return v != null && _.push(
      tt(v, p).then(() => de(e)).finally(() => g == null ? void 0 : g())
    ), Promise.race(_);
  }
  function r(a, f) {
    if (!Ht(a))
      return n((R) => R === a, f);
    const { flush: d = "sync", deep: v = !1, timeout: p, throwOnTimeout: g } = f ?? {};
    let y = null;
    const S = [new Promise((R) => {
      y = G(
        [e, a],
        ([D, C]) => {
          t !== (D === C) && (y ? y() : Ie(() => y == null ? void 0 : y()), R(D));
        },
        {
          flush: d,
          deep: v,
          immediate: !0
        }
      );
    })];
    return p != null && S.push(
      tt(p, g).then(() => de(e)).finally(() => (y == null || y(), de(e)))
    ), Promise.race(S);
  }
  function o(a) {
    return n((f) => !!f, a);
  }
  function s(a) {
    return r(null, a);
  }
  function i(a) {
    return r(void 0, a);
  }
  function u(a) {
    return n(Number.isNaN, a);
  }
  function l(a, f) {
    return n((d) => {
      const v = Array.from(d);
      return v.includes(a) || v.includes(de(a));
    }, f);
  }
  function h(a) {
    return c(1, a);
  }
  function c(a = 1, f) {
    let d = -1;
    return n(() => (d += 1, d >= a), f);
  }
  return Array.isArray(de(e)) ? {
    toMatch: n,
    toContains: l,
    changed: h,
    changedTimes: c,
    get not() {
      return nt(e, !t);
    }
  } : {
    toMatch: n,
    toBe: r,
    toBeTruthy: o,
    toBeNull: s,
    toBeNaN: u,
    toBeUndefined: i,
    changed: h,
    changedTimes: c,
    get not() {
      return nt(e, !t);
    }
  };
}
function fr(e) {
  return nt(e);
}
function hr(e, t, n) {
  let r;
  Ht(n) ? r = {
    evaluating: n
  } : r = n || {};
  const {
    lazy: o = !1,
    evaluating: s = void 0,
    shallow: i = !0,
    onError: u = et
  } = r, l = Z(!o), h = i ? J(t) : Z(t);
  let c = 0;
  return zt(async (a) => {
    if (!l.value)
      return;
    c++;
    const f = c;
    let d = !1;
    s && Promise.resolve().then(() => {
      s.value = !0;
    });
    try {
      const v = await e((p) => {
        a(() => {
          s && (s.value = !1), d || p();
        });
      });
      f === c && (h.value = v);
    } catch (v) {
      u(v);
    } finally {
      s && f === c && (s.value = !1), d = !0;
    }
  }), o ? K(() => (l.value = !0, h.value)) : h;
}
function dr(e, t, n) {
  const {
    immediate: r = !0,
    delay: o = 0,
    onError: s = et,
    onSuccess: i = et,
    resetOnExecute: u = !0,
    shallow: l = !0,
    throwError: h
  } = {}, c = l ? J(t) : Z(t), a = Z(!1), f = Z(!1), d = J(void 0);
  async function v(y = 0, ..._) {
    u && (c.value = t), d.value = void 0, a.value = !1, f.value = !0, y > 0 && await tt(y);
    const S = typeof e == "function" ? e(..._) : e;
    try {
      const R = await S;
      c.value = R, a.value = !0, i(R);
    } catch (R) {
      if (d.value = R, s(R), h)
        throw R;
    } finally {
      f.value = !1;
    }
    return c.value;
  }
  r && v(o);
  const p = {
    state: c,
    isReady: a,
    isLoading: f,
    error: d,
    execute: v
  };
  function g() {
    return new Promise((y, _) => {
      fr(f).toBe(!1).then(() => y(p)).catch(_);
    });
  }
  return {
    ...p,
    then(y, _) {
      return g().then(y, _);
    }
  };
}
function W(e, t) {
  t = t || {};
  const n = [...Object.keys(t), "__Vue"], r = [...Object.values(t), Gn];
  try {
    return new Function(...n, `return (${e})`)(...r);
  } catch (o) {
    throw new Error(o + " in function code: " + e);
  }
}
function pr(e) {
  if (e.startsWith(":")) {
    e = e.slice(1);
    try {
      return W(e);
    } catch (t) {
      throw new Error(t + " in function code: " + e);
    }
  }
}
function rn(e) {
  return e.constructor.name === "AsyncFunction";
}
function mr(e, t) {
  const { deepCompare: n = !1 } = e;
  return n ? ht(e.value) : Z(e.value);
}
function gr(e, t, n) {
  const { bind: r = {}, code: o, const: s = [] } = e, i = Object.values(r).map((c, a) => s[a] === 1 ? c : t.getVueRefObjectOrValue(c));
  if (rn(new Function(o)))
    return hr(
      async () => {
        const c = Object.fromEntries(
          Object.keys(r).map((a, f) => [a, i[f]])
        );
        return await W(o, c)();
      },
      null,
      { lazy: !0 }
    );
  const u = Object.fromEntries(
    Object.keys(r).map((c, a) => [c, i[a]])
  ), l = W(o, u);
  return K(l);
}
function vr(e, t, n) {
  const {
    inputs: r = [],
    code: o,
    slient: s,
    data: i,
    asyncInit: u = null,
    deepEqOnInput: l = 0
  } = e, h = s || Array(r.length).fill(0), c = i || Array(r.length).fill(0), a = r.filter((g, y) => h[y] === 0 && c[y] === 0).map((g) => t.getVueRefObject(g));
  function f() {
    return r.map(
      (g, y) => c[y] === 1 ? g : t.getObjectToValue(g)
    );
  }
  const d = W(o), v = l === 0 ? J(we) : ht(we), p = { immediate: !0, deep: !0 };
  return rn(d) ? (v.value = u, G(
    a,
    async () => {
      f().some(Ee) || (v.value = await d(...f()));
    },
    p
  )) : G(
    a,
    () => {
      const g = f();
      g.some(Ee) || (v.value = d(...g));
    },
    p
  ), Hn(v);
}
function yr() {
  return [];
}
const Se = _e(yr);
function on(e, t) {
  var s, i, u, l, h;
  const n = Se.getOrDefault(e.id), r = /* @__PURE__ */ new Map();
  n.push(r), t.replaceSnapshot({
    scopeSnapshot: sn()
  });
  const o = (c, a) => {
    r.set(c.id, a);
  };
  return (s = e.refs) == null || s.forEach((c) => {
    o(c, mr(c));
  }), (i = e.web_computed) == null || i.forEach((c) => {
    const { init: a } = c, f = c.deepEqOnInput === void 0 ? J(a ?? we) : ht(a ?? we);
    o(c, f);
  }), (u = e.vue_computed) == null || u.forEach((c) => {
    o(
      c,
      gr(c, t)
    );
  }), (l = e.js_computed) == null || l.forEach((c) => {
    o(
      c,
      vr(c, t)
    );
  }), (h = e.data) == null || h.forEach((c) => {
    o(c, c.value);
  }), n.length - 1;
}
function sn() {
  const e = /* @__PURE__ */ new Map();
  for (const [n, r] of Se) {
    const o = r[r.length - 1];
    e.set(n, [o]);
  }
  function t(n) {
    return an(n, e);
  }
  return {
    getVueRef: t
  };
}
function wr(e) {
  return an(e, Se);
}
function an(e, t) {
  const n = t.get(e.sid);
  if (!n)
    throw new Error(`Scope ${e.sid} not found`);
  const o = n[n.length - 1].get(e.id);
  if (!o)
    throw new Error(`Var ${e.id} not found in scope ${e.sid}`);
  return o;
}
function Er(e) {
  Se.delete(e);
}
function cn(e, t) {
  const n = Se.get(e);
  n && n.splice(t, 1);
}
const dt = _e(() => []);
function _r(e) {
  var r;
  const t = /* @__PURE__ */ new Map(), n = dt.getOrDefault(e.id).push(t);
  return (r = e.eRefs) == null || r.forEach((o) => {
    const s = J();
    t.set(o.id, s);
  }), n;
}
function br(e, t) {
  const n = dt.get(e);
  n && n.splice(t, 1);
}
function un() {
  const e = new Map(
    Array.from(dt.entries()).map(([n, r]) => [
      n,
      r[r.length - 1]
    ])
  );
  function t(n) {
    return e.get(n.sid).get(n.id);
  }
  return {
    getRef: t
  };
}
var N;
((e) => {
  function t(a) {
    return a.type === "var";
  }
  e.isVar = t;
  function n(a) {
    return a.type === "routePar";
  }
  e.isRouterParams = n;
  function r(a) {
    return a.type === "routeAct";
  }
  e.isRouterAction = r;
  function o(a) {
    return a.type === "jsFn";
  }
  e.isJsFn = o;
  function s(a) {
    return a.type === "vf";
  }
  e.isVForItem = s;
  function i(a) {
    return a.type === "vf-i";
  }
  e.isVForIndex = i;
  function u(a) {
    return a.type === "sp";
  }
  e.isSlotProp = u;
  function l(a) {
    return a.type === "event";
  }
  e.isEventContext = l;
  function h(a) {
    return a.type === "ele_ref";
  }
  e.isElementRef = h;
  function c(a) {
    return a.type !== void 0;
  }
  e.IsBinding = c;
})(N || (N = {}));
const Me = _e(() => []);
function Sr(e) {
  const t = Me.getOrDefault(e);
  return t.push(J({})), t.length - 1;
}
function Or(e, t, n) {
  Me.get(e)[t].value = n;
}
function Rr(e) {
  Me.delete(e);
}
function Pr() {
  const e = /* @__PURE__ */ new Map();
  for (const [n, r] of Me) {
    const o = r[r.length - 1];
    e.set(n, o);
  }
  function t(n) {
    return e.get(n.id).value[n.name];
  }
  return {
    getPropsValue: t
  };
}
const ln = /* @__PURE__ */ new Map(), pt = _e(() => /* @__PURE__ */ new Map()), fn = /* @__PURE__ */ new Set(), hn = Symbol("vfor");
function kr(e) {
  const t = dn() ?? {};
  Ne(hn, { ...t, [e.fid]: e.key });
}
function dn() {
  return ee(hn, void 0);
}
function Vr() {
  const e = dn(), t = /* @__PURE__ */ new Map();
  return e === void 0 || Object.keys(e).forEach((n) => {
    t.set(n, e[n]);
  }), t;
}
function Nr(e, t, n, r) {
  if (r) {
    fn.add(e);
    return;
  }
  let o;
  if (n)
    o = new xr(t);
  else {
    const s = Array.isArray(t) ? t : Object.entries(t).map(([i, u], l) => [u, i, l]);
    o = new Cr(s);
  }
  ln.set(e, o);
}
function Ir(e, t, n) {
  const r = pt.getOrDefault(e);
  r.has(t) || r.set(t, Z(n)), r.get(t).value = n;
}
function Tr(e) {
  const t = /* @__PURE__ */ new Set();
  function n(o) {
    t.add(o);
  }
  function r() {
    const o = pt.get(e);
    o !== void 0 && o.forEach((s, i) => {
      t.has(i) || o.delete(i);
    });
  }
  return {
    add: n,
    removeUnusedKeys: r
  };
}
function Ar(e) {
  const t = e, n = Vr();
  function r(o) {
    const s = n.get(o) ?? t;
    return pt.get(o).get(s).value;
  }
  return {
    getVForIndex: r
  };
}
function $r(e) {
  return ln.get(e.binding.fid).createRefObjectWithPaths(e);
}
function jr(e) {
  return fn.has(e);
}
class Cr {
  constructor(t) {
    this.array = t;
  }
  createRefObjectWithPaths(t) {
    const { binding: n } = t, { snapshot: r } = t, { path: o = [] } = n, s = [...o], i = r.getVForIndex(n.fid);
    return s.unshift(i), je(() => ({
      get: () => be(
        this.array,
        s,
        r.getObjectToValue
      ),
      set: () => {
        throw new Error("Cannot set value to a constant array");
      }
    }));
  }
}
class xr {
  constructor(t) {
    B(this, "_isDictSource");
    this.binding = t;
  }
  isDictSource(t) {
    if (this._isDictSource === void 0) {
      const n = q(t);
      this._isDictSource = n !== null && !Array.isArray(n);
    }
    return this._isDictSource;
  }
  createRefObjectWithPaths(t) {
    const { binding: n } = t, { path: r = [] } = n, o = [...r], { snapshot: s } = t, i = s.getVueRefObject(this.binding), u = this.isDictSource(i), l = s.getVForIndex(n.fid), h = u && o.length === 0 ? [0] : [];
    return o.unshift(l, ...h), je(() => ({
      get: () => {
        const c = q(i), a = u ? Object.entries(c).map(([f, d], v) => [
          d,
          f,
          v
        ]) : c;
        try {
          return be(
            q(a),
            o,
            s.getObjectToValue
          );
        } catch {
          return;
        }
      },
      set: (c) => {
        const a = q(i);
        if (u) {
          const f = Object.keys(a);
          if (l >= f.length)
            throw new Error("Cannot set value to a non-existent key");
          const d = f[l];
          Ze(
            a,
            [d],
            c,
            s.getObjectToValue
          );
          return;
        }
        Ze(
          a,
          o,
          c,
          s.getObjectToValue
        );
      }
    }));
  }
}
function Rt(e) {
  return e == null;
}
function Dr() {
  return pn().__VUE_DEVTOOLS_GLOBAL_HOOK__;
}
function pn() {
  return typeof navigator < "u" && typeof window < "u" ? window : typeof globalThis < "u" ? globalThis : {};
}
const Mr = typeof Proxy == "function", Fr = "devtools-plugin:setup", Br = "plugin:settings:set";
let ie, rt;
function Lr() {
  var e;
  return ie !== void 0 || (typeof window < "u" && window.performance ? (ie = !0, rt = window.performance) : typeof globalThis < "u" && (!((e = globalThis.perf_hooks) === null || e === void 0) && e.performance) ? (ie = !0, rt = globalThis.perf_hooks.performance) : ie = !1), ie;
}
function Wr() {
  return Lr() ? rt.now() : Date.now();
}
class Ur {
  constructor(t, n) {
    this.target = null, this.targetQueue = [], this.onQueue = [], this.plugin = t, this.hook = n;
    const r = {};
    if (t.settings)
      for (const i in t.settings) {
        const u = t.settings[i];
        r[i] = u.defaultValue;
      }
    const o = `__vue-devtools-plugin-settings__${t.id}`;
    let s = Object.assign({}, r);
    try {
      const i = localStorage.getItem(o), u = JSON.parse(i);
      Object.assign(s, u);
    } catch {
    }
    this.fallbacks = {
      getSettings() {
        return s;
      },
      setSettings(i) {
        try {
          localStorage.setItem(o, JSON.stringify(i));
        } catch {
        }
        s = i;
      },
      now() {
        return Wr();
      }
    }, n && n.on(Br, (i, u) => {
      i === this.plugin.id && this.fallbacks.setSettings(u);
    }), this.proxiedOn = new Proxy({}, {
      get: (i, u) => this.target ? this.target.on[u] : (...l) => {
        this.onQueue.push({
          method: u,
          args: l
        });
      }
    }), this.proxiedTarget = new Proxy({}, {
      get: (i, u) => this.target ? this.target[u] : u === "on" ? this.proxiedOn : Object.keys(this.fallbacks).includes(u) ? (...l) => (this.targetQueue.push({
        method: u,
        args: l,
        resolve: () => {
        }
      }), this.fallbacks[u](...l)) : (...l) => new Promise((h) => {
        this.targetQueue.push({
          method: u,
          args: l,
          resolve: h
        });
      })
    });
  }
  async setRealTarget(t) {
    this.target = t;
    for (const n of this.onQueue)
      this.target.on[n.method](...n.args);
    for (const n of this.targetQueue)
      n.resolve(await this.target[n.method](...n.args));
  }
}
function Kr(e, t) {
  const n = e, r = pn(), o = Dr(), s = Mr && n.enableEarlyProxy;
  if (o && (r.__VUE_DEVTOOLS_PLUGIN_API_AVAILABLE__ || !s))
    o.emit(Fr, e, t);
  else {
    const i = s ? new Ur(n, o) : null;
    (r.__VUE_DEVTOOLS_PLUGINS__ = r.__VUE_DEVTOOLS_PLUGINS__ || []).push({
      pluginDescriptor: n,
      setupFn: t,
      proxy: i
    }), i && t(i.proxiedTarget);
  }
}
var O = {};
const z = typeof document < "u";
function mn(e) {
  return typeof e == "object" || "displayName" in e || "props" in e || "__vccOpts" in e;
}
function Gr(e) {
  return e.__esModule || e[Symbol.toStringTag] === "Module" || // support CF with dynamic imports that do not
  // add the Module string tag
  e.default && mn(e.default);
}
const I = Object.assign;
function He(e, t) {
  const n = {};
  for (const r in t) {
    const o = t[r];
    n[r] = U(o) ? o.map(e) : e(o);
  }
  return n;
}
const ve = () => {
}, U = Array.isArray;
function P(e) {
  const t = Array.from(arguments).slice(1);
  console.warn.apply(console, ["[Vue Router warn]: " + e].concat(t));
}
const gn = /#/g, qr = /&/g, Hr = /\//g, zr = /=/g, Jr = /\?/g, vn = /\+/g, Qr = /%5B/g, Yr = /%5D/g, yn = /%5E/g, Xr = /%60/g, wn = /%7B/g, Zr = /%7C/g, En = /%7D/g, eo = /%20/g;
function mt(e) {
  return encodeURI("" + e).replace(Zr, "|").replace(Qr, "[").replace(Yr, "]");
}
function to(e) {
  return mt(e).replace(wn, "{").replace(En, "}").replace(yn, "^");
}
function ot(e) {
  return mt(e).replace(vn, "%2B").replace(eo, "+").replace(gn, "%23").replace(qr, "%26").replace(Xr, "`").replace(wn, "{").replace(En, "}").replace(yn, "^");
}
function no(e) {
  return ot(e).replace(zr, "%3D");
}
function ro(e) {
  return mt(e).replace(gn, "%23").replace(Jr, "%3F");
}
function oo(e) {
  return e == null ? "" : ro(e).replace(Hr, "%2F");
}
function ae(e) {
  try {
    return decodeURIComponent("" + e);
  } catch {
    O.NODE_ENV !== "production" && P(`Error decoding "${e}". Using original value`);
  }
  return "" + e;
}
const so = /\/$/, io = (e) => e.replace(so, "");
function ze(e, t, n = "/") {
  let r, o = {}, s = "", i = "";
  const u = t.indexOf("#");
  let l = t.indexOf("?");
  return u < l && u >= 0 && (l = -1), l > -1 && (r = t.slice(0, l), s = t.slice(l + 1, u > -1 ? u : t.length), o = e(s)), u > -1 && (r = r || t.slice(0, u), i = t.slice(u, t.length)), r = uo(r ?? t, n), {
    fullPath: r + (s && "?") + s + i,
    path: r,
    query: o,
    hash: ae(i)
  };
}
function ao(e, t) {
  const n = t.query ? e(t.query) : "";
  return t.path + (n && "?") + n + (t.hash || "");
}
function Pt(e, t) {
  return !t || !e.toLowerCase().startsWith(t.toLowerCase()) ? e : e.slice(t.length) || "/";
}
function kt(e, t, n) {
  const r = t.matched.length - 1, o = n.matched.length - 1;
  return r > -1 && r === o && te(t.matched[r], n.matched[o]) && _n(t.params, n.params) && e(t.query) === e(n.query) && t.hash === n.hash;
}
function te(e, t) {
  return (e.aliasOf || e) === (t.aliasOf || t);
}
function _n(e, t) {
  if (Object.keys(e).length !== Object.keys(t).length)
    return !1;
  for (const n in e)
    if (!co(e[n], t[n]))
      return !1;
  return !0;
}
function co(e, t) {
  return U(e) ? Vt(e, t) : U(t) ? Vt(t, e) : e === t;
}
function Vt(e, t) {
  return U(t) ? e.length === t.length && e.every((n, r) => n === t[r]) : e.length === 1 && e[0] === t;
}
function uo(e, t) {
  if (e.startsWith("/"))
    return e;
  if (O.NODE_ENV !== "production" && !t.startsWith("/"))
    return P(`Cannot resolve a relative location without an absolute path. Trying to resolve "${e}" from "${t}". It should look like "/${t}".`), e;
  if (!e)
    return t;
  const n = t.split("/"), r = e.split("/"), o = r[r.length - 1];
  (o === ".." || o === ".") && r.push("");
  let s = n.length - 1, i, u;
  for (i = 0; i < r.length; i++)
    if (u = r[i], u !== ".")
      if (u === "..")
        s > 1 && s--;
      else
        break;
  return n.slice(0, s).join("/") + "/" + r.slice(i).join("/");
}
const Y = {
  path: "/",
  // TODO: could we use a symbol in the future?
  name: void 0,
  params: {},
  query: {},
  hash: "",
  fullPath: "/",
  matched: [],
  meta: {},
  redirectedFrom: void 0
};
var ce;
(function(e) {
  e.pop = "pop", e.push = "push";
})(ce || (ce = {}));
var oe;
(function(e) {
  e.back = "back", e.forward = "forward", e.unknown = "";
})(oe || (oe = {}));
const Je = "";
function bn(e) {
  if (!e)
    if (z) {
      const t = document.querySelector("base");
      e = t && t.getAttribute("href") || "/", e = e.replace(/^\w+:\/\/[^\/]+/, "");
    } else
      e = "/";
  return e[0] !== "/" && e[0] !== "#" && (e = "/" + e), io(e);
}
const lo = /^[^#]+#/;
function Sn(e, t) {
  return e.replace(lo, "#") + t;
}
function fo(e, t) {
  const n = document.documentElement.getBoundingClientRect(), r = e.getBoundingClientRect();
  return {
    behavior: t.behavior,
    left: r.left - n.left - (t.left || 0),
    top: r.top - n.top - (t.top || 0)
  };
}
const Fe = () => ({
  left: window.scrollX,
  top: window.scrollY
});
function ho(e) {
  let t;
  if ("el" in e) {
    const n = e.el, r = typeof n == "string" && n.startsWith("#");
    if (O.NODE_ENV !== "production" && typeof e.el == "string" && (!r || !document.getElementById(e.el.slice(1))))
      try {
        const s = document.querySelector(e.el);
        if (r && s) {
          P(`The selector "${e.el}" should be passed as "el: document.querySelector('${e.el}')" because it starts with "#".`);
          return;
        }
      } catch {
        P(`The selector "${e.el}" is invalid. If you are using an id selector, make sure to escape it. You can find more information about escaping characters in selectors at https://mathiasbynens.be/notes/css-escapes or use CSS.escape (https://developer.mozilla.org/en-US/docs/Web/API/CSS/escape).`);
        return;
      }
    const o = typeof n == "string" ? r ? document.getElementById(n.slice(1)) : document.querySelector(n) : n;
    if (!o) {
      O.NODE_ENV !== "production" && P(`Couldn't find element using selector "${e.el}" returned by scrollBehavior.`);
      return;
    }
    t = fo(o, e);
  } else
    t = e;
  "scrollBehavior" in document.documentElement.style ? window.scrollTo(t) : window.scrollTo(t.left != null ? t.left : window.scrollX, t.top != null ? t.top : window.scrollY);
}
function Nt(e, t) {
  return (history.state ? history.state.position - t : -1) + e;
}
const st = /* @__PURE__ */ new Map();
function po(e, t) {
  st.set(e, t);
}
function mo(e) {
  const t = st.get(e);
  return st.delete(e), t;
}
let go = () => location.protocol + "//" + location.host;
function On(e, t) {
  const { pathname: n, search: r, hash: o } = t, s = e.indexOf("#");
  if (s > -1) {
    let u = o.includes(e.slice(s)) ? e.slice(s).length : 1, l = o.slice(u);
    return l[0] !== "/" && (l = "/" + l), Pt(l, "");
  }
  return Pt(n, e) + r + o;
}
function vo(e, t, n, r) {
  let o = [], s = [], i = null;
  const u = ({ state: f }) => {
    const d = On(e, location), v = n.value, p = t.value;
    let g = 0;
    if (f) {
      if (n.value = d, t.value = f, i && i === v) {
        i = null;
        return;
      }
      g = p ? f.position - p.position : 0;
    } else
      r(d);
    o.forEach((y) => {
      y(n.value, v, {
        delta: g,
        type: ce.pop,
        direction: g ? g > 0 ? oe.forward : oe.back : oe.unknown
      });
    });
  };
  function l() {
    i = n.value;
  }
  function h(f) {
    o.push(f);
    const d = () => {
      const v = o.indexOf(f);
      v > -1 && o.splice(v, 1);
    };
    return s.push(d), d;
  }
  function c() {
    const { history: f } = window;
    f.state && f.replaceState(I({}, f.state, { scroll: Fe() }), "");
  }
  function a() {
    for (const f of s)
      f();
    s = [], window.removeEventListener("popstate", u), window.removeEventListener("beforeunload", c);
  }
  return window.addEventListener("popstate", u), window.addEventListener("beforeunload", c, {
    passive: !0
  }), {
    pauseListeners: l,
    listen: h,
    destroy: a
  };
}
function It(e, t, n, r = !1, o = !1) {
  return {
    back: e,
    current: t,
    forward: n,
    replaced: r,
    position: window.history.length,
    scroll: o ? Fe() : null
  };
}
function yo(e) {
  const { history: t, location: n } = window, r = {
    value: On(e, n)
  }, o = { value: t.state };
  o.value || s(r.value, {
    back: null,
    current: r.value,
    forward: null,
    // the length is off by one, we need to decrease it
    position: t.length - 1,
    replaced: !0,
    // don't add a scroll as the user may have an anchor, and we want
    // scrollBehavior to be triggered without a saved position
    scroll: null
  }, !0);
  function s(l, h, c) {
    const a = e.indexOf("#"), f = a > -1 ? (n.host && document.querySelector("base") ? e : e.slice(a)) + l : go() + e + l;
    try {
      t[c ? "replaceState" : "pushState"](h, "", f), o.value = h;
    } catch (d) {
      O.NODE_ENV !== "production" ? P("Error with push/replace State", d) : console.error(d), n[c ? "replace" : "assign"](f);
    }
  }
  function i(l, h) {
    const c = I({}, t.state, It(
      o.value.back,
      // keep back and forward entries but override current position
      l,
      o.value.forward,
      !0
    ), h, { position: o.value.position });
    s(l, c, !0), r.value = l;
  }
  function u(l, h) {
    const c = I(
      {},
      // use current history state to gracefully handle a wrong call to
      // history.replaceState
      // https://github.com/vuejs/router/issues/366
      o.value,
      t.state,
      {
        forward: l,
        scroll: Fe()
      }
    );
    O.NODE_ENV !== "production" && !t.state && P(`history.state seems to have been manually replaced without preserving the necessary values. Make sure to preserve existing history state if you are manually calling history.replaceState:

history.replaceState(history.state, '', url)

You can find more information at https://router.vuejs.org/guide/migration/#Usage-of-history-state`), s(c.current, c, !0);
    const a = I({}, It(r.value, l, null), { position: c.position + 1 }, h);
    s(l, a, !1), r.value = l;
  }
  return {
    location: r,
    state: o,
    push: u,
    replace: i
  };
}
function Rn(e) {
  e = bn(e);
  const t = yo(e), n = vo(e, t.state, t.location, t.replace);
  function r(s, i = !0) {
    i || n.pauseListeners(), history.go(s);
  }
  const o = I({
    // it's overridden right after
    location: "",
    base: e,
    go: r,
    createHref: Sn.bind(null, e)
  }, t, n);
  return Object.defineProperty(o, "location", {
    enumerable: !0,
    get: () => t.location.value
  }), Object.defineProperty(o, "state", {
    enumerable: !0,
    get: () => t.state.value
  }), o;
}
function wo(e = "") {
  let t = [], n = [Je], r = 0;
  e = bn(e);
  function o(u) {
    r++, r !== n.length && n.splice(r), n.push(u);
  }
  function s(u, l, { direction: h, delta: c }) {
    const a = {
      direction: h,
      delta: c,
      type: ce.pop
    };
    for (const f of t)
      f(u, l, a);
  }
  const i = {
    // rewritten by Object.defineProperty
    location: Je,
    // TODO: should be kept in queue
    state: {},
    base: e,
    createHref: Sn.bind(null, e),
    replace(u) {
      n.splice(r--, 1), o(u);
    },
    push(u, l) {
      o(u);
    },
    listen(u) {
      return t.push(u), () => {
        const l = t.indexOf(u);
        l > -1 && t.splice(l, 1);
      };
    },
    destroy() {
      t = [], n = [Je], r = 0;
    },
    go(u, l = !0) {
      const h = this.location, c = (
        // we are considering delta === 0 going forward, but in abstract mode
        // using 0 for the delta doesn't make sense like it does in html5 where
        // it reloads the page
        u < 0 ? oe.back : oe.forward
      );
      r = Math.max(0, Math.min(r + u, n.length - 1)), l && s(this.location, h, {
        direction: c,
        delta: u
      });
    }
  };
  return Object.defineProperty(i, "location", {
    enumerable: !0,
    get: () => n[r]
  }), i;
}
function Eo(e) {
  return e = location.host ? e || location.pathname + location.search : "", e.includes("#") || (e += "#"), O.NODE_ENV !== "production" && !e.endsWith("#/") && !e.endsWith("#") && P(`A hash base must end with a "#":
"${e}" should be "${e.replace(/#.*$/, "#")}".`), Rn(e);
}
function Te(e) {
  return typeof e == "string" || e && typeof e == "object";
}
function Pn(e) {
  return typeof e == "string" || typeof e == "symbol";
}
const it = Symbol(O.NODE_ENV !== "production" ? "navigation failure" : "");
var Tt;
(function(e) {
  e[e.aborted = 4] = "aborted", e[e.cancelled = 8] = "cancelled", e[e.duplicated = 16] = "duplicated";
})(Tt || (Tt = {}));
const _o = {
  1({ location: e, currentLocation: t }) {
    return `No match for
 ${JSON.stringify(e)}${t ? `
while being at
` + JSON.stringify(t) : ""}`;
  },
  2({ from: e, to: t }) {
    return `Redirected from "${e.fullPath}" to "${So(t)}" via a navigation guard.`;
  },
  4({ from: e, to: t }) {
    return `Navigation aborted from "${e.fullPath}" to "${t.fullPath}" via a navigation guard.`;
  },
  8({ from: e, to: t }) {
    return `Navigation cancelled from "${e.fullPath}" to "${t.fullPath}" with a new navigation.`;
  },
  16({ from: e, to: t }) {
    return `Avoided redundant navigation to current location: "${e.fullPath}".`;
  }
};
function ue(e, t) {
  return O.NODE_ENV !== "production" ? I(new Error(_o[e](t)), {
    type: e,
    [it]: !0
  }, t) : I(new Error(), {
    type: e,
    [it]: !0
  }, t);
}
function H(e, t) {
  return e instanceof Error && it in e && (t == null || !!(e.type & t));
}
const bo = ["params", "query", "hash"];
function So(e) {
  if (typeof e == "string")
    return e;
  if (e.path != null)
    return e.path;
  const t = {};
  for (const n of bo)
    n in e && (t[n] = e[n]);
  return JSON.stringify(t, null, 2);
}
const At = "[^/]+?", Oo = {
  sensitive: !1,
  strict: !1,
  start: !0,
  end: !0
}, Ro = /[.+*?^${}()[\]/\\]/g;
function Po(e, t) {
  const n = I({}, Oo, t), r = [];
  let o = n.start ? "^" : "";
  const s = [];
  for (const h of e) {
    const c = h.length ? [] : [
      90
      /* PathScore.Root */
    ];
    n.strict && !h.length && (o += "/");
    for (let a = 0; a < h.length; a++) {
      const f = h[a];
      let d = 40 + (n.sensitive ? 0.25 : 0);
      if (f.type === 0)
        a || (o += "/"), o += f.value.replace(Ro, "\\$&"), d += 40;
      else if (f.type === 1) {
        const { value: v, repeatable: p, optional: g, regexp: y } = f;
        s.push({
          name: v,
          repeatable: p,
          optional: g
        });
        const _ = y || At;
        if (_ !== At) {
          d += 10;
          try {
            new RegExp(`(${_})`);
          } catch (R) {
            throw new Error(`Invalid custom RegExp for param "${v}" (${_}): ` + R.message);
          }
        }
        let S = p ? `((?:${_})(?:/(?:${_}))*)` : `(${_})`;
        a || (S = // avoid an optional / if there are more segments e.g. /:p?-static
        // or /:p?-:p2
        g && h.length < 2 ? `(?:/${S})` : "/" + S), g && (S += "?"), o += S, d += 20, g && (d += -8), p && (d += -20), _ === ".*" && (d += -50);
      }
      c.push(d);
    }
    r.push(c);
  }
  if (n.strict && n.end) {
    const h = r.length - 1;
    r[h][r[h].length - 1] += 0.7000000000000001;
  }
  n.strict || (o += "/?"), n.end ? o += "$" : n.strict && !o.endsWith("/") && (o += "(?:/|$)");
  const i = new RegExp(o, n.sensitive ? "" : "i");
  function u(h) {
    const c = h.match(i), a = {};
    if (!c)
      return null;
    for (let f = 1; f < c.length; f++) {
      const d = c[f] || "", v = s[f - 1];
      a[v.name] = d && v.repeatable ? d.split("/") : d;
    }
    return a;
  }
  function l(h) {
    let c = "", a = !1;
    for (const f of e) {
      (!a || !c.endsWith("/")) && (c += "/"), a = !1;
      for (const d of f)
        if (d.type === 0)
          c += d.value;
        else if (d.type === 1) {
          const { value: v, repeatable: p, optional: g } = d, y = v in h ? h[v] : "";
          if (U(y) && !p)
            throw new Error(`Provided param "${v}" is an array but it is not repeatable (* or + modifiers)`);
          const _ = U(y) ? y.join("/") : y;
          if (!_)
            if (g)
              f.length < 2 && (c.endsWith("/") ? c = c.slice(0, -1) : a = !0);
            else
              throw new Error(`Missing required param "${v}"`);
          c += _;
        }
    }
    return c || "/";
  }
  return {
    re: i,
    score: r,
    keys: s,
    parse: u,
    stringify: l
  };
}
function ko(e, t) {
  let n = 0;
  for (; n < e.length && n < t.length; ) {
    const r = t[n] - e[n];
    if (r)
      return r;
    n++;
  }
  return e.length < t.length ? e.length === 1 && e[0] === 80 ? -1 : 1 : e.length > t.length ? t.length === 1 && t[0] === 80 ? 1 : -1 : 0;
}
function kn(e, t) {
  let n = 0;
  const r = e.score, o = t.score;
  for (; n < r.length && n < o.length; ) {
    const s = ko(r[n], o[n]);
    if (s)
      return s;
    n++;
  }
  if (Math.abs(o.length - r.length) === 1) {
    if ($t(r))
      return 1;
    if ($t(o))
      return -1;
  }
  return o.length - r.length;
}
function $t(e) {
  const t = e[e.length - 1];
  return e.length > 0 && t[t.length - 1] < 0;
}
const Vo = {
  type: 0,
  value: ""
}, No = /[a-zA-Z0-9_]/;
function Io(e) {
  if (!e)
    return [[]];
  if (e === "/")
    return [[Vo]];
  if (!e.startsWith("/"))
    throw new Error(O.NODE_ENV !== "production" ? `Route paths should start with a "/": "${e}" should be "/${e}".` : `Invalid path "${e}"`);
  function t(d) {
    throw new Error(`ERR (${n})/"${h}": ${d}`);
  }
  let n = 0, r = n;
  const o = [];
  let s;
  function i() {
    s && o.push(s), s = [];
  }
  let u = 0, l, h = "", c = "";
  function a() {
    h && (n === 0 ? s.push({
      type: 0,
      value: h
    }) : n === 1 || n === 2 || n === 3 ? (s.length > 1 && (l === "*" || l === "+") && t(`A repeatable param (${h}) must be alone in its segment. eg: '/:ids+.`), s.push({
      type: 1,
      value: h,
      regexp: c,
      repeatable: l === "*" || l === "+",
      optional: l === "*" || l === "?"
    })) : t("Invalid state to consume buffer"), h = "");
  }
  function f() {
    h += l;
  }
  for (; u < e.length; ) {
    if (l = e[u++], l === "\\" && n !== 2) {
      r = n, n = 4;
      continue;
    }
    switch (n) {
      case 0:
        l === "/" ? (h && a(), i()) : l === ":" ? (a(), n = 1) : f();
        break;
      case 4:
        f(), n = r;
        break;
      case 1:
        l === "(" ? n = 2 : No.test(l) ? f() : (a(), n = 0, l !== "*" && l !== "?" && l !== "+" && u--);
        break;
      case 2:
        l === ")" ? c[c.length - 1] == "\\" ? c = c.slice(0, -1) + l : n = 3 : c += l;
        break;
      case 3:
        a(), n = 0, l !== "*" && l !== "?" && l !== "+" && u--, c = "";
        break;
      default:
        t("Unknown state");
        break;
    }
  }
  return n === 2 && t(`Unfinished custom RegExp for param "${h}"`), a(), i(), o;
}
function To(e, t, n) {
  const r = Po(Io(e.path), n);
  if (O.NODE_ENV !== "production") {
    const s = /* @__PURE__ */ new Set();
    for (const i of r.keys)
      s.has(i.name) && P(`Found duplicated params with name "${i.name}" for path "${e.path}". Only the last one will be available on "$route.params".`), s.add(i.name);
  }
  const o = I(r, {
    record: e,
    parent: t,
    // these needs to be populated by the parent
    children: [],
    alias: []
  });
  return t && !o.record.aliasOf == !t.record.aliasOf && t.children.push(o), o;
}
function Ao(e, t) {
  const n = [], r = /* @__PURE__ */ new Map();
  t = Dt({ strict: !1, end: !0, sensitive: !1 }, t);
  function o(a) {
    return r.get(a);
  }
  function s(a, f, d) {
    const v = !d, p = Ct(a);
    O.NODE_ENV !== "production" && xo(p, f), p.aliasOf = d && d.record;
    const g = Dt(t, a), y = [p];
    if ("alias" in a) {
      const R = typeof a.alias == "string" ? [a.alias] : a.alias;
      for (const D of R)
        y.push(
          // we need to normalize again to ensure the `mods` property
          // being non enumerable
          Ct(I({}, p, {
            // this allows us to hold a copy of the `components` option
            // so that async components cache is hold on the original record
            components: d ? d.record.components : p.components,
            path: D,
            // we might be the child of an alias
            aliasOf: d ? d.record : p
            // the aliases are always of the same kind as the original since they
            // are defined on the same record
          }))
        );
    }
    let _, S;
    for (const R of y) {
      const { path: D } = R;
      if (f && D[0] !== "/") {
        const C = f.record.path, x = C[C.length - 1] === "/" ? "" : "/";
        R.path = f.record.path + (D && x + D);
      }
      if (O.NODE_ENV !== "production" && R.path === "*")
        throw new Error(`Catch all routes ("*") must now be defined using a param with a custom regexp.
See more at https://router.vuejs.org/guide/migration/#Removed-star-or-catch-all-routes.`);
      if (_ = To(R, f, g), O.NODE_ENV !== "production" && f && D[0] === "/" && Mo(_, f), d ? (d.alias.push(_), O.NODE_ENV !== "production" && Co(d, _)) : (S = S || _, S !== _ && S.alias.push(_), v && a.name && !xt(_) && (O.NODE_ENV !== "production" && Do(a, f), i(a.name))), Vn(_) && l(_), p.children) {
        const C = p.children;
        for (let x = 0; x < C.length; x++)
          s(C[x], _, d && d.children[x]);
      }
      d = d || _;
    }
    return S ? () => {
      i(S);
    } : ve;
  }
  function i(a) {
    if (Pn(a)) {
      const f = r.get(a);
      f && (r.delete(a), n.splice(n.indexOf(f), 1), f.children.forEach(i), f.alias.forEach(i));
    } else {
      const f = n.indexOf(a);
      f > -1 && (n.splice(f, 1), a.record.name && r.delete(a.record.name), a.children.forEach(i), a.alias.forEach(i));
    }
  }
  function u() {
    return n;
  }
  function l(a) {
    const f = Fo(a, n);
    n.splice(f, 0, a), a.record.name && !xt(a) && r.set(a.record.name, a);
  }
  function h(a, f) {
    let d, v = {}, p, g;
    if ("name" in a && a.name) {
      if (d = r.get(a.name), !d)
        throw ue(1, {
          location: a
        });
      if (O.NODE_ENV !== "production") {
        const S = Object.keys(a.params || {}).filter((R) => !d.keys.find((D) => D.name === R));
        S.length && P(`Discarded invalid param(s) "${S.join('", "')}" when navigating. See https://github.com/vuejs/router/blob/main/packages/router/CHANGELOG.md#414-2022-08-22 for more details.`);
      }
      g = d.record.name, v = I(
        // paramsFromLocation is a new object
        jt(
          f.params,
          // only keep params that exist in the resolved location
          // only keep optional params coming from a parent record
          d.keys.filter((S) => !S.optional).concat(d.parent ? d.parent.keys.filter((S) => S.optional) : []).map((S) => S.name)
        ),
        // discard any existing params in the current location that do not exist here
        // #1497 this ensures better active/exact matching
        a.params && jt(a.params, d.keys.map((S) => S.name))
      ), p = d.stringify(v);
    } else if (a.path != null)
      p = a.path, O.NODE_ENV !== "production" && !p.startsWith("/") && P(`The Matcher cannot resolve relative paths but received "${p}". Unless you directly called \`matcher.resolve("${p}")\`, this is probably a bug in vue-router. Please open an issue at https://github.com/vuejs/router/issues/new/choose.`), d = n.find((S) => S.re.test(p)), d && (v = d.parse(p), g = d.record.name);
    else {
      if (d = f.name ? r.get(f.name) : n.find((S) => S.re.test(f.path)), !d)
        throw ue(1, {
          location: a,
          currentLocation: f
        });
      g = d.record.name, v = I({}, f.params, a.params), p = d.stringify(v);
    }
    const y = [];
    let _ = d;
    for (; _; )
      y.unshift(_.record), _ = _.parent;
    return {
      name: g,
      path: p,
      params: v,
      matched: y,
      meta: jo(y)
    };
  }
  e.forEach((a) => s(a));
  function c() {
    n.length = 0, r.clear();
  }
  return {
    addRoute: s,
    resolve: h,
    removeRoute: i,
    clearRoutes: c,
    getRoutes: u,
    getRecordMatcher: o
  };
}
function jt(e, t) {
  const n = {};
  for (const r of t)
    r in e && (n[r] = e[r]);
  return n;
}
function Ct(e) {
  const t = {
    path: e.path,
    redirect: e.redirect,
    name: e.name,
    meta: e.meta || {},
    aliasOf: e.aliasOf,
    beforeEnter: e.beforeEnter,
    props: $o(e),
    children: e.children || [],
    instances: {},
    leaveGuards: /* @__PURE__ */ new Set(),
    updateGuards: /* @__PURE__ */ new Set(),
    enterCallbacks: {},
    // must be declared afterwards
    // mods: {},
    components: "components" in e ? e.components || null : e.component && { default: e.component }
  };
  return Object.defineProperty(t, "mods", {
    value: {}
  }), t;
}
function $o(e) {
  const t = {}, n = e.props || !1;
  if ("component" in e)
    t.default = n;
  else
    for (const r in e.components)
      t[r] = typeof n == "object" ? n[r] : n;
  return t;
}
function xt(e) {
  for (; e; ) {
    if (e.record.aliasOf)
      return !0;
    e = e.parent;
  }
  return !1;
}
function jo(e) {
  return e.reduce((t, n) => I(t, n.meta), {});
}
function Dt(e, t) {
  const n = {};
  for (const r in e)
    n[r] = r in t ? t[r] : e[r];
  return n;
}
function at(e, t) {
  return e.name === t.name && e.optional === t.optional && e.repeatable === t.repeatable;
}
function Co(e, t) {
  for (const n of e.keys)
    if (!n.optional && !t.keys.find(at.bind(null, n)))
      return P(`Alias "${t.record.path}" and the original record: "${e.record.path}" must have the exact same param named "${n.name}"`);
  for (const n of t.keys)
    if (!n.optional && !e.keys.find(at.bind(null, n)))
      return P(`Alias "${t.record.path}" and the original record: "${e.record.path}" must have the exact same param named "${n.name}"`);
}
function xo(e, t) {
  t && t.record.name && !e.name && !e.path && P(`The route named "${String(t.record.name)}" has a child without a name and an empty path. Using that name won't render the empty path child so you probably want to move the name to the child instead. If this is intentional, add a name to the child route to remove the warning.`);
}
function Do(e, t) {
  for (let n = t; n; n = n.parent)
    if (n.record.name === e.name)
      throw new Error(`A route named "${String(e.name)}" has been added as a ${t === n ? "child" : "descendant"} of a route with the same name. Route names must be unique and a nested route cannot use the same name as an ancestor.`);
}
function Mo(e, t) {
  for (const n of t.keys)
    if (!e.keys.find(at.bind(null, n)))
      return P(`Absolute path "${e.record.path}" must have the exact same param named "${n.name}" as its parent "${t.record.path}".`);
}
function Fo(e, t) {
  let n = 0, r = t.length;
  for (; n !== r; ) {
    const s = n + r >> 1;
    kn(e, t[s]) < 0 ? r = s : n = s + 1;
  }
  const o = Bo(e);
  return o && (r = t.lastIndexOf(o, r - 1), O.NODE_ENV !== "production" && r < 0 && P(`Finding ancestor route "${o.record.path}" failed for "${e.record.path}"`)), r;
}
function Bo(e) {
  let t = e;
  for (; t = t.parent; )
    if (Vn(t) && kn(e, t) === 0)
      return t;
}
function Vn({ record: e }) {
  return !!(e.name || e.components && Object.keys(e.components).length || e.redirect);
}
function Lo(e) {
  const t = {};
  if (e === "" || e === "?")
    return t;
  const r = (e[0] === "?" ? e.slice(1) : e).split("&");
  for (let o = 0; o < r.length; ++o) {
    const s = r[o].replace(vn, " "), i = s.indexOf("="), u = ae(i < 0 ? s : s.slice(0, i)), l = i < 0 ? null : ae(s.slice(i + 1));
    if (u in t) {
      let h = t[u];
      U(h) || (h = t[u] = [h]), h.push(l);
    } else
      t[u] = l;
  }
  return t;
}
function Mt(e) {
  let t = "";
  for (let n in e) {
    const r = e[n];
    if (n = no(n), r == null) {
      r !== void 0 && (t += (t.length ? "&" : "") + n);
      continue;
    }
    (U(r) ? r.map((s) => s && ot(s)) : [r && ot(r)]).forEach((s) => {
      s !== void 0 && (t += (t.length ? "&" : "") + n, s != null && (t += "=" + s));
    });
  }
  return t;
}
function Wo(e) {
  const t = {};
  for (const n in e) {
    const r = e[n];
    r !== void 0 && (t[n] = U(r) ? r.map((o) => o == null ? null : "" + o) : r == null ? r : "" + r);
  }
  return t;
}
const Uo = Symbol(O.NODE_ENV !== "production" ? "router view location matched" : ""), Ft = Symbol(O.NODE_ENV !== "production" ? "router view depth" : ""), Be = Symbol(O.NODE_ENV !== "production" ? "router" : ""), gt = Symbol(O.NODE_ENV !== "production" ? "route location" : ""), ct = Symbol(O.NODE_ENV !== "production" ? "router view location" : "");
function pe() {
  let e = [];
  function t(r) {
    return e.push(r), () => {
      const o = e.indexOf(r);
      o > -1 && e.splice(o, 1);
    };
  }
  function n() {
    e = [];
  }
  return {
    add: t,
    list: () => e.slice(),
    reset: n
  };
}
function X(e, t, n, r, o, s = (i) => i()) {
  const i = r && // name is defined if record is because of the function overload
  (r.enterCallbacks[o] = r.enterCallbacks[o] || []);
  return () => new Promise((u, l) => {
    const h = (f) => {
      f === !1 ? l(ue(4, {
        from: n,
        to: t
      })) : f instanceof Error ? l(f) : Te(f) ? l(ue(2, {
        from: t,
        to: f
      })) : (i && // since enterCallbackArray is truthy, both record and name also are
      r.enterCallbacks[o] === i && typeof f == "function" && i.push(f), u());
    }, c = s(() => e.call(r && r.instances[o], t, n, O.NODE_ENV !== "production" ? Ko(h, t, n) : h));
    let a = Promise.resolve(c);
    if (e.length < 3 && (a = a.then(h)), O.NODE_ENV !== "production" && e.length > 2) {
      const f = `The "next" callback was never called inside of ${e.name ? '"' + e.name + '"' : ""}:
${e.toString()}
. If you are returning a value instead of calling "next", make sure to remove the "next" parameter from your function.`;
      if (typeof c == "object" && "then" in c)
        a = a.then((d) => h._called ? d : (P(f), Promise.reject(new Error("Invalid navigation guard"))));
      else if (c !== void 0 && !h._called) {
        P(f), l(new Error("Invalid navigation guard"));
        return;
      }
    }
    a.catch((f) => l(f));
  });
}
function Ko(e, t, n) {
  let r = 0;
  return function() {
    r++ === 1 && P(`The "next" callback was called more than once in one navigation guard when going from "${n.fullPath}" to "${t.fullPath}". It should be called exactly one time in each navigation guard. This will fail in production.`), e._called = !0, r === 1 && e.apply(null, arguments);
  };
}
function Qe(e, t, n, r, o = (s) => s()) {
  const s = [];
  for (const i of e) {
    O.NODE_ENV !== "production" && !i.components && !i.children.length && P(`Record with path "${i.path}" is either missing a "component(s)" or "children" property.`);
    for (const u in i.components) {
      let l = i.components[u];
      if (O.NODE_ENV !== "production") {
        if (!l || typeof l != "object" && typeof l != "function")
          throw P(`Component "${u}" in record with path "${i.path}" is not a valid component. Received "${String(l)}".`), new Error("Invalid route component");
        if ("then" in l) {
          P(`Component "${u}" in record with path "${i.path}" is a Promise instead of a function that returns a Promise. Did you write "import('./MyPage.vue')" instead of "() => import('./MyPage.vue')" ? This will break in production if not fixed.`);
          const h = l;
          l = () => h;
        } else l.__asyncLoader && // warn only once per component
        !l.__warnedDefineAsync && (l.__warnedDefineAsync = !0, P(`Component "${u}" in record with path "${i.path}" is defined using "defineAsyncComponent()". Write "() => import('./MyPage.vue')" instead of "defineAsyncComponent(() => import('./MyPage.vue'))".`));
      }
      if (!(t !== "beforeRouteEnter" && !i.instances[u]))
        if (mn(l)) {
          const c = (l.__vccOpts || l)[t];
          c && s.push(X(c, n, r, i, u, o));
        } else {
          let h = l();
          O.NODE_ENV !== "production" && !("catch" in h) && (P(`Component "${u}" in record with path "${i.path}" is a function that does not return a Promise. If you were passing a functional component, make sure to add a "displayName" to the component. This will break in production if not fixed.`), h = Promise.resolve(h)), s.push(() => h.then((c) => {
            if (!c)
              throw new Error(`Couldn't resolve component "${u}" at "${i.path}"`);
            const a = Gr(c) ? c.default : c;
            i.mods[u] = c, i.components[u] = a;
            const d = (a.__vccOpts || a)[t];
            return d && X(d, n, r, i, u, o)();
          }));
        }
    }
  }
  return s;
}
function Bt(e) {
  const t = ee(Be), n = ee(gt);
  let r = !1, o = null;
  const s = K(() => {
    const c = L(e.to);
    return O.NODE_ENV !== "production" && (!r || c !== o) && (Te(c) || (r ? P(`Invalid value for prop "to" in useLink()
- to:`, c, `
- previous to:`, o, `
- props:`, e) : P(`Invalid value for prop "to" in useLink()
- to:`, c, `
- props:`, e)), o = c, r = !0), t.resolve(c);
  }), i = K(() => {
    const { matched: c } = s.value, { length: a } = c, f = c[a - 1], d = n.matched;
    if (!f || !d.length)
      return -1;
    const v = d.findIndex(te.bind(null, f));
    if (v > -1)
      return v;
    const p = Lt(c[a - 2]);
    return (
      // we are dealing with nested routes
      a > 1 && // if the parent and matched route have the same path, this link is
      // referring to the empty child. Or we currently are on a different
      // child of the same parent
      Lt(f) === p && // avoid comparing the child with its parent
      d[d.length - 1].path !== p ? d.findIndex(te.bind(null, c[a - 2])) : v
    );
  }), u = K(() => i.value > -1 && Jo(n.params, s.value.params)), l = K(() => i.value > -1 && i.value === n.matched.length - 1 && _n(n.params, s.value.params));
  function h(c = {}) {
    if (zo(c)) {
      const a = t[L(e.replace) ? "replace" : "push"](
        L(e.to)
        // avoid uncaught errors are they are logged anyway
      ).catch(ve);
      return e.viewTransition && typeof document < "u" && "startViewTransition" in document && document.startViewTransition(() => a), a;
    }
    return Promise.resolve();
  }
  if (O.NODE_ENV !== "production" && z) {
    const c = Jt();
    if (c) {
      const a = {
        route: s.value,
        isActive: u.value,
        isExactActive: l.value,
        error: null
      };
      c.__vrl_devtools = c.__vrl_devtools || [], c.__vrl_devtools.push(a), zt(() => {
        a.route = s.value, a.isActive = u.value, a.isExactActive = l.value, a.error = Te(L(e.to)) ? null : 'Invalid "to" value';
      }, { flush: "post" });
    }
  }
  return {
    route: s,
    href: K(() => s.value.href),
    isActive: u,
    isExactActive: l,
    navigate: h
  };
}
function Go(e) {
  return e.length === 1 ? e[0] : e;
}
const qo = /* @__PURE__ */ F({
  name: "RouterLink",
  compatConfig: { MODE: 3 },
  props: {
    to: {
      type: [String, Object],
      required: !0
    },
    replace: Boolean,
    activeClass: String,
    // inactiveClass: String,
    exactActiveClass: String,
    custom: Boolean,
    ariaCurrentValue: {
      type: String,
      default: "page"
    }
  },
  useLink: Bt,
  setup(e, { slots: t }) {
    const n = Jn(Bt(e)), { options: r } = ee(Be), o = K(() => ({
      [Wt(e.activeClass, r.linkActiveClass, "router-link-active")]: n.isActive,
      // [getLinkClass(
      //   props.inactiveClass,
      //   options.linkInactiveClass,
      //   'router-link-inactive'
      // )]: !link.isExactActive,
      [Wt(e.exactActiveClass, r.linkExactActiveClass, "router-link-exact-active")]: n.isExactActive
    }));
    return () => {
      const s = t.default && Go(t.default(n));
      return e.custom ? s : A("a", {
        "aria-current": n.isExactActive ? e.ariaCurrentValue : null,
        href: n.href,
        // this would override user added attrs but Vue will still add
        // the listener, so we end up triggering both
        onClick: n.navigate,
        class: o.value
      }, s);
    };
  }
}), Ho = qo;
function zo(e) {
  if (!(e.metaKey || e.altKey || e.ctrlKey || e.shiftKey) && !e.defaultPrevented && !(e.button !== void 0 && e.button !== 0)) {
    if (e.currentTarget && e.currentTarget.getAttribute) {
      const t = e.currentTarget.getAttribute("target");
      if (/\b_blank\b/i.test(t))
        return;
    }
    return e.preventDefault && e.preventDefault(), !0;
  }
}
function Jo(e, t) {
  for (const n in t) {
    const r = t[n], o = e[n];
    if (typeof r == "string") {
      if (r !== o)
        return !1;
    } else if (!U(o) || o.length !== r.length || r.some((s, i) => s !== o[i]))
      return !1;
  }
  return !0;
}
function Lt(e) {
  return e ? e.aliasOf ? e.aliasOf.path : e.path : "";
}
const Wt = (e, t, n) => e ?? t ?? n, Qo = /* @__PURE__ */ F({
  name: "RouterView",
  // #674 we manually inherit them
  inheritAttrs: !1,
  props: {
    name: {
      type: String,
      default: "default"
    },
    route: Object
  },
  // Better compat for @vue/compat users
  // https://github.com/vuejs/router/issues/1315
  compatConfig: { MODE: 3 },
  setup(e, { attrs: t, slots: n }) {
    O.NODE_ENV !== "production" && Xo();
    const r = ee(ct), o = K(() => e.route || r.value), s = ee(Ft, 0), i = K(() => {
      let h = L(s);
      const { matched: c } = o.value;
      let a;
      for (; (a = c[h]) && !a.components; )
        h++;
      return h;
    }), u = K(() => o.value.matched[i.value]);
    Ne(Ft, K(() => i.value + 1)), Ne(Uo, u), Ne(ct, o);
    const l = Z();
    return G(() => [l.value, u.value, e.name], ([h, c, a], [f, d, v]) => {
      c && (c.instances[a] = h, d && d !== c && h && h === f && (c.leaveGuards.size || (c.leaveGuards = d.leaveGuards), c.updateGuards.size || (c.updateGuards = d.updateGuards))), h && c && // if there is no instance but to and from are the same this might be
      // the first visit
      (!d || !te(c, d) || !f) && (c.enterCallbacks[a] || []).forEach((p) => p(h));
    }, { flush: "post" }), () => {
      const h = o.value, c = e.name, a = u.value, f = a && a.components[c];
      if (!f)
        return Ut(n.default, { Component: f, route: h });
      const d = a.props[c], v = d ? d === !0 ? h.params : typeof d == "function" ? d(h) : d : null, g = A(f, I({}, v, t, {
        onVnodeUnmounted: (y) => {
          y.component.isUnmounted && (a.instances[c] = null);
        },
        ref: l
      }));
      if (O.NODE_ENV !== "production" && z && g.ref) {
        const y = {
          depth: i.value,
          name: a.name,
          path: a.path,
          meta: a.meta
        };
        (U(g.ref) ? g.ref.map((S) => S.i) : [g.ref.i]).forEach((S) => {
          S.__vrv_devtools = y;
        });
      }
      return (
        // pass the vnode to the slot as a prop.
        // h and <component :is="..."> both accept vnodes
        Ut(n.default, { Component: g, route: h }) || g
      );
    };
  }
});
function Ut(e, t) {
  if (!e)
    return null;
  const n = e(t);
  return n.length === 1 ? n[0] : n;
}
const Yo = Qo;
function Xo() {
  const e = Jt(), t = e.parent && e.parent.type.name, n = e.parent && e.parent.subTree && e.parent.subTree.type;
  if (t && (t === "KeepAlive" || t.includes("Transition")) && typeof n == "object" && n.name === "RouterView") {
    const r = t === "KeepAlive" ? "keep-alive" : "transition";
    P(`<router-view> can no longer be used directly inside <transition> or <keep-alive>.
Use slot props instead:

<router-view v-slot="{ Component }">
  <${r}>
    <component :is="Component" />
  </${r}>
</router-view>`);
  }
}
function me(e, t) {
  const n = I({}, e, {
    // remove variables that can contain vue instances
    matched: e.matched.map((r) => us(r, ["instances", "children", "aliasOf"]))
  });
  return {
    _custom: {
      type: null,
      readOnly: !0,
      display: e.fullPath,
      tooltip: t,
      value: n
    }
  };
}
function Ve(e) {
  return {
    _custom: {
      display: e
    }
  };
}
let Zo = 0;
function es(e, t, n) {
  if (t.__hasDevtools)
    return;
  t.__hasDevtools = !0;
  const r = Zo++;
  Kr({
    id: "org.vuejs.router" + (r ? "." + r : ""),
    label: "Vue Router",
    packageName: "vue-router",
    homepage: "https://router.vuejs.org",
    logo: "https://router.vuejs.org/logo.png",
    componentStateTypes: ["Routing"],
    app: e
  }, (o) => {
    typeof o.now != "function" && console.warn("[Vue Router]: You seem to be using an outdated version of Vue Devtools. Are you still using the Beta release instead of the stable one? You can find the links at https://devtools.vuejs.org/guide/installation.html."), o.on.inspectComponent((c, a) => {
      c.instanceData && c.instanceData.state.push({
        type: "Routing",
        key: "$route",
        editable: !1,
        value: me(t.currentRoute.value, "Current Route")
      });
    }), o.on.visitComponentTree(({ treeNode: c, componentInstance: a }) => {
      if (a.__vrv_devtools) {
        const f = a.__vrv_devtools;
        c.tags.push({
          label: (f.name ? `${f.name.toString()}: ` : "") + f.path,
          textColor: 0,
          tooltip: "This component is rendered by &lt;router-view&gt;",
          backgroundColor: Nn
        });
      }
      U(a.__vrl_devtools) && (a.__devtoolsApi = o, a.__vrl_devtools.forEach((f) => {
        let d = f.route.path, v = An, p = "", g = 0;
        f.error ? (d = f.error, v = ss, g = is) : f.isExactActive ? (v = Tn, p = "This is exactly active") : f.isActive && (v = In, p = "This link is active"), c.tags.push({
          label: d,
          textColor: g,
          tooltip: p,
          backgroundColor: v
        });
      }));
    }), G(t.currentRoute, () => {
      l(), o.notifyComponentUpdate(), o.sendInspectorTree(u), o.sendInspectorState(u);
    });
    const s = "router:navigations:" + r;
    o.addTimelineLayer({
      id: s,
      label: `Router${r ? " " + r : ""} Navigations`,
      color: 4237508
    }), t.onError((c, a) => {
      o.addTimelineEvent({
        layerId: s,
        event: {
          title: "Error during Navigation",
          subtitle: a.fullPath,
          logType: "error",
          time: o.now(),
          data: { error: c },
          groupId: a.meta.__navigationId
        }
      });
    });
    let i = 0;
    t.beforeEach((c, a) => {
      const f = {
        guard: Ve("beforeEach"),
        from: me(a, "Current Location during this navigation"),
        to: me(c, "Target location")
      };
      Object.defineProperty(c.meta, "__navigationId", {
        value: i++
      }), o.addTimelineEvent({
        layerId: s,
        event: {
          time: o.now(),
          title: "Start of navigation",
          subtitle: c.fullPath,
          data: f,
          groupId: c.meta.__navigationId
        }
      });
    }), t.afterEach((c, a, f) => {
      const d = {
        guard: Ve("afterEach")
      };
      f ? (d.failure = {
        _custom: {
          type: Error,
          readOnly: !0,
          display: f ? f.message : "",
          tooltip: "Navigation Failure",
          value: f
        }
      }, d.status = Ve("❌")) : d.status = Ve("✅"), d.from = me(a, "Current Location during this navigation"), d.to = me(c, "Target location"), o.addTimelineEvent({
        layerId: s,
        event: {
          title: "End of navigation",
          subtitle: c.fullPath,
          time: o.now(),
          data: d,
          logType: f ? "warning" : "default",
          groupId: c.meta.__navigationId
        }
      });
    });
    const u = "router-inspector:" + r;
    o.addInspector({
      id: u,
      label: "Routes" + (r ? " " + r : ""),
      icon: "book",
      treeFilterPlaceholder: "Search routes"
    });
    function l() {
      if (!h)
        return;
      const c = h;
      let a = n.getRoutes().filter((f) => !f.parent || // these routes have a parent with no component which will not appear in the view
      // therefore we still need to include them
      !f.parent.record.components);
      a.forEach(Cn), c.filter && (a = a.filter((f) => (
        // save matches state based on the payload
        ut(f, c.filter.toLowerCase())
      ))), a.forEach((f) => jn(f, t.currentRoute.value)), c.rootNodes = a.map($n);
    }
    let h;
    o.on.getInspectorTree((c) => {
      h = c, c.app === e && c.inspectorId === u && l();
    }), o.on.getInspectorState((c) => {
      if (c.app === e && c.inspectorId === u) {
        const f = n.getRoutes().find((d) => d.record.__vd_id === c.nodeId);
        f && (c.state = {
          options: ns(f)
        });
      }
    }), o.sendInspectorTree(u), o.sendInspectorState(u);
  });
}
function ts(e) {
  return e.optional ? e.repeatable ? "*" : "?" : e.repeatable ? "+" : "";
}
function ns(e) {
  const { record: t } = e, n = [
    { editable: !1, key: "path", value: t.path }
  ];
  return t.name != null && n.push({
    editable: !1,
    key: "name",
    value: t.name
  }), n.push({ editable: !1, key: "regexp", value: e.re }), e.keys.length && n.push({
    editable: !1,
    key: "keys",
    value: {
      _custom: {
        type: null,
        readOnly: !0,
        display: e.keys.map((r) => `${r.name}${ts(r)}`).join(" "),
        tooltip: "Param keys",
        value: e.keys
      }
    }
  }), t.redirect != null && n.push({
    editable: !1,
    key: "redirect",
    value: t.redirect
  }), e.alias.length && n.push({
    editable: !1,
    key: "aliases",
    value: e.alias.map((r) => r.record.path)
  }), Object.keys(e.record.meta).length && n.push({
    editable: !1,
    key: "meta",
    value: e.record.meta
  }), n.push({
    key: "score",
    editable: !1,
    value: {
      _custom: {
        type: null,
        readOnly: !0,
        display: e.score.map((r) => r.join(", ")).join(" | "),
        tooltip: "Score used to sort routes",
        value: e.score
      }
    }
  }), n;
}
const Nn = 15485081, In = 2450411, Tn = 8702998, rs = 2282478, An = 16486972, os = 6710886, ss = 16704226, is = 12131356;
function $n(e) {
  const t = [], { record: n } = e;
  n.name != null && t.push({
    label: String(n.name),
    textColor: 0,
    backgroundColor: rs
  }), n.aliasOf && t.push({
    label: "alias",
    textColor: 0,
    backgroundColor: An
  }), e.__vd_match && t.push({
    label: "matches",
    textColor: 0,
    backgroundColor: Nn
  }), e.__vd_exactActive && t.push({
    label: "exact",
    textColor: 0,
    backgroundColor: Tn
  }), e.__vd_active && t.push({
    label: "active",
    textColor: 0,
    backgroundColor: In
  }), n.redirect && t.push({
    label: typeof n.redirect == "string" ? `redirect: ${n.redirect}` : "redirects",
    textColor: 16777215,
    backgroundColor: os
  });
  let r = n.__vd_id;
  return r == null && (r = String(as++), n.__vd_id = r), {
    id: r,
    label: n.path,
    tags: t,
    children: e.children.map($n)
  };
}
let as = 0;
const cs = /^\/(.*)\/([a-z]*)$/;
function jn(e, t) {
  const n = t.matched.length && te(t.matched[t.matched.length - 1], e.record);
  e.__vd_exactActive = e.__vd_active = n, n || (e.__vd_active = t.matched.some((r) => te(r, e.record))), e.children.forEach((r) => jn(r, t));
}
function Cn(e) {
  e.__vd_match = !1, e.children.forEach(Cn);
}
function ut(e, t) {
  const n = String(e.re).match(cs);
  if (e.__vd_match = !1, !n || n.length < 3)
    return !1;
  if (new RegExp(n[1].replace(/\$$/, ""), n[2]).test(t))
    return e.children.forEach((i) => ut(i, t)), e.record.path !== "/" || t === "/" ? (e.__vd_match = e.re.test(t), !0) : !1;
  const o = e.record.path.toLowerCase(), s = ae(o);
  return !t.startsWith("/") && (s.includes(t) || o.includes(t)) || s.startsWith(t) || o.startsWith(t) || e.record.name && String(e.record.name).includes(t) ? !0 : e.children.some((i) => ut(i, t));
}
function us(e, t) {
  const n = {};
  for (const r in e)
    t.includes(r) || (n[r] = e[r]);
  return n;
}
function ls(e) {
  const t = Ao(e.routes, e), n = e.parseQuery || Lo, r = e.stringifyQuery || Mt, o = e.history;
  if (O.NODE_ENV !== "production" && !o)
    throw new Error('Provide the "history" option when calling "createRouter()": https://router.vuejs.org/api/interfaces/RouterOptions.html#history');
  const s = pe(), i = pe(), u = pe(), l = J(Y);
  let h = Y;
  z && e.scrollBehavior && "scrollRestoration" in history && (history.scrollRestoration = "manual");
  const c = He.bind(null, (m) => "" + m), a = He.bind(null, oo), f = (
    // @ts-expect-error: intentionally avoid the type check
    He.bind(null, ae)
  );
  function d(m, E) {
    let w, b;
    return Pn(m) ? (w = t.getRecordMatcher(m), O.NODE_ENV !== "production" && !w && P(`Parent route "${String(m)}" not found when adding child route`, E), b = E) : b = m, t.addRoute(b, w);
  }
  function v(m) {
    const E = t.getRecordMatcher(m);
    E ? t.removeRoute(E) : O.NODE_ENV !== "production" && P(`Cannot remove non-existent route "${String(m)}"`);
  }
  function p() {
    return t.getRoutes().map((m) => m.record);
  }
  function g(m) {
    return !!t.getRecordMatcher(m);
  }
  function y(m, E) {
    if (E = I({}, E || l.value), typeof m == "string") {
      const k = ze(n, m, E.path), $ = t.resolve({ path: k.path }, E), re = o.createHref(k.fullPath);
      return O.NODE_ENV !== "production" && (re.startsWith("//") ? P(`Location "${m}" resolved to "${re}". A resolved location cannot start with multiple slashes.`) : $.matched.length || P(`No match found for location with path "${m}"`)), I(k, $, {
        params: f($.params),
        hash: ae(k.hash),
        redirectedFrom: void 0,
        href: re
      });
    }
    if (O.NODE_ENV !== "production" && !Te(m))
      return P(`router.resolve() was passed an invalid location. This will fail in production.
- Location:`, m), y({});
    let w;
    if (m.path != null)
      O.NODE_ENV !== "production" && "params" in m && !("name" in m) && // @ts-expect-error: the type is never
      Object.keys(m.params).length && P(`Path "${m.path}" was passed with params but they will be ignored. Use a named route alongside params instead.`), w = I({}, m, {
        path: ze(n, m.path, E.path).path
      });
    else {
      const k = I({}, m.params);
      for (const $ in k)
        k[$] == null && delete k[$];
      w = I({}, m, {
        params: a(k)
      }), E.params = a(E.params);
    }
    const b = t.resolve(w, E), T = m.hash || "";
    O.NODE_ENV !== "production" && T && !T.startsWith("#") && P(`A \`hash\` should always start with the character "#". Replace "${T}" with "#${T}".`), b.params = c(f(b.params));
    const j = ao(r, I({}, m, {
      hash: to(T),
      path: b.path
    })), V = o.createHref(j);
    return O.NODE_ENV !== "production" && (V.startsWith("//") ? P(`Location "${m}" resolved to "${V}". A resolved location cannot start with multiple slashes.`) : b.matched.length || P(`No match found for location with path "${m.path != null ? m.path : m}"`)), I({
      fullPath: j,
      // keep the hash encoded so fullPath is effectively path + encodedQuery +
      // hash
      hash: T,
      query: (
        // if the user is using a custom query lib like qs, we might have
        // nested objects, so we keep the query as is, meaning it can contain
        // numbers at `$route.query`, but at the point, the user will have to
        // use their own type anyway.
        // https://github.com/vuejs/router/issues/328#issuecomment-649481567
        r === Mt ? Wo(m.query) : m.query || {}
      )
    }, b, {
      redirectedFrom: void 0,
      href: V
    });
  }
  function _(m) {
    return typeof m == "string" ? ze(n, m, l.value.path) : I({}, m);
  }
  function S(m, E) {
    if (h !== m)
      return ue(8, {
        from: E,
        to: m
      });
  }
  function R(m) {
    return x(m);
  }
  function D(m) {
    return R(I(_(m), { replace: !0 }));
  }
  function C(m) {
    const E = m.matched[m.matched.length - 1];
    if (E && E.redirect) {
      const { redirect: w } = E;
      let b = typeof w == "function" ? w(m) : w;
      if (typeof b == "string" && (b = b.includes("?") || b.includes("#") ? b = _(b) : (
        // force empty params
        { path: b }
      ), b.params = {}), O.NODE_ENV !== "production" && b.path == null && !("name" in b))
        throw P(`Invalid redirect found:
${JSON.stringify(b, null, 2)}
 when navigating to "${m.fullPath}". A redirect must contain a name or path. This will break in production.`), new Error("Invalid redirect");
      return I({
        query: m.query,
        hash: m.hash,
        // avoid transferring params if the redirect has a path
        params: b.path != null ? {} : m.params
      }, b);
    }
  }
  function x(m, E) {
    const w = h = y(m), b = l.value, T = m.state, j = m.force, V = m.replace === !0, k = C(w);
    if (k)
      return x(
        I(_(k), {
          state: typeof k == "object" ? I({}, T, k.state) : T,
          force: j,
          replace: V
        }),
        // keep original redirectedFrom if it exists
        E || w
      );
    const $ = w;
    $.redirectedFrom = E;
    let re;
    return !j && kt(r, b, w) && (re = ue(16, { to: $, from: b }), _t(
      b,
      b,
      // this is a push, the only way for it to be triggered from a
      // history.listen is with a redirect, which makes it become a push
      !0,
      // This cannot be the first navigation because the initial location
      // cannot be manually navigated to
      !1
    )), (re ? Promise.resolve(re) : vt($, b)).catch((M) => H(M) ? (
      // navigation redirects still mark the router as ready
      H(
        M,
        2
        /* ErrorTypes.NAVIGATION_GUARD_REDIRECT */
      ) ? M : Ke(M)
    ) : (
      // reject any unknown error
      Ue(M, $, b)
    )).then((M) => {
      if (M) {
        if (H(
          M,
          2
          /* ErrorTypes.NAVIGATION_GUARD_REDIRECT */
        ))
          return O.NODE_ENV !== "production" && // we are redirecting to the same location we were already at
          kt(r, y(M.to), $) && // and we have done it a couple of times
          E && // @ts-expect-error: added only in dev
          (E._count = E._count ? (
            // @ts-expect-error
            E._count + 1
          ) : 1) > 30 ? (P(`Detected a possibly infinite redirection in a navigation guard when going from "${b.fullPath}" to "${$.fullPath}". Aborting to avoid a Stack Overflow.
 Are you always returning a new location within a navigation guard? That would lead to this error. Only return when redirecting or aborting, that should fix this. This might break in production if not fixed.`), Promise.reject(new Error("Infinite redirect in navigation guard"))) : x(
            // keep options
            I({
              // preserve an existing replacement but allow the redirect to override it
              replace: V
            }, _(M.to), {
              state: typeof M.to == "object" ? I({}, T, M.to.state) : T,
              force: j
            }),
            // preserve the original redirectedFrom if any
            E || $
          );
      } else
        M = wt($, b, !0, V, T);
      return yt($, b, M), M;
    });
  }
  function Le(m, E) {
    const w = S(m, E);
    return w ? Promise.reject(w) : Promise.resolve();
  }
  function le(m) {
    const E = Pe.values().next().value;
    return E && typeof E.runWithContext == "function" ? E.runWithContext(m) : m();
  }
  function vt(m, E) {
    let w;
    const [b, T, j] = fs(m, E);
    w = Qe(b.reverse(), "beforeRouteLeave", m, E);
    for (const k of b)
      k.leaveGuards.forEach(($) => {
        w.push(X($, m, E));
      });
    const V = Le.bind(null, m, E);
    return w.push(V), se(w).then(() => {
      w = [];
      for (const k of s.list())
        w.push(X(k, m, E));
      return w.push(V), se(w);
    }).then(() => {
      w = Qe(T, "beforeRouteUpdate", m, E);
      for (const k of T)
        k.updateGuards.forEach(($) => {
          w.push(X($, m, E));
        });
      return w.push(V), se(w);
    }).then(() => {
      w = [];
      for (const k of j)
        if (k.beforeEnter)
          if (U(k.beforeEnter))
            for (const $ of k.beforeEnter)
              w.push(X($, m, E));
          else
            w.push(X(k.beforeEnter, m, E));
      return w.push(V), se(w);
    }).then(() => (m.matched.forEach((k) => k.enterCallbacks = {}), w = Qe(j, "beforeRouteEnter", m, E, le), w.push(V), se(w))).then(() => {
      w = [];
      for (const k of i.list())
        w.push(X(k, m, E));
      return w.push(V), se(w);
    }).catch((k) => H(
      k,
      8
      /* ErrorTypes.NAVIGATION_CANCELLED */
    ) ? k : Promise.reject(k));
  }
  function yt(m, E, w) {
    u.list().forEach((b) => le(() => b(m, E, w)));
  }
  function wt(m, E, w, b, T) {
    const j = S(m, E);
    if (j)
      return j;
    const V = E === Y, k = z ? history.state : {};
    w && (b || V ? o.replace(m.fullPath, I({
      scroll: V && k && k.scroll
    }, T)) : o.push(m.fullPath, T)), l.value = m, _t(m, E, w, V), Ke();
  }
  let fe;
  function Ln() {
    fe || (fe = o.listen((m, E, w) => {
      if (!bt.listening)
        return;
      const b = y(m), T = C(b);
      if (T) {
        x(I(T, { replace: !0, force: !0 }), b).catch(ve);
        return;
      }
      h = b;
      const j = l.value;
      z && po(Nt(j.fullPath, w.delta), Fe()), vt(b, j).catch((V) => H(
        V,
        12
        /* ErrorTypes.NAVIGATION_CANCELLED */
      ) ? V : H(
        V,
        2
        /* ErrorTypes.NAVIGATION_GUARD_REDIRECT */
      ) ? (x(
        I(_(V.to), {
          force: !0
        }),
        b
        // avoid an uncaught rejection, let push call triggerError
      ).then((k) => {
        H(
          k,
          20
          /* ErrorTypes.NAVIGATION_DUPLICATED */
        ) && !w.delta && w.type === ce.pop && o.go(-1, !1);
      }).catch(ve), Promise.reject()) : (w.delta && o.go(-w.delta, !1), Ue(V, b, j))).then((V) => {
        V = V || wt(
          // after navigation, all matched components are resolved
          b,
          j,
          !1
        ), V && (w.delta && // a new navigation has been triggered, so we do not want to revert, that will change the current history
        // entry while a different route is displayed
        !H(
          V,
          8
          /* ErrorTypes.NAVIGATION_CANCELLED */
        ) ? o.go(-w.delta, !1) : w.type === ce.pop && H(
          V,
          20
          /* ErrorTypes.NAVIGATION_DUPLICATED */
        ) && o.go(-1, !1)), yt(b, j, V);
      }).catch(ve);
    }));
  }
  let We = pe(), Et = pe(), Re;
  function Ue(m, E, w) {
    Ke(m);
    const b = Et.list();
    return b.length ? b.forEach((T) => T(m, E, w)) : (O.NODE_ENV !== "production" && P("uncaught error during route navigation:"), console.error(m)), Promise.reject(m);
  }
  function Wn() {
    return Re && l.value !== Y ? Promise.resolve() : new Promise((m, E) => {
      We.add([m, E]);
    });
  }
  function Ke(m) {
    return Re || (Re = !m, Ln(), We.list().forEach(([E, w]) => m ? w(m) : E()), We.reset()), m;
  }
  function _t(m, E, w, b) {
    const { scrollBehavior: T } = e;
    if (!z || !T)
      return Promise.resolve();
    const j = !w && mo(Nt(m.fullPath, 0)) || (b || !w) && history.state && history.state.scroll || null;
    return Ie().then(() => T(m, E, j)).then((V) => V && ho(V)).catch((V) => Ue(V, m, E));
  }
  const Ge = (m) => o.go(m);
  let qe;
  const Pe = /* @__PURE__ */ new Set(), bt = {
    currentRoute: l,
    listening: !0,
    addRoute: d,
    removeRoute: v,
    clearRoutes: t.clearRoutes,
    hasRoute: g,
    getRoutes: p,
    resolve: y,
    options: e,
    push: R,
    replace: D,
    go: Ge,
    back: () => Ge(-1),
    forward: () => Ge(1),
    beforeEach: s.add,
    beforeResolve: i.add,
    afterEach: u.add,
    onError: Et.add,
    isReady: Wn,
    install(m) {
      const E = this;
      m.component("RouterLink", Ho), m.component("RouterView", Yo), m.config.globalProperties.$router = E, Object.defineProperty(m.config.globalProperties, "$route", {
        enumerable: !0,
        get: () => L(l)
      }), z && // used for the initial navigation client side to avoid pushing
      // multiple times when the router is used in multiple apps
      !qe && l.value === Y && (qe = !0, R(o.location).catch((T) => {
        O.NODE_ENV !== "production" && P("Unexpected error when starting the router:", T);
      }));
      const w = {};
      for (const T in Y)
        Object.defineProperty(w, T, {
          get: () => l.value[T],
          enumerable: !0
        });
      m.provide(Be, E), m.provide(gt, zn(w)), m.provide(ct, l);
      const b = m.unmount;
      Pe.add(m), m.unmount = function() {
        Pe.delete(m), Pe.size < 1 && (h = Y, fe && fe(), fe = null, l.value = Y, qe = !1, Re = !1), b();
      }, O.NODE_ENV !== "production" && z && es(m, E, t);
    }
  };
  function se(m) {
    return m.reduce((E, w) => E.then(() => le(w)), Promise.resolve());
  }
  return bt;
}
function fs(e, t) {
  const n = [], r = [], o = [], s = Math.max(t.matched.length, e.matched.length);
  for (let i = 0; i < s; i++) {
    const u = t.matched[i];
    u && (e.matched.find((h) => te(h, u)) ? r.push(u) : n.push(u));
    const l = e.matched[i];
    l && (t.matched.find((h) => te(h, l)) || o.push(l));
  }
  return [n, r, o];
}
function hs() {
  return ee(Be);
}
function ds(e) {
  return ee(gt);
}
const xn = /* @__PURE__ */ new Map();
function ps(e) {
  var t;
  (t = e.jsFn) == null || t.forEach((n) => {
    xn.set(n.id, W(n.code));
  });
}
function ms(e) {
  return xn.get(e);
}
function ne(e) {
  let t = sn(), n = Pr(), r = Ar(e), o = un(), s = hs(), i = ds();
  function u(p) {
    p.scopeSnapshot && (t = p.scopeSnapshot), p.slotSnapshot && (n = p.slotSnapshot), p.vforSnapshot && (r = p.vforSnapshot), p.elementRefSnapshot && (o = p.elementRefSnapshot), p.routerSnapshot && (s = p.routerSnapshot);
  }
  function l(p) {
    if (N.isVar(p))
      return q(h(p));
    if (N.isVForItem(p))
      return jr(p.fid) ? r.getVForIndex(p.fid) : q(h(p));
    if (N.isVForIndex(p))
      return r.getVForIndex(p.fid);
    if (N.isJsFn(p)) {
      const { id: g } = p;
      return ms(g);
    }
    if (N.isSlotProp(p))
      return n.getPropsValue(p);
    if (N.isRouterParams(p))
      return q(h(p));
    throw new Error(`Invalid binding: ${p}`);
  }
  function h(p) {
    if (N.isVar(p)) {
      const g = t.getVueRef(p) || wr(p);
      return Ot(g, {
        paths: p.path,
        getBindableValueFn: l
      });
    }
    if (N.isVForItem(p))
      return $r({
        binding: p,
        snapshot: v
      });
    if (N.isVForIndex(p))
      return () => l(p);
    if (N.isRouterParams(p)) {
      const { prop: g = "params" } = p;
      return Ot(() => i[g], {
        paths: p.path,
        getBindableValueFn: l
      });
    }
    throw new Error(`Invalid binding: ${p}`);
  }
  function c(p) {
    if (N.isVar(p) || N.isVForItem(p))
      return h(p);
    if (N.isVForIndex(p) || N.isJsFn(p))
      return l(p);
    if (N.isRouterParams(p))
      return h(p);
    throw new Error(`Invalid binding: ${p}`);
  }
  function a(p) {
    if (N.isVar(p))
      return {
        sid: p.sid,
        id: p.id
      };
    if (N.isVForItem(p))
      return {
        type: "vf",
        fid: p.fid
      };
    if (N.isVForIndex(p))
      return {
        type: "vf-i",
        fid: p.fid,
        value: null
      };
    if (N.isJsFn(p))
      return l(p);
  }
  function f(p) {
    var g, y;
    (g = p.vars) == null || g.forEach((_) => {
      h({ type: "var", ..._ }).value = _.val;
    }), (y = p.ele_refs) == null || y.forEach((_) => {
      o.getRef({
        sid: _.sid,
        id: _.id
      }).value[_.method](..._.args);
    });
  }
  function d(p, g) {
    if (Rt(g) || Rt(p.values))
      return;
    g = g;
    const y = p.values, _ = p.skips || new Array(g.length).fill(0);
    g.forEach((S, R) => {
      if (_[R] === 1)
        return;
      if (N.isVar(S)) {
        const C = h(S);
        C.value = y[R];
        return;
      }
      if (N.isRouterAction(S)) {
        const C = y[R], x = s[C.fn];
        x(...C.args);
        return;
      }
      if (N.isElementRef(S)) {
        const C = o.getRef(S).value, x = y[R], { method: Le, args: le = [] } = x;
        C[Le](...le);
        return;
      }
      const D = h(S);
      D.value = y[R];
    });
  }
  const v = {
    getVForIndex: r.getVForIndex,
    getObjectToValue: l,
    getVueRefObject: h,
    getVueRefObjectOrValue: c,
    getBindingServerInfo: a,
    updateRefFromServer: f,
    updateOutputsRefFromServer: d,
    replaceSnapshot: u
  };
  return v;
}
class gs {
  async eventSend(t, n) {
    const { fType: r, hKey: o, key: s } = t, i = Xe().webServerInfo, u = s !== void 0 ? { key: s } : {}, l = r === "sync" ? i.event_url : i.event_async_url;
    let h = {};
    const c = await fetch(l, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        bind: n,
        hKey: o,
        ...u,
        page: ye(),
        ...h
      })
    });
    if (!c.ok)
      throw new Error(`HTTP error! status: ${c.status}`);
    return await c.json();
  }
  async watchSend(t) {
    const { outputs: n, fType: r, key: o } = t.watchConfig, s = Xe().webServerInfo, i = r === "sync" ? s.watch_url : s.watch_async_url, u = t.getServerInputs(), l = {
      key: o,
      input: u,
      page: ye()
    };
    return await (await fetch(i, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(l)
    })).json();
  }
}
class vs {
  async eventSend(t, n) {
    const { fType: r, hKey: o, key: s } = t, i = s !== void 0 ? { key: s } : {};
    let u = {};
    const l = {
      bind: n,
      fType: r,
      hKey: o,
      ...i,
      page: ye(),
      ...u
    };
    return await window.pywebview.api.event_call(l);
  }
  async watchSend(t) {
    const { outputs: n, fType: r, key: o } = t.watchConfig, s = t.getServerInputs(), i = {
      key: o,
      input: s,
      fType: r,
      page: ye()
    };
    return await window.pywebview.api.watch_call(i);
  }
}
let lt;
function ys(e) {
  switch (e.mode) {
    case "web":
      lt = new gs();
      break;
    case "webview":
      lt = new vs();
      break;
  }
}
function Dn() {
  return lt;
}
function ws(e) {
  const t = {
    type: "var",
    sid: e.sid,
    id: e.id
  };
  return {
    ...e,
    immediate: !0,
    outputs: [t, ...e.outputs || []]
  };
}
function Es(e, t, n) {
  return new _s(e, t, n);
}
class _s {
  constructor(t, n, r) {
    B(this, "taskQueue", []);
    B(this, "id2TaskMap", /* @__PURE__ */ new Map());
    B(this, "input2TaskIdMap", _e(() => []));
    this.snapshots = r;
    const o = [], s = (i) => {
      var l;
      const u = new bs(i, r);
      return this.id2TaskMap.set(u.id, u), (l = i.inputs) == null || l.forEach((h, c) => {
        var f, d;
        if (((f = i.data) == null ? void 0 : f[c]) === 0 && ((d = i.slient) == null ? void 0 : d[c]) === 0) {
          const v = `${h.sid}-${h.id}`;
          this.input2TaskIdMap.getOrDefault(v).push(u.id);
        }
      }), u;
    };
    t == null || t.forEach((i) => {
      const u = s(i);
      o.push(u);
    }), n == null || n.forEach((i) => {
      const u = s(
        ws(i)
      );
      o.push(u);
    }), o.forEach((i) => {
      const {
        deep: u = !0,
        once: l,
        flush: h,
        immediate: c = !0
      } = i.watchConfig, a = {
        immediate: c,
        deep: u,
        once: l,
        flush: h
      }, f = this._getWatchTargets(i);
      G(
        f,
        (d) => {
          d.some(Ee) || (i.modify = !0, this.taskQueue.push(new Ss(i)), this._scheduleNextTick());
        },
        a
      );
    });
  }
  _getWatchTargets(t) {
    if (!t.watchConfig.inputs)
      return [];
    const n = t.slientInputs, r = t.constDataInputs;
    return t.watchConfig.inputs.filter(
      (s, i) => !r[i] && (N.isVar(s) || N.isVForItem(s) || N.isRouterParams(s)) && !n[i]
    ).map((s) => this.snapshots.getVueRefObjectOrValue(s));
  }
  _scheduleNextTick() {
    Ie(() => this._runAllTasks());
  }
  _runAllTasks() {
    const t = this.taskQueue.slice();
    this.taskQueue.length = 0, this._setTaskNodeRelations(t), t.forEach((n) => {
      n.run();
    });
  }
  _setTaskNodeRelations(t) {
    t.forEach((n) => {
      const r = this._findNextNodes(n, t);
      n.appendNextNodes(...r), r.forEach((o) => {
        o.appendPrevNodes(n);
      });
    });
  }
  _findNextNodes(t, n) {
    const r = t.watchTask.watchConfig.outputs;
    if (r && r.length <= 0)
      return [];
    const o = this._getCalculatorTasksByOutput(
      t.watchTask.watchConfig.outputs
    );
    return n.filter(
      (s) => o.has(s.watchTask.id) && s.watchTask.id !== t.watchTask.id
    );
  }
  _getCalculatorTasksByOutput(t) {
    const n = /* @__PURE__ */ new Set();
    return t == null || t.forEach((r) => {
      const o = `${r.sid}-${r.id}`;
      (this.input2TaskIdMap.get(o) || []).forEach((i) => n.add(i));
    }), n;
  }
}
class bs {
  constructor(t, n) {
    B(this, "modify", !0);
    B(this, "_running", !1);
    B(this, "id");
    B(this, "_runningPromise", null);
    B(this, "_runningPromiseResolve", null);
    B(this, "_inputInfos");
    this.watchConfig = t, this.snapshot = n, this.id = Symbol(t.debug), this._inputInfos = this.createInputInfos();
  }
  createInputInfos() {
    const { inputs: t = [] } = this.watchConfig, n = this.watchConfig.data || new Array(t.length).fill(0), r = this.watchConfig.slient || new Array(t.length).fill(0);
    return {
      const_data: n,
      slients: r
    };
  }
  get slientInputs() {
    return this._inputInfos.slients;
  }
  get constDataInputs() {
    return this._inputInfos.const_data;
  }
  getServerInputs() {
    const { const_data: t } = this._inputInfos;
    return this.watchConfig.inputs ? this.watchConfig.inputs.map((n, r) => t[r] === 0 ? this.snapshot.getObjectToValue(n) : n) : [];
  }
  get running() {
    return this._running;
  }
  get runningPromise() {
    return this._runningPromise;
  }
  /**
   * setRunning
   */
  setRunning() {
    this._running = !0, this._runningPromise = new Promise((t) => {
      this._runningPromiseResolve = t;
    }), this._trySetRunningRef(!0);
  }
  /**
   * taskDone
   */
  taskDone() {
    this._running = !1, this._runningPromiseResolve && (this._runningPromiseResolve(), this._runningPromiseResolve = null), this._trySetRunningRef(!1);
  }
  _trySetRunningRef(t) {
    if (this.watchConfig.running) {
      const n = this.snapshot.getVueRefObject(
        this.watchConfig.running
      );
      n.value = t;
    }
  }
}
class Ss {
  /**
   *
   */
  constructor(t) {
    B(this, "prevNodes", []);
    B(this, "nextNodes", []);
    B(this, "_runningPrev", !1);
    this.watchTask = t;
  }
  /**
   * appendPrevNodes
   */
  appendPrevNodes(...t) {
    this.prevNodes.push(...t);
  }
  /**
   *
   */
  appendNextNodes(...t) {
    this.nextNodes.push(...t);
  }
  /**
   * hasNextNodes
   */
  hasNextNodes() {
    return this.nextNodes.length > 0;
  }
  /**
   * run
   */
  async run() {
    if (this.prevNodes.length > 0 && !this._runningPrev)
      try {
        this._runningPrev = !0, await Promise.all(this.prevNodes.map((t) => t.run()));
      } finally {
        this._runningPrev = !1;
      }
    if (this.watchTask.running) {
      await this.watchTask.runningPromise;
      return;
    }
    if (this.watchTask.modify) {
      this.watchTask.modify = !1, this.watchTask.setRunning();
      try {
        await Os(this.watchTask);
      } finally {
        this.watchTask.taskDone();
      }
    }
  }
}
async function Os(e) {
  const { snapshot: t } = e, { outputs: n } = e.watchConfig, r = await Dn().watchSend(e);
  r && t.updateOutputsRefFromServer(r, n);
}
function Rs(e, t) {
  const {
    on: n,
    code: r,
    immediate: o,
    deep: s,
    once: i,
    flush: u,
    bind: l = {},
    onData: h,
    bindData: c
  } = e, a = h || new Array(n.length).fill(0), f = c || new Array(Object.keys(l).length).fill(0), d = De(
    l,
    (g, y, _) => f[_] === 0 ? t.getVueRefObject(g) : g
  ), v = W(r, d), p = n.length === 1 ? Kt(a[0] === 1, n[0], t) : n.map(
    (g, y) => Kt(a[y] === 1, g, t)
  );
  return G(p, v, { immediate: o, deep: s, once: i, flush: u });
}
function Kt(e, t, n) {
  return e ? () => t : n.getVueRefObject(t);
}
function Ps(e, t) {
  const {
    inputs: n = [],
    outputs: r,
    slient: o,
    data: s,
    code: i,
    immediate: u = !0,
    deep: l,
    once: h,
    flush: c
  } = e, a = o || new Array(n.length).fill(0), f = s || new Array(n.length).fill(0), d = W(i), v = n.filter((g, y) => a[y] === 0 && f[y] === 0).map((g) => t.getVueRefObject(g));
  function p() {
    return n.map((g, y) => f[y] === 0 ? nn(q(t.getVueRefObject(g))) : g);
  }
  G(
    v,
    () => {
      let g = d(...p());
      if (!r)
        return;
      const _ = r.length === 1 ? [g] : g, S = _.map((R) => R === void 0 ? 1 : 0);
      t.updateOutputsRefFromServer(
        { values: _, skips: S },
        r
      );
    },
    { immediate: u, deep: l, once: h, flush: c }
  );
}
function ks(e, t) {
  return Object.assign(
    {},
    ...Object.entries(e ?? {}).map(([n, r]) => {
      const o = r.map((u) => {
        if (u.type === "web") {
          const l = Vs(u.bind, t);
          return Ns(u, l, t);
        } else {
          if (u.type === "vue")
            return Ts(u, t);
          if (u.type === "js")
            return Is(u, t);
        }
        throw new Error(`unknown event type ${u}`);
      }), i = W(
        " (...args)=> Promise.all(promises(...args))",
        {
          promises: (...u) => o.map(async (l) => {
            await l(...u);
          })
        }
      );
      return { [n]: i };
    })
  );
}
function Vs(e, t) {
  return (...n) => (e ?? []).map((r) => {
    if (N.isEventContext(r)) {
      if (r.path.startsWith(":")) {
        const o = r.path.slice(1);
        return W(o)(...n);
      }
      return be(n[0], r.path.split("."));
    }
    return N.IsBinding(r) ? t.getObjectToValue(r) : r;
  });
}
function Ns(e, t, n) {
  async function r(...o) {
    const s = t(...o), i = await Dn().eventSend(e, s);
    i && n.updateOutputsRefFromServer(i, e.set);
  }
  return r;
}
function Is(e, t) {
  const { code: n, inputs: r = [], set: o } = e, s = W(n);
  function i(...u) {
    const l = (r ?? []).map((c) => {
      if (N.isEventContext(c)) {
        if (c.path.startsWith(":")) {
          const a = c.path.slice(1);
          return W(a)(...u);
        }
        return be(u[0], c.path.split("."));
      }
      return N.IsBinding(c) ? nn(t.getObjectToValue(c)) : c;
    }), h = s(...l);
    if (o !== void 0) {
      const a = o.length === 1 ? [h] : h, f = a.map((d) => d === void 0 ? 1 : 0);
      t.updateOutputsRefFromServer({ values: a, skips: f }, o);
    }
  }
  return i;
}
function Ts(e, t) {
  const { code: n, bind: r = {}, bindData: o } = e, s = o || new Array(Object.keys(r).length).fill(0), i = De(
    r,
    (h, c, a) => s[a] === 0 ? t.getVueRefObject(h) : h
  ), u = W(n, i);
  function l(...h) {
    u(...h);
  }
  return l;
}
function As(e, t) {
  const n = [];
  (e.bStyle || []).forEach((s) => {
    Array.isArray(s) ? n.push(
      ...s.map((i) => t.getObjectToValue(i))
    ) : n.push(
      De(
        s,
        (i) => t.getObjectToValue(i)
      )
    );
  });
  const r = Qn([e.style || {}, n]);
  return {
    hasStyle: r && Object.keys(r).length > 0,
    styles: r
  };
}
function $s(e, t) {
  const n = e.classes;
  if (!n)
    return null;
  if (typeof n == "string")
    return Ye(n);
  const { str: r, map: o, bind: s } = n, i = [];
  return r && i.push(r), o && i.push(
    De(
      o,
      (u) => t.getObjectToValue(u)
    )
  ), s && i.push(...s.map((u) => t.getObjectToValue(u))), Ye(i);
}
function Ae(e, t = !0) {
  if (!(typeof e != "object" || e === null)) {
    if (Array.isArray(e)) {
      t && e.forEach((n) => Ae(n, !0));
      return;
    }
    for (const [n, r] of Object.entries(e))
      if (n.startsWith(":"))
        try {
          e[n.slice(1)] = new Function(`return (${r})`)(), delete e[n];
        } catch (o) {
          console.error(
            `Error while converting ${n} attribute to function:`,
            o
          );
        }
      else
        t && Ae(r, !0);
  }
}
function js(e, t) {
  const n = e.startsWith(":");
  return n && (e = e.slice(1), t = W(t)), { name: e, value: t, isFunc: n };
}
function Cs(e, t, n) {
  var o;
  const r = {};
  return St(e.bProps || {}, (s, i) => {
    const u = n.getObjectToValue(s);
    Ee(u) || (Ae(u), r[i] = xs(u, i));
  }), (o = e.proxyProps) == null || o.forEach((s) => {
    const i = n.getObjectToValue(s);
    typeof i == "object" && St(i, (u, l) => {
      const { name: h, value: c } = js(l, u);
      r[h] = c;
    });
  }), { ...t || {}, ...r };
}
function xs(e, t) {
  return t === "innerText" ? Qt(e) : e;
}
function Ds(e, { slots: t }) {
  const { id: n, use: r } = e.propsInfo, o = Sr(n);
  return Ce(() => {
    Rr(n);
  }), () => {
    const s = e.propsValue;
    return Or(
      n,
      o,
      Object.fromEntries(
        r.map((i) => [i, s[i]])
      )
    ), A(xe, null, t.default());
  };
}
const Ms = F(Ds, {
  props: ["propsInfo", "propsValue"]
});
function Fs(e, t) {
  if (!e.slots)
    return null;
  const n = e.slots ?? {};
  return Array.isArray(n) ? t ? ge(n) : () => ge(n) : Zt(n, { keyFn: (i) => i === ":" ? "default" : i, valueFn: (i) => {
    const { items: u } = i;
    return (l) => {
      if (i.scope) {
        const h = () => i.props ? Gt(i.props, l, u) : ge(u);
        return A(Oe, { scope: i.scope }, h);
      }
      return i.props ? Gt(i.props, l, u) : ge(u);
    };
  } });
}
function Gt(e, t, n) {
  return A(
    Ms,
    { propsInfo: e, propsValue: t },
    () => ge(n)
  );
}
function ge(e) {
  const t = (e ?? []).map((n) => A(Q, {
    component: n
  }));
  return t.length <= 0 ? null : t;
}
function Bs(e, t) {
  const n = {}, r = [];
  return (e || []).forEach((o) => {
    const { sys: s, name: i, arg: u, value: l, mf: h } = o;
    if (i === "vmodel") {
      const c = t.getVueRefObject(l);
      if (n[`onUpdate:${u}`] = (a) => {
        c.value = a;
      }, s === 1) {
        const a = h ? Object.fromEntries(h.map((f) => [f, !0])) : {};
        r.push([Yn, c.value, void 0, a]);
      } else
        n[u] = c.value;
    } else if (i === "vshow") {
      const c = t.getVueRefObject(l);
      r.push([Xn, c.value]);
    } else
      console.warn(`Directive ${i} is not supported yet`);
  }), {
    newProps: n,
    directiveArray: r
  };
}
function Ls(e, t) {
  const { eRef: n } = e;
  return n === void 0 ? {} : { ref: t.getRef(n) };
}
function Ws(e) {
  const t = ne(), n = un(), r = e.component.props ?? {};
  return Ae(r, !0), () => {
    const { tag: o } = e.component, s = N.IsBinding(o) ? t.getObjectToValue(o) : o, i = ft(s), u = typeof i == "string", l = $s(e.component, t), { styles: h, hasStyle: c } = As(e.component, t), a = ks(e.component.events ?? {}, t), f = Fs(e.component, u), d = Cs(e.component, r, t), { newProps: v, directiveArray: p } = Bs(
      e.component.dir,
      t
    ), g = Ls(
      e.component,
      n
    ), y = Zn({
      ...d,
      ...a,
      ...v,
      ...g
    }) || {};
    c && (y.style = h), l && (y.class = l);
    const _ = A(i, { ...y }, f);
    return p.length > 0 ? er(
      // @ts-ignore
      _,
      p
    ) : _;
  };
}
const Q = F(Ws, {
  props: ["component"]
});
function Mn(e, t) {
  var n, r;
  if (e) {
    const o = _r(e), s = on(e, ne(t)), i = ne(t);
    Es(e.py_watch, e.web_computed, i), (n = e.vue_watch) == null || n.forEach((u) => Rs(u, i)), (r = e.js_watch) == null || r.forEach((u) => Ps(u, i)), Ce(() => {
      cn(e.id, s), br(e.id, o);
    });
  }
}
function Us(e, { slots: t }) {
  const { scope: n } = e;
  return Mn(n), () => A(xe, null, t.default());
}
const Oe = F(Us, {
  props: ["scope"]
}), Ks = F(
  (e) => {
    const { scope: t, items: n, vforInfo: r } = e;
    return kr(r), Mn(t, r.key), n.length === 1 ? () => A(Q, {
      component: n[0]
    }) : () => n.map(
      (s) => A(Q, {
        component: s
      })
    );
  },
  {
    props: ["scope", "items", "vforInfo"]
  }
);
function Gs(e, t) {
  const { state: n, isReady: r, isLoading: o } = dr(async () => {
    let s = e;
    const i = t;
    if (!s && !i)
      throw new Error("Either config or configUrl must be provided");
    if (!s && i && (s = await (await fetch(i)).json()), !s)
      throw new Error("Failed to load config");
    return s;
  }, {});
  return { config: n, isReady: r, isLoading: o };
}
function qs(e, t) {
  let n;
  return t.component ? n = `Error captured from component:tag: ${t.component.tag} ; id: ${t.component.id} ` : n = "Error captured from app init", console.group(n), console.error("Component:", t.component), console.error("Error:", e), console.groupEnd(), !1;
}
const Hs = { class: "app-box" }, zs = {
  key: 0,
  style: { position: "absolute", top: "50%", left: "50%", transform: "translate(-50%, -50%)" }
}, Js = /* @__PURE__ */ F({
  __name: "App",
  props: {
    config: {},
    configUrl: {}
  },
  setup(e) {
    const t = e, { config: n, isLoading: r } = Gs(
      t.config,
      t.configUrl
    );
    let o = null;
    return G(n, (s) => {
      o = s, s.url && (cr({
        mode: s.mode,
        version: s.version,
        queryPath: s.url.path,
        pathParams: s.url.params,
        webServerInfo: s.webInfo
      }), ys(s), ps(s));
    }), tr(qs), (s, i) => (he(), ke("div", Hs, [
      L(r) ? (he(), ke("div", zs, i[0] || (i[0] = [
        nr("p", { style: { margin: "auto" } }, "Loading ...", -1)
      ]))) : (he(), ke("div", {
        key: 1,
        class: Ye(["insta-main", L(n).class])
      }, [
        rr(L(Oe), {
          scope: L(o).scope
        }, {
          default: or(() => [
            (he(!0), ke(xe, null, sr(L(o).items, (u) => (he(), ir(L(Q), { component: u }, null, 8, ["component"]))), 256))
          ]),
          _: 1
        }, 8, ["scope"])
      ], 2))
    ]));
  }
});
function Qs(e) {
  const { on: t, scope: n, items: r } = e, o = ne();
  return () => {
    const s = typeof t == "boolean" ? t : o.getObjectToValue(t);
    return A(Oe, { scope: n }, () => s ? r.map(
      (u) => A(Q, { component: u })
    ) : void 0);
  };
}
const Ys = F(Qs, {
  props: ["on", "scope", "items"]
});
function Xs(e) {
  const { start: t = 0, end: n, step: r = 1 } = e;
  let o = [];
  if (r > 0)
    for (let s = t; s < n; s += r)
      o.push(s);
  else
    for (let s = t; s > n; s += r)
      o.push(s);
  return o;
}
function Zs(e) {
  const { array: t, bArray: n, items: r, fkey: o, fid: s, scope: i, num: u, tsGroup: l = {} } = e, h = t === void 0, c = u !== void 0, a = h ? n : t, f = ne();
  Nr(s, a, h, c);
  const v = oi(o ?? "index");
  return Ce(() => {
    Er(i.id);
  }), () => {
    const p = ti(
      c,
      h,
      a,
      f,
      u
    ), g = Tr(s), y = p.map((_, S) => {
      const R = v(_, S);
      return g.add(R), Ir(s, R, S), A(Ks, {
        scope: e.scope,
        items: r,
        vforInfo: {
          fid: s,
          key: R
        },
        key: R
      });
    });
    return g.removeUnusedKeys(), l && Object.keys(l).length > 0 ? A(Yt, l, {
      default: () => y
    }) : y;
  };
}
const ei = F(Zs, {
  props: ["array", "items", "fid", "bArray", "scope", "num", "fkey", "tsGroup"]
});
function ti(e, t, n, r, o) {
  if (e) {
    let i = 0;
    return typeof o == "number" ? i = o : i = r.getObjectToValue(o) ?? 0, Xs({
      end: Math.max(0, i)
    });
  }
  const s = t ? r.getObjectToValue(n) || [] : n;
  return typeof s == "object" ? Object.values(s) : s;
}
const ni = (e) => e, ri = (e, t) => t;
function oi(e) {
  const t = pr(e);
  return typeof t == "function" ? t : e === "item" ? ni : ri;
}
function si(e) {
  return e.map((n) => {
    if (n.tag)
      return A(Q, { component: n });
    const r = ft(Fn);
    return A(r, {
      scope: n
    });
  });
}
const Fn = F(
  (e) => {
    const t = e.scope;
    return () => si(t.items ?? []);
  },
  {
    props: ["scope"]
  }
);
function ii(e) {
  return e.map((t) => {
    if (t.tag)
      return A(Q, { component: t });
    const n = ft(Fn);
    return A(n, {
      scope: t
    });
  });
}
const ai = F(
  (e) => {
    const { scope: t, on: n, items: r } = e, o = J(r), s = on(t), i = ne();
    return $e.createDynamicWatchRefresh(n, i, async () => {
      const { items: u, on: l } = await $e.fetchRemote(e, i);
      return o.value = u, l;
    }), Ce(() => {
      cn(t.id, s);
    }), () => ii(o.value);
  },
  {
    props: ["sid", "url", "hKey", "on", "bind", "items", "scope"]
  }
);
var $e;
((e) => {
  function t(r, o, s) {
    let i = null, u = r, l = u.map((c) => o.getVueRefObject(c));
    function h() {
      i && i(), i = G(
        l,
        async () => {
          u = await s(), l = u.map((c) => o.getVueRefObject(c)), h();
        },
        { deep: !0 }
      );
    }
    return h(), () => {
      i && i();
    };
  }
  e.createDynamicWatchRefresh = t;
  async function n(r, o) {
    const s = Object.values(r.bind).map((c) => ({
      sid: c.sid,
      id: c.id,
      value: o.getObjectToValue(c)
    })), i = {
      sid: r.sid,
      bind: s,
      hKey: r.hKey,
      page: ye()
    }, u = {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(i)
    }, l = await fetch(r.url, u);
    if (!l.ok)
      throw new Error("Failed to fetch data");
    return await l.json();
  }
  e.fetchRemote = n;
})($e || ($e = {}));
function ci(e) {
  const { scope: t, items: n } = e;
  return () => {
    const r = n.map((o) => A(Q, { component: o }));
    return A(Oe, { scope: t }, () => r);
  };
}
const qt = F(ci, {
  props: ["scope", "items"]
});
function ui(e) {
  const { on: t, case: n, default: r } = e, o = ne();
  return () => {
    const s = o.getObjectToValue(t), i = n.map((u) => {
      const { value: l, items: h, scope: c } = u.props;
      if (s === l)
        return A(qt, {
          scope: c,
          items: h,
          key: ["case", l].join("-")
        });
    }).filter((u) => u);
    if (r && !i.length) {
      const { items: u, scope: l } = r.props;
      i.push(A(qt, { scope: l, items: u, key: "default" }));
    }
    return A(xe, i);
  };
}
const li = F(ui, {
  props: ["case", "on", "default"]
});
function fi(e, { slots: t }) {
  const { name: n = "fade", tag: r } = e;
  return () => A(
    Yt,
    { name: n, tag: r },
    {
      default: t.default
    }
  );
}
const hi = F(fi, {
  props: ["name", "tag"]
});
function di(e) {
  const { content: t, r: n = 0 } = e, r = ne(), o = n === 1 ? () => r.getObjectToValue(t) : () => t;
  return () => Qt(o());
}
const pi = F(di, {
  props: ["content", "r"]
});
function mi(e) {
  if (!e.router)
    throw new Error("Router config is not provided.");
  const { routes: t, kAlive: n = !1 } = e.router;
  return t.map(
    (o) => Bn(o, n)
  );
}
function Bn(e, t) {
  var l;
  const { server: n = !1, vueItem: r, scope: o } = e, s = () => {
    if (n)
      throw new Error("Server-side rendering is not supported yet.");
    return Promise.resolve(gi(r, o, t));
  }, i = (l = r.children) == null ? void 0 : l.map(
    (h) => Bn(h, t)
  ), u = {
    ...r,
    children: i,
    component: s
  };
  return r.component.length === 0 && delete u.component, i === void 0 && delete u.children, u;
}
function gi(e, t, n) {
  const { path: r, component: o } = e, s = A(
    Oe,
    { scope: t, key: r },
    () => o.map((u) => A(Q, { component: u }))
  );
  return n ? A(ar, null, () => s) : s;
}
function vi(e, t) {
  const { mode: n = "hash" } = t.router, r = n === "hash" ? Eo() : n === "memory" ? wo() : Rn();
  e.use(
    ls({
      history: r,
      routes: mi(t)
    })
  );
}
function Ei(e, t) {
  e.component("insta-ui", Js), e.component("vif", Ys), e.component("vfor", ei), e.component("match", li), e.component("refresh", ai), e.component("ts-group", hi), e.component("content", pi), t.router && vi(e, t);
}
export {
  Ae as convertDynamicProperties,
  Ei as install
};
//# sourceMappingURL=insta-ui.js.map
