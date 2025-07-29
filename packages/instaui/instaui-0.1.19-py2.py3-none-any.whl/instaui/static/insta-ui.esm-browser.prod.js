var Gn = Object.defineProperty;
var qn = (e, t, n) => t in e ? Gn(e, t, { enumerable: !0, configurable: !0, writable: !0, value: n }) : e[t] = n;
var B = (e, t, n) => qn(e, typeof t != "symbol" ? t + "" : t, n);
import * as Hn from "vue";
import { toRaw as zn, customRef as Ce, toValue as q, unref as L, watch as G, nextTick as Te, isRef as zt, ref as Z, shallowRef as J, watchEffect as Jt, computed as K, readonly as Jn, provide as Ie, inject as ee, shallowReactive as Qn, defineComponent as F, reactive as Yn, h as A, getCurrentInstance as Qt, normalizeStyle as Xn, normalizeClass as Xe, toDisplayString as Yt, onUnmounted as xe, Fragment as De, vModelDynamic as Zn, vShow as er, resolveDynamicComponent as dt, normalizeProps as tr, withDirectives as nr, onErrorCaptured as rr, openBlock as he, createElementBlock as Ve, createElementVNode as or, createVNode as sr, withCtx as ir, renderList as ar, createBlock as cr, TransitionGroup as Xt, KeepAlive as ur } from "vue";
let Zt;
function lr(e) {
  Zt = e;
}
function Ze() {
  return Zt;
}
function we() {
  const { queryPath: e, pathParams: t, queryParams: n } = Ze();
  return {
    path: e,
    ...t === void 0 ? {} : { params: t },
    ...n === void 0 ? {} : { queryParams: n }
  };
}
class fr extends Map {
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
function Se(e) {
  return new fr(e);
}
function Ot(e, t) {
  Object.entries(e).forEach(([n, r]) => t(r, n));
}
function Me(e, t) {
  return en(e, {
    valueFn: t
  });
}
function en(e, t) {
  const { valueFn: n, keyFn: r } = t;
  return Object.fromEntries(
    Object.entries(e).map(([o, s], i) => [
      r ? r(o, s) : o,
      n(s, o, i)
    ])
  );
}
function tn(e, t, n) {
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
  const r = nn(t, n);
  return e[r];
}
function nn(e, t) {
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
    (r, o) => tn(r, o, n),
    e
  );
}
function et(e, t, n, r) {
  t.reduce((o, s, i) => {
    if (i === t.length - 1)
      o[nn(s, r)] = n;
    else
      return tn(o, s, r);
  }, e);
}
function rn(e) {
  return JSON.parse(JSON.stringify(e));
}
class dr {
  toString() {
    return "";
  }
}
const Ee = new dr();
function _e(e) {
  return zn(e) === Ee;
}
function Rt(e, t, n) {
  const { paths: r, getBindableValueFn: o } = t, { paths: s, getBindableValueFn: i } = t;
  return r === void 0 || r.length === 0 ? e : Ce(() => ({
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
      et(
        q(e),
        s || r,
        u,
        i
      );
    }
  }));
}
function ht(e) {
  return Ce((t, n) => ({
    get() {
      return t(), e;
    },
    set(r) {
      !_e(e) && JSON.stringify(r) === JSON.stringify(e) || (e = r, n());
    }
  }));
}
function pe(e) {
  return typeof e == "function" ? e() : L(e);
}
typeof WorkerGlobalScope < "u" && globalThis instanceof WorkerGlobalScope;
const tt = () => {
};
function nt(e, t = !1, n = "Timeout") {
  return new Promise((r, o) => {
    setTimeout(t ? () => o(n) : r, e);
  });
}
function rt(e, t = !1) {
  function n(a, { flush: f = "sync", deep: h = !1, timeout: v, throwOnTimeout: p } = {}) {
    let g = null;
    const _ = [new Promise((b) => {
      g = G(
        e,
        (P) => {
          a(P) !== t && (g ? g() : Te(() => g == null ? void 0 : g()), b(P));
        },
        {
          flush: f,
          deep: h,
          immediate: !0
        }
      );
    })];
    return v != null && _.push(
      nt(v, p).then(() => pe(e)).finally(() => g == null ? void 0 : g())
    ), Promise.race(_);
  }
  function r(a, f) {
    if (!zt(a))
      return n((P) => P === a, f);
    const { flush: h = "sync", deep: v = !1, timeout: p, throwOnTimeout: g } = f ?? {};
    let y = null;
    const b = [new Promise((P) => {
      y = G(
        [e, a],
        ([j, x]) => {
          t !== (j === x) && (y ? y() : Te(() => y == null ? void 0 : y()), P(j));
        },
        {
          flush: h,
          deep: v,
          immediate: !0
        }
      );
    })];
    return p != null && b.push(
      nt(p, g).then(() => pe(e)).finally(() => (y == null || y(), pe(e)))
    ), Promise.race(b);
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
    return n((h) => {
      const v = Array.from(h);
      return v.includes(a) || v.includes(pe(a));
    }, f);
  }
  function d(a) {
    return c(1, a);
  }
  function c(a = 1, f) {
    let h = -1;
    return n(() => (h += 1, h >= a), f);
  }
  return Array.isArray(pe(e)) ? {
    toMatch: n,
    toContains: l,
    changed: d,
    changedTimes: c,
    get not() {
      return rt(e, !t);
    }
  } : {
    toMatch: n,
    toBe: r,
    toBeTruthy: o,
    toBeNull: s,
    toBeNaN: u,
    toBeUndefined: i,
    changed: d,
    changedTimes: c,
    get not() {
      return rt(e, !t);
    }
  };
}
function hr(e) {
  return rt(e);
}
function pr(e, t, n) {
  let r;
  zt(n) ? r = {
    evaluating: n
  } : r = n || {};
  const {
    lazy: o = !1,
    evaluating: s = void 0,
    shallow: i = !0,
    onError: u = tt
  } = r, l = Z(!o), d = i ? J(t) : Z(t);
  let c = 0;
  return Jt(async (a) => {
    if (!l.value)
      return;
    c++;
    const f = c;
    let h = !1;
    s && Promise.resolve().then(() => {
      s.value = !0;
    });
    try {
      const v = await e((p) => {
        a(() => {
          s && (s.value = !1), h || p();
        });
      });
      f === c && (d.value = v);
    } catch (v) {
      u(v);
    } finally {
      s && f === c && (s.value = !1), h = !0;
    }
  }), o ? K(() => (l.value = !0, d.value)) : d;
}
function mr(e, t, n) {
  const {
    immediate: r = !0,
    delay: o = 0,
    onError: s = tt,
    onSuccess: i = tt,
    resetOnExecute: u = !0,
    shallow: l = !0,
    throwError: d
  } = {}, c = l ? J(t) : Z(t), a = Z(!1), f = Z(!1), h = J(void 0);
  async function v(y = 0, ..._) {
    u && (c.value = t), h.value = void 0, a.value = !1, f.value = !0, y > 0 && await nt(y);
    const b = typeof e == "function" ? e(..._) : e;
    try {
      const P = await b;
      c.value = P, a.value = !0, i(P);
    } catch (P) {
      if (h.value = P, s(P), d)
        throw P;
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
    error: h,
    execute: v
  };
  function g() {
    return new Promise((y, _) => {
      hr(f).toBe(!1).then(() => y(p)).catch(_);
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
  const n = [...Object.keys(t), "__Vue"], r = [...Object.values(t), Hn];
  try {
    return new Function(...n, `return (${e})`)(...r);
  } catch (o) {
    throw new Error(o + " in function code: " + e);
  }
}
function gr(e) {
  if (e.startsWith(":")) {
    e = e.slice(1);
    try {
      return W(e);
    } catch (t) {
      throw new Error(t + " in function code: " + e);
    }
  }
}
function on(e) {
  return e.constructor.name === "AsyncFunction";
}
function vr(e, t) {
  const { deepCompare: n = !1 } = e;
  return n ? ht(e.value) : Z(e.value);
}
function yr(e, t, n) {
  const { bind: r = {}, code: o, const: s = [] } = e, i = Object.values(r).map((c, a) => s[a] === 1 ? c : t.getVueRefObjectOrValue(c));
  if (on(new Function(o)))
    return pr(
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
function wr(e, t, n) {
  const {
    inputs: r = [],
    code: o,
    slient: s,
    data: i,
    asyncInit: u = null,
    deepEqOnInput: l = 0
  } = e, d = s || Array(r.length).fill(0), c = i || Array(r.length).fill(0), a = r.filter((g, y) => d[y] === 0 && c[y] === 0).map((g) => t.getVueRefObject(g));
  function f() {
    return r.map(
      (g, y) => c[y] === 1 ? g : t.getObjectToValue(g)
    );
  }
  const h = W(o), v = l === 0 ? J(Ee) : ht(Ee), p = { immediate: !0, deep: !0 };
  return on(h) ? (v.value = u, G(
    a,
    async () => {
      f().some(_e) || (v.value = await h(...f()));
    },
    p
  )) : G(
    a,
    () => {
      const g = f();
      g.some(_e) || (v.value = h(...g));
    },
    p
  ), Jn(v);
}
function Er() {
  return [];
}
const Oe = Se(Er);
function sn(e, t) {
  var s, i, u, l, d;
  const n = Oe.getOrDefault(e.id), r = /* @__PURE__ */ new Map();
  n.push(r), t.replaceSnapshot({
    scopeSnapshot: an()
  });
  const o = (c, a) => {
    r.set(c.id, a);
  };
  return (s = e.refs) == null || s.forEach((c) => {
    o(c, vr(c));
  }), (i = e.web_computed) == null || i.forEach((c) => {
    const { init: a } = c, f = c.deepEqOnInput === void 0 ? J(a ?? Ee) : ht(a ?? Ee);
    o(c, f);
  }), (u = e.vue_computed) == null || u.forEach((c) => {
    o(
      c,
      yr(c, t)
    );
  }), (l = e.js_computed) == null || l.forEach((c) => {
    o(
      c,
      wr(c, t)
    );
  }), (d = e.data) == null || d.forEach((c) => {
    o(c, c.value);
  }), n.length - 1;
}
function an() {
  const e = /* @__PURE__ */ new Map();
  for (const [n, r] of Oe) {
    const o = r[r.length - 1];
    e.set(n, [o]);
  }
  function t(n) {
    return cn(n, e);
  }
  return {
    getVueRef: t
  };
}
function _r(e) {
  return cn(e, Oe);
}
function cn(e, t) {
  const n = t.get(e.sid);
  if (!n)
    throw new Error(`Scope ${e.sid} not found`);
  const o = n[n.length - 1].get(e.id);
  if (!o)
    throw new Error(`Var ${e.id} not found in scope ${e.sid}`);
  return o;
}
function Sr(e) {
  Oe.delete(e);
}
function un(e, t) {
  const n = Oe.get(e);
  n && n.splice(t, 1);
}
const pt = Se(() => []);
function br(e) {
  var r;
  const t = /* @__PURE__ */ new Map(), n = pt.getOrDefault(e.id).push(t);
  return (r = e.eRefs) == null || r.forEach((o) => {
    const s = J();
    t.set(o.id, s);
  }), n;
}
function Or(e, t) {
  const n = pt.get(e);
  n && n.splice(t, 1);
}
function ln() {
  const e = new Map(
    Array.from(pt.entries()).map(([n, r]) => [
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
  function d(a) {
    return a.type === "ele_ref";
  }
  e.isElementRef = d;
  function c(a) {
    return a.type !== void 0;
  }
  e.IsBinding = c;
})(N || (N = {}));
const Fe = Se(() => []);
function Rr(e) {
  const t = Fe.getOrDefault(e);
  return t.push(J({})), t.length - 1;
}
function Pr(e, t, n) {
  Fe.get(e)[t].value = n;
}
function kr(e) {
  Fe.delete(e);
}
function Vr() {
  const e = /* @__PURE__ */ new Map();
  for (const [n, r] of Fe) {
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
const fn = /* @__PURE__ */ new Map(), mt = Se(() => /* @__PURE__ */ new Map()), dn = /* @__PURE__ */ new Set(), hn = Symbol("vfor");
function Nr(e) {
  const t = pn() ?? {};
  Ie(hn, { ...t, [e.fid]: e.key });
}
function pn() {
  return ee(hn, void 0);
}
function Ir() {
  const e = pn(), t = /* @__PURE__ */ new Map();
  return e === void 0 || Object.keys(e).forEach((n) => {
    t.set(n, e[n]);
  }), t;
}
function Tr(e, t, n, r) {
  if (r) {
    dn.add(e);
    return;
  }
  let o;
  if (n)
    o = new Mr(t);
  else {
    const s = Array.isArray(t) ? t : Object.entries(t).map(([i, u], l) => [u, i, l]);
    o = new Dr(s);
  }
  fn.set(e, o);
}
function Ar(e, t, n) {
  const r = mt.getOrDefault(e);
  r.has(t) || r.set(t, Z(n)), r.get(t).value = n;
}
function $r(e) {
  const t = /* @__PURE__ */ new Set();
  function n(o) {
    t.add(o);
  }
  function r() {
    const o = mt.get(e);
    o !== void 0 && o.forEach((s, i) => {
      t.has(i) || o.delete(i);
    });
  }
  return {
    add: n,
    removeUnusedKeys: r
  };
}
function jr(e) {
  const t = e, n = Ir();
  function r(o) {
    const s = n.get(o) ?? t;
    return mt.get(o).get(s).value;
  }
  return {
    getVForIndex: r
  };
}
function Cr(e) {
  return fn.get(e.binding.fid).createRefObjectWithPaths(e);
}
function xr(e) {
  return dn.has(e);
}
class Dr {
  constructor(t) {
    this.array = t;
  }
  createRefObjectWithPaths(t) {
    const { binding: n } = t, { snapshot: r } = t, { path: o = [] } = n, s = [...o], i = r.getVForIndex(n.fid);
    return s.unshift(i), Ce(() => ({
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
class Mr {
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
    const { binding: n } = t, { path: r = [] } = n, o = [...r], { snapshot: s } = t, i = s.getVueRefObject(this.binding), u = this.isDictSource(i), l = s.getVForIndex(n.fid), d = u && o.length === 0 ? [0] : [];
    return o.unshift(l, ...d), Ce(() => ({
      get: () => {
        const c = q(i), a = u ? Object.entries(c).map(([f, h], v) => [
          h,
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
          const h = f[l];
          et(
            a,
            [h],
            c,
            s.getObjectToValue
          );
          return;
        }
        et(
          a,
          o,
          c,
          s.getObjectToValue
        );
      }
    }));
  }
}
function Pt(e) {
  return e == null;
}
function Fr() {
  return mn().__VUE_DEVTOOLS_GLOBAL_HOOK__;
}
function mn() {
  return typeof navigator < "u" && typeof window < "u" ? window : typeof globalThis < "u" ? globalThis : {};
}
const Br = typeof Proxy == "function", Lr = "devtools-plugin:setup", Wr = "plugin:settings:set";
let ie, ot;
function Ur() {
  var e;
  return ie !== void 0 || (typeof window < "u" && window.performance ? (ie = !0, ot = window.performance) : typeof globalThis < "u" && (!((e = globalThis.perf_hooks) === null || e === void 0) && e.performance) ? (ie = !0, ot = globalThis.perf_hooks.performance) : ie = !1), ie;
}
function Kr() {
  return Ur() ? ot.now() : Date.now();
}
class Gr {
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
        return Kr();
      }
    }, n && n.on(Wr, (i, u) => {
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
      }), this.fallbacks[u](...l)) : (...l) => new Promise((d) => {
        this.targetQueue.push({
          method: u,
          args: l,
          resolve: d
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
function qr(e, t) {
  const n = e, r = mn(), o = Fr(), s = Br && n.enableEarlyProxy;
  if (o && (r.__VUE_DEVTOOLS_PLUGIN_API_AVAILABLE__ || !s))
    o.emit(Lr, e, t);
  else {
    const i = s ? new Gr(n, o) : null;
    (r.__VUE_DEVTOOLS_PLUGINS__ = r.__VUE_DEVTOOLS_PLUGINS__ || []).push({
      pluginDescriptor: n,
      setupFn: t,
      proxy: i
    }), i && t(i.proxiedTarget);
  }
}
var O = {};
const z = typeof document < "u";
function gn(e) {
  return typeof e == "object" || "displayName" in e || "props" in e || "__vccOpts" in e;
}
function Hr(e) {
  return e.__esModule || e[Symbol.toStringTag] === "Module" || // support CF with dynamic imports that do not
  // add the Module string tag
  e.default && gn(e.default);
}
const I = Object.assign;
function ze(e, t) {
  const n = {};
  for (const r in t) {
    const o = t[r];
    n[r] = U(o) ? o.map(e) : e(o);
  }
  return n;
}
const ye = () => {
}, U = Array.isArray;
function R(e) {
  const t = Array.from(arguments).slice(1);
  console.warn.apply(console, ["[Vue Router warn]: " + e].concat(t));
}
const vn = /#/g, zr = /&/g, Jr = /\//g, Qr = /=/g, Yr = /\?/g, yn = /\+/g, Xr = /%5B/g, Zr = /%5D/g, wn = /%5E/g, eo = /%60/g, En = /%7B/g, to = /%7C/g, _n = /%7D/g, no = /%20/g;
function gt(e) {
  return encodeURI("" + e).replace(to, "|").replace(Xr, "[").replace(Zr, "]");
}
function ro(e) {
  return gt(e).replace(En, "{").replace(_n, "}").replace(wn, "^");
}
function st(e) {
  return gt(e).replace(yn, "%2B").replace(no, "+").replace(vn, "%23").replace(zr, "%26").replace(eo, "`").replace(En, "{").replace(_n, "}").replace(wn, "^");
}
function oo(e) {
  return st(e).replace(Qr, "%3D");
}
function so(e) {
  return gt(e).replace(vn, "%23").replace(Yr, "%3F");
}
function io(e) {
  return e == null ? "" : so(e).replace(Jr, "%2F");
}
function ae(e) {
  try {
    return decodeURIComponent("" + e);
  } catch {
    O.NODE_ENV !== "production" && R(`Error decoding "${e}". Using original value`);
  }
  return "" + e;
}
const ao = /\/$/, co = (e) => e.replace(ao, "");
function Je(e, t, n = "/") {
  let r, o = {}, s = "", i = "";
  const u = t.indexOf("#");
  let l = t.indexOf("?");
  return u < l && u >= 0 && (l = -1), l > -1 && (r = t.slice(0, l), s = t.slice(l + 1, u > -1 ? u : t.length), o = e(s)), u > -1 && (r = r || t.slice(0, u), i = t.slice(u, t.length)), r = fo(r ?? t, n), {
    fullPath: r + (s && "?") + s + i,
    path: r,
    query: o,
    hash: ae(i)
  };
}
function uo(e, t) {
  const n = t.query ? e(t.query) : "";
  return t.path + (n && "?") + n + (t.hash || "");
}
function kt(e, t) {
  return !t || !e.toLowerCase().startsWith(t.toLowerCase()) ? e : e.slice(t.length) || "/";
}
function Vt(e, t, n) {
  const r = t.matched.length - 1, o = n.matched.length - 1;
  return r > -1 && r === o && te(t.matched[r], n.matched[o]) && Sn(t.params, n.params) && e(t.query) === e(n.query) && t.hash === n.hash;
}
function te(e, t) {
  return (e.aliasOf || e) === (t.aliasOf || t);
}
function Sn(e, t) {
  if (Object.keys(e).length !== Object.keys(t).length)
    return !1;
  for (const n in e)
    if (!lo(e[n], t[n]))
      return !1;
  return !0;
}
function lo(e, t) {
  return U(e) ? Nt(e, t) : U(t) ? Nt(t, e) : e === t;
}
function Nt(e, t) {
  return U(t) ? e.length === t.length && e.every((n, r) => n === t[r]) : e.length === 1 && e[0] === t;
}
function fo(e, t) {
  if (e.startsWith("/"))
    return e;
  if (O.NODE_ENV !== "production" && !t.startsWith("/"))
    return R(`Cannot resolve a relative location without an absolute path. Trying to resolve "${e}" from "${t}". It should look like "/${t}".`), e;
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
const Qe = "";
function bn(e) {
  if (!e)
    if (z) {
      const t = document.querySelector("base");
      e = t && t.getAttribute("href") || "/", e = e.replace(/^\w+:\/\/[^\/]+/, "");
    } else
      e = "/";
  return e[0] !== "/" && e[0] !== "#" && (e = "/" + e), co(e);
}
const ho = /^[^#]+#/;
function On(e, t) {
  return e.replace(ho, "#") + t;
}
function po(e, t) {
  const n = document.documentElement.getBoundingClientRect(), r = e.getBoundingClientRect();
  return {
    behavior: t.behavior,
    left: r.left - n.left - (t.left || 0),
    top: r.top - n.top - (t.top || 0)
  };
}
const Be = () => ({
  left: window.scrollX,
  top: window.scrollY
});
function mo(e) {
  let t;
  if ("el" in e) {
    const n = e.el, r = typeof n == "string" && n.startsWith("#");
    if (O.NODE_ENV !== "production" && typeof e.el == "string" && (!r || !document.getElementById(e.el.slice(1))))
      try {
        const s = document.querySelector(e.el);
        if (r && s) {
          R(`The selector "${e.el}" should be passed as "el: document.querySelector('${e.el}')" because it starts with "#".`);
          return;
        }
      } catch {
        R(`The selector "${e.el}" is invalid. If you are using an id selector, make sure to escape it. You can find more information about escaping characters in selectors at https://mathiasbynens.be/notes/css-escapes or use CSS.escape (https://developer.mozilla.org/en-US/docs/Web/API/CSS/escape).`);
        return;
      }
    const o = typeof n == "string" ? r ? document.getElementById(n.slice(1)) : document.querySelector(n) : n;
    if (!o) {
      O.NODE_ENV !== "production" && R(`Couldn't find element using selector "${e.el}" returned by scrollBehavior.`);
      return;
    }
    t = po(o, e);
  } else
    t = e;
  "scrollBehavior" in document.documentElement.style ? window.scrollTo(t) : window.scrollTo(t.left != null ? t.left : window.scrollX, t.top != null ? t.top : window.scrollY);
}
function It(e, t) {
  return (history.state ? history.state.position - t : -1) + e;
}
const it = /* @__PURE__ */ new Map();
function go(e, t) {
  it.set(e, t);
}
function vo(e) {
  const t = it.get(e);
  return it.delete(e), t;
}
let yo = () => location.protocol + "//" + location.host;
function Rn(e, t) {
  const { pathname: n, search: r, hash: o } = t, s = e.indexOf("#");
  if (s > -1) {
    let u = o.includes(e.slice(s)) ? e.slice(s).length : 1, l = o.slice(u);
    return l[0] !== "/" && (l = "/" + l), kt(l, "");
  }
  return kt(n, e) + r + o;
}
function wo(e, t, n, r) {
  let o = [], s = [], i = null;
  const u = ({ state: f }) => {
    const h = Rn(e, location), v = n.value, p = t.value;
    let g = 0;
    if (f) {
      if (n.value = h, t.value = f, i && i === v) {
        i = null;
        return;
      }
      g = p ? f.position - p.position : 0;
    } else
      r(h);
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
  function d(f) {
    o.push(f);
    const h = () => {
      const v = o.indexOf(f);
      v > -1 && o.splice(v, 1);
    };
    return s.push(h), h;
  }
  function c() {
    const { history: f } = window;
    f.state && f.replaceState(I({}, f.state, { scroll: Be() }), "");
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
    listen: d,
    destroy: a
  };
}
function Tt(e, t, n, r = !1, o = !1) {
  return {
    back: e,
    current: t,
    forward: n,
    replaced: r,
    position: window.history.length,
    scroll: o ? Be() : null
  };
}
function Eo(e) {
  const { history: t, location: n } = window, r = {
    value: Rn(e, n)
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
  function s(l, d, c) {
    const a = e.indexOf("#"), f = a > -1 ? (n.host && document.querySelector("base") ? e : e.slice(a)) + l : yo() + e + l;
    try {
      t[c ? "replaceState" : "pushState"](d, "", f), o.value = d;
    } catch (h) {
      O.NODE_ENV !== "production" ? R("Error with push/replace State", h) : console.error(h), n[c ? "replace" : "assign"](f);
    }
  }
  function i(l, d) {
    const c = I({}, t.state, Tt(
      o.value.back,
      // keep back and forward entries but override current position
      l,
      o.value.forward,
      !0
    ), d, { position: o.value.position });
    s(l, c, !0), r.value = l;
  }
  function u(l, d) {
    const c = I(
      {},
      // use current history state to gracefully handle a wrong call to
      // history.replaceState
      // https://github.com/vuejs/router/issues/366
      o.value,
      t.state,
      {
        forward: l,
        scroll: Be()
      }
    );
    O.NODE_ENV !== "production" && !t.state && R(`history.state seems to have been manually replaced without preserving the necessary values. Make sure to preserve existing history state if you are manually calling history.replaceState:

history.replaceState(history.state, '', url)

You can find more information at https://router.vuejs.org/guide/migration/#Usage-of-history-state`), s(c.current, c, !0);
    const a = I({}, Tt(r.value, l, null), { position: c.position + 1 }, d);
    s(l, a, !1), r.value = l;
  }
  return {
    location: r,
    state: o,
    push: u,
    replace: i
  };
}
function Pn(e) {
  e = bn(e);
  const t = Eo(e), n = wo(e, t.state, t.location, t.replace);
  function r(s, i = !0) {
    i || n.pauseListeners(), history.go(s);
  }
  const o = I({
    // it's overridden right after
    location: "",
    base: e,
    go: r,
    createHref: On.bind(null, e)
  }, t, n);
  return Object.defineProperty(o, "location", {
    enumerable: !0,
    get: () => t.location.value
  }), Object.defineProperty(o, "state", {
    enumerable: !0,
    get: () => t.state.value
  }), o;
}
function _o(e = "") {
  let t = [], n = [Qe], r = 0;
  e = bn(e);
  function o(u) {
    r++, r !== n.length && n.splice(r), n.push(u);
  }
  function s(u, l, { direction: d, delta: c }) {
    const a = {
      direction: d,
      delta: c,
      type: ce.pop
    };
    for (const f of t)
      f(u, l, a);
  }
  const i = {
    // rewritten by Object.defineProperty
    location: Qe,
    // TODO: should be kept in queue
    state: {},
    base: e,
    createHref: On.bind(null, e),
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
      t = [], n = [Qe], r = 0;
    },
    go(u, l = !0) {
      const d = this.location, c = (
        // we are considering delta === 0 going forward, but in abstract mode
        // using 0 for the delta doesn't make sense like it does in html5 where
        // it reloads the page
        u < 0 ? oe.back : oe.forward
      );
      r = Math.max(0, Math.min(r + u, n.length - 1)), l && s(this.location, d, {
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
function So(e) {
  return e = location.host ? e || location.pathname + location.search : "", e.includes("#") || (e += "#"), O.NODE_ENV !== "production" && !e.endsWith("#/") && !e.endsWith("#") && R(`A hash base must end with a "#":
"${e}" should be "${e.replace(/#.*$/, "#")}".`), Pn(e);
}
function Ae(e) {
  return typeof e == "string" || e && typeof e == "object";
}
function kn(e) {
  return typeof e == "string" || typeof e == "symbol";
}
const at = Symbol(O.NODE_ENV !== "production" ? "navigation failure" : "");
var At;
(function(e) {
  e[e.aborted = 4] = "aborted", e[e.cancelled = 8] = "cancelled", e[e.duplicated = 16] = "duplicated";
})(At || (At = {}));
const bo = {
  1({ location: e, currentLocation: t }) {
    return `No match for
 ${JSON.stringify(e)}${t ? `
while being at
` + JSON.stringify(t) : ""}`;
  },
  2({ from: e, to: t }) {
    return `Redirected from "${e.fullPath}" to "${Ro(t)}" via a navigation guard.`;
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
  return O.NODE_ENV !== "production" ? I(new Error(bo[e](t)), {
    type: e,
    [at]: !0
  }, t) : I(new Error(), {
    type: e,
    [at]: !0
  }, t);
}
function H(e, t) {
  return e instanceof Error && at in e && (t == null || !!(e.type & t));
}
const Oo = ["params", "query", "hash"];
function Ro(e) {
  if (typeof e == "string")
    return e;
  if (e.path != null)
    return e.path;
  const t = {};
  for (const n of Oo)
    n in e && (t[n] = e[n]);
  return JSON.stringify(t, null, 2);
}
const $t = "[^/]+?", Po = {
  sensitive: !1,
  strict: !1,
  start: !0,
  end: !0
}, ko = /[.+*?^${}()[\]/\\]/g;
function Vo(e, t) {
  const n = I({}, Po, t), r = [];
  let o = n.start ? "^" : "";
  const s = [];
  for (const d of e) {
    const c = d.length ? [] : [
      90
      /* PathScore.Root */
    ];
    n.strict && !d.length && (o += "/");
    for (let a = 0; a < d.length; a++) {
      const f = d[a];
      let h = 40 + (n.sensitive ? 0.25 : 0);
      if (f.type === 0)
        a || (o += "/"), o += f.value.replace(ko, "\\$&"), h += 40;
      else if (f.type === 1) {
        const { value: v, repeatable: p, optional: g, regexp: y } = f;
        s.push({
          name: v,
          repeatable: p,
          optional: g
        });
        const _ = y || $t;
        if (_ !== $t) {
          h += 10;
          try {
            new RegExp(`(${_})`);
          } catch (P) {
            throw new Error(`Invalid custom RegExp for param "${v}" (${_}): ` + P.message);
          }
        }
        let b = p ? `((?:${_})(?:/(?:${_}))*)` : `(${_})`;
        a || (b = // avoid an optional / if there are more segments e.g. /:p?-static
        // or /:p?-:p2
        g && d.length < 2 ? `(?:/${b})` : "/" + b), g && (b += "?"), o += b, h += 20, g && (h += -8), p && (h += -20), _ === ".*" && (h += -50);
      }
      c.push(h);
    }
    r.push(c);
  }
  if (n.strict && n.end) {
    const d = r.length - 1;
    r[d][r[d].length - 1] += 0.7000000000000001;
  }
  n.strict || (o += "/?"), n.end ? o += "$" : n.strict && !o.endsWith("/") && (o += "(?:/|$)");
  const i = new RegExp(o, n.sensitive ? "" : "i");
  function u(d) {
    const c = d.match(i), a = {};
    if (!c)
      return null;
    for (let f = 1; f < c.length; f++) {
      const h = c[f] || "", v = s[f - 1];
      a[v.name] = h && v.repeatable ? h.split("/") : h;
    }
    return a;
  }
  function l(d) {
    let c = "", a = !1;
    for (const f of e) {
      (!a || !c.endsWith("/")) && (c += "/"), a = !1;
      for (const h of f)
        if (h.type === 0)
          c += h.value;
        else if (h.type === 1) {
          const { value: v, repeatable: p, optional: g } = h, y = v in d ? d[v] : "";
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
function No(e, t) {
  let n = 0;
  for (; n < e.length && n < t.length; ) {
    const r = t[n] - e[n];
    if (r)
      return r;
    n++;
  }
  return e.length < t.length ? e.length === 1 && e[0] === 80 ? -1 : 1 : e.length > t.length ? t.length === 1 && t[0] === 80 ? 1 : -1 : 0;
}
function Vn(e, t) {
  let n = 0;
  const r = e.score, o = t.score;
  for (; n < r.length && n < o.length; ) {
    const s = No(r[n], o[n]);
    if (s)
      return s;
    n++;
  }
  if (Math.abs(o.length - r.length) === 1) {
    if (jt(r))
      return 1;
    if (jt(o))
      return -1;
  }
  return o.length - r.length;
}
function jt(e) {
  const t = e[e.length - 1];
  return e.length > 0 && t[t.length - 1] < 0;
}
const Io = {
  type: 0,
  value: ""
}, To = /[a-zA-Z0-9_]/;
function Ao(e) {
  if (!e)
    return [[]];
  if (e === "/")
    return [[Io]];
  if (!e.startsWith("/"))
    throw new Error(O.NODE_ENV !== "production" ? `Route paths should start with a "/": "${e}" should be "/${e}".` : `Invalid path "${e}"`);
  function t(h) {
    throw new Error(`ERR (${n})/"${d}": ${h}`);
  }
  let n = 0, r = n;
  const o = [];
  let s;
  function i() {
    s && o.push(s), s = [];
  }
  let u = 0, l, d = "", c = "";
  function a() {
    d && (n === 0 ? s.push({
      type: 0,
      value: d
    }) : n === 1 || n === 2 || n === 3 ? (s.length > 1 && (l === "*" || l === "+") && t(`A repeatable param (${d}) must be alone in its segment. eg: '/:ids+.`), s.push({
      type: 1,
      value: d,
      regexp: c,
      repeatable: l === "*" || l === "+",
      optional: l === "*" || l === "?"
    })) : t("Invalid state to consume buffer"), d = "");
  }
  function f() {
    d += l;
  }
  for (; u < e.length; ) {
    if (l = e[u++], l === "\\" && n !== 2) {
      r = n, n = 4;
      continue;
    }
    switch (n) {
      case 0:
        l === "/" ? (d && a(), i()) : l === ":" ? (a(), n = 1) : f();
        break;
      case 4:
        f(), n = r;
        break;
      case 1:
        l === "(" ? n = 2 : To.test(l) ? f() : (a(), n = 0, l !== "*" && l !== "?" && l !== "+" && u--);
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
  return n === 2 && t(`Unfinished custom RegExp for param "${d}"`), a(), i(), o;
}
function $o(e, t, n) {
  const r = Vo(Ao(e.path), n);
  if (O.NODE_ENV !== "production") {
    const s = /* @__PURE__ */ new Set();
    for (const i of r.keys)
      s.has(i.name) && R(`Found duplicated params with name "${i.name}" for path "${e.path}". Only the last one will be available on "$route.params".`), s.add(i.name);
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
function jo(e, t) {
  const n = [], r = /* @__PURE__ */ new Map();
  t = Mt({ strict: !1, end: !0, sensitive: !1 }, t);
  function o(a) {
    return r.get(a);
  }
  function s(a, f, h) {
    const v = !h, p = xt(a);
    O.NODE_ENV !== "production" && Mo(p, f), p.aliasOf = h && h.record;
    const g = Mt(t, a), y = [p];
    if ("alias" in a) {
      const P = typeof a.alias == "string" ? [a.alias] : a.alias;
      for (const j of P)
        y.push(
          // we need to normalize again to ensure the `mods` property
          // being non enumerable
          xt(I({}, p, {
            // this allows us to hold a copy of the `components` option
            // so that async components cache is hold on the original record
            components: h ? h.record.components : p.components,
            path: j,
            // we might be the child of an alias
            aliasOf: h ? h.record : p
            // the aliases are always of the same kind as the original since they
            // are defined on the same record
          }))
        );
    }
    let _, b;
    for (const P of y) {
      const { path: j } = P;
      if (f && j[0] !== "/") {
        const x = f.record.path, D = x[x.length - 1] === "/" ? "" : "/";
        P.path = f.record.path + (j && D + j);
      }
      if (O.NODE_ENV !== "production" && P.path === "*")
        throw new Error(`Catch all routes ("*") must now be defined using a param with a custom regexp.
See more at https://router.vuejs.org/guide/migration/#Removed-star-or-catch-all-routes.`);
      if (_ = $o(P, f, g), O.NODE_ENV !== "production" && f && j[0] === "/" && Bo(_, f), h ? (h.alias.push(_), O.NODE_ENV !== "production" && Do(h, _)) : (b = b || _, b !== _ && b.alias.push(_), v && a.name && !Dt(_) && (O.NODE_ENV !== "production" && Fo(a, f), i(a.name))), Nn(_) && l(_), p.children) {
        const x = p.children;
        for (let D = 0; D < x.length; D++)
          s(x[D], _, h && h.children[D]);
      }
      h = h || _;
    }
    return b ? () => {
      i(b);
    } : ye;
  }
  function i(a) {
    if (kn(a)) {
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
    const f = Lo(a, n);
    n.splice(f, 0, a), a.record.name && !Dt(a) && r.set(a.record.name, a);
  }
  function d(a, f) {
    let h, v = {}, p, g;
    if ("name" in a && a.name) {
      if (h = r.get(a.name), !h)
        throw ue(1, {
          location: a
        });
      if (O.NODE_ENV !== "production") {
        const b = Object.keys(a.params || {}).filter((P) => !h.keys.find((j) => j.name === P));
        b.length && R(`Discarded invalid param(s) "${b.join('", "')}" when navigating. See https://github.com/vuejs/router/blob/main/packages/router/CHANGELOG.md#414-2022-08-22 for more details.`);
      }
      g = h.record.name, v = I(
        // paramsFromLocation is a new object
        Ct(
          f.params,
          // only keep params that exist in the resolved location
          // only keep optional params coming from a parent record
          h.keys.filter((b) => !b.optional).concat(h.parent ? h.parent.keys.filter((b) => b.optional) : []).map((b) => b.name)
        ),
        // discard any existing params in the current location that do not exist here
        // #1497 this ensures better active/exact matching
        a.params && Ct(a.params, h.keys.map((b) => b.name))
      ), p = h.stringify(v);
    } else if (a.path != null)
      p = a.path, O.NODE_ENV !== "production" && !p.startsWith("/") && R(`The Matcher cannot resolve relative paths but received "${p}". Unless you directly called \`matcher.resolve("${p}")\`, this is probably a bug in vue-router. Please open an issue at https://github.com/vuejs/router/issues/new/choose.`), h = n.find((b) => b.re.test(p)), h && (v = h.parse(p), g = h.record.name);
    else {
      if (h = f.name ? r.get(f.name) : n.find((b) => b.re.test(f.path)), !h)
        throw ue(1, {
          location: a,
          currentLocation: f
        });
      g = h.record.name, v = I({}, f.params, a.params), p = h.stringify(v);
    }
    const y = [];
    let _ = h;
    for (; _; )
      y.unshift(_.record), _ = _.parent;
    return {
      name: g,
      path: p,
      params: v,
      matched: y,
      meta: xo(y)
    };
  }
  e.forEach((a) => s(a));
  function c() {
    n.length = 0, r.clear();
  }
  return {
    addRoute: s,
    resolve: d,
    removeRoute: i,
    clearRoutes: c,
    getRoutes: u,
    getRecordMatcher: o
  };
}
function Ct(e, t) {
  const n = {};
  for (const r of t)
    r in e && (n[r] = e[r]);
  return n;
}
function xt(e) {
  const t = {
    path: e.path,
    redirect: e.redirect,
    name: e.name,
    meta: e.meta || {},
    aliasOf: e.aliasOf,
    beforeEnter: e.beforeEnter,
    props: Co(e),
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
function Co(e) {
  const t = {}, n = e.props || !1;
  if ("component" in e)
    t.default = n;
  else
    for (const r in e.components)
      t[r] = typeof n == "object" ? n[r] : n;
  return t;
}
function Dt(e) {
  for (; e; ) {
    if (e.record.aliasOf)
      return !0;
    e = e.parent;
  }
  return !1;
}
function xo(e) {
  return e.reduce((t, n) => I(t, n.meta), {});
}
function Mt(e, t) {
  const n = {};
  for (const r in e)
    n[r] = r in t ? t[r] : e[r];
  return n;
}
function ct(e, t) {
  return e.name === t.name && e.optional === t.optional && e.repeatable === t.repeatable;
}
function Do(e, t) {
  for (const n of e.keys)
    if (!n.optional && !t.keys.find(ct.bind(null, n)))
      return R(`Alias "${t.record.path}" and the original record: "${e.record.path}" must have the exact same param named "${n.name}"`);
  for (const n of t.keys)
    if (!n.optional && !e.keys.find(ct.bind(null, n)))
      return R(`Alias "${t.record.path}" and the original record: "${e.record.path}" must have the exact same param named "${n.name}"`);
}
function Mo(e, t) {
  t && t.record.name && !e.name && !e.path && R(`The route named "${String(t.record.name)}" has a child without a name and an empty path. Using that name won't render the empty path child so you probably want to move the name to the child instead. If this is intentional, add a name to the child route to remove the warning.`);
}
function Fo(e, t) {
  for (let n = t; n; n = n.parent)
    if (n.record.name === e.name)
      throw new Error(`A route named "${String(e.name)}" has been added as a ${t === n ? "child" : "descendant"} of a route with the same name. Route names must be unique and a nested route cannot use the same name as an ancestor.`);
}
function Bo(e, t) {
  for (const n of t.keys)
    if (!e.keys.find(ct.bind(null, n)))
      return R(`Absolute path "${e.record.path}" must have the exact same param named "${n.name}" as its parent "${t.record.path}".`);
}
function Lo(e, t) {
  let n = 0, r = t.length;
  for (; n !== r; ) {
    const s = n + r >> 1;
    Vn(e, t[s]) < 0 ? r = s : n = s + 1;
  }
  const o = Wo(e);
  return o && (r = t.lastIndexOf(o, r - 1), O.NODE_ENV !== "production" && r < 0 && R(`Finding ancestor route "${o.record.path}" failed for "${e.record.path}"`)), r;
}
function Wo(e) {
  let t = e;
  for (; t = t.parent; )
    if (Nn(t) && Vn(e, t) === 0)
      return t;
}
function Nn({ record: e }) {
  return !!(e.name || e.components && Object.keys(e.components).length || e.redirect);
}
function Uo(e) {
  const t = {};
  if (e === "" || e === "?")
    return t;
  const r = (e[0] === "?" ? e.slice(1) : e).split("&");
  for (let o = 0; o < r.length; ++o) {
    const s = r[o].replace(yn, " "), i = s.indexOf("="), u = ae(i < 0 ? s : s.slice(0, i)), l = i < 0 ? null : ae(s.slice(i + 1));
    if (u in t) {
      let d = t[u];
      U(d) || (d = t[u] = [d]), d.push(l);
    } else
      t[u] = l;
  }
  return t;
}
function Ft(e) {
  let t = "";
  for (let n in e) {
    const r = e[n];
    if (n = oo(n), r == null) {
      r !== void 0 && (t += (t.length ? "&" : "") + n);
      continue;
    }
    (U(r) ? r.map((s) => s && st(s)) : [r && st(r)]).forEach((s) => {
      s !== void 0 && (t += (t.length ? "&" : "") + n, s != null && (t += "=" + s));
    });
  }
  return t;
}
function Ko(e) {
  const t = {};
  for (const n in e) {
    const r = e[n];
    r !== void 0 && (t[n] = U(r) ? r.map((o) => o == null ? null : "" + o) : r == null ? r : "" + r);
  }
  return t;
}
const Go = Symbol(O.NODE_ENV !== "production" ? "router view location matched" : ""), Bt = Symbol(O.NODE_ENV !== "production" ? "router view depth" : ""), Le = Symbol(O.NODE_ENV !== "production" ? "router" : ""), vt = Symbol(O.NODE_ENV !== "production" ? "route location" : ""), ut = Symbol(O.NODE_ENV !== "production" ? "router view location" : "");
function me() {
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
    const d = (f) => {
      f === !1 ? l(ue(4, {
        from: n,
        to: t
      })) : f instanceof Error ? l(f) : Ae(f) ? l(ue(2, {
        from: t,
        to: f
      })) : (i && // since enterCallbackArray is truthy, both record and name also are
      r.enterCallbacks[o] === i && typeof f == "function" && i.push(f), u());
    }, c = s(() => e.call(r && r.instances[o], t, n, O.NODE_ENV !== "production" ? qo(d, t, n) : d));
    let a = Promise.resolve(c);
    if (e.length < 3 && (a = a.then(d)), O.NODE_ENV !== "production" && e.length > 2) {
      const f = `The "next" callback was never called inside of ${e.name ? '"' + e.name + '"' : ""}:
${e.toString()}
. If you are returning a value instead of calling "next", make sure to remove the "next" parameter from your function.`;
      if (typeof c == "object" && "then" in c)
        a = a.then((h) => d._called ? h : (R(f), Promise.reject(new Error("Invalid navigation guard"))));
      else if (c !== void 0 && !d._called) {
        R(f), l(new Error("Invalid navigation guard"));
        return;
      }
    }
    a.catch((f) => l(f));
  });
}
function qo(e, t, n) {
  let r = 0;
  return function() {
    r++ === 1 && R(`The "next" callback was called more than once in one navigation guard when going from "${n.fullPath}" to "${t.fullPath}". It should be called exactly one time in each navigation guard. This will fail in production.`), e._called = !0, r === 1 && e.apply(null, arguments);
  };
}
function Ye(e, t, n, r, o = (s) => s()) {
  const s = [];
  for (const i of e) {
    O.NODE_ENV !== "production" && !i.components && !i.children.length && R(`Record with path "${i.path}" is either missing a "component(s)" or "children" property.`);
    for (const u in i.components) {
      let l = i.components[u];
      if (O.NODE_ENV !== "production") {
        if (!l || typeof l != "object" && typeof l != "function")
          throw R(`Component "${u}" in record with path "${i.path}" is not a valid component. Received "${String(l)}".`), new Error("Invalid route component");
        if ("then" in l) {
          R(`Component "${u}" in record with path "${i.path}" is a Promise instead of a function that returns a Promise. Did you write "import('./MyPage.vue')" instead of "() => import('./MyPage.vue')" ? This will break in production if not fixed.`);
          const d = l;
          l = () => d;
        } else l.__asyncLoader && // warn only once per component
        !l.__warnedDefineAsync && (l.__warnedDefineAsync = !0, R(`Component "${u}" in record with path "${i.path}" is defined using "defineAsyncComponent()". Write "() => import('./MyPage.vue')" instead of "defineAsyncComponent(() => import('./MyPage.vue'))".`));
      }
      if (!(t !== "beforeRouteEnter" && !i.instances[u]))
        if (gn(l)) {
          const c = (l.__vccOpts || l)[t];
          c && s.push(X(c, n, r, i, u, o));
        } else {
          let d = l();
          O.NODE_ENV !== "production" && !("catch" in d) && (R(`Component "${u}" in record with path "${i.path}" is a function that does not return a Promise. If you were passing a functional component, make sure to add a "displayName" to the component. This will break in production if not fixed.`), d = Promise.resolve(d)), s.push(() => d.then((c) => {
            if (!c)
              throw new Error(`Couldn't resolve component "${u}" at "${i.path}"`);
            const a = Hr(c) ? c.default : c;
            i.mods[u] = c, i.components[u] = a;
            const h = (a.__vccOpts || a)[t];
            return h && X(h, n, r, i, u, o)();
          }));
        }
    }
  }
  return s;
}
function Lt(e) {
  const t = ee(Le), n = ee(vt);
  let r = !1, o = null;
  const s = K(() => {
    const c = L(e.to);
    return O.NODE_ENV !== "production" && (!r || c !== o) && (Ae(c) || (r ? R(`Invalid value for prop "to" in useLink()
- to:`, c, `
- previous to:`, o, `
- props:`, e) : R(`Invalid value for prop "to" in useLink()
- to:`, c, `
- props:`, e)), o = c, r = !0), t.resolve(c);
  }), i = K(() => {
    const { matched: c } = s.value, { length: a } = c, f = c[a - 1], h = n.matched;
    if (!f || !h.length)
      return -1;
    const v = h.findIndex(te.bind(null, f));
    if (v > -1)
      return v;
    const p = Wt(c[a - 2]);
    return (
      // we are dealing with nested routes
      a > 1 && // if the parent and matched route have the same path, this link is
      // referring to the empty child. Or we currently are on a different
      // child of the same parent
      Wt(f) === p && // avoid comparing the child with its parent
      h[h.length - 1].path !== p ? h.findIndex(te.bind(null, c[a - 2])) : v
    );
  }), u = K(() => i.value > -1 && Yo(n.params, s.value.params)), l = K(() => i.value > -1 && i.value === n.matched.length - 1 && Sn(n.params, s.value.params));
  function d(c = {}) {
    if (Qo(c)) {
      const a = t[L(e.replace) ? "replace" : "push"](
        L(e.to)
        // avoid uncaught errors are they are logged anyway
      ).catch(ye);
      return e.viewTransition && typeof document < "u" && "startViewTransition" in document && document.startViewTransition(() => a), a;
    }
    return Promise.resolve();
  }
  if (O.NODE_ENV !== "production" && z) {
    const c = Qt();
    if (c) {
      const a = {
        route: s.value,
        isActive: u.value,
        isExactActive: l.value,
        error: null
      };
      c.__vrl_devtools = c.__vrl_devtools || [], c.__vrl_devtools.push(a), Jt(() => {
        a.route = s.value, a.isActive = u.value, a.isExactActive = l.value, a.error = Ae(L(e.to)) ? null : 'Invalid "to" value';
      }, { flush: "post" });
    }
  }
  return {
    route: s,
    href: K(() => s.value.href),
    isActive: u,
    isExactActive: l,
    navigate: d
  };
}
function Ho(e) {
  return e.length === 1 ? e[0] : e;
}
const zo = /* @__PURE__ */ F({
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
  useLink: Lt,
  setup(e, { slots: t }) {
    const n = Yn(Lt(e)), { options: r } = ee(Le), o = K(() => ({
      [Ut(e.activeClass, r.linkActiveClass, "router-link-active")]: n.isActive,
      // [getLinkClass(
      //   props.inactiveClass,
      //   options.linkInactiveClass,
      //   'router-link-inactive'
      // )]: !link.isExactActive,
      [Ut(e.exactActiveClass, r.linkExactActiveClass, "router-link-exact-active")]: n.isExactActive
    }));
    return () => {
      const s = t.default && Ho(t.default(n));
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
}), Jo = zo;
function Qo(e) {
  if (!(e.metaKey || e.altKey || e.ctrlKey || e.shiftKey) && !e.defaultPrevented && !(e.button !== void 0 && e.button !== 0)) {
    if (e.currentTarget && e.currentTarget.getAttribute) {
      const t = e.currentTarget.getAttribute("target");
      if (/\b_blank\b/i.test(t))
        return;
    }
    return e.preventDefault && e.preventDefault(), !0;
  }
}
function Yo(e, t) {
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
function Wt(e) {
  return e ? e.aliasOf ? e.aliasOf.path : e.path : "";
}
const Ut = (e, t, n) => e ?? t ?? n, Xo = /* @__PURE__ */ F({
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
    O.NODE_ENV !== "production" && es();
    const r = ee(ut), o = K(() => e.route || r.value), s = ee(Bt, 0), i = K(() => {
      let d = L(s);
      const { matched: c } = o.value;
      let a;
      for (; (a = c[d]) && !a.components; )
        d++;
      return d;
    }), u = K(() => o.value.matched[i.value]);
    Ie(Bt, K(() => i.value + 1)), Ie(Go, u), Ie(ut, o);
    const l = Z();
    return G(() => [l.value, u.value, e.name], ([d, c, a], [f, h, v]) => {
      c && (c.instances[a] = d, h && h !== c && d && d === f && (c.leaveGuards.size || (c.leaveGuards = h.leaveGuards), c.updateGuards.size || (c.updateGuards = h.updateGuards))), d && c && // if there is no instance but to and from are the same this might be
      // the first visit
      (!h || !te(c, h) || !f) && (c.enterCallbacks[a] || []).forEach((p) => p(d));
    }, { flush: "post" }), () => {
      const d = o.value, c = e.name, a = u.value, f = a && a.components[c];
      if (!f)
        return Kt(n.default, { Component: f, route: d });
      const h = a.props[c], v = h ? h === !0 ? d.params : typeof h == "function" ? h(d) : h : null, g = A(f, I({}, v, t, {
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
        (U(g.ref) ? g.ref.map((b) => b.i) : [g.ref.i]).forEach((b) => {
          b.__vrv_devtools = y;
        });
      }
      return (
        // pass the vnode to the slot as a prop.
        // h and <component :is="..."> both accept vnodes
        Kt(n.default, { Component: g, route: d }) || g
      );
    };
  }
});
function Kt(e, t) {
  if (!e)
    return null;
  const n = e(t);
  return n.length === 1 ? n[0] : n;
}
const Zo = Xo;
function es() {
  const e = Qt(), t = e.parent && e.parent.type.name, n = e.parent && e.parent.subTree && e.parent.subTree.type;
  if (t && (t === "KeepAlive" || t.includes("Transition")) && typeof n == "object" && n.name === "RouterView") {
    const r = t === "KeepAlive" ? "keep-alive" : "transition";
    R(`<router-view> can no longer be used directly inside <transition> or <keep-alive>.
Use slot props instead:

<router-view v-slot="{ Component }">
  <${r}>
    <component :is="Component" />
  </${r}>
</router-view>`);
  }
}
function ge(e, t) {
  const n = I({}, e, {
    // remove variables that can contain vue instances
    matched: e.matched.map((r) => fs(r, ["instances", "children", "aliasOf"]))
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
function Ne(e) {
  return {
    _custom: {
      display: e
    }
  };
}
let ts = 0;
function ns(e, t, n) {
  if (t.__hasDevtools)
    return;
  t.__hasDevtools = !0;
  const r = ts++;
  qr({
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
        value: ge(t.currentRoute.value, "Current Route")
      });
    }), o.on.visitComponentTree(({ treeNode: c, componentInstance: a }) => {
      if (a.__vrv_devtools) {
        const f = a.__vrv_devtools;
        c.tags.push({
          label: (f.name ? `${f.name.toString()}: ` : "") + f.path,
          textColor: 0,
          tooltip: "This component is rendered by &lt;router-view&gt;",
          backgroundColor: In
        });
      }
      U(a.__vrl_devtools) && (a.__devtoolsApi = o, a.__vrl_devtools.forEach((f) => {
        let h = f.route.path, v = $n, p = "", g = 0;
        f.error ? (h = f.error, v = as, g = cs) : f.isExactActive ? (v = An, p = "This is exactly active") : f.isActive && (v = Tn, p = "This link is active"), c.tags.push({
          label: h,
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
        guard: Ne("beforeEach"),
        from: ge(a, "Current Location during this navigation"),
        to: ge(c, "Target location")
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
      const h = {
        guard: Ne("afterEach")
      };
      f ? (h.failure = {
        _custom: {
          type: Error,
          readOnly: !0,
          display: f ? f.message : "",
          tooltip: "Navigation Failure",
          value: f
        }
      }, h.status = Ne("❌")) : h.status = Ne("✅"), h.from = ge(a, "Current Location during this navigation"), h.to = ge(c, "Target location"), o.addTimelineEvent({
        layerId: s,
        event: {
          title: "End of navigation",
          subtitle: c.fullPath,
          time: o.now(),
          data: h,
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
      if (!d)
        return;
      const c = d;
      let a = n.getRoutes().filter((f) => !f.parent || // these routes have a parent with no component which will not appear in the view
      // therefore we still need to include them
      !f.parent.record.components);
      a.forEach(xn), c.filter && (a = a.filter((f) => (
        // save matches state based on the payload
        lt(f, c.filter.toLowerCase())
      ))), a.forEach((f) => Cn(f, t.currentRoute.value)), c.rootNodes = a.map(jn);
    }
    let d;
    o.on.getInspectorTree((c) => {
      d = c, c.app === e && c.inspectorId === u && l();
    }), o.on.getInspectorState((c) => {
      if (c.app === e && c.inspectorId === u) {
        const f = n.getRoutes().find((h) => h.record.__vd_id === c.nodeId);
        f && (c.state = {
          options: os(f)
        });
      }
    }), o.sendInspectorTree(u), o.sendInspectorState(u);
  });
}
function rs(e) {
  return e.optional ? e.repeatable ? "*" : "?" : e.repeatable ? "+" : "";
}
function os(e) {
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
        display: e.keys.map((r) => `${r.name}${rs(r)}`).join(" "),
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
const In = 15485081, Tn = 2450411, An = 8702998, ss = 2282478, $n = 16486972, is = 6710886, as = 16704226, cs = 12131356;
function jn(e) {
  const t = [], { record: n } = e;
  n.name != null && t.push({
    label: String(n.name),
    textColor: 0,
    backgroundColor: ss
  }), n.aliasOf && t.push({
    label: "alias",
    textColor: 0,
    backgroundColor: $n
  }), e.__vd_match && t.push({
    label: "matches",
    textColor: 0,
    backgroundColor: In
  }), e.__vd_exactActive && t.push({
    label: "exact",
    textColor: 0,
    backgroundColor: An
  }), e.__vd_active && t.push({
    label: "active",
    textColor: 0,
    backgroundColor: Tn
  }), n.redirect && t.push({
    label: typeof n.redirect == "string" ? `redirect: ${n.redirect}` : "redirects",
    textColor: 16777215,
    backgroundColor: is
  });
  let r = n.__vd_id;
  return r == null && (r = String(us++), n.__vd_id = r), {
    id: r,
    label: n.path,
    tags: t,
    children: e.children.map(jn)
  };
}
let us = 0;
const ls = /^\/(.*)\/([a-z]*)$/;
function Cn(e, t) {
  const n = t.matched.length && te(t.matched[t.matched.length - 1], e.record);
  e.__vd_exactActive = e.__vd_active = n, n || (e.__vd_active = t.matched.some((r) => te(r, e.record))), e.children.forEach((r) => Cn(r, t));
}
function xn(e) {
  e.__vd_match = !1, e.children.forEach(xn);
}
function lt(e, t) {
  const n = String(e.re).match(ls);
  if (e.__vd_match = !1, !n || n.length < 3)
    return !1;
  if (new RegExp(n[1].replace(/\$$/, ""), n[2]).test(t))
    return e.children.forEach((i) => lt(i, t)), e.record.path !== "/" || t === "/" ? (e.__vd_match = e.re.test(t), !0) : !1;
  const o = e.record.path.toLowerCase(), s = ae(o);
  return !t.startsWith("/") && (s.includes(t) || o.includes(t)) || s.startsWith(t) || o.startsWith(t) || e.record.name && String(e.record.name).includes(t) ? !0 : e.children.some((i) => lt(i, t));
}
function fs(e, t) {
  const n = {};
  for (const r in e)
    t.includes(r) || (n[r] = e[r]);
  return n;
}
function ds(e) {
  const t = jo(e.routes, e), n = e.parseQuery || Uo, r = e.stringifyQuery || Ft, o = e.history;
  if (O.NODE_ENV !== "production" && !o)
    throw new Error('Provide the "history" option when calling "createRouter()": https://router.vuejs.org/api/interfaces/RouterOptions.html#history');
  const s = me(), i = me(), u = me(), l = J(Y);
  let d = Y;
  z && e.scrollBehavior && "scrollRestoration" in history && (history.scrollRestoration = "manual");
  const c = ze.bind(null, (m) => "" + m), a = ze.bind(null, io), f = (
    // @ts-expect-error: intentionally avoid the type check
    ze.bind(null, ae)
  );
  function h(m, E) {
    let w, S;
    return kn(m) ? (w = t.getRecordMatcher(m), O.NODE_ENV !== "production" && !w && R(`Parent route "${String(m)}" not found when adding child route`, E), S = E) : S = m, t.addRoute(S, w);
  }
  function v(m) {
    const E = t.getRecordMatcher(m);
    E ? t.removeRoute(E) : O.NODE_ENV !== "production" && R(`Cannot remove non-existent route "${String(m)}"`);
  }
  function p() {
    return t.getRoutes().map((m) => m.record);
  }
  function g(m) {
    return !!t.getRecordMatcher(m);
  }
  function y(m, E) {
    if (E = I({}, E || l.value), typeof m == "string") {
      const k = Je(n, m, E.path), $ = t.resolve({ path: k.path }, E), re = o.createHref(k.fullPath);
      return O.NODE_ENV !== "production" && (re.startsWith("//") ? R(`Location "${m}" resolved to "${re}". A resolved location cannot start with multiple slashes.`) : $.matched.length || R(`No match found for location with path "${m}"`)), I(k, $, {
        params: f($.params),
        hash: ae(k.hash),
        redirectedFrom: void 0,
        href: re
      });
    }
    if (O.NODE_ENV !== "production" && !Ae(m))
      return R(`router.resolve() was passed an invalid location. This will fail in production.
- Location:`, m), y({});
    let w;
    if (m.path != null)
      O.NODE_ENV !== "production" && "params" in m && !("name" in m) && // @ts-expect-error: the type is never
      Object.keys(m.params).length && R(`Path "${m.path}" was passed with params but they will be ignored. Use a named route alongside params instead.`), w = I({}, m, {
        path: Je(n, m.path, E.path).path
      });
    else {
      const k = I({}, m.params);
      for (const $ in k)
        k[$] == null && delete k[$];
      w = I({}, m, {
        params: a(k)
      }), E.params = a(E.params);
    }
    const S = t.resolve(w, E), T = m.hash || "";
    O.NODE_ENV !== "production" && T && !T.startsWith("#") && R(`A \`hash\` should always start with the character "#". Replace "${T}" with "#${T}".`), S.params = c(f(S.params));
    const C = uo(r, I({}, m, {
      hash: ro(T),
      path: S.path
    })), V = o.createHref(C);
    return O.NODE_ENV !== "production" && (V.startsWith("//") ? R(`Location "${m}" resolved to "${V}". A resolved location cannot start with multiple slashes.`) : S.matched.length || R(`No match found for location with path "${m.path != null ? m.path : m}"`)), I({
      fullPath: C,
      // keep the hash encoded so fullPath is effectively path + encodedQuery +
      // hash
      hash: T,
      query: (
        // if the user is using a custom query lib like qs, we might have
        // nested objects, so we keep the query as is, meaning it can contain
        // numbers at `$route.query`, but at the point, the user will have to
        // use their own type anyway.
        // https://github.com/vuejs/router/issues/328#issuecomment-649481567
        r === Ft ? Ko(m.query) : m.query || {}
      )
    }, S, {
      redirectedFrom: void 0,
      href: V
    });
  }
  function _(m) {
    return typeof m == "string" ? Je(n, m, l.value.path) : I({}, m);
  }
  function b(m, E) {
    if (d !== m)
      return ue(8, {
        from: E,
        to: m
      });
  }
  function P(m) {
    return D(m);
  }
  function j(m) {
    return P(I(_(m), { replace: !0 }));
  }
  function x(m) {
    const E = m.matched[m.matched.length - 1];
    if (E && E.redirect) {
      const { redirect: w } = E;
      let S = typeof w == "function" ? w(m) : w;
      if (typeof S == "string" && (S = S.includes("?") || S.includes("#") ? S = _(S) : (
        // force empty params
        { path: S }
      ), S.params = {}), O.NODE_ENV !== "production" && S.path == null && !("name" in S))
        throw R(`Invalid redirect found:
${JSON.stringify(S, null, 2)}
 when navigating to "${m.fullPath}". A redirect must contain a name or path. This will break in production.`), new Error("Invalid redirect");
      return I({
        query: m.query,
        hash: m.hash,
        // avoid transferring params if the redirect has a path
        params: S.path != null ? {} : m.params
      }, S);
    }
  }
  function D(m, E) {
    const w = d = y(m), S = l.value, T = m.state, C = m.force, V = m.replace === !0, k = x(w);
    if (k)
      return D(
        I(_(k), {
          state: typeof k == "object" ? I({}, T, k.state) : T,
          force: C,
          replace: V
        }),
        // keep original redirectedFrom if it exists
        E || w
      );
    const $ = w;
    $.redirectedFrom = E;
    let re;
    return !C && Vt(r, S, w) && (re = ue(16, { to: $, from: S }), St(
      S,
      S,
      // this is a push, the only way for it to be triggered from a
      // history.listen is with a redirect, which makes it become a push
      !0,
      // This cannot be the first navigation because the initial location
      // cannot be manually navigated to
      !1
    )), (re ? Promise.resolve(re) : yt($, S)).catch((M) => H(M) ? (
      // navigation redirects still mark the router as ready
      H(
        M,
        2
        /* ErrorTypes.NAVIGATION_GUARD_REDIRECT */
      ) ? M : Ge(M)
    ) : (
      // reject any unknown error
      Ke(M, $, S)
    )).then((M) => {
      if (M) {
        if (H(
          M,
          2
          /* ErrorTypes.NAVIGATION_GUARD_REDIRECT */
        ))
          return O.NODE_ENV !== "production" && // we are redirecting to the same location we were already at
          Vt(r, y(M.to), $) && // and we have done it a couple of times
          E && // @ts-expect-error: added only in dev
          (E._count = E._count ? (
            // @ts-expect-error
            E._count + 1
          ) : 1) > 30 ? (R(`Detected a possibly infinite redirection in a navigation guard when going from "${S.fullPath}" to "${$.fullPath}". Aborting to avoid a Stack Overflow.
 Are you always returning a new location within a navigation guard? That would lead to this error. Only return when redirecting or aborting, that should fix this. This might break in production if not fixed.`), Promise.reject(new Error("Infinite redirect in navigation guard"))) : D(
            // keep options
            I({
              // preserve an existing replacement but allow the redirect to override it
              replace: V
            }, _(M.to), {
              state: typeof M.to == "object" ? I({}, T, M.to.state) : T,
              force: C
            }),
            // preserve the original redirectedFrom if any
            E || $
          );
      } else
        M = Et($, S, !0, V, T);
      return wt($, S, M), M;
    });
  }
  function We(m, E) {
    const w = b(m, E);
    return w ? Promise.reject(w) : Promise.resolve();
  }
  function fe(m) {
    const E = ke.values().next().value;
    return E && typeof E.runWithContext == "function" ? E.runWithContext(m) : m();
  }
  function yt(m, E) {
    let w;
    const [S, T, C] = hs(m, E);
    w = Ye(S.reverse(), "beforeRouteLeave", m, E);
    for (const k of S)
      k.leaveGuards.forEach(($) => {
        w.push(X($, m, E));
      });
    const V = We.bind(null, m, E);
    return w.push(V), se(w).then(() => {
      w = [];
      for (const k of s.list())
        w.push(X(k, m, E));
      return w.push(V), se(w);
    }).then(() => {
      w = Ye(T, "beforeRouteUpdate", m, E);
      for (const k of T)
        k.updateGuards.forEach(($) => {
          w.push(X($, m, E));
        });
      return w.push(V), se(w);
    }).then(() => {
      w = [];
      for (const k of C)
        if (k.beforeEnter)
          if (U(k.beforeEnter))
            for (const $ of k.beforeEnter)
              w.push(X($, m, E));
          else
            w.push(X(k.beforeEnter, m, E));
      return w.push(V), se(w);
    }).then(() => (m.matched.forEach((k) => k.enterCallbacks = {}), w = Ye(C, "beforeRouteEnter", m, E, fe), w.push(V), se(w))).then(() => {
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
  function wt(m, E, w) {
    u.list().forEach((S) => fe(() => S(m, E, w)));
  }
  function Et(m, E, w, S, T) {
    const C = b(m, E);
    if (C)
      return C;
    const V = E === Y, k = z ? history.state : {};
    w && (S || V ? o.replace(m.fullPath, I({
      scroll: V && k && k.scroll
    }, T)) : o.push(m.fullPath, T)), l.value = m, St(m, E, w, V), Ge();
  }
  let de;
  function Un() {
    de || (de = o.listen((m, E, w) => {
      if (!bt.listening)
        return;
      const S = y(m), T = x(S);
      if (T) {
        D(I(T, { replace: !0, force: !0 }), S).catch(ye);
        return;
      }
      d = S;
      const C = l.value;
      z && go(It(C.fullPath, w.delta), Be()), yt(S, C).catch((V) => H(
        V,
        12
        /* ErrorTypes.NAVIGATION_CANCELLED */
      ) ? V : H(
        V,
        2
        /* ErrorTypes.NAVIGATION_GUARD_REDIRECT */
      ) ? (D(
        I(_(V.to), {
          force: !0
        }),
        S
        // avoid an uncaught rejection, let push call triggerError
      ).then((k) => {
        H(
          k,
          20
          /* ErrorTypes.NAVIGATION_DUPLICATED */
        ) && !w.delta && w.type === ce.pop && o.go(-1, !1);
      }).catch(ye), Promise.reject()) : (w.delta && o.go(-w.delta, !1), Ke(V, S, C))).then((V) => {
        V = V || Et(
          // after navigation, all matched components are resolved
          S,
          C,
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
        ) && o.go(-1, !1)), wt(S, C, V);
      }).catch(ye);
    }));
  }
  let Ue = me(), _t = me(), Pe;
  function Ke(m, E, w) {
    Ge(m);
    const S = _t.list();
    return S.length ? S.forEach((T) => T(m, E, w)) : (O.NODE_ENV !== "production" && R("uncaught error during route navigation:"), console.error(m)), Promise.reject(m);
  }
  function Kn() {
    return Pe && l.value !== Y ? Promise.resolve() : new Promise((m, E) => {
      Ue.add([m, E]);
    });
  }
  function Ge(m) {
    return Pe || (Pe = !m, Un(), Ue.list().forEach(([E, w]) => m ? w(m) : E()), Ue.reset()), m;
  }
  function St(m, E, w, S) {
    const { scrollBehavior: T } = e;
    if (!z || !T)
      return Promise.resolve();
    const C = !w && vo(It(m.fullPath, 0)) || (S || !w) && history.state && history.state.scroll || null;
    return Te().then(() => T(m, E, C)).then((V) => V && mo(V)).catch((V) => Ke(V, m, E));
  }
  const qe = (m) => o.go(m);
  let He;
  const ke = /* @__PURE__ */ new Set(), bt = {
    currentRoute: l,
    listening: !0,
    addRoute: h,
    removeRoute: v,
    clearRoutes: t.clearRoutes,
    hasRoute: g,
    getRoutes: p,
    resolve: y,
    options: e,
    push: P,
    replace: j,
    go: qe,
    back: () => qe(-1),
    forward: () => qe(1),
    beforeEach: s.add,
    beforeResolve: i.add,
    afterEach: u.add,
    onError: _t.add,
    isReady: Kn,
    install(m) {
      const E = this;
      m.component("RouterLink", Jo), m.component("RouterView", Zo), m.config.globalProperties.$router = E, Object.defineProperty(m.config.globalProperties, "$route", {
        enumerable: !0,
        get: () => L(l)
      }), z && // used for the initial navigation client side to avoid pushing
      // multiple times when the router is used in multiple apps
      !He && l.value === Y && (He = !0, P(o.location).catch((T) => {
        O.NODE_ENV !== "production" && R("Unexpected error when starting the router:", T);
      }));
      const w = {};
      for (const T in Y)
        Object.defineProperty(w, T, {
          get: () => l.value[T],
          enumerable: !0
        });
      m.provide(Le, E), m.provide(vt, Qn(w)), m.provide(ut, l);
      const S = m.unmount;
      ke.add(m), m.unmount = function() {
        ke.delete(m), ke.size < 1 && (d = Y, de && de(), de = null, l.value = Y, He = !1, Pe = !1), S();
      }, O.NODE_ENV !== "production" && z && ns(m, E, t);
    }
  };
  function se(m) {
    return m.reduce((E, w) => E.then(() => fe(w)), Promise.resolve());
  }
  return bt;
}
function hs(e, t) {
  const n = [], r = [], o = [], s = Math.max(t.matched.length, e.matched.length);
  for (let i = 0; i < s; i++) {
    const u = t.matched[i];
    u && (e.matched.find((d) => te(d, u)) ? r.push(u) : n.push(u));
    const l = e.matched[i];
    l && (t.matched.find((d) => te(d, l)) || o.push(l));
  }
  return [n, r, o];
}
function ps() {
  return ee(Le);
}
function ms(e) {
  return ee(vt);
}
const Dn = /* @__PURE__ */ new Map();
function gs(e) {
  var t;
  (t = e.jsFn) == null || t.forEach((n) => {
    Dn.set(n.id, W(n.code));
  });
}
function vs(e) {
  return Dn.get(e);
}
function ne(e) {
  let t = an(), n = Vr(), r = jr(e), o = ln(), s = ps(), i = ms();
  function u(p) {
    p.scopeSnapshot && (t = p.scopeSnapshot), p.slotSnapshot && (n = p.slotSnapshot), p.vforSnapshot && (r = p.vforSnapshot), p.elementRefSnapshot && (o = p.elementRefSnapshot), p.routerSnapshot && (s = p.routerSnapshot);
  }
  function l(p) {
    if (N.isVar(p))
      return q(d(p));
    if (N.isVForItem(p))
      return xr(p.fid) ? r.getVForIndex(p.fid) : q(d(p));
    if (N.isVForIndex(p))
      return r.getVForIndex(p.fid);
    if (N.isJsFn(p)) {
      const { id: g } = p;
      return vs(g);
    }
    if (N.isSlotProp(p))
      return n.getPropsValue(p);
    if (N.isRouterParams(p))
      return q(d(p));
    throw new Error(`Invalid binding: ${p}`);
  }
  function d(p) {
    if (N.isVar(p)) {
      const g = t.getVueRef(p) || _r(p);
      return Rt(g, {
        paths: p.path,
        getBindableValueFn: l
      });
    }
    if (N.isVForItem(p))
      return Cr({
        binding: p,
        snapshot: v
      });
    if (N.isVForIndex(p))
      return () => l(p);
    if (N.isRouterParams(p)) {
      const { prop: g = "params" } = p;
      return Rt(() => i[g], {
        paths: p.path,
        getBindableValueFn: l
      });
    }
    throw new Error(`Invalid binding: ${p}`);
  }
  function c(p) {
    if (N.isVar(p) || N.isVForItem(p))
      return d(p);
    if (N.isVForIndex(p) || N.isJsFn(p))
      return l(p);
    if (N.isRouterParams(p))
      return d(p);
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
      d({ type: "var", ..._ }).value = _.val;
    }), (y = p.ele_refs) == null || y.forEach((_) => {
      o.getRef({
        sid: _.sid,
        id: _.id
      }).value[_.method](..._.args);
    });
  }
  function h(p, g) {
    if (Pt(g) || Pt(p.values))
      return;
    g = g;
    const y = p.values, _ = p.skips || new Array(g.length).fill(0);
    g.forEach((b, P) => {
      if (_[P] === 1)
        return;
      if (N.isVar(b)) {
        const x = d(b);
        x.value = y[P];
        return;
      }
      if (N.isRouterAction(b)) {
        const x = y[P], D = s[x.fn];
        D(...x.args);
        return;
      }
      if (N.isElementRef(b)) {
        const x = o.getRef(b).value, D = y[P], { method: We, args: fe = [] } = D;
        x[We](...fe);
        return;
      }
      const j = d(b);
      j.value = y[P];
    });
  }
  const v = {
    getVForIndex: r.getVForIndex,
    getObjectToValue: l,
    getVueRefObject: d,
    getVueRefObjectOrValue: c,
    getBindingServerInfo: a,
    updateRefFromServer: f,
    updateOutputsRefFromServer: h,
    replaceSnapshot: u
  };
  return v;
}
class ys {
  async eventSend(t, n) {
    const { fType: r, hKey: o, key: s } = t, i = Ze().webServerInfo, u = s !== void 0 ? { key: s } : {}, l = r === "sync" ? i.event_url : i.event_async_url;
    let d = {};
    const c = await fetch(l, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        bind: n,
        hKey: o,
        ...u,
        page: we(),
        ...d
      })
    });
    if (!c.ok)
      throw new Error(`HTTP error! status: ${c.status}`);
    return await c.json();
  }
  async watchSend(t) {
    const { outputs: n, fType: r, key: o } = t.watchConfig, s = Ze().webServerInfo, i = r === "sync" ? s.watch_url : s.watch_async_url, u = t.getServerInputs(), l = {
      key: o,
      input: u,
      page: we()
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
class ws {
  async eventSend(t, n) {
    const { fType: r, hKey: o, key: s } = t, i = s !== void 0 ? { key: s } : {};
    let u = {};
    const l = {
      bind: n,
      fType: r,
      hKey: o,
      ...i,
      page: we(),
      ...u
    };
    return await window.pywebview.api.event_call(l);
  }
  async watchSend(t) {
    const { outputs: n, fType: r, key: o } = t.watchConfig, s = t.getServerInputs(), i = {
      key: o,
      input: s,
      fType: r,
      page: we()
    };
    return await window.pywebview.api.watch_call(i);
  }
}
let ft;
function Es(e) {
  switch (e.mode) {
    case "web":
      ft = new ys();
      break;
    case "webview":
      ft = new ws();
      break;
  }
}
function Mn() {
  return ft;
}
function _s(e) {
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
function Ss(e, t, n) {
  return new bs(e, t, n);
}
class bs {
  constructor(t, n, r) {
    B(this, "taskQueue", []);
    B(this, "id2TaskMap", /* @__PURE__ */ new Map());
    B(this, "input2TaskIdMap", Se(() => []));
    this.snapshots = r;
    const o = [], s = (i) => {
      var l;
      const u = new Os(i, r);
      return this.id2TaskMap.set(u.id, u), (l = i.inputs) == null || l.forEach((d, c) => {
        var f, h;
        if (((f = i.data) == null ? void 0 : f[c]) === 0 && ((h = i.slient) == null ? void 0 : h[c]) === 0) {
          const v = `${d.sid}-${d.id}`;
          this.input2TaskIdMap.getOrDefault(v).push(u.id);
        }
      }), u;
    };
    t == null || t.forEach((i) => {
      const u = s(i);
      o.push(u);
    }), n == null || n.forEach((i) => {
      const u = s(
        _s(i)
      );
      o.push(u);
    }), o.forEach((i) => {
      const {
        deep: u = !0,
        once: l,
        flush: d,
        immediate: c = !0
      } = i.watchConfig, a = {
        immediate: c,
        deep: u,
        once: l,
        flush: d
      }, f = this._getWatchTargets(i);
      G(
        f,
        (h) => {
          h.some(_e) || (i.modify = !0, this.taskQueue.push(new Rs(i)), this._scheduleNextTick());
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
    Te(() => this._runAllTasks());
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
class Os {
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
class Rs {
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
        await Ps(this.watchTask);
      } finally {
        this.watchTask.taskDone();
      }
    }
  }
}
async function Ps(e) {
  const { snapshot: t } = e, { outputs: n } = e.watchConfig, r = await Mn().watchSend(e);
  r && t.updateOutputsRefFromServer(r, n);
}
function ks(e, t) {
  const {
    on: n,
    code: r,
    immediate: o,
    deep: s,
    once: i,
    flush: u,
    bind: l = {},
    onData: d,
    bindData: c
  } = e, a = d || new Array(n.length).fill(0), f = c || new Array(Object.keys(l).length).fill(0), h = Me(
    l,
    (g, y, _) => f[_] === 0 ? t.getVueRefObject(g) : g
  ), v = W(r, h), p = n.length === 1 ? Gt(a[0] === 1, n[0], t) : n.map(
    (g, y) => Gt(a[y] === 1, g, t)
  );
  return G(p, v, { immediate: o, deep: s, once: i, flush: u });
}
function Gt(e, t, n) {
  return e ? () => t : n.getVueRefObject(t);
}
function Vs(e, t) {
  const {
    inputs: n = [],
    outputs: r,
    slient: o,
    data: s,
    code: i,
    immediate: u = !0,
    deep: l,
    once: d,
    flush: c
  } = e, a = o || new Array(n.length).fill(0), f = s || new Array(n.length).fill(0), h = W(i), v = n.filter((g, y) => a[y] === 0 && f[y] === 0).map((g) => t.getVueRefObject(g));
  function p() {
    return n.map((g, y) => f[y] === 0 ? rn(q(t.getVueRefObject(g))) : g);
  }
  G(
    v,
    () => {
      let g = h(...p());
      if (!r)
        return;
      const _ = r.length === 1 ? [g] : g, b = _.map((P) => P === void 0 ? 1 : 0);
      t.updateOutputsRefFromServer(
        { values: _, skips: b },
        r
      );
    },
    { immediate: u, deep: l, once: d, flush: c }
  );
}
function Ns(e, t) {
  return Object.assign(
    {},
    ...Object.entries(e ?? {}).map(([n, r]) => {
      const o = r.map((u) => {
        if (u.type === "web") {
          const l = Is(u.bind, t);
          return Ts(u, l, t);
        } else {
          if (u.type === "vue")
            return $s(u, t);
          if (u.type === "js")
            return As(u, t);
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
function Is(e, t) {
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
function Ts(e, t, n) {
  async function r(...o) {
    const s = t(...o), i = await Mn().eventSend(e, s);
    i && n.updateOutputsRefFromServer(i, e.set);
  }
  return r;
}
function As(e, t) {
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
      return N.IsBinding(c) ? rn(t.getObjectToValue(c)) : c;
    }), d = s(...l);
    if (o !== void 0) {
      const a = o.length === 1 ? [d] : d, f = a.map((h) => h === void 0 ? 1 : 0);
      t.updateOutputsRefFromServer({ values: a, skips: f }, o);
    }
  }
  return i;
}
function $s(e, t) {
  const { code: n, bind: r = {}, bindData: o } = e, s = o || new Array(Object.keys(r).length).fill(0), i = Me(
    r,
    (d, c, a) => s[a] === 0 ? t.getVueRefObject(d) : d
  ), u = W(n, i);
  function l(...d) {
    u(...d);
  }
  return l;
}
function js(e, t) {
  const n = [];
  (e.bStyle || []).forEach((s) => {
    Array.isArray(s) ? n.push(
      ...s.map((i) => t.getObjectToValue(i))
    ) : n.push(
      Me(
        s,
        (i) => t.getObjectToValue(i)
      )
    );
  });
  const r = Xn([e.style || {}, n]);
  return {
    hasStyle: r && Object.keys(r).length > 0,
    styles: r
  };
}
function Cs(e, t) {
  const n = e.classes;
  if (!n)
    return null;
  if (typeof n == "string")
    return Xe(n);
  const { str: r, map: o, bind: s } = n, i = [];
  return r && i.push(r), o && i.push(
    Me(
      o,
      (u) => t.getObjectToValue(u)
    )
  ), s && i.push(...s.map((u) => t.getObjectToValue(u))), Xe(i);
}
function $e(e, t = !0) {
  if (!(typeof e != "object" || e === null)) {
    if (Array.isArray(e)) {
      t && e.forEach((n) => $e(n, !0));
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
        t && $e(r, !0);
  }
}
function xs(e, t) {
  const n = e.startsWith(":");
  return n && (e = e.slice(1), t = W(t)), { name: e, value: t, isFunc: n };
}
function Ds(e, t, n) {
  var o;
  const r = {};
  return Ot(e.bProps || {}, (s, i) => {
    const u = n.getObjectToValue(s);
    _e(u) || ($e(u), r[i] = Ms(u, i));
  }), (o = e.proxyProps) == null || o.forEach((s) => {
    const i = n.getObjectToValue(s);
    typeof i == "object" && Ot(i, (u, l) => {
      const { name: d, value: c } = xs(l, u);
      r[d] = c;
    });
  }), { ...t || {}, ...r };
}
function Ms(e, t) {
  return t === "innerText" ? Yt(e) : e;
}
function Fs(e, { slots: t }) {
  const { id: n, use: r } = e.propsInfo, o = Rr(n);
  return xe(() => {
    kr(n);
  }), () => {
    const s = e.propsValue;
    return Pr(
      n,
      o,
      Object.fromEntries(
        r.map((i) => [i, s[i]])
      )
    ), A(De, null, t.default());
  };
}
const Bs = F(Fs, {
  props: ["propsInfo", "propsValue"]
}), Fn = /* @__PURE__ */ new Map();
function Ls(e) {
  var t;
  (t = e.scopes) == null || t.forEach((n) => {
    Fn.set(n.id, n);
  });
}
function le(e) {
  return Fn.get(e);
}
function Ws(e, t) {
  if (!e.slots)
    return null;
  const n = e.slots ?? {};
  return Array.isArray(n) ? t ? ve(n) : () => ve(n) : en(n, { keyFn: (i) => i === ":" ? "default" : i, valueFn: (i) => {
    const { items: u } = i;
    return (l) => {
      if (i.scopeId) {
        const d = () => i.props ? qt(i.props, l, u) : ve(u);
        return A(
          Re,
          { scope: le(i.scopeId) },
          d
        );
      }
      return i.props ? qt(i.props, l, u) : ve(u);
    };
  } });
}
function qt(e, t, n) {
  return A(
    Bs,
    { propsInfo: e, propsValue: t },
    () => ve(n)
  );
}
function ve(e) {
  const t = (e ?? []).map((n) => A(Q, {
    component: n
  }));
  return t.length <= 0 ? null : t;
}
function Us(e, t) {
  const n = {}, r = [];
  return (e || []).forEach((o) => {
    const { sys: s, name: i, arg: u, value: l, mf: d } = o;
    if (i === "vmodel") {
      const c = t.getVueRefObject(l);
      if (n[`onUpdate:${u}`] = (a) => {
        c.value = a;
      }, s === 1) {
        const a = d ? Object.fromEntries(d.map((f) => [f, !0])) : {};
        r.push([Zn, c.value, void 0, a]);
      } else
        n[u] = c.value;
    } else if (i === "vshow") {
      const c = t.getVueRefObject(l);
      r.push([er, c.value]);
    } else
      console.warn(`Directive ${i} is not supported yet`);
  }), {
    newProps: n,
    directiveArray: r
  };
}
function Ks(e, t) {
  const { eRef: n } = e;
  return n === void 0 ? {} : { ref: t.getRef(n) };
}
function Gs(e) {
  const t = ne(), n = ln(), r = e.component.props ?? {};
  return $e(r, !0), () => {
    const { tag: o } = e.component, s = N.IsBinding(o) ? t.getObjectToValue(o) : o, i = dt(s), u = typeof i == "string", l = Cs(e.component, t), { styles: d, hasStyle: c } = js(e.component, t), a = Ns(e.component.events ?? {}, t), f = Ws(e.component, u), h = Ds(e.component, r, t), { newProps: v, directiveArray: p } = Us(
      e.component.dir,
      t
    ), g = Ks(
      e.component,
      n
    ), y = tr({
      ...h,
      ...a,
      ...v,
      ...g
    }) || {};
    c && (y.style = d), l && (y.class = l);
    const _ = A(i, { ...y }, f);
    return p.length > 0 ? nr(
      // @ts-ignore
      _,
      p
    ) : _;
  };
}
const Q = F(Gs, {
  props: ["component"]
});
function Bn(e, t) {
  var n, r;
  if (e) {
    const o = br(e), s = sn(e, ne(t)), i = ne(t);
    Ss(e.py_watch, e.web_computed, i), (n = e.vue_watch) == null || n.forEach((u) => ks(u, i)), (r = e.js_watch) == null || r.forEach((u) => Vs(u, i)), xe(() => {
      un(e.id, s), Or(e.id, o);
    });
  }
}
function qs(e, { slots: t }) {
  const { scope: n } = e;
  return Bn(n), () => A(De, null, t.default());
}
const Re = F(qs, {
  props: ["scope"]
}), Hs = F(
  (e) => {
    const { scope: t, items: n, vforInfo: r } = e;
    return Nr(r), Bn(t, r.key), n.length === 1 ? () => A(Q, {
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
function zs(e, t) {
  const { state: n, isReady: r, isLoading: o } = mr(async () => {
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
function Js(e, t) {
  let n;
  return t.component ? n = `Error captured from component:tag: ${t.component.tag} ; id: ${t.component.id} ` : n = "Error captured from app init", console.group(n), console.error("Component:", t.component), console.error("Error:", e), console.groupEnd(), !1;
}
const Qs = { class: "app-box" }, Ys = {
  key: 0,
  style: { position: "absolute", top: "50%", left: "50%", transform: "translate(-50%, -50%)" }
}, Xs = /* @__PURE__ */ F({
  __name: "App",
  props: {
    config: {},
    configUrl: {}
  },
  setup(e) {
    const t = e, { config: n, isLoading: r } = zs(
      t.config,
      t.configUrl
    );
    let o = null;
    return G(n, (s) => {
      o = s, s.url && (lr({
        mode: s.mode,
        version: s.version,
        queryPath: s.url.path,
        pathParams: s.url.params,
        webServerInfo: s.webInfo
      }), Es(s)), Ls(s), gs(s);
    }), rr(Js), (s, i) => (he(), Ve("div", Qs, [
      L(r) ? (he(), Ve("div", Ys, i[0] || (i[0] = [
        or("p", { style: { margin: "auto" } }, "Loading ...", -1)
      ]))) : (he(), Ve("div", {
        key: 1,
        class: Xe(["insta-main", L(n).class])
      }, [
        sr(L(Re), {
          scope: L(le)(L(o).scopeId)
        }, {
          default: ir(() => [
            (he(!0), Ve(De, null, ar(L(o).items, (u) => (he(), cr(L(Q), { component: u }, null, 8, ["component"]))), 256))
          ]),
          _: 1
        }, 8, ["scope"])
      ], 2))
    ]));
  }
});
function Zs(e) {
  const { on: t, scopeId: n, items: r } = e, o = le(n), s = ne();
  return () => {
    const i = typeof t == "boolean" ? t : s.getObjectToValue(t);
    return A(Re, { scope: o }, () => i ? r.map(
      (l) => A(Q, { component: l })
    ) : void 0);
  };
}
const ei = F(Zs, {
  props: ["on", "scopeId", "items"]
});
function ti(e) {
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
function ni(e) {
  const { array: t, bArray: n, items: r, fkey: o, fid: s, scopeId: i, num: u, tsGroup: l = {} } = e, d = t === void 0, c = u !== void 0, a = d ? n : t, f = ne();
  Tr(s, a, d, c);
  const v = ai(o ?? "index");
  xe(() => {
    Sr(i);
  });
  const p = le(i);
  return () => {
    const g = oi(
      c,
      d,
      a,
      f,
      u
    ), y = $r(s), _ = g.map((b, P) => {
      const j = v(b, P);
      return y.add(j), Ar(s, j, P), A(Hs, {
        scope: p,
        items: r,
        vforInfo: {
          fid: s,
          key: j
        },
        key: j
      });
    });
    return y.removeUnusedKeys(), l && Object.keys(l).length > 0 ? A(Xt, l, {
      default: () => _
    }) : _;
  };
}
const ri = F(ni, {
  props: [
    "array",
    "items",
    "fid",
    "bArray",
    "scopeId",
    "num",
    "fkey",
    "tsGroup"
  ]
});
function oi(e, t, n, r, o) {
  if (e) {
    let i = 0;
    return typeof o == "number" ? i = o : i = r.getObjectToValue(o) ?? 0, ti({
      end: Math.max(0, i)
    });
  }
  const s = t ? r.getObjectToValue(n) || [] : n;
  return typeof s == "object" ? Object.values(s) : s;
}
const si = (e) => e, ii = (e, t) => t;
function ai(e) {
  const t = gr(e);
  return typeof t == "function" ? t : e === "item" ? si : ii;
}
function ci(e) {
  return e.map((n) => {
    if (n.tag)
      return A(Q, { component: n });
    const r = dt(Ln);
    return A(r, {
      scope: n
    });
  });
}
const Ln = F(
  (e) => {
    const t = e.scope;
    return () => ci(t.items ?? []);
  },
  {
    props: ["scope"]
  }
);
function ui(e) {
  return e.map((t) => {
    if (t.tag)
      return A(Q, { component: t });
    const n = dt(Ln);
    return A(n, {
      scope: t
    });
  });
}
const li = F(
  (e) => {
    const { scope: t, on: n, items: r } = e, o = J(r), s = sn(t), i = ne();
    return je.createDynamicWatchRefresh(n, i, async () => {
      const { items: u, on: l } = await je.fetchRemote(e, i);
      return o.value = u, l;
    }), xe(() => {
      un(t.id, s);
    }), () => ui(o.value);
  },
  {
    props: ["sid", "url", "hKey", "on", "bind", "items", "scope"]
  }
);
var je;
((e) => {
  function t(r, o, s) {
    let i = null, u = r, l = u.map((c) => o.getVueRefObject(c));
    function d() {
      i && i(), i = G(
        l,
        async () => {
          u = await s(), l = u.map((c) => o.getVueRefObject(c)), d();
        },
        { deep: !0 }
      );
    }
    return d(), () => {
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
      page: we()
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
})(je || (je = {}));
function fi(e) {
  const { scopeId: t, items: n } = e, r = le(t);
  return () => {
    const o = n.map((s) => A(Q, { component: s }));
    return A(Re, { scope: r }, () => o);
  };
}
const Ht = F(fi, {
  props: ["scopeId", "items"]
});
function di(e) {
  const { on: t, case: n, default: r } = e, o = ne();
  return () => {
    const s = o.getObjectToValue(t), i = n.map((u) => {
      const { value: l, items: d, scopeId: c } = u.props;
      if (s === l)
        return A(Ht, {
          scopeId: c,
          items: d,
          key: ["case", l].join("-")
        });
    }).filter((u) => u);
    if (r && !i.length) {
      const { items: u, scopeId: l } = r.props;
      i.push(A(Ht, { scopeId: l, items: u, key: "default" }));
    }
    return A(De, i);
  };
}
const hi = F(di, {
  props: ["case", "on", "default"]
});
function pi(e, { slots: t }) {
  const { name: n = "fade", tag: r } = e;
  return () => A(
    Xt,
    { name: n, tag: r },
    {
      default: t.default
    }
  );
}
const mi = F(pi, {
  props: ["name", "tag"]
});
function gi(e) {
  const { content: t, r: n = 0 } = e, r = ne(), o = n === 1 ? () => r.getObjectToValue(t) : () => t;
  return () => Yt(o());
}
const vi = F(gi, {
  props: ["content", "r"]
});
function yi(e) {
  if (!e.router)
    throw new Error("Router config is not provided.");
  const { routes: t, kAlive: n = !1 } = e.router;
  return t.map(
    (o) => Wn(o, n)
  );
}
function Wn(e, t) {
  var l;
  const { server: n = !1, vueItem: r, scopeId: o } = e, s = () => {
    if (n)
      throw new Error("Server-side rendering is not supported yet.");
    return Promise.resolve(
      wi(r, le(o), t)
    );
  }, i = (l = r.children) == null ? void 0 : l.map(
    (d) => Wn(d, t)
  ), u = {
    ...r,
    children: i,
    component: s
  };
  return r.component.length === 0 && delete u.component, i === void 0 && delete u.children, u;
}
function wi(e, t, n) {
  const { path: r, component: o } = e, s = A(
    Re,
    { scope: t, key: r },
    () => o.map((u) => A(Q, { component: u }))
  );
  return n ? A(ur, null, () => s) : s;
}
function Ei(e, t) {
  const { mode: n = "hash" } = t.router, r = n === "hash" ? So() : n === "memory" ? _o() : Pn();
  e.use(
    ds({
      history: r,
      routes: yi(t)
    })
  );
}
function bi(e, t) {
  e.component("insta-ui", Xs), e.component("vif", ei), e.component("vfor", ri), e.component("match", hi), e.component("refresh", li), e.component("ts-group", mi), e.component("content", vi), t.router && Ei(e, t);
}
export {
  $e as convertDynamicProperties,
  bi as install
};
//# sourceMappingURL=insta-ui.js.map
