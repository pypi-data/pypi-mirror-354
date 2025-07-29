var ol = Object.defineProperty;
var da = (e) => {
  throw TypeError(e);
};
var fl = (e, t, n) => t in e ? ol(e, t, { enumerable: !0, configurable: !0, writable: !0, value: n }) : e[t] = n;
var va = (e, t, n) => fl(e, typeof t != "symbol" ? t + "" : t, n), mr = (e, t, n) => t.has(e) || da("Cannot " + n);
var oe = (e, t, n) => (mr(e, t, "read from private field"), n ? n.call(e) : t.get(e)), Le = (e, t, n) => t.has(e) ? da("Cannot add the same private member more than once") : t instanceof WeakSet ? t.add(e) : t.set(e, n), He = (e, t, n, r) => (mr(e, t, "write to private field"), r ? r.call(e, n) : t.set(e, n), n), ga = (e, t, n) => (mr(e, t, "access private method"), n);
const ul = "5";
var ai;
typeof window < "u" && ((ai = window.__svelte ?? (window.__svelte = {})).v ?? (ai.v = /* @__PURE__ */ new Set())).add(ul);
const Wr = 1, Vr = 2, ii = 4, cl = 8, dl = 16, vl = 1, gl = 4, hl = 8, bl = 16, li = 1, _l = 2, Ie = Symbol(), ml = "http://www.w3.org/1999/xhtml", ha = !1;
var tr = Array.isArray, xl = Array.prototype.indexOf, Yr = Array.from, pl = Object.defineProperty, pt = Object.getOwnPropertyDescriptor, wl = Object.getOwnPropertyDescriptors, yl = Object.prototype, kl = Array.prototype, si = Object.getPrototypeOf, ba = Object.isExtensible;
function rn(e) {
  return typeof e == "function";
}
const Ml = () => {
};
function Tl(e) {
  for (var t = 0; t < e.length; t++)
    e[t]();
}
const $e = 2, oi = 4, nr = 8, Xr = 16, ht = 32, Qt = 64, Pn = 128, We = 256, Rn = 512, Be = 1024, lt = 2048, Ft = 4096, vt = 8192, rr = 16384, Al = 32768, ar = 65536, ql = 1 << 19, fi = 1 << 20, qr = 1 << 21, wt = Symbol("$state"), ui = Symbol("legacy props"), Sl = Symbol("");
function ci(e) {
  return e === this.v;
}
function El(e, t) {
  return e != e ? t == t : e !== t || e !== null && typeof e == "object" || typeof e == "function";
}
function Gr(e) {
  return !El(e, this.v);
}
function Ll(e) {
  throw new Error("https://svelte.dev/e/effect_in_teardown");
}
function Nl() {
  throw new Error("https://svelte.dev/e/effect_in_unowned_derived");
}
function Fl(e) {
  throw new Error("https://svelte.dev/e/effect_orphan");
}
function Cl() {
  throw new Error("https://svelte.dev/e/effect_update_depth_exceeded");
}
function Pl(e) {
  throw new Error("https://svelte.dev/e/props_invalid_value");
}
function Rl() {
  throw new Error("https://svelte.dev/e/state_descriptors_fixed");
}
function Il() {
  throw new Error("https://svelte.dev/e/state_prototype_fixed");
}
function Dl() {
  throw new Error("https://svelte.dev/e/state_unsafe_mutation");
}
let zl = !1, Ve = null;
function _a(e) {
  Ve = e;
}
function pe(e, t = !1, n) {
  var r = Ve = {
    p: Ve,
    c: null,
    d: !1,
    e: null,
    m: !1,
    s: e,
    x: null,
    l: null
  };
  wi(() => {
    r.d = !0;
  });
}
function we(e) {
  const t = Ve;
  if (t !== null) {
    const s = t.e;
    if (s !== null) {
      var n = he, r = ve;
      t.e = null;
      try {
        for (var a = 0; a < s.length; a++) {
          var l = s[a];
          yt(l.effect), st(l.reaction), $t(l.fn);
        }
      } finally {
        yt(n), st(r);
      }
    }
    Ve = t.p, t.m = !0;
  }
  return (
    /** @type {T} */
    {}
  );
}
function di() {
  return !0;
}
function nt(e) {
  if (typeof e != "object" || e === null || wt in e)
    return e;
  const t = si(e);
  if (t !== yl && t !== kl)
    return e;
  var n = /* @__PURE__ */ new Map(), r = tr(e), a = /* @__PURE__ */ re(0), l = ve, s = (o) => {
    var u = ve;
    st(l);
    var f = o();
    return st(u), f;
  };
  return r && n.set("length", /* @__PURE__ */ re(
    /** @type {any[]} */
    e.length
  )), new Proxy(
    /** @type {any} */
    e,
    {
      defineProperty(o, u, f) {
        (!("value" in f) || f.configurable === !1 || f.enumerable === !1 || f.writable === !1) && Rl();
        var v = n.get(u);
        return v === void 0 ? (v = s(() => /* @__PURE__ */ re(f.value)), n.set(u, v)) : J(
          v,
          s(() => nt(f.value))
        ), !0;
      },
      deleteProperty(o, u) {
        var f = n.get(u);
        if (f === void 0)
          u in o && (n.set(
            u,
            s(() => /* @__PURE__ */ re(Ie))
          ), xr(a));
        else {
          if (r && typeof u == "string") {
            var v = (
              /** @type {Source<number>} */
              n.get("length")
            ), c = Number(u);
            Number.isInteger(c) && c < v.v && J(v, c);
          }
          J(f, Ie), xr(a);
        }
        return !0;
      },
      get(o, u, f) {
        var g;
        if (u === wt)
          return e;
        var v = n.get(u), c = u in o;
        if (v === void 0 && (!c || (g = pt(o, u)) != null && g.writable) && (v = s(() => /* @__PURE__ */ re(nt(c ? o[u] : Ie))), n.set(u, v)), v !== void 0) {
          var d = i(v);
          return d === Ie ? void 0 : d;
        }
        return Reflect.get(o, u, f);
      },
      getOwnPropertyDescriptor(o, u) {
        var f = Reflect.getOwnPropertyDescriptor(o, u);
        if (f && "value" in f) {
          var v = n.get(u);
          v && (f.value = i(v));
        } else if (f === void 0) {
          var c = n.get(u), d = c == null ? void 0 : c.v;
          if (c !== void 0 && d !== Ie)
            return {
              enumerable: !0,
              configurable: !0,
              value: d,
              writable: !0
            };
        }
        return f;
      },
      has(o, u) {
        var d;
        if (u === wt)
          return !0;
        var f = n.get(u), v = f !== void 0 && f.v !== Ie || Reflect.has(o, u);
        if (f !== void 0 || he !== null && (!v || (d = pt(o, u)) != null && d.writable)) {
          f === void 0 && (f = s(() => /* @__PURE__ */ re(v ? nt(o[u]) : Ie)), n.set(u, f));
          var c = i(f);
          if (c === Ie)
            return !1;
        }
        return v;
      },
      set(o, u, f, v) {
        var k;
        var c = n.get(u), d = u in o;
        if (r && u === "length")
          for (var g = f; g < /** @type {Source<number>} */
          c.v; g += 1) {
            var h = n.get(g + "");
            h !== void 0 ? J(h, Ie) : g in o && (h = s(() => /* @__PURE__ */ re(Ie)), n.set(g + "", h));
          }
        c === void 0 ? (!d || (k = pt(o, u)) != null && k.writable) && (c = s(() => /* @__PURE__ */ re(void 0)), J(
          c,
          s(() => nt(f))
        ), n.set(u, c)) : (d = c.v !== Ie, J(
          c,
          s(() => nt(f))
        ));
        var _ = Reflect.getOwnPropertyDescriptor(o, u);
        if (_ != null && _.set && _.set.call(v, f), !d) {
          if (r && typeof u == "string") {
            var p = (
              /** @type {Source<number>} */
              n.get("length")
            ), E = Number(u);
            Number.isInteger(E) && E >= p.v && J(p, E + 1);
          }
          xr(a);
        }
        return !0;
      },
      ownKeys(o) {
        i(a);
        var u = Reflect.ownKeys(o).filter((c) => {
          var d = n.get(c);
          return d === void 0 || d.v !== Ie;
        });
        for (var [f, v] of n)
          v.v !== Ie && !(f in o) && u.push(f);
        return u;
      },
      setPrototypeOf() {
        Il();
      }
    }
  );
}
function xr(e, t = 1) {
  J(e, e.v + t);
}
function ma(e) {
  try {
    if (e !== null && typeof e == "object" && wt in e)
      return e[wt];
  } catch {
  }
  return e;
}
function Ol(e, t) {
  return Object.is(ma(e), ma(t));
}
// @__NO_SIDE_EFFECTS__
function ir(e) {
  var t = $e | lt, n = ve !== null && (ve.f & $e) !== 0 ? (
    /** @type {Derived} */
    ve
  ) : null;
  return he === null || n !== null && (n.f & We) !== 0 ? t |= We : he.f |= fi, {
    ctx: Ve,
    deps: null,
    effects: null,
    equals: ci,
    f: t,
    fn: e,
    reactions: null,
    rv: 0,
    v: (
      /** @type {V} */
      null
    ),
    wv: 0,
    parent: n ?? he
  };
}
// @__NO_SIDE_EFFECTS__
function x(e) {
  const t = /* @__PURE__ */ ir(e);
  return qi(t), t;
}
// @__NO_SIDE_EFFECTS__
function Bl(e) {
  const t = /* @__PURE__ */ ir(e);
  return t.equals = Gr, t;
}
function vi(e) {
  var t = e.effects;
  if (t !== null) {
    e.effects = null;
    for (var n = 0; n < t.length; n += 1)
      gt(
        /** @type {Effect} */
        t[n]
      );
  }
}
function Hl(e) {
  for (var t = e.parent; t !== null; ) {
    if ((t.f & $e) === 0)
      return (
        /** @type {Effect} */
        t
      );
    t = t.parent;
  }
  return null;
}
function gi(e) {
  var t, n = he;
  yt(Hl(e));
  try {
    vi(e), t = Ni(e);
  } finally {
    yt(n);
  }
  return t;
}
function hi(e) {
  var t = gi(e);
  if (e.equals(t) || (e.v = t, e.wv = Ei()), !en) {
    var n = (xt || (e.f & We) !== 0) && e.deps !== null ? Ft : Be;
    et(e, n);
  }
}
const un = /* @__PURE__ */ new Map();
function In(e, t) {
  var n = {
    f: 0,
    // TODO ideally we could skip this altogether, but it causes type errors
    v: e,
    reactions: null,
    equals: ci,
    rv: 0,
    wv: 0
  };
  return n;
}
// @__NO_SIDE_EFFECTS__
function re(e, t) {
  const n = In(e);
  return qi(n), n;
}
// @__NO_SIDE_EFFECTS__
function bi(e, t = !1) {
  const n = In(e);
  return t || (n.equals = Gr), n;
}
function J(e, t, n = !1) {
  ve !== null && !rt && di() && (ve.f & ($e | Xr)) !== 0 && !(Fe != null && Fe.includes(e)) && Dl();
  let r = n ? nt(t) : t;
  return Sr(e, r);
}
function Sr(e, t) {
  if (!e.equals(t)) {
    var n = e.v;
    en ? un.set(e, t) : un.set(e, n), e.v = t, (e.f & $e) !== 0 && ((e.f & lt) !== 0 && gi(
      /** @type {Derived} */
      e
    ), et(e, (e.f & We) === 0 ? Be : Ft)), e.wv = Ei(), _i(e, lt), he !== null && (he.f & Be) !== 0 && (he.f & (ht | Qt)) === 0 && (Ge === null ? Jl([e]) : Ge.push(e));
  }
  return t;
}
function _i(e, t) {
  var n = e.reactions;
  if (n !== null)
    for (var r = n.length, a = 0; a < r; a++) {
      var l = n[a], s = l.f;
      (s & lt) === 0 && (et(l, t), (s & (Be | We)) !== 0 && ((s & $e) !== 0 ? _i(
        /** @type {Derived} */
        l,
        Ft
      ) : ur(
        /** @type {Effect} */
        l
      )));
    }
}
function jl() {
  console.warn("https://svelte.dev/e/select_multiple_invalid_value");
}
let Wl = !1;
var xa, mi, xi, pi;
function Vl() {
  if (xa === void 0) {
    xa = window, mi = /Firefox/.test(navigator.userAgent);
    var e = Element.prototype, t = Node.prototype, n = Text.prototype;
    xi = pt(t, "firstChild").get, pi = pt(t, "nextSibling").get, ba(e) && (e.__click = void 0, e.__className = void 0, e.__attributes = null, e.__style = void 0, e.__e = void 0), ba(n) && (n.__t = void 0);
  }
}
function lr(e = "") {
  return document.createTextNode(e);
}
// @__NO_SIDE_EFFECTS__
function dt(e) {
  return xi.call(e);
}
// @__NO_SIDE_EFFECTS__
function sr(e) {
  return pi.call(e);
}
function b(e, t) {
  return /* @__PURE__ */ dt(e);
}
function Se(e, t) {
  {
    var n = (
      /** @type {DocumentFragment} */
      /* @__PURE__ */ dt(
        /** @type {Node} */
        e
      )
    );
    return n instanceof Comment && n.data === "" ? /* @__PURE__ */ sr(n) : n;
  }
}
function m(e, t = 1, n = !1) {
  let r = e;
  for (; t--; )
    r = /** @type {TemplateNode} */
    /* @__PURE__ */ sr(r);
  return r;
}
function Yl(e) {
  e.textContent = "";
}
function Xl(e) {
  he === null && ve === null && Fl(), ve !== null && (ve.f & We) !== 0 && he === null && Nl(), en && Ll();
}
function Gl(e, t) {
  var n = t.last;
  n === null ? t.last = t.first = e : (n.next = e, e.prev = n, t.last = e);
}
function Jt(e, t, n, r = !0) {
  var a = he, l = {
    ctx: Ve,
    deps: null,
    nodes_start: null,
    nodes_end: null,
    f: e | lt,
    first: null,
    fn: t,
    last: null,
    next: null,
    parent: a,
    prev: null,
    teardown: null,
    transitions: null,
    wv: 0
  };
  if (n)
    try {
      Qr(l), l.f |= Al;
    } catch (u) {
      throw gt(l), u;
    }
  else t !== null && ur(l);
  var s = n && l.deps === null && l.first === null && l.nodes_start === null && l.teardown === null && (l.f & (fi | Pn)) === 0;
  if (!s && r && (a !== null && Gl(l, a), ve !== null && (ve.f & $e) !== 0)) {
    var o = (
      /** @type {Derived} */
      ve
    );
    (o.effects ?? (o.effects = [])).push(l);
  }
  return l;
}
function wi(e) {
  const t = Jt(nr, null, !1);
  return et(t, Be), t.teardown = e, t;
}
function Er(e) {
  Xl();
  var t = he !== null && (he.f & ht) !== 0 && Ve !== null && !Ve.m;
  if (t) {
    var n = (
      /** @type {ComponentContext} */
      Ve
    );
    (n.e ?? (n.e = [])).push({
      fn: e,
      effect: he,
      reaction: ve
    });
  } else {
    var r = $t(e);
    return r;
  }
}
function Ul(e) {
  const t = Jt(Qt, e, !0);
  return (n = {}) => new Promise((r) => {
    n.outro ? Dn(t, () => {
      gt(t), r(void 0);
    }) : (gt(t), r(void 0));
  });
}
function $t(e) {
  return Jt(oi, e, !1);
}
function Ur(e) {
  return Jt(nr, e, !0);
}
function te(e, t = [], n = ir) {
  const r = t.map(n);
  return or(() => e(...r.map(i)));
}
function or(e, t = 0) {
  return Jt(nr | Xr | t, e, !0);
}
function Xt(e, t = !0) {
  return Jt(nr | ht, e, !0, t);
}
function yi(e) {
  var t = e.teardown;
  if (t !== null) {
    const n = en, r = ve;
    pa(!0), st(null);
    try {
      t.call(null);
    } finally {
      pa(n), st(r);
    }
  }
}
function ki(e, t = !1) {
  var n = e.first;
  for (e.first = e.last = null; n !== null; ) {
    var r = n.next;
    (n.f & Qt) !== 0 ? n.parent = null : gt(n, t), n = r;
  }
}
function Kl(e) {
  for (var t = e.first; t !== null; ) {
    var n = t.next;
    (t.f & ht) === 0 && gt(t), t = n;
  }
}
function gt(e, t = !0) {
  var n = !1;
  (t || (e.f & ql) !== 0) && e.nodes_start !== null && (Zl(
    e.nodes_start,
    /** @type {TemplateNode} */
    e.nodes_end
  ), n = !0), ki(e, t && !n), jn(e, 0), et(e, rr);
  var r = e.transitions;
  if (r !== null)
    for (const l of r)
      l.stop();
  yi(e);
  var a = e.parent;
  a !== null && a.first !== null && Mi(e), e.next = e.prev = e.teardown = e.ctx = e.deps = e.fn = e.nodes_start = e.nodes_end = null;
}
function Zl(e, t) {
  for (; e !== null; ) {
    var n = e === t ? null : (
      /** @type {TemplateNode} */
      /* @__PURE__ */ sr(e)
    );
    e.remove(), e = n;
  }
}
function Mi(e) {
  var t = e.parent, n = e.prev, r = e.next;
  n !== null && (n.next = r), r !== null && (r.prev = n), t !== null && (t.first === e && (t.first = r), t.last === e && (t.last = n));
}
function Dn(e, t) {
  var n = [];
  Kr(e, n, !0), Ti(n, () => {
    gt(e), t && t();
  });
}
function Ti(e, t) {
  var n = e.length;
  if (n > 0) {
    var r = () => --n || t();
    for (var a of e)
      a.out(r);
  } else
    t();
}
function Kr(e, t, n) {
  if ((e.f & vt) === 0) {
    if (e.f ^= vt, e.transitions !== null)
      for (const s of e.transitions)
        (s.is_global || n) && t.push(s);
    for (var r = e.first; r !== null; ) {
      var a = r.next, l = (r.f & ar) !== 0 || (r.f & ht) !== 0;
      Kr(r, t, l ? n : !1), r = a;
    }
  }
}
function zn(e) {
  Ai(e, !0);
}
function Ai(e, t) {
  if ((e.f & vt) !== 0) {
    e.f ^= vt, (e.f & Be) === 0 && (e.f ^= Be), yn(e) && (et(e, lt), ur(e));
    for (var n = e.first; n !== null; ) {
      var r = n.next, a = (n.f & ar) !== 0 || (n.f & ht) !== 0;
      Ai(n, a ? t : !1), n = r;
    }
    if (e.transitions !== null)
      for (const l of e.transitions)
        (l.is_global || t) && l.in();
  }
}
let On = [];
function Ql() {
  var e = On;
  On = [], Tl(e);
}
function Zr(e) {
  On.length === 0 && queueMicrotask(Ql), On.push(e);
}
let En = !1, Lr = !1, Bn = null, At = !1, en = !1;
function pa(e) {
  en = e;
}
let Ln = [];
let ve = null, rt = !1;
function st(e) {
  ve = e;
}
let he = null;
function yt(e) {
  he = e;
}
let Fe = null;
function qi(e) {
  ve !== null && ve.f & qr && (Fe === null ? Fe = [e] : Fe.push(e));
}
let Ne = null, je = 0, Ge = null;
function Jl(e) {
  Ge = e;
}
let Si = 1, Hn = 0, xt = !1;
function Ei() {
  return ++Si;
}
function yn(e) {
  var c;
  var t = e.f;
  if ((t & lt) !== 0)
    return !0;
  if ((t & Ft) !== 0) {
    var n = e.deps, r = (t & We) !== 0;
    if (n !== null) {
      var a, l, s = (t & Rn) !== 0, o = r && he !== null && !xt, u = n.length;
      if (s || o) {
        var f = (
          /** @type {Derived} */
          e
        ), v = f.parent;
        for (a = 0; a < u; a++)
          l = n[a], (s || !((c = l == null ? void 0 : l.reactions) != null && c.includes(f))) && (l.reactions ?? (l.reactions = [])).push(f);
        s && (f.f ^= Rn), o && v !== null && (v.f & We) === 0 && (f.f ^= We);
      }
      for (a = 0; a < u; a++)
        if (l = n[a], yn(
          /** @type {Derived} */
          l
        ) && hi(
          /** @type {Derived} */
          l
        ), l.wv > e.wv)
          return !0;
    }
    (!r || he !== null && !xt) && et(e, Be);
  }
  return !1;
}
function $l(e, t) {
  for (var n = t; n !== null; ) {
    if ((n.f & Pn) !== 0)
      try {
        n.fn(e);
        return;
      } catch {
        n.f ^= Pn;
      }
    n = n.parent;
  }
  throw En = !1, e;
}
function wa(e) {
  return (e.f & rr) === 0 && (e.parent === null || (e.parent.f & Pn) === 0);
}
function fr(e, t, n, r) {
  if (En) {
    if (n === null && (En = !1), wa(t))
      throw e;
    return;
  }
  if (n !== null && (En = !0), $l(e, t), wa(t))
    throw e;
}
function Li(e, t, n = !0) {
  var r = e.reactions;
  if (r !== null)
    for (var a = 0; a < r.length; a++) {
      var l = r[a];
      Fe != null && Fe.includes(e) || ((l.f & $e) !== 0 ? Li(
        /** @type {Derived} */
        l,
        t,
        !1
      ) : t === l && (n ? et(l, lt) : (l.f & Be) !== 0 && et(l, Ft), ur(
        /** @type {Effect} */
        l
      )));
    }
}
function Ni(e) {
  var g;
  var t = Ne, n = je, r = Ge, a = ve, l = xt, s = Fe, o = Ve, u = rt, f = e.f;
  Ne = /** @type {null | Value[]} */
  null, je = 0, Ge = null, xt = (f & We) !== 0 && (rt || !At || ve === null), ve = (f & (ht | Qt)) === 0 ? e : null, Fe = null, _a(e.ctx), rt = !1, Hn++, e.f |= qr;
  try {
    var v = (
      /** @type {Function} */
      (0, e.fn)()
    ), c = e.deps;
    if (Ne !== null) {
      var d;
      if (jn(e, je), c !== null && je > 0)
        for (c.length = je + Ne.length, d = 0; d < Ne.length; d++)
          c[je + d] = Ne[d];
      else
        e.deps = c = Ne;
      if (!xt)
        for (d = je; d < c.length; d++)
          ((g = c[d]).reactions ?? (g.reactions = [])).push(e);
    } else c !== null && je < c.length && (jn(e, je), c.length = je);
    if (di() && Ge !== null && !rt && c !== null && (e.f & ($e | Ft | lt)) === 0)
      for (d = 0; d < /** @type {Source[]} */
      Ge.length; d++)
        Li(
          Ge[d],
          /** @type {Effect} */
          e
        );
    return a !== null && a !== e && (Hn++, Ge !== null && (r === null ? r = Ge : r.push(.../** @type {Source[]} */
    Ge))), v;
  } finally {
    Ne = t, je = n, Ge = r, ve = a, xt = l, Fe = s, _a(o), rt = u, e.f ^= qr;
  }
}
function es(e, t) {
  let n = t.reactions;
  if (n !== null) {
    var r = xl.call(n, e);
    if (r !== -1) {
      var a = n.length - 1;
      a === 0 ? n = t.reactions = null : (n[r] = n[a], n.pop());
    }
  }
  n === null && (t.f & $e) !== 0 && // Destroying a child effect while updating a parent effect can cause a dependency to appear
  // to be unused, when in fact it is used by the currently-updating parent. Checking `new_deps`
  // allows us to skip the expensive work of disconnecting and immediately reconnecting it
  (Ne === null || !Ne.includes(t)) && (et(t, Ft), (t.f & (We | Rn)) === 0 && (t.f ^= Rn), vi(
    /** @type {Derived} **/
    t
  ), jn(
    /** @type {Derived} **/
    t,
    0
  ));
}
function jn(e, t) {
  var n = e.deps;
  if (n !== null)
    for (var r = t; r < n.length; r++)
      es(e, n[r]);
}
function Qr(e) {
  var t = e.f;
  if ((t & rr) === 0) {
    et(e, Be);
    var n = he, r = Ve, a = At;
    he = e, At = !0;
    try {
      (t & Xr) !== 0 ? Kl(e) : ki(e), yi(e);
      var l = Ni(e);
      e.teardown = typeof l == "function" ? l : null, e.wv = Si;
      var s = e.deps, o;
      ha && zl && e.f & lt;
    } catch (u) {
      fr(u, e, n, r || e.ctx);
    } finally {
      At = a, he = n;
    }
  }
}
function ts() {
  try {
    Cl();
  } catch (e) {
    if (Bn !== null)
      fr(e, Bn, null);
    else
      throw e;
  }
}
function ns() {
  var e = At;
  try {
    var t = 0;
    for (At = !0; Ln.length > 0; ) {
      t++ > 1e3 && ts();
      var n = Ln, r = n.length;
      Ln = [];
      for (var a = 0; a < r; a++) {
        var l = as(n[a]);
        rs(l);
      }
      un.clear();
    }
  } finally {
    Lr = !1, At = e, Bn = null;
  }
}
function rs(e) {
  var t = e.length;
  if (t !== 0)
    for (var n = 0; n < t; n++) {
      var r = e[n];
      if ((r.f & (rr | vt)) === 0)
        try {
          yn(r) && (Qr(r), r.deps === null && r.first === null && r.nodes_start === null && (r.teardown === null ? Mi(r) : r.fn = null));
        } catch (a) {
          fr(a, r, null, r.ctx);
        }
    }
}
function ur(e) {
  Lr || (Lr = !0, queueMicrotask(ns));
  for (var t = Bn = e; t.parent !== null; ) {
    t = t.parent;
    var n = t.f;
    if ((n & (Qt | ht)) !== 0) {
      if ((n & Be) === 0) return;
      t.f ^= Be;
    }
  }
  Ln.push(t);
}
function as(e) {
  for (var t = [], n = e; n !== null; ) {
    var r = n.f, a = (r & (ht | Qt)) !== 0, l = a && (r & Be) !== 0;
    if (!l && (r & vt) === 0) {
      if ((r & oi) !== 0)
        t.push(n);
      else if (a)
        n.f ^= Be;
      else
        try {
          yn(n) && Qr(n);
        } catch (u) {
          fr(u, n, null, n.ctx);
        }
      var s = n.first;
      if (s !== null) {
        n = s;
        continue;
      }
    }
    var o = n.parent;
    for (n = n.next; n === null && o !== null; )
      n = o.next, o = o.parent;
  }
  return t;
}
function i(e) {
  var t = e.f, n = (t & $e) !== 0;
  if (ve !== null && !rt) {
    if (!(Fe != null && Fe.includes(e))) {
      var r = ve.deps;
      e.rv < Hn && (e.rv = Hn, Ne === null && r !== null && r[je] === e ? je++ : Ne === null ? Ne = [e] : (!xt || !Ne.includes(e)) && Ne.push(e));
    }
  } else if (n && /** @type {Derived} */
  e.deps === null && /** @type {Derived} */
  e.effects === null) {
    var a = (
      /** @type {Derived} */
      e
    ), l = a.parent;
    l !== null && (l.f & We) === 0 && (a.f ^= We);
  }
  return n && (a = /** @type {Derived} */
  e, yn(a) && hi(a)), en && un.has(e) ? un.get(e) : e.v;
}
function Lt(e) {
  var t = rt;
  try {
    return rt = !0, e();
  } finally {
    rt = t;
  }
}
const is = -7169;
function et(e, t) {
  e.f = e.f & is | t;
}
let ya = !1;
function ls() {
  ya || (ya = !0, document.addEventListener(
    "reset",
    (e) => {
      Promise.resolve().then(() => {
        var t;
        if (!e.defaultPrevented)
          for (
            const n of
            /**@type {HTMLFormElement} */
            e.target.elements
          )
            (t = n.__on_r) == null || t.call(n);
      });
    },
    // In the capture phase to guarantee we get noticed of it (no possiblity of stopPropagation)
    { capture: !0 }
  ));
}
function Fi(e) {
  var t = ve, n = he;
  st(null), yt(null);
  try {
    return e();
  } finally {
    st(t), yt(n);
  }
}
function Jr(e, t, n, r = n) {
  e.addEventListener(t, () => Fi(n));
  const a = e.__on_r;
  a ? e.__on_r = () => {
    a(), r(!0);
  } : e.__on_r = () => r(!0), ls();
}
const Ci = /* @__PURE__ */ new Set(), Nr = /* @__PURE__ */ new Set();
function ss(e, t, n, r = {}) {
  function a(l) {
    if (r.capture || ln.call(t, l), !l.cancelBubble)
      return Fi(() => n == null ? void 0 : n.call(this, l));
  }
  return e.startsWith("pointer") || e.startsWith("touch") || e === "wheel" ? Zr(() => {
    t.addEventListener(e, a, r);
  }) : t.addEventListener(e, a, r), a;
}
function Ke(e, t, n, r, a) {
  var l = { capture: r, passive: a }, s = ss(e, t, n, l);
  (t === document.body || // @ts-ignore
  t === window || // @ts-ignore
  t === document || // Firefox has quirky behavior, it can happen that we still get "canplay" events when the element is already removed
  t instanceof HTMLMediaElement) && wi(() => {
    t.removeEventListener(e, s, l);
  });
}
function Ct(e) {
  for (var t = 0; t < e.length; t++)
    Ci.add(e[t]);
  for (var n of Nr)
    n(e);
}
function ln(e) {
  var k;
  var t = this, n = (
    /** @type {Node} */
    t.ownerDocument
  ), r = e.type, a = ((k = e.composedPath) == null ? void 0 : k.call(e)) || [], l = (
    /** @type {null | Element} */
    a[0] || e.target
  ), s = 0, o = e.__root;
  if (o) {
    var u = a.indexOf(o);
    if (u !== -1 && (t === document || t === /** @type {any} */
    window)) {
      e.__root = t;
      return;
    }
    var f = a.indexOf(t);
    if (f === -1)
      return;
    u <= f && (s = u);
  }
  if (l = /** @type {Element} */
  a[s] || e.target, l !== t) {
    pl(e, "currentTarget", {
      configurable: !0,
      get() {
        return l || n;
      }
    });
    var v = ve, c = he;
    st(null), yt(null);
    try {
      for (var d, g = []; l !== null; ) {
        var h = l.assignedSlot || l.parentNode || /** @type {any} */
        l.host || null;
        try {
          var _ = l["__" + r];
          if (_ != null && (!/** @type {any} */
          l.disabled || // DOM could've been updated already by the time this is reached, so we check this as well
          // -> the target could not have been disabled because it emits the event in the first place
          e.target === l))
            if (tr(_)) {
              var [p, ...E] = _;
              p.apply(l, [e, ...E]);
            } else
              _.call(l, e);
        } catch (T) {
          d ? g.push(T) : d = T;
        }
        if (e.cancelBubble || h === t || h === null)
          break;
        l = h;
      }
      if (d) {
        for (let T of g)
          queueMicrotask(() => {
            throw T;
          });
        throw d;
      }
    } finally {
      e.__root = t, delete e.currentTarget, st(v), yt(c);
    }
  }
}
function Pi(e) {
  var t = document.createElement("template");
  return t.innerHTML = e.replaceAll("<!>", "<!---->"), t.content;
}
function Gt(e, t) {
  var n = (
    /** @type {Effect} */
    he
  );
  n.nodes_start === null && (n.nodes_start = e, n.nodes_end = t);
}
// @__NO_SIDE_EFFECTS__
function ne(e, t) {
  var n = (t & li) !== 0, r = (t & _l) !== 0, a, l = !e.startsWith("<!>");
  return () => {
    a === void 0 && (a = Pi(l ? e : "<!>" + e), n || (a = /** @type {Node} */
    /* @__PURE__ */ dt(a)));
    var s = (
      /** @type {TemplateNode} */
      r || mi ? document.importNode(a, !0) : a.cloneNode(!0)
    );
    if (n) {
      var o = (
        /** @type {TemplateNode} */
        /* @__PURE__ */ dt(s)
      ), u = (
        /** @type {TemplateNode} */
        s.lastChild
      );
      Gt(o, u);
    } else
      Gt(s, s);
    return s;
  };
}
// @__NO_SIDE_EFFECTS__
function os(e, t, n = "svg") {
  var r = !e.startsWith("<!>"), a = (t & li) !== 0, l = `<${n}>${r ? e : "<!>" + e}</${n}>`, s;
  return () => {
    if (!s) {
      var o = (
        /** @type {DocumentFragment} */
        Pi(l)
      ), u = (
        /** @type {Element} */
        /* @__PURE__ */ dt(o)
      );
      if (a)
        for (s = document.createDocumentFragment(); /* @__PURE__ */ dt(u); )
          s.appendChild(
            /** @type {Node} */
            /* @__PURE__ */ dt(u)
          );
      else
        s = /** @type {Element} */
        /* @__PURE__ */ dt(u);
    }
    var f = (
      /** @type {TemplateNode} */
      s.cloneNode(!0)
    );
    if (a) {
      var v = (
        /** @type {TemplateNode} */
        /* @__PURE__ */ dt(f)
      ), c = (
        /** @type {TemplateNode} */
        f.lastChild
      );
      Gt(v, c);
    } else
      Gt(f, f);
    return f;
  };
}
// @__NO_SIDE_EFFECTS__
function ke(e, t) {
  return /* @__PURE__ */ os(e, t, "svg");
}
function ka(e = "") {
  {
    var t = lr(e + "");
    return Gt(t, t), t;
  }
}
function Nt() {
  var e = document.createDocumentFragment(), t = document.createComment(""), n = lr();
  return e.append(t, n), Gt(t, n), e;
}
function D(e, t) {
  e !== null && e.before(
    /** @type {Node} */
    t
  );
}
function fs() {
  var e;
  return (e = window.__svelte ?? (window.__svelte = {})).uid ?? (e.uid = 1), `c${window.__svelte.uid++}`;
}
const us = ["touchstart", "touchmove"];
function cs(e) {
  return us.includes(e);
}
function de(e, t) {
  var n = t == null ? "" : typeof t == "object" ? t + "" : t;
  n !== (e.__t ?? (e.__t = e.nodeValue)) && (e.__t = n, e.nodeValue = n + "");
}
function ds(e, t) {
  return vs(e, t);
}
const Rt = /* @__PURE__ */ new Map();
function vs(e, { target: t, anchor: n, props: r = {}, events: a, context: l, intro: s = !0 }) {
  Vl();
  var o = /* @__PURE__ */ new Set(), u = (c) => {
    for (var d = 0; d < c.length; d++) {
      var g = c[d];
      if (!o.has(g)) {
        o.add(g);
        var h = cs(g);
        t.addEventListener(g, ln, { passive: h });
        var _ = Rt.get(g);
        _ === void 0 ? (document.addEventListener(g, ln, { passive: h }), Rt.set(g, 1)) : Rt.set(g, _ + 1);
      }
    }
  };
  u(Yr(Ci)), Nr.add(u);
  var f = void 0, v = Ul(() => {
    var c = n ?? t.appendChild(lr());
    return Xt(() => {
      if (l) {
        pe({});
        var d = (
          /** @type {ComponentContext} */
          Ve
        );
        d.c = l;
      }
      a && (r.$$events = a), f = e(c, r) || {}, l && we();
    }), () => {
      var h;
      for (var d of o) {
        t.removeEventListener(d, ln);
        var g = (
          /** @type {number} */
          Rt.get(d)
        );
        --g === 0 ? (document.removeEventListener(d, ln), Rt.delete(d)) : Rt.set(d, g);
      }
      Nr.delete(u), c !== n && ((h = c.parentNode) == null || h.removeChild(c));
    };
  });
  return Fr.set(f, v), f;
}
let Fr = /* @__PURE__ */ new WeakMap();
function gs(e, t) {
  const n = Fr.get(e);
  return n ? (Fr.delete(e), n(t)) : Promise.resolve();
}
function Cr(e, t, ...n) {
  var r = e, a = Ml, l;
  or(() => {
    a !== (a = t()) && (l && (gt(l), l = null), l = Xt(() => (
      /** @type {SnippetFn} */
      a(r, ...n)
    )));
  }, ar);
}
function se(e, t, [n, r] = [0, 0]) {
  var a = e, l = null, s = null, o = Ie, u = n > 0 ? ar : 0, f = !1;
  const v = (d, g = !0) => {
    f = !0, c(g, d);
  }, c = (d, g) => {
    o !== (o = d) && (o ? (l ? zn(l) : g && (l = Xt(() => g(a))), s && Dn(s, () => {
      s = null;
    })) : (s ? zn(s) : g && (s = Xt(() => g(a, [n + 1, r]))), l && Dn(l, () => {
      l = null;
    })));
  };
  or(() => {
    f = !1, t(v), f || c(null, null);
  }, u);
}
function Te(e, t) {
  return t;
}
function hs(e, t, n, r) {
  for (var a = [], l = t.length, s = 0; s < l; s++)
    Kr(t[s].e, a, !0);
  var o = l > 0 && a.length === 0 && n !== null;
  if (o) {
    var u = (
      /** @type {Element} */
      /** @type {Element} */
      n.parentNode
    );
    Yl(u), u.append(
      /** @type {Element} */
      n
    ), r.clear(), bt(e, t[0].prev, t[l - 1].next);
  }
  Ti(a, () => {
    for (var f = 0; f < l; f++) {
      var v = t[f];
      o || (r.delete(v.k), bt(e, v.prev, v.next)), gt(v.e, !o);
    }
  });
}
function Ae(e, t, n, r, a, l = null) {
  var s = e, o = { flags: t, items: /* @__PURE__ */ new Map(), first: null }, u = (t & ii) !== 0;
  if (u) {
    var f = (
      /** @type {Element} */
      e
    );
    s = f.appendChild(lr());
  }
  var v = null, c = !1, d = /* @__PURE__ */ Bl(() => {
    var g = n();
    return tr(g) ? g : g == null ? [] : Yr(g);
  });
  or(() => {
    var g = i(d), h = g.length;
    c && h === 0 || (c = h === 0, bs(g, o, s, a, t, r, n), l !== null && (h === 0 ? v ? zn(v) : v = Xt(() => l(s)) : v !== null && Dn(v, () => {
      v = null;
    })), i(d));
  });
}
function bs(e, t, n, r, a, l, s) {
  var R, P, F, G;
  var o = (a & cl) !== 0, u = (a & (Wr | Vr)) !== 0, f = e.length, v = t.items, c = t.first, d = c, g, h = null, _, p = [], E = [], k, T, w, q;
  if (o)
    for (q = 0; q < f; q += 1)
      k = e[q], T = l(k, q), w = v.get(T), w !== void 0 && ((R = w.a) == null || R.measure(), (_ ?? (_ = /* @__PURE__ */ new Set())).add(w));
  for (q = 0; q < f; q += 1) {
    if (k = e[q], T = l(k, q), w = v.get(T), w === void 0) {
      var L = d ? (
        /** @type {TemplateNode} */
        d.e.nodes_start
      ) : n;
      h = ms(
        L,
        t,
        h,
        h === null ? t.first : h.next,
        k,
        T,
        q,
        r,
        a,
        s
      ), v.set(T, h), p = [], E = [], d = h.next;
      continue;
    }
    if (u && _s(w, k, q, a), (w.e.f & vt) !== 0 && (zn(w.e), o && ((P = w.a) == null || P.unfix(), (_ ?? (_ = /* @__PURE__ */ new Set())).delete(w))), w !== d) {
      if (g !== void 0 && g.has(w)) {
        if (p.length < E.length) {
          var C = E[0], I;
          h = C.prev;
          var X = p[0], $ = p[p.length - 1];
          for (I = 0; I < p.length; I += 1)
            Ma(p[I], C, n);
          for (I = 0; I < E.length; I += 1)
            g.delete(E[I]);
          bt(t, X.prev, $.next), bt(t, h, X), bt(t, $, C), d = C, h = $, q -= 1, p = [], E = [];
        } else
          g.delete(w), Ma(w, d, n), bt(t, w.prev, w.next), bt(t, w, h === null ? t.first : h.next), bt(t, h, w), h = w;
        continue;
      }
      for (p = [], E = []; d !== null && d.k !== T; )
        (d.e.f & vt) === 0 && (g ?? (g = /* @__PURE__ */ new Set())).add(d), E.push(d), d = d.next;
      if (d === null)
        continue;
      w = d;
    }
    p.push(w), h = w, d = w.next;
  }
  if (d !== null || g !== void 0) {
    for (var A = g === void 0 ? [] : Yr(g); d !== null; )
      (d.e.f & vt) === 0 && A.push(d), d = d.next;
    var S = A.length;
    if (S > 0) {
      var y = (a & ii) !== 0 && f === 0 ? n : null;
      if (o) {
        for (q = 0; q < S; q += 1)
          (F = A[q].a) == null || F.measure();
        for (q = 0; q < S; q += 1)
          (G = A[q].a) == null || G.fix();
      }
      hs(t, A, y, v);
    }
  }
  o && Zr(() => {
    var O;
    if (_ !== void 0)
      for (w of _)
        (O = w.a) == null || O.apply();
  }), he.first = t.first && t.first.e, he.last = h && h.e;
}
function _s(e, t, n, r) {
  (r & Wr) !== 0 && Sr(e.v, t), (r & Vr) !== 0 ? Sr(
    /** @type {Value<number>} */
    e.i,
    n
  ) : e.i = n;
}
function ms(e, t, n, r, a, l, s, o, u, f) {
  var v = (u & Wr) !== 0, c = (u & dl) === 0, d = v ? c ? /* @__PURE__ */ bi(a) : In(a) : a, g = (u & Vr) === 0 ? s : In(s), h = {
    i: g,
    v: d,
    k: l,
    a: null,
    // @ts-expect-error
    e: null,
    prev: n,
    next: r
  };
  try {
    return h.e = Xt(() => o(e, d, g, f), Wl), h.e.prev = n && n.e, h.e.next = r && r.e, n === null ? t.first = h : (n.next = h, n.e.next = h.e), r !== null && (r.prev = h, r.e.prev = h.e), h;
  } finally {
  }
}
function Ma(e, t, n) {
  for (var r = e.next ? (
    /** @type {TemplateNode} */
    e.next.e.nodes_start
  ) : n, a = t ? (
    /** @type {TemplateNode} */
    t.e.nodes_start
  ) : n, l = (
    /** @type {TemplateNode} */
    e.e.nodes_start
  ); l !== r; ) {
    var s = (
      /** @type {TemplateNode} */
      /* @__PURE__ */ sr(l)
    );
    a.before(l), l = s;
  }
}
function bt(e, t, n) {
  t === null ? e.first = n : (t.next = n, t.e.next = n && n.e), n !== null && (n.prev = t, n.e.prev = t && t.e);
}
function Ri(e) {
  var t, n, r = "";
  if (typeof e == "string" || typeof e == "number") r += e;
  else if (typeof e == "object") if (Array.isArray(e)) {
    var a = e.length;
    for (t = 0; t < a; t++) e[t] && (n = Ri(e[t])) && (r && (r += " "), r += n);
  } else for (n in e) e[n] && (r && (r += " "), r += n);
  return r;
}
function xs() {
  for (var e, t, n = 0, r = "", a = arguments.length; n < a; n++) (e = arguments[n]) && (t = Ri(e)) && (r && (r += " "), r += t);
  return r;
}
function ps(e) {
  return typeof e == "object" ? xs(e) : e ?? "";
}
const Ta = [...` 	
\r\f \v\uFEFF`];
function ws(e, t, n) {
  var r = e == null ? "" : "" + e;
  if (t && (r = r ? r + " " + t : t), n) {
    for (var a in n)
      if (n[a])
        r = r ? r + " " + a : a;
      else if (r.length)
        for (var l = a.length, s = 0; (s = r.indexOf(a, s)) >= 0; ) {
          var o = s + l;
          (s === 0 || Ta.includes(r[s - 1])) && (o === r.length || Ta.includes(r[o])) ? r = (s === 0 ? "" : r.substring(0, s)) + r.substring(o + 1) : s = o;
        }
  }
  return r === "" ? null : r;
}
function Aa(e, t = !1) {
  var n = t ? " !important;" : ";", r = "";
  for (var a in e) {
    var l = e[a];
    l != null && l !== "" && (r += " " + a + ": " + l + n);
  }
  return r;
}
function pr(e) {
  return e[0] !== "-" || e[1] !== "-" ? e.toLowerCase() : e;
}
function ys(e, t) {
  if (t) {
    var n = "", r, a;
    if (Array.isArray(t) ? (r = t[0], a = t[1]) : r = t, e) {
      e = String(e).replaceAll(/\s*\/\*.*?\*\/\s*/g, "").trim();
      var l = !1, s = 0, o = !1, u = [];
      r && u.push(...Object.keys(r).map(pr)), a && u.push(...Object.keys(a).map(pr));
      var f = 0, v = -1;
      const _ = e.length;
      for (var c = 0; c < _; c++) {
        var d = e[c];
        if (o ? d === "/" && e[c - 1] === "*" && (o = !1) : l ? l === d && (l = !1) : d === "/" && e[c + 1] === "*" ? o = !0 : d === '"' || d === "'" ? l = d : d === "(" ? s++ : d === ")" && s--, !o && l === !1 && s === 0) {
          if (d === ":" && v === -1)
            v = c;
          else if (d === ";" || c === _ - 1) {
            if (v !== -1) {
              var g = pr(e.substring(f, v).trim());
              if (!u.includes(g)) {
                d !== ";" && c++;
                var h = e.substring(f, c).trim();
                n += " " + h + ";";
              }
            }
            f = c + 1, v = -1;
          }
        }
      }
    }
    return r && (n += Aa(r)), a && (n += Aa(a, !0)), n = n.trim(), n === "" ? null : n;
  }
  return e == null ? null : String(e);
}
function ze(e, t, n, r, a, l) {
  var s = e.__className;
  if (s !== n || s === void 0) {
    var o = ws(n, r, l);
    o == null ? e.removeAttribute("class") : e.className = o, e.__className = n;
  } else if (l && a !== l)
    for (var u in l) {
      var f = !!l[u];
      (a == null || f !== !!a[u]) && e.classList.toggle(u, f);
    }
  return l;
}
function wr(e, t = {}, n, r) {
  for (var a in n) {
    var l = n[a];
    t[a] !== l && (n[a] == null ? e.style.removeProperty(a) : e.style.setProperty(a, l, r));
  }
}
function Ce(e, t, n, r) {
  var a = e.__style;
  if (a !== t) {
    var l = ys(t, r);
    l == null ? e.removeAttribute("style") : e.style.cssText = l, e.__style = t;
  } else r && (Array.isArray(r) ? (wr(e, n == null ? void 0 : n[0], r[0]), wr(e, n == null ? void 0 : n[1], r[1], "important")) : wr(e, n, r));
  return r;
}
function zt(e, t, n) {
  if (e.multiple) {
    if (t == null)
      return;
    if (!tr(t))
      return jl();
    for (var r of e.options)
      r.selected = t.includes(on(r));
    return;
  }
  for (r of e.options) {
    var a = on(r);
    if (Ol(a, t)) {
      r.selected = !0;
      return;
    }
  }
  (!n || t !== void 0) && (e.selectedIndex = -1);
}
function Nn(e, t) {
  let n = !0;
  $t(() => {
    t && zt(e, Lt(t), n), n = !1;
    var r = new MutationObserver(() => {
      var a = e.__value;
      zt(e, a);
    });
    return r.observe(e, {
      // Listen to option element changes
      childList: !0,
      subtree: !0,
      // because of <optgroup>
      // Listen to option element value attribute changes
      // (doesn't get notified of select value changes,
      // because that property is not reflected as an attribute)
      attributes: !0,
      attributeFilter: ["value"]
    }), () => {
      r.disconnect();
    };
  });
}
function ks(e, t, n = t) {
  var r = !0;
  Jr(e, "change", (a) => {
    var l = a ? "[selected]" : ":checked", s;
    if (e.multiple)
      s = [].map.call(e.querySelectorAll(l), on);
    else {
      var o = e.querySelector(l) ?? // will fall back to first non-disabled option if no option is selected
      e.querySelector("option:not([disabled])");
      s = o && on(o);
    }
    n(s);
  }), $t(() => {
    var a = t();
    if (zt(e, a, r), r && a === void 0) {
      var l = e.querySelector(":checked");
      l !== null && (a = on(l), n(a));
    }
    e.__value = a, r = !1;
  }), Nn(e);
}
function on(e) {
  return "__value" in e ? e.__value : e.value;
}
const Ms = Symbol("is custom element"), Ts = Symbol("is html");
function qa(e, t) {
  var n = $r(e);
  n.value === (n.value = // treat null and undefined the same for the initial value
  t ?? void 0) || // @ts-expect-error
  // `progress` elements always need their value set when it's `0`
  e.value === t && (t !== 0 || e.nodeName !== "PROGRESS") || (e.value = t ?? "");
}
function Sa(e, t) {
  var n = $r(e);
  n.checked !== (n.checked = // treat null and undefined the same for the initial value
  t ?? void 0) && (e.checked = t);
}
function M(e, t, n, r) {
  var a = $r(e);
  a[t] !== (a[t] = n) && (t === "loading" && (e[Sl] = n), n == null ? e.removeAttribute(t) : typeof n != "string" && As(e).includes(t) ? e[t] = n : e.setAttribute(t, n));
}
function $r(e) {
  return (
    /** @type {Record<string | symbol, unknown>} **/
    // @ts-expect-error
    e.__attributes ?? (e.__attributes = {
      [Ms]: e.nodeName.includes("-"),
      [Ts]: e.namespaceURI === ml
    })
  );
}
var Ea = /* @__PURE__ */ new Map();
function As(e) {
  var t = Ea.get(e.nodeName);
  if (t) return t;
  Ea.set(e.nodeName, t = []);
  for (var n, r = e, a = Element.prototype; a !== r; ) {
    n = wl(r);
    for (var l in n)
      n[l].set && t.push(l);
    r = si(r);
  }
  return t;
}
function cr(e, t, n = t) {
  Jr(e, "input", (r) => {
    var a = r ? e.defaultValue : e.value;
    if (a = yr(e) ? kr(a) : a, n(a), a !== (a = t())) {
      var l = e.selectionStart, s = e.selectionEnd;
      e.value = a ?? "", s !== null && (e.selectionStart = l, e.selectionEnd = Math.min(s, e.value.length));
    }
  }), // If we are hydrating and the value has since changed,
  // then use the updated value from the input instead.
  // If defaultValue is set, then value == defaultValue
  // TODO Svelte 6: remove input.value check and set to empty string?
  Lt(t) == null && e.value && n(yr(e) ? kr(e.value) : e.value), Ur(() => {
    var r = t();
    yr(e) && r === kr(e.value) || e.type === "date" && !r && !e.value || r !== e.value && (e.value = r ?? "");
  });
}
function cn(e, t, n = t) {
  Jr(e, "change", (r) => {
    var a = r ? e.defaultChecked : e.checked;
    n(a);
  }), // If we are hydrating and the value has since changed,
  // then use the update value from the input instead.
  // If defaultChecked is set, then checked == defaultChecked
  Lt(t) == null && n(e.checked), Ur(() => {
    var r = t();
    e.checked = !!r;
  });
}
function yr(e) {
  var t = e.type;
  return t === "number" || t === "range";
}
function kr(e) {
  return e === "" ? null : +e;
}
var _t, jt, _n, $n, Ii;
const er = class er {
  /** @param {ResizeObserverOptions} options */
  constructor(t) {
    Le(this, $n);
    /** */
    Le(this, _t, /* @__PURE__ */ new WeakMap());
    /** @type {ResizeObserver | undefined} */
    Le(this, jt);
    /** @type {ResizeObserverOptions} */
    Le(this, _n);
    He(this, _n, t);
  }
  /**
   * @param {Element} element
   * @param {(entry: ResizeObserverEntry) => any} listener
   */
  observe(t, n) {
    var r = oe(this, _t).get(t) || /* @__PURE__ */ new Set();
    return r.add(n), oe(this, _t).set(t, r), ga(this, $n, Ii).call(this).observe(t, oe(this, _n)), () => {
      var a = oe(this, _t).get(t);
      a.delete(n), a.size === 0 && (oe(this, _t).delete(t), oe(this, jt).unobserve(t));
    };
  }
};
_t = new WeakMap(), jt = new WeakMap(), _n = new WeakMap(), $n = new WeakSet(), Ii = function() {
  return oe(this, jt) ?? He(this, jt, new ResizeObserver(
    /** @param {any} entries */
    (t) => {
      for (var n of t) {
        er.entries.set(n.target, n);
        for (var r of oe(this, _t).get(n.target) || [])
          r(n);
      }
    }
  ));
}, /** @static */
va(er, "entries", /* @__PURE__ */ new WeakMap());
let Pr = er;
var qs = /* @__PURE__ */ new Pr({
  box: "border-box"
});
function Ue(e, t, n) {
  var r = qs.observe(e, () => n(e[t]));
  $t(() => (Lt(() => n(e[t])), r));
}
function La(e, t) {
  return e === t || (e == null ? void 0 : e[wt]) === t;
}
function Wn(e = {}, t, n, r) {
  return $t(() => {
    var a, l;
    return Ur(() => {
      a = l, l = [], Lt(() => {
        e !== n(...l) && (t(e, ...l), a && La(n(...a), e) && t(null, ...a));
      });
    }), () => {
      Zr(() => {
        l && La(n(...l), e) && t(null, ...l);
      });
    };
  }), e;
}
let Tn = !1;
function Ss(e) {
  var t = Tn;
  try {
    return Tn = !1, [e(), Tn];
  } finally {
    Tn = t;
  }
}
const Es = {
  get(e, t) {
    let n = e.props.length;
    for (; n--; ) {
      let r = e.props[n];
      if (rn(r) && (r = r()), typeof r == "object" && r !== null && t in r) return r[t];
    }
  },
  set(e, t, n) {
    let r = e.props.length;
    for (; r--; ) {
      let a = e.props[r];
      rn(a) && (a = a());
      const l = pt(a, t);
      if (l && l.set)
        return l.set(n), !0;
    }
    return !1;
  },
  getOwnPropertyDescriptor(e, t) {
    let n = e.props.length;
    for (; n--; ) {
      let r = e.props[n];
      if (rn(r) && (r = r()), typeof r == "object" && r !== null && t in r) {
        const a = pt(r, t);
        return a && !a.configurable && (a.configurable = !0), a;
      }
    }
  },
  has(e, t) {
    if (t === wt || t === ui) return !1;
    for (let n of e.props)
      if (rn(n) && (n = n()), n != null && t in n) return !0;
    return !1;
  },
  ownKeys(e) {
    const t = [];
    for (let n of e.props)
      if (rn(n) && (n = n()), !!n) {
        for (const r in n)
          t.includes(r) || t.push(r);
        for (const r of Object.getOwnPropertySymbols(n))
          t.includes(r) || t.push(r);
      }
    return t;
  }
};
function dr(...e) {
  return new Proxy({ props: e }, Es);
}
function Na(e) {
  var t;
  return ((t = e.ctx) == null ? void 0 : t.d) ?? !1;
}
function N(e, t, n, r) {
  var q;
  var a = (n & vl) !== 0, l = !0, s = (n & hl) !== 0, o = (n & bl) !== 0, u = !1, f;
  s ? [f, u] = Ss(() => (
    /** @type {V} */
    e[t]
  )) : f = /** @type {V} */
  e[t];
  var v = wt in e || ui in e, c = s && (((q = pt(e, t)) == null ? void 0 : q.set) ?? (v && t in e && ((L) => e[t] = L))) || void 0, d = (
    /** @type {V} */
    r
  ), g = !0, h = !1, _ = () => (h = !0, g && (g = !1, o ? d = Lt(
    /** @type {() => V} */
    r
  ) : d = /** @type {V} */
  r), d);
  f === void 0 && r !== void 0 && (c && l && Pl(), f = _(), c && c(f));
  var p;
  if (p = () => {
    var L = (
      /** @type {V} */
      e[t]
    );
    return L === void 0 ? _() : (g = !0, h = !1, L);
  }, (n & gl) === 0)
    return p;
  if (c) {
    var E = e.$$legacy;
    return function(L, C) {
      return arguments.length > 0 ? ((!C || E || u) && c(C ? p() : L), L) : p();
    };
  }
  var k = !1, T = /* @__PURE__ */ bi(f), w = /* @__PURE__ */ ir(() => {
    var L = p(), C = i(T);
    return k ? (k = !1, C) : T.v = L;
  });
  return s && i(w), a || (w.equals = Gr), function(L, C) {
    if (arguments.length > 0) {
      const I = C ? i(w) : s ? nt(L) : L;
      if (!w.equals(I)) {
        if (k = !0, J(T, I), h && d !== void 0 && (d = I), Na(w))
          return L;
        Lt(() => i(w));
      }
      return L;
    }
    return Na(w) ? w.v : i(w);
  };
}
var Ls = (e, t, n) => t.changeTab(n()), Ns = /* @__PURE__ */ ne('<li class="svelte-1fi7f2s"><button> </button></li>'), Fs = /* @__PURE__ */ ne('<div class="svelte-1fi7f2s"><ul class="svelte-1fi7f2s"></ul></div>');
function Cs(e, t) {
  pe(t, !0);
  const n = [
    { value: "overview", title: "Overview" },
    { value: "table", title: "Feature Table" },
    { value: "detail", title: "Feature Detail" }
  ];
  var r = Fs(), a = b(r);
  Ae(a, 21, () => n, Te, (l, s) => {
    let o = () => i(s).value, u = () => i(s).title;
    var f = Ns(), v = b(f);
    v.__click = [Ls, t, o];
    let c;
    var d = b(v);
    te(
      (g) => {
        c = ze(v, 1, "svelte-1fi7f2s", null, c, g), de(d, u());
      },
      [
        () => ({
          "tab-selected": o() === t.selectedTab
        })
      ]
    ), D(l, f);
  }), D(e, r), we();
}
Ct(["click"]);
var mt, ut, Wt;
class an {
  constructor(t, n) {
    Le(this, mt);
    Le(this, ut);
    Le(this, Wt);
    He(this, mt, t), He(this, ut, n), He(this, Wt, /* @__PURE__ */ re(nt(oe(this, ut).get(oe(this, mt))))), oe(this, ut).on(`change:${oe(this, mt)}`, () => J(oe(this, Wt), oe(this, ut).get(oe(this, mt)), !0));
  }
  get value() {
    return i(oe(this, Wt));
  }
  set value(t) {
    oe(this, ut).set(oe(this, mt), t), oe(this, ut).save_changes();
  }
}
mt = new WeakMap(), ut = new WeakMap(), Wt = new WeakMap();
var Vt;
class De {
  constructor(t, n) {
    Le(this, Vt);
    He(this, Vt, /* @__PURE__ */ re(nt(n.get(t)))), n.on(`change:${t}`, () => J(oe(this, Vt), n.get(t), !0));
  }
  get value() {
    return i(oe(this, Vt));
  }
}
Vt = new WeakMap();
var ct, mn, xn, pn, wn;
class Ps {
  constructor(t) {
    Le(this, ct);
    Le(this, mn);
    Le(this, xn);
    Le(this, pn);
    Le(this, wn);
    He(this, ct, new De("base_font_size", t)), He(this, mn, /* @__PURE__ */ x(() => oe(this, ct).value * 0.75)), He(this, xn, /* @__PURE__ */ x(() => oe(this, ct).value * 0.875)), He(this, pn, /* @__PURE__ */ x(() => oe(this, ct).value * 1.125)), He(this, wn, /* @__PURE__ */ x(() => oe(this, ct).value * 1.25));
  }
  get base() {
    return oe(this, ct).value;
  }
  get xs() {
    return i(oe(this, mn));
  }
  get sm() {
    return i(oe(this, xn));
  }
  get lg() {
    return i(oe(this, pn));
  }
  get xl() {
    return i(oe(this, wn));
  }
}
ct = new WeakMap(), mn = new WeakMap(), xn = new WeakMap(), pn = new WeakMap(), wn = new WeakMap();
let Di, qe, Ot, Mt, ce, Rr, It, sn, Ir, ft, fn, Dr, Fn, Dt, le;
function Rs(e) {
  Di = new De("height", e), new De("n_table_rows", e), qe = new De("dataset_info", e), Ot = new De("model_info", e), new De("sae_ids", e), new De("sae_id", e), Mt = new De("sae_data", e), ce = new an("table_ranking_option", e), Rr = new an("table_min_act_rate", e), It = new an("table_page_index", e), sn = new De("max_table_page_index", e), new De("num_filtered_features", e), Ir = new De("table_features", e), ft = new De("detail_feature", e), fn = new an("detail_feature_id", e), Dr = new De("can_inference", e), Fn = new an("inference_input", e), Dt = new De("inference_output", e), le = new Ps(e);
}
var Is = /* @__PURE__ */ ke('<svg stroke-width="2" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" color="currentcolor"><path d="M12 11.5V16.5" stroke="currentcolor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path><path d="M12 7.51L12.01 7.49889" stroke="currentcolor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path><path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="currentcolor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg>');
function Ze(e, t) {
  pe(t, !0);
  let n = N(t, "width", 19, () => le.base), r = N(t, "height", 19, () => le.base);
  var a = Is();
  te(() => {
    M(a, "width", `${n() ?? ""}px`), M(a, "height", `${r() ?? ""}px`);
  }), D(e, a), we();
}
var Yt;
class Ds {
  constructor(t) {
    Le(this, Yt);
    He(this, Yt, /* @__PURE__ */ re(nt(t)));
  }
  get value() {
    return i(oe(this, Yt));
  }
  set value(t) {
    J(oe(this, Yt), t, !0);
  }
}
Yt = new WeakMap();
let ea;
function zs(e) {
  ea = new Ds(e);
}
function Os(e) {
  e.preventDefault();
}
var Bs = /* @__PURE__ */ ne('<div class="sae-tooltip-container svelte-1grq8y5"><button class="svelte-1grq8y5"><!></button> <div popover="auto" class="svelte-1grq8y5"><!></div></div>');
function Qe(e, t) {
  const n = fs();
  pe(t, !0);
  let r = N(t, "position", 3, "auto");
  function a(C, I, X, $, A) {
    if (I === null || X === null)
      return 0;
    const S = C / 2, y = X.height / 2;
    return A === "right" || A === "left" ? X.top + y - S : A === "bottom" || A === "auto" && X.top - C < I.top ? X.bottom + $ : X.top - C - $;
  }
  function l(C, I, X, $, A) {
    if (I === null || X === null)
      return 0;
    const S = C / 2, y = X.left + X.width / 2;
    return A === "right" || A === "auto" && y - S < I.left ? X.right + $ : A === "left" || A === "auto" && y + S > I.right ? X.left - C - $ : y - S;
  }
  const s = 4;
  let o = /* @__PURE__ */ re(void 0), u = /* @__PURE__ */ re(void 0), f = /* @__PURE__ */ re(0), v = /* @__PURE__ */ re(0), c = /* @__PURE__ */ re(null), d = /* @__PURE__ */ re(null), g = /* @__PURE__ */ x(() => a(i(v), i(d), i(c), s, r())), h = /* @__PURE__ */ x(() => l(i(f), i(d), i(c), s, r()));
  function _() {
    i(o) && i(u) && (J(c, i(o).getBoundingClientRect(), !0), J(d, ea.value.getBoundingClientRect(), !0), i(u).showPopover());
  }
  function p() {
    i(o) && i(u) && i(u).hidePopover();
  }
  var E = Bs(), k = b(E);
  k.__click = [Os];
  var T = b(k);
  Cr(T, () => t.trigger), Wn(k, (C) => J(o, C), () => i(o));
  var w = m(k, 2);
  let q;
  var L = b(w);
  Cr(L, () => t.content), Wn(w, (C) => J(u, C), () => i(u)), te(() => {
    M(k, "popovertarget", n), M(w, "id", n), q = Ce(w, "", q, {
      top: `${i(g) ?? ""}px`,
      left: `${i(h) ?? ""}px`
    });
  }), Ke("mouseenter", k, _), Ke("mouseleave", k, p), Ue(w, "offsetWidth", (C) => J(f, C)), Ue(w, "offsetHeight", (C) => J(v, C)), D(e, E), we();
}
Ct(["click"]);
function Cn(e, t) {
  return e == null || t == null ? NaN : e < t ? -1 : e > t ? 1 : e >= t ? 0 : NaN;
}
function zi(e, t) {
  return e == null || t == null ? NaN : t < e ? -1 : t > e ? 1 : t >= e ? 0 : NaN;
}
function Oi(e) {
  let t, n, r;
  e.length !== 2 ? (t = Cn, n = (o, u) => Cn(e(o), u), r = (o, u) => e(o) - u) : (t = e === Cn || e === zi ? e : Hs, n = e, r = e);
  function a(o, u, f = 0, v = o.length) {
    if (f < v) {
      if (t(u, u) !== 0) return v;
      do {
        const c = f + v >>> 1;
        n(o[c], u) < 0 ? f = c + 1 : v = c;
      } while (f < v);
    }
    return f;
  }
  function l(o, u, f = 0, v = o.length) {
    if (f < v) {
      if (t(u, u) !== 0) return v;
      do {
        const c = f + v >>> 1;
        n(o[c], u) <= 0 ? f = c + 1 : v = c;
      } while (f < v);
    }
    return f;
  }
  function s(o, u, f = 0, v = o.length) {
    const c = a(o, u, f, v - 1);
    return c > f && r(o[c - 1], u) > -r(o[c], u) ? c - 1 : c;
  }
  return { left: a, center: s, right: l };
}
function Hs() {
  return 0;
}
function js(e) {
  return e === null ? NaN : +e;
}
const Ws = Oi(Cn), Vs = Ws.right;
Oi(js).center;
function Ys(e, t) {
  let n, r;
  if (t === void 0)
    for (const a of e)
      a != null && (n === void 0 ? a >= a && (n = r = a) : (n > a && (n = a), r < a && (r = a)));
  else {
    let a = -1;
    for (let l of e)
      (l = t(l, ++a, e)) != null && (n === void 0 ? l >= l && (n = r = l) : (n > l && (n = l), r < l && (r = l)));
  }
  return [n, r];
}
class Fa extends Map {
  constructor(t, n = Us) {
    if (super(), Object.defineProperties(this, { _intern: { value: /* @__PURE__ */ new Map() }, _key: { value: n } }), t != null) for (const [r, a] of t) this.set(r, a);
  }
  get(t) {
    return super.get(Ca(this, t));
  }
  has(t) {
    return super.has(Ca(this, t));
  }
  set(t, n) {
    return super.set(Xs(this, t), n);
  }
  delete(t) {
    return super.delete(Gs(this, t));
  }
}
function Ca({ _intern: e, _key: t }, n) {
  const r = t(n);
  return e.has(r) ? e.get(r) : n;
}
function Xs({ _intern: e, _key: t }, n) {
  const r = t(n);
  return e.has(r) ? e.get(r) : (e.set(r, n), n);
}
function Gs({ _intern: e, _key: t }, n) {
  const r = t(n);
  return e.has(r) && (n = e.get(r), e.delete(r)), n;
}
function Us(e) {
  return e !== null && typeof e == "object" ? e.valueOf() : e;
}
const Ks = Math.sqrt(50), Zs = Math.sqrt(10), Qs = Math.sqrt(2);
function Vn(e, t, n) {
  const r = (t - e) / Math.max(0, n), a = Math.floor(Math.log10(r)), l = r / Math.pow(10, a), s = l >= Ks ? 10 : l >= Zs ? 5 : l >= Qs ? 2 : 1;
  let o, u, f;
  return a < 0 ? (f = Math.pow(10, -a) / s, o = Math.round(e * f), u = Math.round(t * f), o / f < e && ++o, u / f > t && --u, f = -f) : (f = Math.pow(10, a) * s, o = Math.round(e / f), u = Math.round(t / f), o * f < e && ++o, u * f > t && --u), u < o && 0.5 <= n && n < 2 ? Vn(e, t, n * 2) : [o, u, f];
}
function Js(e, t, n) {
  if (t = +t, e = +e, n = +n, !(n > 0)) return [];
  if (e === t) return [e];
  const r = t < e, [a, l, s] = r ? Vn(t, e, n) : Vn(e, t, n);
  if (!(l >= a)) return [];
  const o = l - a + 1, u = new Array(o);
  if (r)
    if (s < 0) for (let f = 0; f < o; ++f) u[f] = (l - f) / -s;
    else for (let f = 0; f < o; ++f) u[f] = (l - f) * s;
  else if (s < 0) for (let f = 0; f < o; ++f) u[f] = (a + f) / -s;
  else for (let f = 0; f < o; ++f) u[f] = (a + f) * s;
  return u;
}
function zr(e, t, n) {
  return t = +t, e = +e, n = +n, Vn(e, t, n)[2];
}
function $s(e, t, n) {
  t = +t, e = +e, n = +n;
  const r = t < e, a = r ? zr(t, e, n) : zr(e, t, n);
  return (r ? -1 : 1) * (a < 0 ? 1 / -a : a);
}
function eo(e, t) {
  let n;
  if (t === void 0)
    for (const r of e)
      r != null && (n < r || n === void 0 && r >= r) && (n = r);
  else {
    let r = -1;
    for (let a of e)
      (a = t(a, ++r, e)) != null && (n < a || n === void 0 && a >= a) && (n = a);
  }
  return n;
}
function to(e, t) {
  let n;
  if (t === void 0)
    for (const r of e)
      r != null && (n > r || n === void 0 && r >= r) && (n = r);
  else {
    let r = -1;
    for (let a of e)
      (a = t(a, ++r, e)) != null && (n > a || n === void 0 && a >= a) && (n = a);
  }
  return n;
}
function Bi(e, t = no) {
  const n = [];
  let r, a = !1;
  for (const l of e)
    a && n.push(t(r, l)), r = l, a = !0;
  return n;
}
function no(e, t) {
  return [e, t];
}
function ta(e, t, n) {
  e = +e, t = +t, n = (a = arguments.length) < 2 ? (t = e, e = 0, 1) : a < 3 ? 1 : +n;
  for (var r = -1, a = Math.max(0, Math.ceil((t - e) / n)) | 0, l = new Array(a); ++r < a; )
    l[r] = e + r * n;
  return l;
}
function ro(e) {
  if (!(l = e.length)) return [];
  for (var t = -1, n = to(e, ao), r = new Array(n); ++t < n; )
    for (var a = -1, l, s = r[t] = new Array(l); ++a < l; )
      s[a] = e[a][t];
  return r;
}
function ao(e) {
  return e.length;
}
function io() {
  return ro(arguments);
}
function na(e, t) {
  switch (arguments.length) {
    case 0:
      break;
    case 1:
      this.range(e);
      break;
    default:
      this.range(t).domain(e);
      break;
  }
  return this;
}
function Hi(e, t) {
  switch (arguments.length) {
    case 0:
      break;
    case 1: {
      typeof e == "function" ? this.interpolator(e) : this.range(e);
      break;
    }
    default: {
      this.domain(e), typeof t == "function" ? this.interpolator(t) : this.range(t);
      break;
    }
  }
  return this;
}
const Pa = Symbol("implicit");
function ji() {
  var e = new Fa(), t = [], n = [], r = Pa;
  function a(l) {
    let s = e.get(l);
    if (s === void 0) {
      if (r !== Pa) return r;
      e.set(l, s = t.push(l) - 1);
    }
    return n[s % n.length];
  }
  return a.domain = function(l) {
    if (!arguments.length) return t.slice();
    t = [], e = new Fa();
    for (const s of l)
      e.has(s) || e.set(s, t.push(s) - 1);
    return a;
  }, a.range = function(l) {
    return arguments.length ? (n = Array.from(l), a) : n.slice();
  }, a.unknown = function(l) {
    return arguments.length ? (r = l, a) : r;
  }, a.copy = function() {
    return ji(t, n).unknown(r);
  }, na.apply(a, arguments), a;
}
function Yn() {
  var e = ji().unknown(void 0), t = e.domain, n = e.range, r = 0, a = 1, l, s, o = !1, u = 0, f = 0, v = 0.5;
  delete e.unknown;
  function c() {
    var d = t().length, g = a < r, h = g ? a : r, _ = g ? r : a;
    l = (_ - h) / Math.max(1, d - u + f * 2), o && (l = Math.floor(l)), h += (_ - h - l * (d - u)) * v, s = l * (1 - u), o && (h = Math.round(h), s = Math.round(s));
    var p = ta(d).map(function(E) {
      return h + l * E;
    });
    return n(g ? p.reverse() : p);
  }
  return e.domain = function(d) {
    return arguments.length ? (t(d), c()) : t();
  }, e.range = function(d) {
    return arguments.length ? ([r, a] = d, r = +r, a = +a, c()) : [r, a];
  }, e.rangeRound = function(d) {
    return [r, a] = d, r = +r, a = +a, o = !0, c();
  }, e.bandwidth = function() {
    return s;
  }, e.step = function() {
    return l;
  }, e.round = function(d) {
    return arguments.length ? (o = !!d, c()) : o;
  }, e.padding = function(d) {
    return arguments.length ? (u = Math.min(1, f = +d), c()) : u;
  }, e.paddingInner = function(d) {
    return arguments.length ? (u = Math.min(1, d), c()) : u;
  }, e.paddingOuter = function(d) {
    return arguments.length ? (f = +d, c()) : f;
  }, e.align = function(d) {
    return arguments.length ? (v = Math.max(0, Math.min(1, d)), c()) : v;
  }, e.copy = function() {
    return Yn(t(), [r, a]).round(o).paddingInner(u).paddingOuter(f).align(v);
  }, na.apply(c(), arguments);
}
function ra(e, t, n) {
  e.prototype = t.prototype = n, n.constructor = e;
}
function Wi(e, t) {
  var n = Object.create(e.prototype);
  for (var r in t) n[r] = t[r];
  return n;
}
function kn() {
}
var dn = 0.7, Xn = 1 / dn, Bt = "\\s*([+-]?\\d+)\\s*", vn = "\\s*([+-]?(?:\\d*\\.)?\\d+(?:[eE][+-]?\\d+)?)\\s*", it = "\\s*([+-]?(?:\\d*\\.)?\\d+(?:[eE][+-]?\\d+)?)%\\s*", lo = /^#([0-9a-f]{3,8})$/, so = new RegExp(`^rgb\\(${Bt},${Bt},${Bt}\\)$`), oo = new RegExp(`^rgb\\(${it},${it},${it}\\)$`), fo = new RegExp(`^rgba\\(${Bt},${Bt},${Bt},${vn}\\)$`), uo = new RegExp(`^rgba\\(${it},${it},${it},${vn}\\)$`), co = new RegExp(`^hsl\\(${vn},${it},${it}\\)$`), vo = new RegExp(`^hsla\\(${vn},${it},${it},${vn}\\)$`), Ra = {
  aliceblue: 15792383,
  antiquewhite: 16444375,
  aqua: 65535,
  aquamarine: 8388564,
  azure: 15794175,
  beige: 16119260,
  bisque: 16770244,
  black: 0,
  blanchedalmond: 16772045,
  blue: 255,
  blueviolet: 9055202,
  brown: 10824234,
  burlywood: 14596231,
  cadetblue: 6266528,
  chartreuse: 8388352,
  chocolate: 13789470,
  coral: 16744272,
  cornflowerblue: 6591981,
  cornsilk: 16775388,
  crimson: 14423100,
  cyan: 65535,
  darkblue: 139,
  darkcyan: 35723,
  darkgoldenrod: 12092939,
  darkgray: 11119017,
  darkgreen: 25600,
  darkgrey: 11119017,
  darkkhaki: 12433259,
  darkmagenta: 9109643,
  darkolivegreen: 5597999,
  darkorange: 16747520,
  darkorchid: 10040012,
  darkred: 9109504,
  darksalmon: 15308410,
  darkseagreen: 9419919,
  darkslateblue: 4734347,
  darkslategray: 3100495,
  darkslategrey: 3100495,
  darkturquoise: 52945,
  darkviolet: 9699539,
  deeppink: 16716947,
  deepskyblue: 49151,
  dimgray: 6908265,
  dimgrey: 6908265,
  dodgerblue: 2003199,
  firebrick: 11674146,
  floralwhite: 16775920,
  forestgreen: 2263842,
  fuchsia: 16711935,
  gainsboro: 14474460,
  ghostwhite: 16316671,
  gold: 16766720,
  goldenrod: 14329120,
  gray: 8421504,
  green: 32768,
  greenyellow: 11403055,
  grey: 8421504,
  honeydew: 15794160,
  hotpink: 16738740,
  indianred: 13458524,
  indigo: 4915330,
  ivory: 16777200,
  khaki: 15787660,
  lavender: 15132410,
  lavenderblush: 16773365,
  lawngreen: 8190976,
  lemonchiffon: 16775885,
  lightblue: 11393254,
  lightcoral: 15761536,
  lightcyan: 14745599,
  lightgoldenrodyellow: 16448210,
  lightgray: 13882323,
  lightgreen: 9498256,
  lightgrey: 13882323,
  lightpink: 16758465,
  lightsalmon: 16752762,
  lightseagreen: 2142890,
  lightskyblue: 8900346,
  lightslategray: 7833753,
  lightslategrey: 7833753,
  lightsteelblue: 11584734,
  lightyellow: 16777184,
  lime: 65280,
  limegreen: 3329330,
  linen: 16445670,
  magenta: 16711935,
  maroon: 8388608,
  mediumaquamarine: 6737322,
  mediumblue: 205,
  mediumorchid: 12211667,
  mediumpurple: 9662683,
  mediumseagreen: 3978097,
  mediumslateblue: 8087790,
  mediumspringgreen: 64154,
  mediumturquoise: 4772300,
  mediumvioletred: 13047173,
  midnightblue: 1644912,
  mintcream: 16121850,
  mistyrose: 16770273,
  moccasin: 16770229,
  navajowhite: 16768685,
  navy: 128,
  oldlace: 16643558,
  olive: 8421376,
  olivedrab: 7048739,
  orange: 16753920,
  orangered: 16729344,
  orchid: 14315734,
  palegoldenrod: 15657130,
  palegreen: 10025880,
  paleturquoise: 11529966,
  palevioletred: 14381203,
  papayawhip: 16773077,
  peachpuff: 16767673,
  peru: 13468991,
  pink: 16761035,
  plum: 14524637,
  powderblue: 11591910,
  purple: 8388736,
  rebeccapurple: 6697881,
  red: 16711680,
  rosybrown: 12357519,
  royalblue: 4286945,
  saddlebrown: 9127187,
  salmon: 16416882,
  sandybrown: 16032864,
  seagreen: 3050327,
  seashell: 16774638,
  sienna: 10506797,
  silver: 12632256,
  skyblue: 8900331,
  slateblue: 6970061,
  slategray: 7372944,
  slategrey: 7372944,
  snow: 16775930,
  springgreen: 65407,
  steelblue: 4620980,
  tan: 13808780,
  teal: 32896,
  thistle: 14204888,
  tomato: 16737095,
  turquoise: 4251856,
  violet: 15631086,
  wheat: 16113331,
  white: 16777215,
  whitesmoke: 16119285,
  yellow: 16776960,
  yellowgreen: 10145074
};
ra(kn, gn, {
  copy(e) {
    return Object.assign(new this.constructor(), this, e);
  },
  displayable() {
    return this.rgb().displayable();
  },
  hex: Ia,
  // Deprecated! Use color.formatHex.
  formatHex: Ia,
  formatHex8: go,
  formatHsl: ho,
  formatRgb: Da,
  toString: Da
});
function Ia() {
  return this.rgb().formatHex();
}
function go() {
  return this.rgb().formatHex8();
}
function ho() {
  return Vi(this).formatHsl();
}
function Da() {
  return this.rgb().formatRgb();
}
function gn(e) {
  var t, n;
  return e = (e + "").trim().toLowerCase(), (t = lo.exec(e)) ? (n = t[1].length, t = parseInt(t[1], 16), n === 6 ? za(t) : n === 3 ? new Oe(t >> 8 & 15 | t >> 4 & 240, t >> 4 & 15 | t & 240, (t & 15) << 4 | t & 15, 1) : n === 8 ? An(t >> 24 & 255, t >> 16 & 255, t >> 8 & 255, (t & 255) / 255) : n === 4 ? An(t >> 12 & 15 | t >> 8 & 240, t >> 8 & 15 | t >> 4 & 240, t >> 4 & 15 | t & 240, ((t & 15) << 4 | t & 15) / 255) : null) : (t = so.exec(e)) ? new Oe(t[1], t[2], t[3], 1) : (t = oo.exec(e)) ? new Oe(t[1] * 255 / 100, t[2] * 255 / 100, t[3] * 255 / 100, 1) : (t = fo.exec(e)) ? An(t[1], t[2], t[3], t[4]) : (t = uo.exec(e)) ? An(t[1] * 255 / 100, t[2] * 255 / 100, t[3] * 255 / 100, t[4]) : (t = co.exec(e)) ? Ha(t[1], t[2] / 100, t[3] / 100, 1) : (t = vo.exec(e)) ? Ha(t[1], t[2] / 100, t[3] / 100, t[4]) : Ra.hasOwnProperty(e) ? za(Ra[e]) : e === "transparent" ? new Oe(NaN, NaN, NaN, 0) : null;
}
function za(e) {
  return new Oe(e >> 16 & 255, e >> 8 & 255, e & 255, 1);
}
function An(e, t, n, r) {
  return r <= 0 && (e = t = n = NaN), new Oe(e, t, n, r);
}
function bo(e) {
  return e instanceof kn || (e = gn(e)), e ? (e = e.rgb(), new Oe(e.r, e.g, e.b, e.opacity)) : new Oe();
}
function Gn(e, t, n, r) {
  return arguments.length === 1 ? bo(e) : new Oe(e, t, n, r ?? 1);
}
function Oe(e, t, n, r) {
  this.r = +e, this.g = +t, this.b = +n, this.opacity = +r;
}
ra(Oe, Gn, Wi(kn, {
  brighter(e) {
    return e = e == null ? Xn : Math.pow(Xn, e), new Oe(this.r * e, this.g * e, this.b * e, this.opacity);
  },
  darker(e) {
    return e = e == null ? dn : Math.pow(dn, e), new Oe(this.r * e, this.g * e, this.b * e, this.opacity);
  },
  rgb() {
    return this;
  },
  clamp() {
    return new Oe(qt(this.r), qt(this.g), qt(this.b), Un(this.opacity));
  },
  displayable() {
    return -0.5 <= this.r && this.r < 255.5 && -0.5 <= this.g && this.g < 255.5 && -0.5 <= this.b && this.b < 255.5 && 0 <= this.opacity && this.opacity <= 1;
  },
  hex: Oa,
  // Deprecated! Use color.formatHex.
  formatHex: Oa,
  formatHex8: _o,
  formatRgb: Ba,
  toString: Ba
}));
function Oa() {
  return `#${Tt(this.r)}${Tt(this.g)}${Tt(this.b)}`;
}
function _o() {
  return `#${Tt(this.r)}${Tt(this.g)}${Tt(this.b)}${Tt((isNaN(this.opacity) ? 1 : this.opacity) * 255)}`;
}
function Ba() {
  const e = Un(this.opacity);
  return `${e === 1 ? "rgb(" : "rgba("}${qt(this.r)}, ${qt(this.g)}, ${qt(this.b)}${e === 1 ? ")" : `, ${e})`}`;
}
function Un(e) {
  return isNaN(e) ? 1 : Math.max(0, Math.min(1, e));
}
function qt(e) {
  return Math.max(0, Math.min(255, Math.round(e) || 0));
}
function Tt(e) {
  return e = qt(e), (e < 16 ? "0" : "") + e.toString(16);
}
function Ha(e, t, n, r) {
  return r <= 0 ? e = t = n = NaN : n <= 0 || n >= 1 ? e = t = NaN : t <= 0 && (e = NaN), new Je(e, t, n, r);
}
function Vi(e) {
  if (e instanceof Je) return new Je(e.h, e.s, e.l, e.opacity);
  if (e instanceof kn || (e = gn(e)), !e) return new Je();
  if (e instanceof Je) return e;
  e = e.rgb();
  var t = e.r / 255, n = e.g / 255, r = e.b / 255, a = Math.min(t, n, r), l = Math.max(t, n, r), s = NaN, o = l - a, u = (l + a) / 2;
  return o ? (t === l ? s = (n - r) / o + (n < r) * 6 : n === l ? s = (r - t) / o + 2 : s = (t - n) / o + 4, o /= u < 0.5 ? l + a : 2 - l - a, s *= 60) : o = u > 0 && u < 1 ? 0 : s, new Je(s, o, u, e.opacity);
}
function mo(e, t, n, r) {
  return arguments.length === 1 ? Vi(e) : new Je(e, t, n, r ?? 1);
}
function Je(e, t, n, r) {
  this.h = +e, this.s = +t, this.l = +n, this.opacity = +r;
}
ra(Je, mo, Wi(kn, {
  brighter(e) {
    return e = e == null ? Xn : Math.pow(Xn, e), new Je(this.h, this.s, this.l * e, this.opacity);
  },
  darker(e) {
    return e = e == null ? dn : Math.pow(dn, e), new Je(this.h, this.s, this.l * e, this.opacity);
  },
  rgb() {
    var e = this.h % 360 + (this.h < 0) * 360, t = isNaN(e) || isNaN(this.s) ? 0 : this.s, n = this.l, r = n + (n < 0.5 ? n : 1 - n) * t, a = 2 * n - r;
    return new Oe(
      Mr(e >= 240 ? e - 240 : e + 120, a, r),
      Mr(e, a, r),
      Mr(e < 120 ? e + 240 : e - 120, a, r),
      this.opacity
    );
  },
  clamp() {
    return new Je(ja(this.h), qn(this.s), qn(this.l), Un(this.opacity));
  },
  displayable() {
    return (0 <= this.s && this.s <= 1 || isNaN(this.s)) && 0 <= this.l && this.l <= 1 && 0 <= this.opacity && this.opacity <= 1;
  },
  formatHsl() {
    const e = Un(this.opacity);
    return `${e === 1 ? "hsl(" : "hsla("}${ja(this.h)}, ${qn(this.s) * 100}%, ${qn(this.l) * 100}%${e === 1 ? ")" : `, ${e})`}`;
  }
}));
function ja(e) {
  return e = (e || 0) % 360, e < 0 ? e + 360 : e;
}
function qn(e) {
  return Math.max(0, Math.min(1, e || 0));
}
function Mr(e, t, n) {
  return (e < 60 ? t + (n - t) * e / 60 : e < 180 ? n : e < 240 ? t + (n - t) * (240 - e) / 60 : t) * 255;
}
function xo(e, t, n, r, a) {
  var l = e * e, s = l * e;
  return ((1 - 3 * e + 3 * l - s) * t + (4 - 6 * l + 3 * s) * n + (1 + 3 * e + 3 * l - 3 * s) * r + s * a) / 6;
}
function po(e) {
  var t = e.length - 1;
  return function(n) {
    var r = n <= 0 ? n = 0 : n >= 1 ? (n = 1, t - 1) : Math.floor(n * t), a = e[r], l = e[r + 1], s = r > 0 ? e[r - 1] : 2 * a - l, o = r < t - 1 ? e[r + 2] : 2 * l - a;
    return xo((n - r / t) * t, s, a, l, o);
  };
}
const aa = (e) => () => e;
function wo(e, t) {
  return function(n) {
    return e + n * t;
  };
}
function yo(e, t, n) {
  return e = Math.pow(e, n), t = Math.pow(t, n) - e, n = 1 / n, function(r) {
    return Math.pow(e + r * t, n);
  };
}
function ko(e) {
  return (e = +e) == 1 ? Yi : function(t, n) {
    return n - t ? yo(t, n, e) : aa(isNaN(t) ? n : t);
  };
}
function Yi(e, t) {
  var n = t - e;
  return n ? wo(e, n) : aa(isNaN(e) ? t : e);
}
const Wa = function e(t) {
  var n = ko(t);
  function r(a, l) {
    var s = n((a = Gn(a)).r, (l = Gn(l)).r), o = n(a.g, l.g), u = n(a.b, l.b), f = Yi(a.opacity, l.opacity);
    return function(v) {
      return a.r = s(v), a.g = o(v), a.b = u(v), a.opacity = f(v), a + "";
    };
  }
  return r.gamma = e, r;
}(1);
function Mo(e) {
  return function(t) {
    var n = t.length, r = new Array(n), a = new Array(n), l = new Array(n), s, o;
    for (s = 0; s < n; ++s)
      o = Gn(t[s]), r[s] = o.r || 0, a[s] = o.g || 0, l[s] = o.b || 0;
    return r = e(r), a = e(a), l = e(l), o.opacity = 1, function(u) {
      return o.r = r(u), o.g = a(u), o.b = l(u), o + "";
    };
  };
}
var To = Mo(po);
function Ao(e, t) {
  t || (t = []);
  var n = e ? Math.min(t.length, e.length) : 0, r = t.slice(), a;
  return function(l) {
    for (a = 0; a < n; ++a) r[a] = e[a] * (1 - l) + t[a] * l;
    return r;
  };
}
function qo(e) {
  return ArrayBuffer.isView(e) && !(e instanceof DataView);
}
function So(e, t) {
  var n = t ? t.length : 0, r = e ? Math.min(n, e.length) : 0, a = new Array(r), l = new Array(n), s;
  for (s = 0; s < r; ++s) a[s] = tn(e[s], t[s]);
  for (; s < n; ++s) l[s] = t[s];
  return function(o) {
    for (s = 0; s < r; ++s) l[s] = a[s](o);
    return l;
  };
}
function Eo(e, t) {
  var n = /* @__PURE__ */ new Date();
  return e = +e, t = +t, function(r) {
    return n.setTime(e * (1 - r) + t * r), n;
  };
}
function Kn(e, t) {
  return e = +e, t = +t, function(n) {
    return e * (1 - n) + t * n;
  };
}
function Lo(e, t) {
  var n = {}, r = {}, a;
  (e === null || typeof e != "object") && (e = {}), (t === null || typeof t != "object") && (t = {});
  for (a in t)
    a in e ? n[a] = tn(e[a], t[a]) : r[a] = t[a];
  return function(l) {
    for (a in n) r[a] = n[a](l);
    return r;
  };
}
var Or = /[-+]?(?:\d+\.?\d*|\.?\d+)(?:[eE][-+]?\d+)?/g, Tr = new RegExp(Or.source, "g");
function No(e) {
  return function() {
    return e;
  };
}
function Fo(e) {
  return function(t) {
    return e(t) + "";
  };
}
function Co(e, t) {
  var n = Or.lastIndex = Tr.lastIndex = 0, r, a, l, s = -1, o = [], u = [];
  for (e = e + "", t = t + ""; (r = Or.exec(e)) && (a = Tr.exec(t)); )
    (l = a.index) > n && (l = t.slice(n, l), o[s] ? o[s] += l : o[++s] = l), (r = r[0]) === (a = a[0]) ? o[s] ? o[s] += a : o[++s] = a : (o[++s] = null, u.push({ i: s, x: Kn(r, a) })), n = Tr.lastIndex;
  return n < t.length && (l = t.slice(n), o[s] ? o[s] += l : o[++s] = l), o.length < 2 ? u[0] ? Fo(u[0].x) : No(t) : (t = u.length, function(f) {
    for (var v = 0, c; v < t; ++v) o[(c = u[v]).i] = c.x(f);
    return o.join("");
  });
}
function tn(e, t) {
  var n = typeof t, r;
  return t == null || n === "boolean" ? aa(t) : (n === "number" ? Kn : n === "string" ? (r = gn(t)) ? (t = r, Wa) : Co : t instanceof gn ? Wa : t instanceof Date ? Eo : qo(t) ? Ao : Array.isArray(t) ? So : typeof t.valueOf != "function" && typeof t.toString != "function" || isNaN(t) ? Lo : Kn)(e, t);
}
function ia(e, t) {
  return e = +e, t = +t, function(n) {
    return Math.round(e * (1 - n) + t * n);
  };
}
function Po(e, t) {
  t === void 0 && (t = e, e = tn);
  for (var n = 0, r = t.length - 1, a = t[0], l = new Array(r < 0 ? 0 : r); n < r; ) l[n] = e(a, a = t[++n]);
  return function(s) {
    var o = Math.max(0, Math.min(r - 1, Math.floor(s *= r)));
    return l[o](s - o);
  };
}
function Ro(e) {
  return function() {
    return e;
  };
}
function Io(e) {
  return +e;
}
var Va = [0, 1];
function at(e) {
  return e;
}
function Br(e, t) {
  return (t -= e = +e) ? function(n) {
    return (n - e) / t;
  } : Ro(isNaN(t) ? NaN : 0.5);
}
function Do(e, t) {
  var n;
  return e > t && (n = e, e = t, t = n), function(r) {
    return Math.max(e, Math.min(t, r));
  };
}
function zo(e, t, n) {
  var r = e[0], a = e[1], l = t[0], s = t[1];
  return a < r ? (r = Br(a, r), l = n(s, l)) : (r = Br(r, a), l = n(l, s)), function(o) {
    return l(r(o));
  };
}
function Oo(e, t, n) {
  var r = Math.min(e.length, t.length) - 1, a = new Array(r), l = new Array(r), s = -1;
  for (e[r] < e[0] && (e = e.slice().reverse(), t = t.slice().reverse()); ++s < r; )
    a[s] = Br(e[s], e[s + 1]), l[s] = n(t[s], t[s + 1]);
  return function(o) {
    var u = Vs(e, o, 1, r) - 1;
    return l[u](a[u](o));
  };
}
function Bo(e, t) {
  return t.domain(e.domain()).range(e.range()).interpolate(e.interpolate()).clamp(e.clamp()).unknown(e.unknown());
}
function Ho() {
  var e = Va, t = Va, n = tn, r, a, l, s = at, o, u, f;
  function v() {
    var d = Math.min(e.length, t.length);
    return s !== at && (s = Do(e[0], e[d - 1])), o = d > 2 ? Oo : zo, u = f = null, c;
  }
  function c(d) {
    return d == null || isNaN(d = +d) ? l : (u || (u = o(e.map(r), t, n)))(r(s(d)));
  }
  return c.invert = function(d) {
    return s(a((f || (f = o(t, e.map(r), Kn)))(d)));
  }, c.domain = function(d) {
    return arguments.length ? (e = Array.from(d, Io), v()) : e.slice();
  }, c.range = function(d) {
    return arguments.length ? (t = Array.from(d), v()) : t.slice();
  }, c.rangeRound = function(d) {
    return t = Array.from(d), n = ia, v();
  }, c.clamp = function(d) {
    return arguments.length ? (s = d ? !0 : at, v()) : s !== at;
  }, c.interpolate = function(d) {
    return arguments.length ? (n = d, v()) : n;
  }, c.unknown = function(d) {
    return arguments.length ? (l = d, c) : l;
  }, function(d, g) {
    return r = d, a = g, v();
  };
}
function jo() {
  return Ho()(at, at);
}
function Wo(e) {
  return Math.abs(e = Math.round(e)) >= 1e21 ? e.toLocaleString("en").replace(/,/g, "") : e.toString(10);
}
function Zn(e, t) {
  if ((n = (e = t ? e.toExponential(t - 1) : e.toExponential()).indexOf("e")) < 0) return null;
  var n, r = e.slice(0, n);
  return [
    r.length > 1 ? r[0] + r.slice(2) : r,
    +e.slice(n + 1)
  ];
}
function Ut(e) {
  return e = Zn(Math.abs(e)), e ? e[1] : NaN;
}
function Vo(e, t) {
  return function(n, r) {
    for (var a = n.length, l = [], s = 0, o = e[0], u = 0; a > 0 && o > 0 && (u + o + 1 > r && (o = Math.max(1, r - u)), l.push(n.substring(a -= o, a + o)), !((u += o + 1) > r)); )
      o = e[s = (s + 1) % e.length];
    return l.reverse().join(t);
  };
}
function Yo(e) {
  return function(t) {
    return t.replace(/[0-9]/g, function(n) {
      return e[+n];
    });
  };
}
var Xo = /^(?:(.)?([<>=^]))?([+\-( ])?([$#])?(0)?(\d+)?(,)?(\.\d+)?(~)?([a-z%])?$/i;
function Qn(e) {
  if (!(t = Xo.exec(e))) throw new Error("invalid format: " + e);
  var t;
  return new la({
    fill: t[1],
    align: t[2],
    sign: t[3],
    symbol: t[4],
    zero: t[5],
    width: t[6],
    comma: t[7],
    precision: t[8] && t[8].slice(1),
    trim: t[9],
    type: t[10]
  });
}
Qn.prototype = la.prototype;
function la(e) {
  this.fill = e.fill === void 0 ? " " : e.fill + "", this.align = e.align === void 0 ? ">" : e.align + "", this.sign = e.sign === void 0 ? "-" : e.sign + "", this.symbol = e.symbol === void 0 ? "" : e.symbol + "", this.zero = !!e.zero, this.width = e.width === void 0 ? void 0 : +e.width, this.comma = !!e.comma, this.precision = e.precision === void 0 ? void 0 : +e.precision, this.trim = !!e.trim, this.type = e.type === void 0 ? "" : e.type + "";
}
la.prototype.toString = function() {
  return this.fill + this.align + this.sign + this.symbol + (this.zero ? "0" : "") + (this.width === void 0 ? "" : Math.max(1, this.width | 0)) + (this.comma ? "," : "") + (this.precision === void 0 ? "" : "." + Math.max(0, this.precision | 0)) + (this.trim ? "~" : "") + this.type;
};
function Go(e) {
  e: for (var t = e.length, n = 1, r = -1, a; n < t; ++n)
    switch (e[n]) {
      case ".":
        r = a = n;
        break;
      case "0":
        r === 0 && (r = n), a = n;
        break;
      default:
        if (!+e[n]) break e;
        r > 0 && (r = 0);
        break;
    }
  return r > 0 ? e.slice(0, r) + e.slice(a + 1) : e;
}
var Xi;
function Uo(e, t) {
  var n = Zn(e, t);
  if (!n) return e + "";
  var r = n[0], a = n[1], l = a - (Xi = Math.max(-8, Math.min(8, Math.floor(a / 3))) * 3) + 1, s = r.length;
  return l === s ? r : l > s ? r + new Array(l - s + 1).join("0") : l > 0 ? r.slice(0, l) + "." + r.slice(l) : "0." + new Array(1 - l).join("0") + Zn(e, Math.max(0, t + l - 1))[0];
}
function Ya(e, t) {
  var n = Zn(e, t);
  if (!n) return e + "";
  var r = n[0], a = n[1];
  return a < 0 ? "0." + new Array(-a).join("0") + r : r.length > a + 1 ? r.slice(0, a + 1) + "." + r.slice(a + 1) : r + new Array(a - r.length + 2).join("0");
}
const Xa = {
  "%": (e, t) => (e * 100).toFixed(t),
  b: (e) => Math.round(e).toString(2),
  c: (e) => e + "",
  d: Wo,
  e: (e, t) => e.toExponential(t),
  f: (e, t) => e.toFixed(t),
  g: (e, t) => e.toPrecision(t),
  o: (e) => Math.round(e).toString(8),
  p: (e, t) => Ya(e * 100, t),
  r: Ya,
  s: Uo,
  X: (e) => Math.round(e).toString(16).toUpperCase(),
  x: (e) => Math.round(e).toString(16)
};
function Ga(e) {
  return e;
}
var Ua = Array.prototype.map, Ka = ["y", "z", "a", "f", "p", "n", "µ", "m", "", "k", "M", "G", "T", "P", "E", "Z", "Y"];
function Ko(e) {
  var t = e.grouping === void 0 || e.thousands === void 0 ? Ga : Vo(Ua.call(e.grouping, Number), e.thousands + ""), n = e.currency === void 0 ? "" : e.currency[0] + "", r = e.currency === void 0 ? "" : e.currency[1] + "", a = e.decimal === void 0 ? "." : e.decimal + "", l = e.numerals === void 0 ? Ga : Yo(Ua.call(e.numerals, String)), s = e.percent === void 0 ? "%" : e.percent + "", o = e.minus === void 0 ? "−" : e.minus + "", u = e.nan === void 0 ? "NaN" : e.nan + "";
  function f(c) {
    c = Qn(c);
    var d = c.fill, g = c.align, h = c.sign, _ = c.symbol, p = c.zero, E = c.width, k = c.comma, T = c.precision, w = c.trim, q = c.type;
    q === "n" ? (k = !0, q = "g") : Xa[q] || (T === void 0 && (T = 12), w = !0, q = "g"), (p || d === "0" && g === "=") && (p = !0, d = "0", g = "=");
    var L = _ === "$" ? n : _ === "#" && /[boxX]/.test(q) ? "0" + q.toLowerCase() : "", C = _ === "$" ? r : /[%p]/.test(q) ? s : "", I = Xa[q], X = /[defgprs%]/.test(q);
    T = T === void 0 ? 6 : /[gprs]/.test(q) ? Math.max(1, Math.min(21, T)) : Math.max(0, Math.min(20, T));
    function $(A) {
      var S = L, y = C, R, P, F;
      if (q === "c")
        y = I(A) + y, A = "";
      else {
        A = +A;
        var G = A < 0 || 1 / A < 0;
        if (A = isNaN(A) ? u : I(Math.abs(A), T), w && (A = Go(A)), G && +A == 0 && h !== "+" && (G = !1), S = (G ? h === "(" ? h : o : h === "-" || h === "(" ? "" : h) + S, y = (q === "s" ? Ka[8 + Xi / 3] : "") + y + (G && h === "(" ? ")" : ""), X) {
          for (R = -1, P = A.length; ++R < P; )
            if (F = A.charCodeAt(R), 48 > F || F > 57) {
              y = (F === 46 ? a + A.slice(R + 1) : A.slice(R)) + y, A = A.slice(0, R);
              break;
            }
        }
      }
      k && !p && (A = t(A, 1 / 0));
      var O = S.length + A.length + y.length, W = O < E ? new Array(E - O + 1).join(d) : "";
      switch (k && p && (A = t(W + A, W.length ? E - y.length : 1 / 0), W = ""), g) {
        case "<":
          A = S + A + y + W;
          break;
        case "=":
          A = S + W + A + y;
          break;
        case "^":
          A = W.slice(0, O = W.length >> 1) + S + A + y + W.slice(O);
          break;
        default:
          A = W + S + A + y;
          break;
      }
      return l(A);
    }
    return $.toString = function() {
      return c + "";
    }, $;
  }
  function v(c, d) {
    var g = f((c = Qn(c), c.type = "f", c)), h = Math.max(-8, Math.min(8, Math.floor(Ut(d) / 3))) * 3, _ = Math.pow(10, -h), p = Ka[8 + h / 3];
    return function(E) {
      return g(_ * E) + p;
    };
  }
  return {
    format: f,
    formatPrefix: v
  };
}
var Sn, Pe, Gi;
Zo({
  thousands: ",",
  grouping: [3],
  currency: ["$", ""]
});
function Zo(e) {
  return Sn = Ko(e), Pe = Sn.format, Gi = Sn.formatPrefix, Sn;
}
function Qo(e) {
  return Math.max(0, -Ut(Math.abs(e)));
}
function Jo(e, t) {
  return Math.max(0, Math.max(-8, Math.min(8, Math.floor(Ut(t) / 3))) * 3 - Ut(Math.abs(e)));
}
function $o(e, t) {
  return e = Math.abs(e), t = Math.abs(t) - e, Math.max(0, Ut(t) - Ut(e)) + 1;
}
function ef(e, t, n, r) {
  var a = $s(e, t, n), l;
  switch (r = Qn(r ?? ",f"), r.type) {
    case "s": {
      var s = Math.max(Math.abs(e), Math.abs(t));
      return r.precision == null && !isNaN(l = Jo(a, s)) && (r.precision = l), Gi(r, s);
    }
    case "":
    case "e":
    case "g":
    case "p":
    case "r": {
      r.precision == null && !isNaN(l = $o(a, Math.max(Math.abs(e), Math.abs(t)))) && (r.precision = l - (r.type === "e"));
      break;
    }
    case "f":
    case "%": {
      r.precision == null && !isNaN(l = Qo(a)) && (r.precision = l - (r.type === "%") * 2);
      break;
    }
  }
  return Pe(r);
}
function sa(e) {
  var t = e.domain;
  return e.ticks = function(n) {
    var r = t();
    return Js(r[0], r[r.length - 1], n ?? 10);
  }, e.tickFormat = function(n, r) {
    var a = t();
    return ef(a[0], a[a.length - 1], n ?? 10, r);
  }, e.nice = function(n) {
    n == null && (n = 10);
    var r = t(), a = 0, l = r.length - 1, s = r[a], o = r[l], u, f, v = 10;
    for (o < s && (f = s, s = o, o = f, f = a, a = l, l = f); v-- > 0; ) {
      if (f = zr(s, o, n), f === u)
        return r[a] = s, r[l] = o, t(r);
      if (f > 0)
        s = Math.floor(s / f) * f, o = Math.ceil(o / f) * f;
      else if (f < 0)
        s = Math.ceil(s * f) / f, o = Math.floor(o * f) / f;
      else
        break;
      u = f;
    }
    return e;
  }, e;
}
function Kt() {
  var e = jo();
  return e.copy = function() {
    return Bo(e, Kt());
  }, na.apply(e, arguments), sa(e);
}
function tf() {
  var e = 0, t = 1, n, r, a, l, s = at, o = !1, u;
  function f(c) {
    return c == null || isNaN(c = +c) ? u : s(a === 0 ? 0.5 : (c = (l(c) - n) * a, o ? Math.max(0, Math.min(1, c)) : c));
  }
  f.domain = function(c) {
    return arguments.length ? ([e, t] = c, n = l(e = +e), r = l(t = +t), a = n === r ? 0 : 1 / (r - n), f) : [e, t];
  }, f.clamp = function(c) {
    return arguments.length ? (o = !!c, f) : o;
  }, f.interpolator = function(c) {
    return arguments.length ? (s = c, f) : s;
  };
  function v(c) {
    return function(d) {
      var g, h;
      return arguments.length ? ([g, h] = d, s = c(g, h), f) : [s(0), s(1)];
    };
  }
  return f.range = v(tn), f.rangeRound = v(ia), f.unknown = function(c) {
    return arguments.length ? (u = c, f) : u;
  }, function(c) {
    return l = c, n = c(e), r = c(t), a = n === r ? 0 : 1 / (r - n), f;
  };
}
function Ui(e, t) {
  return t.domain(e.domain()).interpolator(e.interpolator()).clamp(e.clamp()).unknown(e.unknown());
}
function St() {
  var e = sa(tf()(at));
  return e.copy = function() {
    return Ui(e, St());
  }, Hi.apply(e, arguments);
}
function nf() {
  var e = 0, t = 0.5, n = 1, r = 1, a, l, s, o, u, f = at, v, c = !1, d;
  function g(_) {
    return isNaN(_ = +_) ? d : (_ = 0.5 + ((_ = +v(_)) - l) * (r * _ < r * l ? o : u), f(c ? Math.max(0, Math.min(1, _)) : _));
  }
  g.domain = function(_) {
    return arguments.length ? ([e, t, n] = _, a = v(e = +e), l = v(t = +t), s = v(n = +n), o = a === l ? 0 : 0.5 / (l - a), u = l === s ? 0 : 0.5 / (s - l), r = l < a ? -1 : 1, g) : [e, t, n];
  }, g.clamp = function(_) {
    return arguments.length ? (c = !!_, g) : c;
  }, g.interpolator = function(_) {
    return arguments.length ? (f = _, g) : f;
  };
  function h(_) {
    return function(p) {
      var E, k, T;
      return arguments.length ? ([E, k, T] = p, f = Po(_, [E, k, T]), g) : [f(0), f(0.5), f(1)];
    };
  }
  return g.range = h(tn), g.rangeRound = h(ia), g.unknown = function(_) {
    return arguments.length ? (d = _, g) : d;
  }, function(_) {
    return v = _, a = _(e), l = _(t), s = _(n), o = a === l ? 0 : 0.5 / (l - a), u = l === s ? 0 : 0.5 / (s - l), r = l < a ? -1 : 1, g;
  };
}
function oa() {
  var e = sa(nf()(at));
  return e.copy = function() {
    return Ui(e, oa());
  }, Hi.apply(e, arguments);
}
function rf(e, t, n) {
  let r = 0;
  for (; r <= e; ) {
    const a = Math.floor((r + e) / 2), l = t(a);
    if (l === n)
      return a;
    l < n ? r = a + 1 : e = a - 1;
  }
  return e;
}
function Za(e, t, n) {
  const r = e.measureText(t).width, a = "…", l = e.measureText(a).width;
  if (r <= n || r <= l)
    return t;
  const s = rf(
    t.length - 1,
    (o) => e.measureText(t.substring(0, o)).width,
    n - l
  );
  return t.substring(0, s) + a;
}
function Ki(e, t, n, r, a, l, s, o) {
  const u = Math.min(...n.range()), f = Math.max(...n.range()), v = (u + f) / 2, c = e === "left", d = e === "right", g = e === "top";
  if (c || d) {
    const h = c ? -r : l;
    if (t === "top") {
      const _ = u - a, p = 0.71 * o;
      return {
        textAlign: c ? "start" : "end",
        x: h,
        y: _ + p,
        rotate: 0
      };
    } else {
      if (t === "bottom")
        return {
          textAlign: c ? "start" : "end",
          x: h,
          y: f + s,
          rotate: 0
        };
      {
        const _ = c ? 1 : -1, p = h + _ * o / 2, E = v, k = _ * 0.71 * o;
        return {
          textAlign: "center",
          x: p + k,
          y: E,
          rotate: c ? -90 : 90
        };
      }
    }
  } else {
    const h = g ? -a + o / 2 : s - o / 2, _ = g ? o * 0.71 : 0;
    return t === "left" ? {
      textAlign: "start",
      x: u - r,
      y: h + _,
      rotate: 0
    } : t === "right" ? {
      textAlign: "end",
      x: f + l,
      y: h + _,
      rotate: 0
    } : {
      textAlign: "center",
      x: v,
      y: h + _,
      rotate: 0
    };
  }
}
function Qa(e, t) {
  return e === "left" ? "end" : e === "right" ? "start" : t === 0 ? "center" : t > 0 && e === "top" ? "end" : t < 0 && e === "top" || t > 0 && e === "bottom" ? "start" : "end";
}
const Ar = {
  start: "start",
  center: "middle",
  end: "end"
};
function Ja(e, t, n, {
  translateX: r = 0,
  translateY: a = 0,
  marginLeft: l = 0,
  marginTop: s = 0,
  marginRight: o = 0,
  marginBottom: u = 0,
  tickLineSize: f = 6,
  tickLabelFontSize: v = 10,
  tickLabelFontFamily: c = "ui-sans-serif, system-ui, sans-serif",
  tickLabelAngle: d = 0,
  tickPadding: g = 3,
  tickFormat: h,
  numTicks: _,
  tickValues: p,
  showTickMarks: E = !0,
  showTickLabels: k = !0,
  maxTickLabelSpace: T,
  tickLineColor: w = "black",
  tickLabelColor: q = "black",
  showDomain: L = !1,
  domainColor: C = "black",
  title: I = "",
  titleFontSize: X = 12,
  titleFontFamily: $ = "ui-sans-serif, system-ui, sans-serif",
  titleFontWeight: A = 400,
  titleAnchor: S = "center",
  titleOffsetX: y = 0,
  titleOffsetY: R = 0,
  titleColor: P = "black"
} = {}) {
  const F = t === "top" || t === "left" ? -1 : 1, G = Math.max(f, 0) + g, O = n.bandwidth ? n.bandwidth() / 2 : 0, W = Ki(
    t,
    S,
    n,
    l,
    s,
    o,
    u,
    X
  ), ee = p ?? (n.ticks ? n.ticks(_) : n.domain()), H = h ?? (n.tickFormat ? n.tickFormat(_) : (j) => String(j).toString());
  e.save(), e.translate(r, a), e.font = `${v}px ${c}`, e.globalAlpha = 1, e.fillStyle = q, e.strokeStyle = w, t === "left" || t === "right" ? (ee.forEach((j) => {
    const z = (n(j) ?? 0) + O;
    if (E && (e.beginPath(), e.moveTo(f * F, z), e.lineTo(0, z), e.stroke()), k) {
      e.save(), e.translate(G * F, z), e.rotate(d * Math.PI / 180), e.textBaseline = "middle", e.textAlign = t === "left" ? "end" : "start";
      const Y = T ? Za(e, H(j), T) : H(j);
      e.fillText(Y, 0, 0), e.restore();
    }
  }), e.strokeStyle = C, e.lineWidth = 1, L && (e.beginPath(), e.moveTo(0, n.range()[0]), e.lineTo(0, n.range()[1]), e.stroke())) : (ee.forEach((j) => {
    const z = (n(j) ?? 0) + O;
    if (E && (e.beginPath(), e.moveTo(z, f * F), e.lineTo(z, 0), e.stroke()), k) {
      e.save(), e.translate(z, G * F), e.rotate(d * Math.PI / 180), e.textBaseline = t === "top" ? "bottom" : "top", e.textAlign = "center";
      const Y = T ? Za(e, H(j), T) : H(j);
      e.fillText(Y, 0, 0), e.restore();
    }
  }), e.strokeStyle = C, e.lineWidth = 1, L && (e.beginPath(), e.moveTo(n.range()[0], 0), e.lineTo(n.range()[1], 0), e.stroke())), I && (e.fillStyle = P, e.textAlign = W.textAlign, e.textBaseline = "alphabetic", e.font = `${A} ${X}px ${$}`, e.translate(W.x, W.y), e.rotate(W.rotate * Math.PI / 180), e.fillText(I, y, R)), e.restore();
}
var af = /* @__PURE__ */ ke("<text><tspan></tspan> <title> </title></text>");
function $a(e, t) {
  pe(t, !0);
  let n = N(t, "angle", 3, 0), r = N(t, "fontSize", 3, 10), a = N(t, "fontFamily", 3, "ui-sans-serif, system-ui, sans-serif"), l = N(t, "fontColor", 3, "black"), s = N(t, "fontWeight", 3, 400), o = N(t, "dominantBaseline", 3, "auto"), u = N(t, "textAnchor", 3, "start"), f = /* @__PURE__ */ re(void 0);
  function v(_, p, E) {
    E.textContent = _;
    let k = _;
    for (; k.length > 0 && E.getComputedTextLength() > p; )
      k = k.slice(0, -1), E.textContent = k + "…";
  }
  Er(() => {
    i(f) && v(t.label, t.width, i(f));
  });
  var c = af(), d = b(c);
  Wn(d, (_) => J(f, _), () => i(f));
  var g = m(d, 2), h = b(g);
  te(() => {
    M(c, "fill", l()), M(c, "font-size", r()), M(c, "font-family", a()), M(c, "font-weight", s()), M(c, "transform", `translate(${t.x ?? ""} ${t.y ?? ""}) rotate(${n() ?? ""})`), M(d, "dominant-baseline", o()), M(d, "text-anchor", u()), de(h, t.label);
  }), D(e, c), we();
}
var lf = /* @__PURE__ */ ke("<line></line>"), sf = /* @__PURE__ */ ke("<text> </text>"), of = /* @__PURE__ */ ke("<g><!><!></g>"), ff = /* @__PURE__ */ ke("<line></line>"), uf = /* @__PURE__ */ ke("<g></g><!>", 1), cf = /* @__PURE__ */ ke("<line></line>"), df = /* @__PURE__ */ ke("<text> </text>"), vf = /* @__PURE__ */ ke("<g><!><!></g>"), gf = /* @__PURE__ */ ke("<line></line>"), hf = /* @__PURE__ */ ke("<g></g><!>", 1), bf = /* @__PURE__ */ ke("<text> </text>"), _f = /* @__PURE__ */ ke("<g><!><!></g>");
function Zt(e, t) {
  pe(t, !0);
  let n = N(t, "translateX", 3, 0), r = N(t, "translateY", 3, 0), a = N(t, "marginLeft", 3, 0), l = N(t, "marginTop", 3, 0), s = N(t, "marginRight", 3, 0), o = N(t, "marginBottom", 3, 0), u = N(t, "tickLineSize", 3, 6), f = N(t, "tickLabelFontSize", 3, 10), v = N(t, "tickLabelFontFamily", 3, "ui-sans-serif, system-ui, sans-serif"), c = N(t, "tickLabelAngle", 3, 0), d = N(t, "tickPadding", 3, 3), g = N(t, "showTickMarks", 3, !0), h = N(t, "showTickLabels", 3, !0), _ = N(t, "tickLineColor", 3, "black"), p = N(t, "tickLabelColor", 3, "black"), E = N(t, "showDomain", 3, !1), k = N(t, "domainColor", 3, "black"), T = N(t, "title", 3, ""), w = N(t, "titleFontSize", 3, 12), q = N(t, "titleFontFamily", 3, "ui-sans-serif, system-ui, sans-serif"), L = N(t, "titleFontWeight", 3, 400), C = N(t, "titleAnchor", 3, "center"), I = N(t, "titleOffsetX", 3, 0), X = N(t, "titleOffsetY", 3, 0), $ = N(t, "titleColor", 3, "black");
  const A = /* @__PURE__ */ x(() => t.orientation === "top" || t.orientation === "left" ? -1 : 1), S = /* @__PURE__ */ x(() => Math.max(u(), 0) + d()), y = /* @__PURE__ */ x(() => t.scale.bandwidth ? t.scale.bandwidth() / 2 : 0), R = /* @__PURE__ */ x(() => Ki(t.orientation, C(), t.scale, a(), l(), s(), o(), w()));
  let P = /* @__PURE__ */ x(() => t.tickValues ?? (t.scale.ticks ? t.scale.ticks(t.numTicks) : t.scale.domain())), F = /* @__PURE__ */ x(() => t.tickFormat ?? (t.scale.tickFormat ? t.scale.tickFormat(t.numTicks) : (z) => String(z).toString()));
  var G = _f(), O = b(G);
  {
    var W = (z) => {
      var Y = uf(), K = Se(Y);
      Ae(K, 21, () => i(P), Te, (ae, Z) => {
        var ge = of();
        const me = /* @__PURE__ */ x(() => (t.scale(i(Z)) ?? 0) + i(y));
        var ye = b(ge);
        {
          var Me = (Q) => {
            var B = lf();
            M(B, "y1", 0), M(B, "x2", 0), M(B, "y2", 0), te(() => {
              M(B, "x1", u() * i(A)), M(B, "stroke", _());
            }), D(Q, B);
          };
          se(ye, (Q) => {
            g() && Q(Me);
          });
        }
        var Ye = m(ye);
        {
          var U = (Q) => {
            var B = Nt();
            const fe = /* @__PURE__ */ x(() => Ar[Qa(t.orientation, c())]);
            var be = Se(B);
            {
              var xe = (ue) => {
                const _e = /* @__PURE__ */ x(() => i(F)(i(Z))), tt = /* @__PURE__ */ x(() => i(S) * i(A));
                $a(ue, {
                  get label() {
                    return i(_e);
                  },
                  get width() {
                    return t.maxTickLabelSpace;
                  },
                  get x() {
                    return i(tt);
                  },
                  y: 0,
                  dominantBaseline: "middle",
                  get textAnchor() {
                    return i(fe);
                  },
                  get fontSize() {
                    return f();
                  },
                  get fontColor() {
                    return p();
                  },
                  get fontFamily() {
                    return v();
                  },
                  get angle() {
                    return c();
                  }
                });
              }, Ee = (ue) => {
                var _e = sf();
                M(_e, "dominant-baseline", "middle");
                var tt = b(_e);
                te(
                  (Re) => {
                    M(_e, "text-anchor", i(fe)), M(_e, "transform", `translate(${i(S) * i(A)} 0) rotate(${c() ?? ""})`), M(_e, "fill", p()), M(_e, "font-size", f()), M(_e, "font-family", v()), de(tt, Re);
                  },
                  [() => i(F)(i(Z))]
                ), D(ue, _e);
              };
              se(be, (ue) => {
                t.maxTickLabelSpace ? ue(xe) : ue(Ee, !1);
              });
            }
            D(Q, B);
          };
          se(Ye, (Q) => {
            h() && Q(U);
          });
        }
        te(() => M(ge, "transform", `translate(0,${i(me) ?? ""})`)), D(ae, ge);
      });
      var V = m(K);
      {
        var ie = (ae) => {
          var Z = ff();
          M(Z, "x1", 0), M(Z, "x2", 0), M(Z, "stroke-width", 1), te(
            (ge, me) => {
              M(Z, "y1", ge), M(Z, "y2", me), M(Z, "stroke", k());
            },
            [
              () => t.scale.range()[0],
              () => t.scale.range()[1]
            ]
          ), D(ae, Z);
        };
        se(V, (ae) => {
          E() && ae(ie);
        });
      }
      D(z, Y);
    }, ee = (z) => {
      var Y = hf(), K = Se(Y);
      Ae(K, 21, () => i(P), Te, (ae, Z) => {
        var ge = vf();
        const me = /* @__PURE__ */ x(() => (t.scale(i(Z)) ?? 0) + i(y));
        var ye = b(ge);
        {
          var Me = (Q) => {
            var B = cf();
            M(B, "x1", 0), M(B, "x2", 0), M(B, "y2", 0), te(() => {
              M(B, "y1", u() * i(A)), M(B, "stroke", _());
            }), D(Q, B);
          };
          se(ye, (Q) => {
            g() && Q(Me);
          });
        }
        var Ye = m(ye);
        {
          var U = (Q) => {
            var B = Nt();
            const fe = /* @__PURE__ */ x(() => Ar[Qa(t.orientation, c())]);
            var be = Se(B);
            {
              var xe = (ue) => {
                const _e = /* @__PURE__ */ x(() => i(F)(i(Z))), tt = /* @__PURE__ */ x(() => i(S) * i(A)), Re = /* @__PURE__ */ x(() => t.orientation === "top" ? "text-top" : "hanging");
                $a(ue, {
                  get label() {
                    return i(_e);
                  },
                  get width() {
                    return t.maxTickLabelSpace;
                  },
                  x: 0,
                  get y() {
                    return i(tt);
                  },
                  get dominantBaseline() {
                    return i(Re);
                  },
                  get textAnchor() {
                    return i(fe);
                  },
                  get fontSize() {
                    return f();
                  },
                  get fontFamily() {
                    return v();
                  },
                  get fontColor() {
                    return p();
                  },
                  get angle() {
                    return c();
                  }
                });
              }, Ee = (ue) => {
                var _e = df(), tt = b(_e);
                te(
                  (Re) => {
                    M(_e, "dominant-baseline", t.orientation === "top" ? "text-top" : "hanging"), M(_e, "text-anchor", i(fe)), M(_e, "transform", `translate(0 ${i(S) * i(A)}) rotate(${c() ?? ""})`), M(_e, "font-size", f()), M(_e, "font-family", v()), M(_e, "fill", p()), de(tt, Re);
                  },
                  [() => i(F)(i(Z))]
                ), D(ue, _e);
              };
              se(be, (ue) => {
                t.maxTickLabelSpace ? ue(xe) : ue(Ee, !1);
              });
            }
            D(Q, B);
          };
          se(Ye, (Q) => {
            h() && Q(U);
          });
        }
        te(() => M(ge, "transform", `translate(${i(me) ?? ""},0)`)), D(ae, ge);
      });
      var V = m(K);
      {
        var ie = (ae) => {
          var Z = gf();
          M(Z, "y1", 0), M(Z, "y2", 0), M(Z, "stroke-width", 1), te(
            (ge, me) => {
              M(Z, "x1", ge), M(Z, "x2", me), M(Z, "stroke", k());
            },
            [
              () => t.scale.range()[0],
              () => t.scale.range()[1]
            ]
          ), D(ae, Z);
        };
        se(V, (ae) => {
          E() && ae(ie);
        });
      }
      D(z, Y);
    };
    se(O, (z) => {
      t.orientation === "left" || t.orientation == "right" ? z(W) : z(ee, !1);
    });
  }
  var H = m(O);
  {
    var j = (z) => {
      var Y = bf(), K = b(Y);
      te(() => {
        M(Y, "fill", $()), M(Y, "font-size", w()), M(Y, "font-family", q()), M(Y, "font-weight", L()), M(Y, "text-anchor", Ar[i(R).textAlign]), M(Y, "transform", `translate(${i(R).x ?? ""} ${i(R).y ?? ""}) rotate(${i(R).rotate ?? ""}) translate(${I() ?? ""} ${X() ?? ""})`), de(K, T());
      }), D(z, Y);
    };
    se(H, (z) => {
      T() && z(j);
    });
  }
  te(() => M(G, "transform", `translate(${n() ?? ""},${r() ?? ""})`)), D(e, G), we();
}
function kt(e) {
  for (var t = e.length / 6 | 0, n = new Array(t), r = 0; r < t; ) n[r] = "#" + e.slice(r * 6, ++r * 6);
  return n;
}
const vr = (e) => To(e[e.length - 1]);
var mf = new Array(3).concat(
  "af8dc3f7f7f77fbf7b",
  "7b3294c2a5cfa6dba0008837",
  "7b3294c2a5cff7f7f7a6dba0008837",
  "762a83af8dc3e7d4e8d9f0d37fbf7b1b7837",
  "762a83af8dc3e7d4e8f7f7f7d9f0d37fbf7b1b7837",
  "762a839970abc2a5cfe7d4e8d9f0d3a6dba05aae611b7837",
  "762a839970abc2a5cfe7d4e8f7f7f7d9f0d3a6dba05aae611b7837",
  "40004b762a839970abc2a5cfe7d4e8d9f0d3a6dba05aae611b783700441b",
  "40004b762a839970abc2a5cfe7d4e8f7f7f7d9f0d3a6dba05aae611b783700441b"
).map(kt);
const xf = vr(mf);
var pf = new Array(3).concat(
  "e9a3c9f7f7f7a1d76a",
  "d01c8bf1b6dab8e1864dac26",
  "d01c8bf1b6daf7f7f7b8e1864dac26",
  "c51b7de9a3c9fde0efe6f5d0a1d76a4d9221",
  "c51b7de9a3c9fde0eff7f7f7e6f5d0a1d76a4d9221",
  "c51b7dde77aef1b6dafde0efe6f5d0b8e1867fbc414d9221",
  "c51b7dde77aef1b6dafde0eff7f7f7e6f5d0b8e1867fbc414d9221",
  "8e0152c51b7dde77aef1b6dafde0efe6f5d0b8e1867fbc414d9221276419",
  "8e0152c51b7dde77aef1b6dafde0eff7f7f7e6f5d0b8e1867fbc414d9221276419"
).map(kt);
const wf = vr(pf);
var yf = new Array(3).concat(
  "deebf79ecae13182bd",
  "eff3ffbdd7e76baed62171b5",
  "eff3ffbdd7e76baed63182bd08519c",
  "eff3ffc6dbef9ecae16baed63182bd08519c",
  "eff3ffc6dbef9ecae16baed64292c62171b5084594",
  "f7fbffdeebf7c6dbef9ecae16baed64292c62171b5084594",
  "f7fbffdeebf7c6dbef9ecae16baed64292c62171b508519c08306b"
).map(kt);
const Zi = vr(yf);
var kf = new Array(3).concat(
  "fee6cefdae6be6550d",
  "feeddefdbe85fd8d3cd94701",
  "feeddefdbe85fd8d3ce6550da63603",
  "feeddefdd0a2fdae6bfd8d3ce6550da63603",
  "feeddefdd0a2fdae6bfd8d3cf16913d948018c2d04",
  "fff5ebfee6cefdd0a2fdae6bfd8d3cf16913d948018c2d04",
  "fff5ebfee6cefdd0a2fdae6bfd8d3cf16913d94801a636037f2704"
).map(kt);
const Mf = vr(kf);
function gr(e) {
  var t = e.length;
  return function(n) {
    return e[Math.max(0, Math.min(t - 1, Math.floor(n * t)))];
  };
}
gr(kt("44015444025645045745055946075a46085c460a5d460b5e470d60470e6147106347116447136548146748166848176948186a481a6c481b6d481c6e481d6f481f70482071482173482374482475482576482677482878482979472a7a472c7a472d7b472e7c472f7d46307e46327e46337f463480453581453781453882443983443a83443b84433d84433e85423f854240864241864142874144874045884046883f47883f48893e49893e4a893e4c8a3d4d8a3d4e8a3c4f8a3c508b3b518b3b528b3a538b3a548c39558c39568c38588c38598c375a8c375b8d365c8d365d8d355e8d355f8d34608d34618d33628d33638d32648e32658e31668e31678e31688e30698e306a8e2f6b8e2f6c8e2e6d8e2e6e8e2e6f8e2d708e2d718e2c718e2c728e2c738e2b748e2b758e2a768e2a778e2a788e29798e297a8e297b8e287c8e287d8e277e8e277f8e27808e26818e26828e26828e25838e25848e25858e24868e24878e23888e23898e238a8d228b8d228c8d228d8d218e8d218f8d21908d21918c20928c20928c20938c1f948c1f958b1f968b1f978b1f988b1f998a1f9a8a1e9b8a1e9c891e9d891f9e891f9f881fa0881fa1881fa1871fa28720a38620a48621a58521a68522a78522a88423a98324aa8325ab8225ac8226ad8127ad8128ae8029af7f2ab07f2cb17e2db27d2eb37c2fb47c31b57b32b67a34b67935b77937b87838b9773aba763bbb753dbc743fbc7340bd7242be7144bf7046c06f48c16e4ac16d4cc26c4ec36b50c46a52c56954c56856c66758c7655ac8645cc8635ec96260ca6063cb5f65cb5e67cc5c69cd5b6ccd5a6ece5870cf5773d05675d05477d1537ad1517cd2507fd34e81d34d84d44b86d54989d5488bd6468ed64590d74393d74195d84098d83e9bd93c9dd93ba0da39a2da37a5db36a8db34aadc32addc30b0dd2fb2dd2db5de2bb8de29bade28bddf26c0df25c2df23c5e021c8e020cae11fcde11dd0e11cd2e21bd5e21ad8e219dae319dde318dfe318e2e418e5e419e7e419eae51aece51befe51cf1e51df4e61ef6e620f8e621fbe723fde725"));
gr(kt("00000401000501010601010802010902020b02020d03030f03031204041405041606051806051a07061c08071e0907200a08220b09240c09260d0a290e0b2b100b2d110c2f120d31130d34140e36150e38160f3b180f3d19103f1a10421c10441d11471e114920114b21114e22115024125325125527125829115a2a115c2c115f2d11612f116331116533106734106936106b38106c390f6e3b0f703d0f713f0f72400f74420f75440f764510774710784910784a10794c117a4e117b4f127b51127c52137c54137d56147d57157e59157e5a167e5c167f5d177f5f187f601880621980641a80651a80671b80681c816a1c816b1d816d1d816e1e81701f81721f817320817521817621817822817922827b23827c23827e24828025828125818326818426818627818827818928818b29818c29818e2a81902a81912b81932b80942c80962c80982d80992d809b2e7f9c2e7f9e2f7fa02f7fa1307ea3307ea5317ea6317da8327daa337dab337cad347cae347bb0357bb2357bb3367ab5367ab73779b83779ba3878bc3978bd3977bf3a77c03a76c23b75c43c75c53c74c73d73c83e73ca3e72cc3f71cd4071cf4070d0416fd2426fd3436ed5446dd6456cd8456cd9466bdb476adc4869de4968df4a68e04c67e24d66e34e65e44f64e55064e75263e85362e95462ea5661eb5760ec5860ed5a5fee5b5eef5d5ef05f5ef1605df2625df2645cf3655cf4675cf4695cf56b5cf66c5cf66e5cf7705cf7725cf8745cf8765cf9785df9795df97b5dfa7d5efa7f5efa815ffb835ffb8560fb8761fc8961fc8a62fc8c63fc8e64fc9065fd9266fd9467fd9668fd9869fd9a6afd9b6bfe9d6cfe9f6dfea16efea36ffea571fea772fea973feaa74feac76feae77feb078feb27afeb47bfeb67cfeb77efeb97ffebb81febd82febf84fec185fec287fec488fec68afec88cfeca8dfecc8ffecd90fecf92fed194fed395fed597fed799fed89afdda9cfddc9efddea0fde0a1fde2a3fde3a5fde5a7fde7a9fde9aafdebacfcecaefceeb0fcf0b2fcf2b4fcf4b6fcf6b8fcf7b9fcf9bbfcfbbdfcfdbf"));
gr(kt("00000401000501010601010802010a02020c02020e03021004031204031405041706041907051b08051d09061f0a07220b07240c08260d08290e092b10092d110a30120a32140b34150b37160b39180c3c190c3e1b0c411c0c431e0c451f0c48210c4a230c4c240c4f260c51280b53290b552b0b572d0b592f0a5b310a5c320a5e340a5f3609613809623909633b09643d09653e0966400a67420a68440a68450a69470b6a490b6a4a0c6b4c0c6b4d0d6c4f0d6c510e6c520e6d540f6d550f6d57106e59106e5a116e5c126e5d126e5f136e61136e62146e64156e65156e67166e69166e6a176e6c186e6d186e6f196e71196e721a6e741a6e751b6e771c6d781c6d7a1d6d7c1d6d7d1e6d7f1e6c801f6c82206c84206b85216b87216b88226a8a226a8c23698d23698f24699025689225689326679526679727669827669a28659b29649d29649f2a63a02a63a22b62a32c61a52c60a62d60a82e5fa92e5eab2f5ead305dae305cb0315bb1325ab3325ab43359b63458b73557b93556ba3655bc3754bd3853bf3952c03a51c13a50c33b4fc43c4ec63d4dc73e4cc83f4bca404acb4149cc4248ce4347cf4446d04545d24644d34743d44842d54a41d74b3fd84c3ed94d3dda4e3cdb503bdd513ade5238df5337e05536e15635e25734e35933e45a31e55c30e65d2fe75e2ee8602de9612bea632aeb6429eb6628ec6726ed6925ee6a24ef6c23ef6e21f06f20f1711ff1731df2741cf3761bf37819f47918f57b17f57d15f67e14f68013f78212f78410f8850ff8870ef8890cf98b0bf98c0af98e09fa9008fa9207fa9407fb9606fb9706fb9906fb9b06fb9d07fc9f07fca108fca309fca50afca60cfca80dfcaa0ffcac11fcae12fcb014fcb216fcb418fbb61afbb81dfbba1ffbbc21fbbe23fac026fac228fac42afac62df9c72ff9c932f9cb35f8cd37f8cf3af7d13df7d340f6d543f6d746f5d949f5db4cf4dd4ff4df53f4e156f3e35af3e55df2e661f2e865f2ea69f1ec6df1ed71f1ef75f1f179f2f27df2f482f3f586f3f68af4f88ef5f992f6fa96f8fb9af9fc9dfafda1fcffa4"));
var Hr = gr(kt("0d088710078813078916078a19068c1b068d1d068e20068f2206902406912605912805922a05932c05942e05952f059631059733059735049837049938049a3a049a3c049b3e049c3f049c41049d43039e44039e46039f48039f4903a04b03a14c02a14e02a25002a25102a35302a35502a45601a45801a45901a55b01a55c01a65e01a66001a66100a76300a76400a76600a76700a86900a86a00a86c00a86e00a86f00a87100a87201a87401a87501a87701a87801a87a02a87b02a87d03a87e03a88004a88104a78305a78405a78606a68707a68808a68a09a58b0aa58d0ba58e0ca48f0da4910ea3920fa39410a29511a19613a19814a099159f9a169f9c179e9d189d9e199da01a9ca11b9ba21d9aa31e9aa51f99a62098a72197a82296aa2395ab2494ac2694ad2793ae2892b02991b12a90b22b8fb32c8eb42e8db52f8cb6308bb7318ab83289ba3388bb3488bc3587bd3786be3885bf3984c03a83c13b82c23c81c33d80c43e7fc5407ec6417dc7427cc8437bc9447aca457acb4679cc4778cc4977cd4a76ce4b75cf4c74d04d73d14e72d24f71d35171d45270d5536fd5546ed6556dd7566cd8576bd9586ada5a6ada5b69db5c68dc5d67dd5e66de5f65de6164df6263e06363e16462e26561e26660e3685fe4695ee56a5de56b5de66c5ce76e5be76f5ae87059e97158e97257ea7457eb7556eb7655ec7754ed7953ed7a52ee7b51ef7c51ef7e50f07f4ff0804ef1814df1834cf2844bf3854bf3874af48849f48948f58b47f58c46f68d45f68f44f79044f79143f79342f89441f89540f9973ff9983ef99a3efa9b3dfa9c3cfa9e3bfb9f3afba139fba238fca338fca537fca636fca835fca934fdab33fdac33fdae32fdaf31fdb130fdb22ffdb42ffdb52efeb72dfeb82cfeba2cfebb2bfebd2afebe2afec029fdc229fdc328fdc527fdc627fdc827fdca26fdcb26fccd25fcce25fcd025fcd225fbd324fbd524fbd724fad824fada24f9dc24f9dd25f8df25f8e125f7e225f7e425f6e626f6e826f5e926f5eb27f4ed27f3ee27f3f027f2f227f1f426f1f525f0f724f0f921"));
function Tf(e, t, n, r) {
  const a = window.devicePixelRatio || 1;
  e.width = n * a, e.height = r * a, e.style.width = `${n}px`, e.style.height = `${r}px`, t.scale(a, a);
}
function fa(e, t, n) {
  const r = Math.min(e / n, t);
  return {
    width: n * r,
    height: r
  };
}
function Qi(e, t, n, r, a, l, s) {
  const o = e - a - s, u = t - r - l, f = fa(o, u, n);
  return {
    width: f.width + a + s,
    height: f.height + r + l
  };
}
function jr(e) {
  return e >= 1e-3 && e <= 1 || e >= -1 && e <= 1e-3 ? Pe(".3~f")(e) : Pe("~s")(e);
}
function Jn(e) {
  return e < 1e-5 ? Pe(".1~p")(e) : e < 1e-3 ? Pe(".2~p")(e) : Pe(".3~p")(e);
}
const ei = Pe(".3~f"), Et = Pe(".2~f"), ti = Pe(".2~f"), Af = Pe(".3~f"), hn = Pe(".2~%"), ni = (e) => Pe(".2~f")(e * 100), Ht = Pe(",d"), ri = Pe(".3~s"), Ji = [
  {
    key: "Instance count",
    value: (e, t, n) => Ht(n)
  },
  {
    key: "Activation value",
    value: (e, t, n) => `${Et(e)} to ${Et(t)}`
  }
];
var qf = /* @__PURE__ */ ne("<canvas></canvas>");
function bn(e, t) {
  pe(t, !0);
  let n = N(t, "orientation", 3, "horizontal"), r = N(t, "marginTop", 3, 10), a = N(t, "marginRight", 3, 10), l = N(t, "marginBottom", 3, 10), s = N(t, "marginLeft", 3, 10), o = N(t, "title", 3, ""), u = N(t, "tickLabelFontSize", 3, 10), f = N(t, "titleFontSize", 3, 12), v = /* @__PURE__ */ re(null), c = /* @__PURE__ */ x(() => i(v) ? i(v).getContext("2d", { alpha: !1 }) : null);
  function d(_, p, E, k, T, w, q, L) {
    const C = Kt().domain([
      p.domain()[0],
      p.domain()[p.domain().length - 1]
    ]).range([L, E - w]), I = C.range()[1] - C.range()[0], X = k - T - q, $ = p.domain().length, A = t.tickValues ?? C.ticks(Math.max(Math.min(I / 50, 10), $));
    _.fillStyle = "white", _.fillRect(0, 0, E, k);
    for (let S = 0; S < I; S++)
      _.fillStyle = p.interpolator()(S / I), _.fillRect(S + L, T, 1, X);
    Ja(_, "bottom", C, {
      translateY: k - q,
      tickValues: A,
      tickFormat: t.tickFormat,
      title: o(),
      titleAnchor: "left",
      titleOffsetX: L,
      titleOffsetY: -q - X,
      marginTop: T,
      marginRight: w,
      marginBottom: q,
      marginLeft: L,
      tickLabelFontSize: u(),
      titleFontSize: f(),
      numTicks: t.numTicks
    });
  }
  function g(_, p, E, k, T, w, q, L) {
    const C = Kt().domain([
      p.domain()[0],
      p.domain()[p.domain().length - 1]
    ]).range([k - q, T]), I = E - L - w, X = C.range()[0] - C.range()[1];
    _.fillStyle = "white", _.fillRect(0, 0, E, k);
    for (let $ = 0; $ < X; $++)
      _.fillStyle = p.interpolator()(1 - $ / X), _.fillRect(L, $ + T, I, 1);
    Ja(_, "right", C, {
      translateX: E - w,
      tickValues: t.tickValues,
      tickFormat: t.tickFormat,
      title: o(),
      marginTop: T,
      marginRight: w,
      marginBottom: q,
      marginLeft: L,
      tickLabelFontSize: u(),
      titleFontSize: f(),
      numTicks: t.numTicks
    });
  }
  Er(() => {
    i(v) && i(c) && Tf(i(v), i(c), t.width, t.height);
  }), Er(() => {
    i(c) && (n() === "horizontal" ? d(i(c), t.color, t.width, t.height, r(), a(), l(), s()) : g(i(c), t.color, t.width, t.height, r(), a(), l(), s()));
  });
  var h = qf();
  Wn(h, (_) => J(v, _), () => i(v)), D(e, h), we();
}
var Sf = /* @__PURE__ */ ne('<div class="sae-tooltip svelte-medmur"><!></div>');
function hr(e, t) {
  pe(t, !0);
  function n(g, h, _, p) {
    return _.top - g < h.top ? _.bottom - h.top + p : _.top - h.top - g - p;
  }
  function r(g, h, _, p) {
    const E = g / 2, k = (_.left + _.right) / 2;
    return k - E < h.left ? _.right - h.left + p : k + E > h.right ? _.left - h.left - g - p : _.left - h.left + _.width / 2 - E;
  }
  const a = 4;
  let l = /* @__PURE__ */ re(0), s = /* @__PURE__ */ re(0);
  const o = /* @__PURE__ */ x(() => t.anchor.getBoundingClientRect()), u = /* @__PURE__ */ x(() => ea.value.getBoundingClientRect());
  let f = /* @__PURE__ */ x(() => n(i(s), i(u), i(o), a)), v = /* @__PURE__ */ x(() => r(i(l), i(u), i(o), a));
  var c = Sf(), d = b(c);
  Cr(d, () => t.children), te(() => Ce(c, `left: ${i(v) ?? ""}px; top: ${i(f) ?? ""}px;`)), Ue(c, "offsetWidth", (g) => J(l, g)), Ue(c, "offsetHeight", (g) => J(s, g)), D(e, c), we();
}
var Ef = /* @__PURE__ */ ke('<g pointer-events="none"><rect fill="none"></rect><rect fill="none"></rect></g>');
function $i(e, t) {
  let n = N(t, "color1", 3, "var(--color-black)"), r = N(t, "color2", 3, "var(--color-white)"), a = N(t, "strokeWidth", 3, 1), l = N(t, "strokeDashArray", 3, "4");
  var s = Ef(), o = b(s), u = m(o);
  te(() => {
    M(s, "transform", `translate(${t.x ?? ""},${t.y ?? ""})`), M(o, "width", t.width), M(o, "height", t.height), M(o, "stroke-width", a()), M(o, "stroke", n()), M(u, "width", t.width), M(u, "height", t.height), M(u, "stroke-width", a()), M(u, "stroke", r()), M(u, "stroke-dasharray", l());
  }), D(e, s);
}
var Lf = /* @__PURE__ */ ne('<tr class="svelte-1u00ohp"><td class="svelte-1u00ohp"> </td><td class="svelte-1u00ohp"> </td></tr>'), Nf = /* @__PURE__ */ ne('<table class="svelte-1u00ohp"><tbody class="svelte-1u00ohp"></tbody></table>');
function Mn(e, t) {
  var n = Nf(), r = b(n);
  Ae(r, 21, () => t.data, Te, (a, l) => {
    let s = () => i(l).key, o = () => i(l).value;
    var u = Lf(), f = b(u), v = b(f), c = m(f), d = b(c);
    te(() => {
      de(v, s()), de(d, o());
    }), D(a, u);
  }), D(e, n);
}
var Ff = /* @__PURE__ */ ke('<rect class="sae-cm-cell"></rect><!>', 1), Cf = /* @__PURE__ */ ne('<div class="sae-cm-container svelte-kw462c"><svg><g></g><!><!></svg> <!> <!></div>');
function el(e, t) {
  pe(t, !0);
  let n = N(t, "showDifference", 3, !1), r = N(t, "marginTop", 3, 72), a = N(t, "marginRight", 3, 72), l = N(t, "marginBottom", 3, 72), s = N(t, "marginLeft", 3, 72), o = N(t, "legend", 3, "horizontal");
  function u(H, j, z, Y, K, V, ie) {
    if (ie === "none")
      return {
        svgWidth: H,
        svgHeight: j,
        legendWidth: 0,
        legendHeight: 0,
        legendMarginTop: 0,
        legendMarginRight: 0,
        legendMarginBottom: 0,
        legendMarginLeft: 0
      };
    if (ie === "horizontal") {
      const Z = K - 16;
      return {
        svgWidth: H,
        svgHeight: j - Z,
        legendWidth: H,
        legendHeight: Z,
        legendMarginTop: 16,
        legendMarginRight: Y,
        legendMarginBottom: 32,
        legendMarginLeft: V
      };
    } else {
      const Z = Y - 16;
      return {
        svgWidth: H - Z,
        svgHeight: j,
        legendWidth: Z,
        legendHeight: j,
        legendMarginTop: z,
        legendMarginRight: 60,
        legendMarginBottom: K,
        legendMarginLeft: 0
      };
    }
  }
  const f = /* @__PURE__ */ x(() => u(t.width, t.height, r(), a(), l(), s(), o()));
  function v(H, j) {
    return j !== void 0 ? io(H.cells, j.cells).map(([z, Y]) => ({
      ...z,
      pp_delta: z.pct - Y.pct
    })) : H.cells.map((z) => ({ ...z, pp_delta: 0 }));
  }
  const c = /* @__PURE__ */ x(() => v(t.cm, t.other)), d = /* @__PURE__ */ x(() => Yn().domain(qe.value.label_indices).range([
    s(),
    t.width - a()
  ]).padding(0)), g = /* @__PURE__ */ x(() => Yn().domain(qe.value.label_indices).range([
    r(),
    t.height - l()
  ]).padding(0));
  function h(H, j) {
    if (j) {
      const [z, Y] = Ys(H, (V) => V.pp_delta), K = Math.max(Math.abs(z ?? 0), Math.abs(Y ?? 0));
      return oa().domain([-K, 0, K]).interpolator(wf);
    }
    return St().domain([0, eo(H, (z) => z.pct) ?? 0]).interpolator(Mf);
  }
  const _ = /* @__PURE__ */ x(() => h(i(c), n()));
  function p(H) {
    return qe.value.labels[H];
  }
  const E = le.xs, k = 3, T = 6, w = /* @__PURE__ */ x(() => l() - E - k - T), q = /* @__PURE__ */ x(() => s() - E - k - T);
  let L = /* @__PURE__ */ re(null);
  function C(H, j, z) {
    J(L, { data: j, anchor: H.currentTarget, index: z }, !0);
  }
  function I() {
    J(L, null);
  }
  var X = Cf();
  let $;
  var A = b(X), S = b(A);
  Ae(S, 21, () => i(c), Te, (H, j, z) => {
    var Y = Ff();
    const K = /* @__PURE__ */ x(() => n() ? i(_)(i(j).pp_delta) : i(_)(i(j).pct));
    var V = Se(Y), ie = m(V);
    {
      var ae = (Z) => {
        const ge = /* @__PURE__ */ x(() => (i(d)(i(j).label) ?? 0) + 0.5), me = /* @__PURE__ */ x(() => i(d).bandwidth() - 1), ye = /* @__PURE__ */ x(() => (i(g)(i(j).pred_label) ?? 0) + 1), Me = /* @__PURE__ */ x(() => i(g).bandwidth() - 1);
        $i(Z, {
          get x() {
            return i(ge);
          },
          get width() {
            return i(me);
          },
          get y() {
            return i(ye);
          },
          get height() {
            return i(Me);
          }
        });
      };
      se(ie, (Z) => {
        var ge;
        z === ((ge = i(L)) == null ? void 0 : ge.index) && Z(ae);
      });
    }
    te(
      (Z, ge, me, ye) => {
        M(V, "x", Z), M(V, "width", ge), M(V, "y", me), M(V, "height", ye), M(V, "fill", i(K));
      },
      [
        () => (i(d)(i(j).label) ?? 0) + 0.5,
        () => i(d).bandwidth() - 1,
        () => (i(g)(i(j).pred_label) ?? 0) + 1,
        () => i(g).bandwidth() - 1
      ]
    ), Ke("mouseenter", V, (Z) => C(Z, i(j), z)), Ke("mouseleave", V, I), D(H, Y);
  });
  var y = m(S);
  const R = /* @__PURE__ */ x(() => i(f).svgHeight - l()), P = /* @__PURE__ */ x(() => i(w) <= i(d).bandwidth() ? 0 : -45);
  Zt(y, {
    orientation: "bottom",
    get scale() {
      return i(d);
    },
    get translateY() {
      return i(R);
    },
    title: "True label",
    titleAnchor: "center",
    tickFormat: p,
    get tickLabelAngle() {
      return i(P);
    },
    get marginTop() {
      return r();
    },
    get marginRight() {
      return a();
    },
    get marginBottom() {
      return l();
    },
    get marginLeft() {
      return s();
    },
    get tickLabelFontSize() {
      return E;
    },
    tickPadding: k,
    tickLineSize: T,
    get maxTickLabelSpace() {
      return i(w);
    },
    get titleFontSize() {
      return le.sm;
    }
  });
  var F = m(y);
  Zt(F, {
    orientation: "left",
    get scale() {
      return i(g);
    },
    get translateX() {
      return s();
    },
    title: "Predicted label",
    titleAnchor: "center",
    tickFormat: p,
    get marginTop() {
      return r();
    },
    get marginRight() {
      return a();
    },
    get marginBottom() {
      return l();
    },
    get marginLeft() {
      return s();
    },
    get tickLabelFontSize() {
      return E;
    },
    tickPadding: k,
    tickLineSize: T,
    get maxTickLabelSpace() {
      return i(q);
    },
    get titleFontSize() {
      return le.sm;
    }
  });
  var G = m(A, 2);
  {
    var O = (H) => {
      const j = /* @__PURE__ */ x(() => n() ? "Percentage point difference" : "Percent of data"), z = /* @__PURE__ */ x(() => n() ? ni : hn);
      bn(H, {
        get width() {
          return i(f).legendWidth;
        },
        get height() {
          return i(f).legendHeight;
        },
        get color() {
          return i(_);
        },
        get orientation() {
          return o();
        },
        get marginTop() {
          return i(f).legendMarginTop;
        },
        get marginRight() {
          return i(f).legendMarginRight;
        },
        get marginBottom() {
          return i(f).legendMarginBottom;
        },
        get marginLeft() {
          return i(f).legendMarginLeft;
        },
        get title() {
          return i(j);
        },
        get tickLabelFontSize() {
          return E;
        },
        get titleFontSize() {
          return le.sm;
        },
        get tickFormat() {
          return i(z);
        }
      });
    };
    se(G, (H) => {
      o() !== "none" && H(O);
    });
  }
  var W = m(G, 2);
  {
    var ee = (H) => {
      hr(H, dr(() => i(L), {
        children: (j, z) => {
          var Y = Nt(), K = Se(Y);
          {
            var V = (ie) => {
              const ae = /* @__PURE__ */ x(() => [
                {
                  key: "True label",
                  value: qe.value.labels[i(L).data.label]
                },
                {
                  key: "Predicted label",
                  value: qe.value.labels[i(L).data.pred_label]
                },
                {
                  key: "Percent of data",
                  value: hn(i(L).data.pct)
                },
                {
                  key: "Instance count",
                  value: Ht(i(L).data.count)
                },
                ...n() ? [
                  {
                    key: "Difference",
                    value: `${ni(i(L).data.pp_delta)} pp`
                  }
                ] : []
              ]);
              Mn(ie, {
                get data() {
                  return i(ae);
                }
              });
            };
            se(K, (ie) => {
              i(L) && ie(V);
            });
          }
          D(j, Y);
        },
        $$slots: { default: !0 }
      }));
    };
    se(W, (H) => {
      i(L) && H(ee);
    });
  }
  te(() => {
    $ = Ce(X, "", $, {
      "flex-direction": o() === "vertical" ? "row" : "column"
    }), M(A, "width", i(f).svgWidth), M(A, "height", i(f).svgHeight);
  }), D(e, X), we();
}
var Pf = /* @__PURE__ */ ke('<rect></rect><rect pointer-events="none"></rect>', 1), Rf = /* @__PURE__ */ ne("<div><svg><g></g><!><!></svg> <!></div>");
function ua(e, t) {
  pe(t, !0);
  let n = N(t, "marginLeft", 3, 0), r = N(t, "marginTop", 3, 0), a = N(t, "marginRight", 3, 0), l = N(t, "marginBottom", 3, 0), s = N(t, "xAxisLabel", 3, ""), o = N(t, "yAxisLabel", 3, ""), u = N(t, "showXAxis", 3, !0), f = N(t, "showYAxis", 3, !0), v = N(t, "xFormat", 3, jr), c = N(t, "yFormat", 3, jr), d = N(t, "tooltipEnabled", 3, !0), g = N(t, "tooltipData", 19, () => [
    {
      key: s(),
      value: (P, F, G) => `${v()(P)} - ${v()(F)}`
    },
    {
      key: o(),
      value: (P, F, G) => c()(G)
    }
  ]), h = /* @__PURE__ */ x(() => Kt().domain([
    t.data.thresholds[0],
    t.data.thresholds[t.data.thresholds.length - 1]
  ]).range([
    n(),
    t.width - a()
  ])), _ = /* @__PURE__ */ x(() => Math.max(...t.data.counts)), p = /* @__PURE__ */ x(() => Kt().domain([0, i(_)]).nice().range([
    t.height - l(),
    r()
  ])), E = /* @__PURE__ */ x(() => ta(t.data.counts.length)), k = /* @__PURE__ */ x(() => Bi(t.data.thresholds)), T = /* @__PURE__ */ re(null);
  function w(P, F, G, O, W) {
    J(
      T,
      {
        count: F,
        xMin: G,
        xMax: O,
        anchor: P.currentTarget,
        index: W
      },
      !0
    );
  }
  function q() {
    J(T, null);
  }
  var L = Rf(), C = b(L), I = b(C);
  Ae(I, 21, () => i(E), Te, (P, F) => {
    var G = Pf(), O = Se(G), W = m(O);
    te(
      (ee, H, j, z, Y, K, V, ie) => {
        var ae, Z;
        M(O, "x", ee), M(O, "width", H), M(O, "y", j), M(O, "height", z), M(O, "fill", i(F) === ((ae = i(T)) == null ? void 0 : ae.index) ? "var(--color-neutral-200)" : "var(--color-white)"), M(W, "x", Y), M(W, "width", K), M(W, "y", V), M(W, "height", ie), M(W, "fill", i(F) === ((Z = i(T)) == null ? void 0 : Z.index) ? "var(--color-black)" : "var(--color-neutral-500)");
      },
      [
        () => i(h)(i(k)[i(F)][0]),
        () => Math.max(0, i(h)(i(k)[i(F)][1]) - i(h)(i(k)[i(F)][0])),
        () => i(p).range()[1],
        () => i(p).range()[0] - i(p).range()[1],
        () => i(h)(i(k)[i(F)][0]) + 0.5,
        () => Math.max(0, i(h)(i(k)[i(F)][1]) - i(h)(i(k)[i(F)][0]) - 1),
        () => i(p)(t.data.counts[i(F)]),
        () => i(p)(0) - i(p)(t.data.counts[i(F)])
      ]
    ), Ke("mouseenter", O, function(...ee) {
      var H;
      (H = d() ? (j) => w(j, t.data.counts[i(F)], i(k)[i(F)][0], i(k)[i(F)][1], i(F)) : null) == null || H.apply(this, ee);
    }), Ke("mouseleave", O, function(...ee) {
      var H;
      (H = d() ? q : null) == null || H.apply(this, ee);
    }), D(P, G);
  });
  var X = m(I);
  {
    var $ = (P) => {
      const F = /* @__PURE__ */ x(() => t.height - l());
      Zt(P, {
        orientation: "bottom",
        get scale() {
          return i(h);
        },
        get translateY() {
          return i(F);
        },
        get title() {
          return s();
        },
        titleAnchor: "right",
        get tickFormat() {
          return v();
        },
        get marginTop() {
          return r();
        },
        get marginRight() {
          return a();
        },
        get marginBottom() {
          return l();
        },
        get marginLeft() {
          return n();
        },
        numTicks: 5,
        get titleFontSize() {
          return le.sm;
        },
        get tickLabelFontSize() {
          return le.xs;
        },
        showDomain: !0
      });
    };
    se(X, (P) => {
      u() && P($);
    });
  }
  var A = m(X);
  {
    var S = (P) => {
      Zt(P, {
        orientation: "left",
        get scale() {
          return i(p);
        },
        get translateX() {
          return n();
        },
        get title() {
          return o();
        },
        titleAnchor: "top",
        get tickFormat() {
          return c();
        },
        get marginTop() {
          return r();
        },
        get marginRight() {
          return a();
        },
        get marginBottom() {
          return l();
        },
        get marginLeft() {
          return n();
        },
        numTicks: 5,
        get titleFontSize() {
          return le.sm;
        },
        get tickLabelFontSize() {
          return le.xs;
        }
      });
    };
    se(A, (P) => {
      f() && P(S);
    });
  }
  var y = m(C, 2);
  {
    var R = (P) => {
      hr(P, dr(() => i(T), {
        children: (F, G) => {
          const O = /* @__PURE__ */ x(() => g().map(({ key: W, value: ee }) => {
            var H, j, z;
            return {
              key: W,
              value: ee(((H = i(T)) == null ? void 0 : H.xMin) ?? 0, ((j = i(T)) == null ? void 0 : j.xMax) ?? 0, ((z = i(T)) == null ? void 0 : z.count) ?? 0)
            };
          }));
          Mn(F, {
            get data() {
              return i(O);
            }
          });
        },
        $$slots: { default: !0 }
      }));
    };
    se(y, (P) => {
      i(T) && P(R);
    });
  }
  te(() => {
    M(C, "width", t.width), M(C, "height", t.height);
  }), D(e, L), we();
}
var If = /* @__PURE__ */ ne(`<div class="sae-info svelte-v66m4x">This histogram shows how often the features in the SAE activate.
              The activation rate is the percentage of instances that cause a
              feature to activate. Note that the x-axis uses a log scale.</div>`), Df = /* @__PURE__ */ ne('<div class="sae-overview-container svelte-v66m4x"><div class="sae-col svelte-v66m4x"><div class="sae-section svelte-v66m4x"><div class="sae-section-header svelte-v66m4x">Summary</div> <div class="sae-table-container svelte-v66m4x"><table class="svelte-v66m4x"><thead class="svelte-v66m4x"><tr><th colspan="2" class="svelte-v66m4x">Dataset</th></tr></thead><tbody><tr class="svelte-v66m4x"><td class="svelte-v66m4x">Instances</td><td class="svelte-v66m4x"> </td></tr><tr class="svelte-v66m4x"><td class="svelte-v66m4x">Tokens</td><td class="svelte-v66m4x"> </td></tr></tbody></table> <table class="svelte-v66m4x"><thead class="svelte-v66m4x"><tr><th colspan="2" class="svelte-v66m4x">Model</th></tr></thead><tbody><tr class="svelte-v66m4x"><td class="svelte-v66m4x">Error rate</td><td class="svelte-v66m4x"> </td></tr><tr class="svelte-v66m4x"><td class="svelte-v66m4x">Log loss</td><td class="svelte-v66m4x"> </td></tr></tbody></table> <table class="svelte-v66m4x"><thead class="svelte-v66m4x"><tr><th colspan="2" class="svelte-v66m4x">SAE</th></tr></thead><tbody><tr class="svelte-v66m4x"><td class="svelte-v66m4x">Total features</td><td class="svelte-v66m4x"> </td></tr><tr class="svelte-v66m4x"><td class="svelte-v66m4x">Inactive features</td><td class="svelte-v66m4x"> </td></tr></tbody></table></div></div> <div class="sae-section svelte-v66m4x"><div class="sae-section-header-row svelte-v66m4x"><div class="sae-section-header svelte-v66m4x">Feature activation rate distribution</div> <!></div> <div class="sae-vis svelte-v66m4x"><!></div></div></div> <div class="sae-col svelte-v66m4x"><div class="sae-section svelte-v66m4x"><div class="sae-section-header svelte-v66m4x">Confusion Matrix</div> <div class="sae-vis svelte-v66m4x"><!></div></div></div></div>');
function zf(e, t) {
  pe(t, !0);
  const n = /* @__PURE__ */ x(() => Mt.value.n_non_activating_features + Mt.value.n_dead_features), r = /* @__PURE__ */ x(() => i(n) / Mt.value.n_total_features);
  let a = /* @__PURE__ */ re(0), l = /* @__PURE__ */ re(0);
  const s = /* @__PURE__ */ x(() => fa(i(a), i(l), 1.6)), o = 8, u = 88, f = 80, v = 80;
  let c = /* @__PURE__ */ re(0), d = /* @__PURE__ */ re(0);
  const g = /* @__PURE__ */ x(() => Qi(i(c), i(d), 1, o, u, f, v));
  var h = Df(), _ = b(h), p = b(_), E = m(b(p), 2), k = b(E), T = m(b(k)), w = b(T), q = m(b(w)), L = b(q), C = m(w), I = m(b(C)), X = b(I), $ = m(k, 2), A = m(b($)), S = b(A), y = m(b(S)), R = b(y), P = m(S), F = m(b(P)), G = b(F), O = m($, 2), W = m(b(O)), ee = b(W), H = m(b(ee)), j = b(H), z = m(ee), Y = m(b(z)), K = b(Y), V = m(p, 2);
  Ce(V, "", {}, { flex: "1" });
  var ie = b(V), ae = m(b(ie), 2);
  Qe(ae, {
    position: "right",
    trigger: (B) => {
      Ze(B, {});
    },
    content: (B) => {
      var fe = If();
      D(B, fe);
    },
    $$slots: { trigger: !0, content: !0 }
  });
  var Z = m(ie, 2), ge = b(Z);
  ua(ge, {
    get data() {
      return Mt.value.sequence_act_rate_histogram;
    },
    marginTop: 20,
    marginRight: 20,
    marginLeft: 50,
    marginBottom: 40,
    get width() {
      return i(s).width;
    },
    get height() {
      return i(s).height;
    },
    xAxisLabel: "lg activation rate →",
    yAxisLabel: "↑ Feature count",
    tooltipData: [
      {
        key: "Feature count",
        value: (U, Q, B) => Ht(B)
      },
      {
        key: "Activation rate",
        value: (U, Q, B) => `${Jn(10 ** U)} to ${Jn(10 ** Q)}`
      },
      {
        key: "Log 10 act. rate",
        value: (U, Q, B) => `${ei(U)} to ${ei(Q)}`
      }
    ]
  });
  var me = m(_, 2), ye = b(me);
  Ce(ye, "", {}, { flex: "1" });
  var Me = m(b(ye), 2), Ye = b(Me);
  el(Ye, {
    get cm() {
      return Ot.value.cm;
    },
    legend: "vertical",
    get width() {
      return i(g).width;
    },
    get height() {
      return i(g).height;
    },
    marginTop: o,
    marginRight: u,
    marginBottom: f,
    marginLeft: v
  }), te(
    (U, Q, B, fe, be, xe, Ee) => {
      de(L, U), de(X, Q), de(R, B), de(G, fe), de(j, be), de(K, `${xe ?? ""} (${Ee ?? ""})`);
    },
    [
      () => ri(qe.value.n_sequences),
      () => ri(qe.value.n_tokens),
      () => hn(Ot.value.cm.error_pct),
      () => Af(Ot.value.log_loss),
      () => Ht(Mt.value.n_total_features),
      () => Ht(i(n)),
      () => hn(i(r))
    ]
  ), Ue(Z, "offsetWidth", (U) => J(a, U)), Ue(Z, "offsetHeight", (U) => J(l, U)), Ue(Me, "offsetWidth", (U) => J(c, U)), Ue(Me, "offsetHeight", (U) => J(d, U)), D(e, h), we();
}
function Of(e, t) {
  e.key === "Enter" && t();
}
var Bf = /* @__PURE__ */ ne("<option> </option>"), Hf = (e, t) => t(e, "pred_label"), jf = /* @__PURE__ */ ne("<option> </option>"), Wf = /* @__PURE__ */ ne("<option> </option>"), Vf = (e, t) => t(e, "true_label"), Yf = /* @__PURE__ */ ne("<option> </option>"), Xf = /* @__PURE__ */ ne("<option> </option>"), Gf = /* @__PURE__ */ ne('<label class="svelte-1cfvoy8"><span class="sae-title svelte-1cfvoy8">Predicted label:</span> <select class="svelte-1cfvoy8"><optgroup label="Wildcards"></optgroup><optgroup label="Labels"></optgroup></select></label> <label class="svelte-1cfvoy8"><span class="sae-title svelte-1cfvoy8">True label:</span> <select class="svelte-1cfvoy8"><optgroup label="Wildcards"></optgroup><optgroup label="Classes"></optgroup></select></label>', 1), Uf = /* @__PURE__ */ ne(
  `<p>The confusion matrix ranking orders the features based on the
              model's predictions on the instances that cause the features to
              activate.</p> <p> </p>`,
  1
), Kf = /* @__PURE__ */ ne('<div class="sae-info svelte-1cfvoy8"><!></div>'), Zf = /* @__PURE__ */ ne('<div class="sae-container svelte-1cfvoy8"><div class="sae-control-row svelte-1cfvoy8"><label class="svelte-1cfvoy8"><span class="sae-title svelte-1cfvoy8">Ranking:</span> <select class="svelte-1cfvoy8"></select></label> <!> <!></div> <div class="sae-control-row svelte-1cfvoy8"><div class="sae-feature-table-order svelte-1cfvoy8"><span class="sae-title svelte-1cfvoy8">Order:</span> <label class="svelte-1cfvoy8"><input type="radio" name="direction" class="svelte-1cfvoy8"/> <span>Ascending</span></label> <label class="svelte-1cfvoy8"><input type="radio" name="direction" class="svelte-1cfvoy8"/> <span>Descending</span></label></div> <div class="sae-feature-table-min-act-rate"><label class="svelte-1cfvoy8"><span class="sae-title svelte-1cfvoy8">Min. activation rate:</span> <input type="number" step="0.0001" class="svelte-1cfvoy8"/> <span>%</span></label></div></div></div>');
function Qf(e, t) {
  pe(t, !0);
  const n = [
    { label: "ID", value: "feature_id" },
    {
      label: "Activation Rate",
      value: "sequence_act_rate"
    },
    { label: "Confusion Matrix", value: "label" }
  ], r = [
    { label: "Any", value: "any" },
    { label: "Different", value: "different" }
  ], a = /* @__PURE__ */ x(() => qe.value.labels.map((S, y) => ({ label: S, value: `${y}` })));
  function l(S) {
    const y = S.currentTarget.value;
    y === "feature_id" ? ce.value = {
      kind: "feature_id",
      descending: ce.value.descending
    } : y === "sequence_act_rate" ? ce.value = {
      kind: "sequence_act_rate",
      descending: ce.value.descending
    } : ce.value = {
      kind: "label",
      true_label: "different",
      pred_label: "any",
      descending: ce.value.descending
    };
  }
  function s(S, y) {
    if (ce.value.kind !== "label")
      return;
    const R = S.currentTarget.value;
    ce.value = { ...ce.value, [y]: R };
  }
  function o(S) {
    const y = S.currentTarget.value;
    ce.value = {
      ...ce.value,
      descending: y === "descending"
    };
  }
  let u = /* @__PURE__ */ x(() => Rr.value * 100);
  function f() {
    Rr.value = i(u) / 100;
  }
  function v(S) {
    const { true_label: y, pred_label: R } = S, P = "Your current selection ranks the features by", F = "the percentage of instances where", G = "any", O = "different", W = (ee) => qe.value.labels[Number(ee)];
    return y === G && R === G || y === O && R === O ? `${P} their ID. Try another combination!` : y === G && R === O || y === O && R === G ? `${P} ${F} the model is wrong.` : y === G ? `${P} ${F} the model predicts ${W(R)}.` : R === G ? `${P} ${F} the true label is ${W(y)}.` : y === O ? `${P} ${F} the model incorrectly predicts ${W(R)}.` : R === O ? `${P} ${F} the true label is ${W(y)} and the model is incorrect.` : R === y ? `${P} ${F} the model correctly predicts ${W(y)}.` : `${P} ${F} the model predicts ${W(R)}, but the true label is ${W(y)}.`;
  }
  var c = Zf(), d = b(c), g = b(d), h = m(b(g), 2);
  Nn(h, () => ce.value.kind);
  var _;
  h.__change = l, Ae(h, 21, () => n, Te, (S, y) => {
    var R = Bf(), P = {}, F = b(R);
    te(() => {
      P !== (P = i(y).value) && (R.value = (R.__value = i(y).value) ?? ""), de(F, i(y).label);
    }), D(S, R);
  });
  var p = m(g, 2);
  {
    var E = (S) => {
      var y = Gf(), R = Se(y), P = m(b(R), 2);
      Nn(P, () => ce.value.pred_label);
      var F;
      P.__change = [Hf, s];
      var G = b(P);
      Ae(G, 21, () => r, Te, (Y, K) => {
        var V = jf(), ie = {}, ae = b(V);
        te(() => {
          ie !== (ie = i(K).value) && (V.value = (V.__value = i(K).value) ?? ""), de(ae, i(K).label);
        }), D(Y, V);
      });
      var O = m(G);
      Ae(O, 21, () => i(a), Te, (Y, K) => {
        var V = Wf(), ie = {}, ae = b(V);
        te(() => {
          ie !== (ie = i(K).value) && (V.value = (V.__value = i(K).value) ?? ""), de(ae, i(K).label);
        }), D(Y, V);
      });
      var W = m(R, 2), ee = m(b(W), 2);
      Nn(ee, () => ce.value.true_label);
      var H;
      ee.__change = [Vf, s];
      var j = b(ee);
      Ae(j, 21, () => r, Te, (Y, K) => {
        var V = Yf(), ie = {}, ae = b(V);
        te(() => {
          ie !== (ie = i(K).value) && (V.value = (V.__value = i(K).value) ?? ""), de(ae, i(K).label);
        }), D(Y, V);
      });
      var z = m(j);
      Ae(z, 21, () => i(a), Te, (Y, K) => {
        var V = Xf(), ie = {}, ae = b(V);
        te(() => {
          ie !== (ie = i(K).value) && (V.value = (V.__value = i(K).value) ?? ""), de(ae, i(K).label);
        }), D(Y, V);
      }), te(() => {
        F !== (F = ce.value.pred_label) && (P.value = (P.__value = ce.value.pred_label) ?? "", zt(P, ce.value.pred_label)), H !== (H = ce.value.true_label) && (ee.value = (ee.__value = ce.value.true_label) ?? "", zt(ee, ce.value.true_label));
      }), D(S, y);
    };
    se(p, (S) => {
      ce.value.kind === "label" && S(E);
    });
  }
  var k = m(p, 2);
  Qe(k, {
    position: "bottom",
    trigger: (R) => {
      Ze(R, {});
    },
    content: (R) => {
      var P = Kf(), F = b(P);
      {
        var G = (W) => {
          var ee = ka(`The ID ranking orders the features by their index in the SAE. This
            essentially provides a random order.`);
          D(W, ee);
        }, O = (W, ee) => {
          {
            var H = (z) => {
              var Y = ka(`The activation rate ranking orders the features by the percentage of
            instances in the dataset that cause them to activate.`);
              D(z, Y);
            }, j = (z) => {
              var Y = Uf(), K = m(Se(Y), 2), V = b(K);
              te((ie) => de(V, ie), [
                () => v(ce.value)
              ]), D(z, Y);
            };
            se(
              W,
              (z) => {
                ce.value.kind === "sequence_act_rate" ? z(H) : z(j, !1);
              },
              ee
            );
          }
        };
        se(F, (W) => {
          ce.value.kind === "feature_id" ? W(G) : W(O, !1);
        });
      }
      D(R, P);
    },
    $$slots: { trigger: !0, content: !0 }
  });
  var T = m(d, 2), w = b(T), q = m(b(w), 2), L = b(q);
  qa(L, "ascending"), L.__change = o;
  var C = m(q, 2), I = b(C);
  qa(I, "descending"), I.__change = o;
  var X = m(w, 2), $ = b(X), A = m(b($), 2);
  A.__keydown = [Of, f], Ce(A, "", {}, { width: "7em" }), te(() => {
    _ !== (_ = ce.value.kind) && (h.value = (h.__value = ce.value.kind) ?? "", zt(h, ce.value.kind)), Sa(L, !ce.value.descending), Sa(I, ce.value.descending);
  }), Ke("blur", A, () => f()), cr(A, () => i(u), (S) => J(u, S)), D(e, c), we();
}
Ct(["change", "keydown"]);
var Jf = /* @__PURE__ */ ke('<rect></rect><rect pointer-events="none"></rect><!>', 1), $f = /* @__PURE__ */ ne('<div class="sae-heatmap-container svelte-k83kh4"><div><!> <svg><!><!><g></g></svg></div> <!> <!></div>');
function tl(e, t) {
  pe(t, !0);
  let n = N(t, "distribution", 3, null), r = N(t, "compareToBaseProbs", 3, !1), a = N(t, "maxColorDomain", 3, null), l = N(t, "marginTop", 3, 0), s = N(t, "marginRight", 3, 0), o = N(t, "marginBottom", 3, 0), u = N(t, "marginLeft", 3, 0), f = N(t, "xAxisLabel", 3, ""), v = N(t, "yAxisLabel", 3, ""), c = N(t, "showColorLegend", 3, !0), d = N(t, "showXAxis", 3, !0), g = N(t, "showYAxis", 3, !0), h = N(t, "tooltipEnabled", 3, !0);
  const _ = 16, p = /* @__PURE__ */ x(() => c() ? s() - _ : 0), E = /* @__PURE__ */ x(() => c() ? t.height : 0), k = /* @__PURE__ */ x(() => n() ? l() - 2 : 0), T = /* @__PURE__ */ x(() => l() - i(k)), w = /* @__PURE__ */ x(() => s() - i(p)), q = /* @__PURE__ */ x(() => t.width - i(p)), L = /* @__PURE__ */ x(() => t.height - i(k)), C = /* @__PURE__ */ x(() => c() ? l() : 0), I = /* @__PURE__ */ x(() => c() ? 60 : 0), X = /* @__PURE__ */ x(() => c() ? o() : 0), $ = /* @__PURE__ */ x(() => 0), A = /* @__PURE__ */ x(() => t.marginalEffects.probs.map((U, Q) => ({
    labelIndex: Q,
    points: Bi(t.marginalEffects.thresholds).map(([B, fe], be) => {
      const xe = U[be] >= 0 ? U[be] : NaN, Ee = Number.isNaN(xe) ? NaN : xe - Ot.value.cm.pred_label_pcts[Q];
      return {
        startAct: B,
        endAct: fe,
        prob: xe,
        delta: Ee
      };
    })
  })).filter((U, Q) => t.classes.includes(Q))), S = /* @__PURE__ */ x(() => Kt().domain([
    t.marginalEffects.thresholds[0],
    t.marginalEffects.thresholds[t.marginalEffects.thresholds.length - 1]
  ]).range([
    u(),
    i(q) - i(w)
  ])), y = /* @__PURE__ */ x(() => Yn().domain(t.classes).range([
    i(T),
    i(L) - o()
  ])), R = /* @__PURE__ */ x(() => a() ?? Math.max(...i(A).flatMap((U) => U.points.map((Q) => Number.isNaN(Q.prob) ? 0 : Q.prob)))), P = /* @__PURE__ */ x(() => a() ?? Math.max(...i(A).flatMap((U) => U.points.map((Q) => Math.abs(Number.isNaN(Q.delta) ? 0 : Q.delta))))), F = /* @__PURE__ */ x(() => St().domain([0, i(R)]).interpolator(Zi).unknown("var(--color-neutral-300)")), G = /* @__PURE__ */ x(() => oa().domain([-i(P), 0, i(P)]).interpolator(xf).unknown("var(--color-neutral-300)"));
  let O = /* @__PURE__ */ re(null);
  function W(U, Q, B, fe) {
    J(
      O,
      {
        point: Q,
        anchor: U.currentTarget,
        labelIndex: B,
        pointIndex: fe
      },
      !0
    );
  }
  function ee() {
    J(O, null);
  }
  var H = $f(), j = b(H), z = b(j);
  {
    var Y = (U) => {
      ua(U, {
        get data() {
          return n();
        },
        marginTop: 0,
        get marginRight() {
          return i(w);
        },
        get marginLeft() {
          return u();
        },
        marginBottom: 0,
        get width() {
          return i(q);
        },
        get height() {
          return i(k);
        },
        showXAxis: !1,
        showYAxis: !1,
        get xFormat() {
          return Et;
        },
        get tooltipEnabled() {
          return h();
        },
        get tooltipData() {
          return Ji;
        }
      });
    };
    se(z, (U) => {
      n() && U(Y);
    });
  }
  var K = m(z, 2), V = b(K);
  {
    var ie = (U) => {
      const Q = /* @__PURE__ */ x(() => i(L) - o());
      Zt(U, {
        orientation: "bottom",
        get scale() {
          return i(S);
        },
        get translateY() {
          return i(Q);
        },
        get title() {
          return f();
        },
        get marginTop() {
          return i(T);
        },
        get marginRight() {
          return i(w);
        },
        get marginBottom() {
          return o();
        },
        get marginLeft() {
          return u();
        },
        numTicks: 5,
        get tickLabelFontSize() {
          return le.xs;
        },
        get titleFontSize() {
          return le.sm;
        }
      });
    };
    se(V, (U) => {
      d() && U(ie);
    });
  }
  var ae = m(V);
  {
    var Z = (U) => {
      Zt(U, {
        orientation: "left",
        get scale() {
          return i(y);
        },
        get translateX() {
          return u();
        },
        tickFormat: (Q) => qe.value.labels[Q],
        get title() {
          return v();
        },
        get marginTop() {
          return i(T);
        },
        get marginRight() {
          return i(w);
        },
        get marginBottom() {
          return o();
        },
        get marginLeft() {
          return u();
        },
        get tickLabelFontSize() {
          return le.xs;
        },
        get titleFontSize() {
          return le.sm;
        }
      });
    };
    se(ae, (U) => {
      g() && U(Z);
    });
  }
  var ge = m(ae);
  Ae(ge, 21, () => i(A), Te, (U, Q) => {
    let B = () => i(Q).points, fe = () => i(Q).labelIndex;
    var be = Nt(), xe = Se(be);
    Ae(xe, 17, B, Te, (Ee, ue, _e) => {
      var tt = Jf(), Re = Se(tt);
      M(Re, "fill", "white");
      var Pt = m(Re), nl = m(Pt);
      {
        var rl = (ot) => {
          const Xe = /* @__PURE__ */ x(() => i(S)(i(ue).startAct) + 0.5), nn = /* @__PURE__ */ x(() => i(S)(i(ue).endAct) - i(S)(i(ue).startAct) - 1), br = /* @__PURE__ */ x(() => (i(y)(fe()) ?? 0) + 0.5), _r = /* @__PURE__ */ x(() => i(y).bandwidth() - 1);
          $i(ot, {
            get x() {
              return i(Xe);
            },
            get width() {
              return i(nn);
            },
            get y() {
              return i(br);
            },
            get height() {
              return i(_r);
            }
          });
        };
        se(nl, (ot) => {
          var Xe;
          fe() === ((Xe = i(O)) == null ? void 0 : Xe.labelIndex) && _e === i(O).pointIndex && ot(rl);
        });
      }
      te(
        (ot, Xe, nn, br, _r, al, il, ll, sl) => {
          M(Re, "x", ot), M(Re, "width", Xe), M(Re, "y", nn), M(Re, "height", br), M(Pt, "x", _r), M(Pt, "width", al), M(Pt, "y", il), M(Pt, "height", ll), M(Pt, "fill", sl);
        },
        [
          () => i(S)(i(ue).startAct),
          () => i(S)(i(ue).endAct) - i(S)(i(ue).startAct),
          () => i(y)(fe()) ?? 0,
          () => i(y).bandwidth(),
          () => i(S)(i(ue).startAct) + 0.5,
          () => i(S)(i(ue).endAct) - i(S)(i(ue).startAct) - 1,
          () => (i(y)(fe()) ?? 0) + 0.5,
          () => i(y).bandwidth() - 1,
          () => r() ? i(G)(i(ue).delta) : i(F)(i(ue).prob)
        ]
      ), Ke("mouseenter", Re, function(...ot) {
        var Xe;
        (Xe = h() ? (nn) => W(nn, i(ue), fe(), _e) : null) == null || Xe.apply(this, ot);
      }), Ke("mouseleave", Re, function(...ot) {
        var Xe;
        (Xe = h() ? ee : null) == null || Xe.apply(this, ot);
      }), D(Ee, tt);
    }), D(U, be);
  });
  var me = m(j, 2);
  {
    var ye = (U) => {
      const Q = /* @__PURE__ */ x(() => r() ? i(G) : i(F)), B = /* @__PURE__ */ x(() => r() ? "Difference from base prob." : "Mean predicted probability");
      bn(U, {
        get width() {
          return i(p);
        },
        get height() {
          return i(E);
        },
        get color() {
          return i(Q);
        },
        orientation: "vertical",
        get marginTop() {
          return i(C);
        },
        get marginRight() {
          return i(I);
        },
        get marginBottom() {
          return i(X);
        },
        marginLeft: i($),
        get title() {
          return i(B);
        },
        get tickLabelFontSize() {
          return le.xs;
        },
        get titleFontSize() {
          return le.sm;
        },
        get tickFormat() {
          return jr;
        }
      });
    };
    se(me, (U) => {
      c() && U(ye);
    });
  }
  var Me = m(me, 2);
  {
    var Ye = (U) => {
      hr(U, dr(() => i(O), {
        children: (Q, B) => {
          var fe = Nt(), be = Se(fe);
          {
            var xe = (Ee) => {
              const ue = /* @__PURE__ */ x(() => [
                {
                  key: "Activation value",
                  value: `${Et(i(O).point.startAct)} to ${Et(i(O).point.endAct)}`
                },
                {
                  key: "Predicted label",
                  value: qe.value.labels[i(O).labelIndex]
                },
                {
                  key: "Mean probability",
                  value: Number.isNaN(i(O).point.prob) ? "No data" : ti(i(O).point.prob)
                },
                ...r() ? [
                  {
                    key: "Diff. from base prob.",
                    value: ti(i(O).point.delta)
                  }
                ] : []
              ]);
              Mn(Ee, {
                get data() {
                  return i(ue);
                }
              });
            };
            se(be, (Ee) => {
              i(O) && Ee(xe);
            });
          }
          D(Q, fe);
        },
        $$slots: { default: !0 }
      }));
    };
    se(Me, (U) => {
      i(O) && U(Ye);
    });
  }
  te(() => {
    M(K, "width", i(q)), M(K, "height", i(L));
  }), D(e, H), we();
}
var eu = /* @__PURE__ */ ne('<div class="sae-token svelte-165qlb"><span class="sae-token-name svelte-165qlb"> </span></div>'), tu = /* @__PURE__ */ ne('<div class="sae-sequence svelte-165qlb"><!> <!></div>');
function ca(e, t) {
  pe(t, !0);
  let n = N(t, "tooltipEnabled", 3, !0), r = N(t, "hidePadding", 3, !1), a = /* @__PURE__ */ re(null);
  function l(d, g, h) {
    J(a, { data: g, anchor: d.currentTarget, index: h }, !0);
  }
  function s() {
    J(a, null);
  }
  var o = tu();
  let u;
  var f = b(o);
  Ae(f, 17, () => t.sequence.display_tokens, Te, (d, g, h) => {
    var _ = Nt(), p = Se(_);
    {
      var E = (k) => {
        var T = eu();
        const w = /* @__PURE__ */ x(() => i(g).max_act > 0 ? t.colorScale(i(g).max_act) : "var(--color-white)");
        let q;
        var L = b(T), C = b(L);
        te(() => {
          var I;
          q = Ce(T, "", q, {
            "--token-color": i(w),
            "font-weight": h === t.sequence.max_token_index && i(g).max_act > 0 ? "var(--font-bold)" : "var(--font-normal)",
            "background-color": n() && ((I = i(a)) == null ? void 0 : I.index) === h ? "var(--color-neutral-300)" : "var(--color-white)"
          }), de(C, i(g).display);
        }), Ke("mouseenter", T, function(...I) {
          var X;
          (X = n() ? ($) => l($, i(g), h) : null) == null || X.apply(this, I);
        }), Ke("mouseleave", T, function(...I) {
          var X;
          (X = n() ? s : null) == null || X.apply(this, I);
        }), D(k, T);
      };
      se(p, (k) => {
        r() && i(g).is_padding || k(E);
      });
    }
    D(d, _);
  });
  var v = m(f, 2);
  {
    var c = (d) => {
      hr(d, dr(() => i(a), {
        children: (g, h) => {
          var _ = Nt(), p = Se(_);
          {
            var E = (k) => {
              const T = /* @__PURE__ */ x(() => [
                {
                  key: "Token",
                  value: i(a).data.display
                },
                {
                  key: "Activation",
                  value: Et(i(a).data.max_act)
                }
              ]);
              Mn(k, {
                get data() {
                  return i(T);
                }
              });
            };
            se(p, (k) => {
              i(a) && k(E);
            });
          }
          D(g, _);
        },
        $$slots: { default: !0 }
      }));
    };
    se(v, (d) => {
      i(a) && d(c);
    });
  }
  te(() => u = Ce(o, "", u, { "flex-wrap": t.wrap ? "wrap" : "nowrap" })), D(e, o), we();
}
function nu(e, t, n) {
  return e < t ? t : e > n ? n : e;
}
function ru(e, t, n) {
  e.key === "Enter" && t(i(n) - 1);
}
var au = (e, t, n) => t(i(n) - 2), iu = (e, t, n) => t(i(n)), lu = /* @__PURE__ */ ne('<div class="sae-page-container svelte-xg014a"><button class="svelte-xg014a">←</button> <div class="sae-page-select svelte-xg014a"><span>Page</span> <input type="number" class="svelte-xg014a"/> <span>/</span> <span> </span></div> <button class="svelte-xg014a">→</button></div>');
function su(e, t) {
  pe(t, !0);
  let n = /* @__PURE__ */ x(() => It.value + 1);
  const r = /* @__PURE__ */ x(() => Math.log10(sn.value + 1) + 1);
  function a(g) {
    const h = nu(g, 0, sn.value);
    h === It.value ? J(n, h + 1) : It.value = h;
  }
  var l = lu(), s = b(l);
  s.__click = [au, a, n];
  var o = m(s, 2), u = m(b(o), 2);
  u.__keydown = [
    ru,
    a,
    n
  ];
  let f;
  var v = m(u, 4), c = b(v), d = m(o, 2);
  d.__click = [iu, a, n], te(() => {
    s.disabled = It.value <= 0, f = Ce(u, "", f, { width: `${i(r) ?? ""}em` }), de(c, sn.value + 1), d.disabled = It.value >= sn.value;
  }), Ke("blur", u, () => a(i(n) - 1)), cr(u, () => i(n), (g) => J(n, g)), D(e, l), we();
}
Ct(["click", "keydown"]);
var ou = /* @__PURE__ */ ne('<div class="sae-info svelte-6xvqq1">The index of the feature in the SAE.</div>'), fu = /* @__PURE__ */ ne('<div class="sae-info svelte-6xvqq1">The percentage of instances that activate the feature.</div>'), uu = /* @__PURE__ */ ne(`<div class="sae-info svelte-6xvqq1">A histogram of the feature's instance-level activation values.</div>`), cu = /* @__PURE__ */ ne(`<div class="sae-info sae-probabilities-info svelte-6xvqq1"><div>The probabilities of the top classes for instances that activate
              the feature. The x-axis encodes the activation value.</div> <!></div>`), du = /* @__PURE__ */ ne(`<div class="sae-info sae-example-info svelte-6xvqq1"><div>The token that maximally activates the feature and its surrounding
              context.</div> <!></div>`), vu = (e, t, n) => t.onClickFeature(i(n).feature_id), gu = /* @__PURE__ */ ne('<div><div><button class="sae-table-feature-id-btn svelte-6xvqq1"> </button></div></div> <div><div> </div></div> <div><!></div> <div><!></div> <div><!></div>', 1), hu = /* @__PURE__ */ ne('<div class="sae-table-container svelte-6xvqq1"><div class="sae-table-controls"><!></div> <div class="sae-table svelte-6xvqq1"><div class="sae-table-cell sae-table-header sae-table-header-align-right svelte-6xvqq1"><span class="svelte-6xvqq1">ID</span> <!></div> <div class="sae-table-cell sae-table-header sae-table-header-align-right svelte-6xvqq1"><span class="svelte-6xvqq1">Act. Rate</span> <!></div> <div class="sae-table-cell sae-table-header sae-table-header-align-right svelte-6xvqq1"><span class="svelte-6xvqq1">Act. Distribution</span> <!></div> <div class="sae-table-cell sae-table-header sae-table-header-align-right svelte-6xvqq1"><span class="svelte-6xvqq1">Top Class Probabilities</span> <!></div> <div class="sae-table-cell sae-table-header svelte-6xvqq1"><span class="svelte-6xvqq1">Example</span> <!></div> <!></div> <div class="sae-table-pagination"><!></div></div>');
function bu(e, t) {
  pe(t, !0);
  const n = /* @__PURE__ */ x(() => le.base * 0.5), r = /* @__PURE__ */ x(() => le.base * 0.25), a = /* @__PURE__ */ x(() => le.base * 3), l = /* @__PURE__ */ x(() => i(a) * 3), s = 80;
  function o(A) {
    return A.cm.pred_label_pcts.map((S, y) => ({ pct: S, label: y })).sort((S, y) => zi(S.pct, y.pct)).slice(0, 3).map(({ label: S }) => S);
  }
  const u = !0;
  var f = hu(), v = b(f), c = b(v);
  Qf(c, {});
  var d = m(v, 2);
  let g;
  var h = b(d), _ = m(b(h), 2);
  Qe(_, {
    position: "right",
    trigger: (y) => {
      Ze(y, {});
    },
    content: (y) => {
      var R = ou();
      D(y, R);
    },
    $$slots: { trigger: !0, content: !0 }
  });
  var p = m(h, 2), E = m(b(p), 2);
  Qe(E, {
    position: "right",
    trigger: (y) => {
      Ze(y, {});
    },
    content: (y) => {
      var R = fu();
      D(y, R);
    },
    $$slots: { trigger: !0, content: !0 }
  });
  var k = m(p, 2), T = m(b(k), 2);
  Qe(T, {
    position: "right",
    trigger: (y) => {
      Ze(y, {});
    },
    content: (y) => {
      var R = uu();
      D(y, R);
    },
    $$slots: { trigger: !0, content: !0 }
  });
  var w = m(k, 2), q = m(b(w), 2);
  Qe(q, {
    position: "right",
    trigger: (y) => {
      Ze(y, {});
    },
    content: (y) => {
      var R = cu(), P = m(b(R), 2);
      const F = /* @__PURE__ */ x(() => St([0, 1], Zi)), G = /* @__PURE__ */ x(() => le.sm * 16), O = /* @__PURE__ */ x(() => le.sm * 2), W = /* @__PURE__ */ x(() => le.sm * 2);
      bn(P, {
        get color() {
          return i(F);
        },
        get width() {
          return i(G);
        },
        height: 56,
        orientation: "horizontal",
        title: "Mean predicted probability",
        marginTop: 18,
        marginBottom: 24,
        get marginLeft() {
          return i(O);
        },
        get marginRight() {
          return i(W);
        },
        get titleFontSize() {
          return le.sm;
        },
        get tickLabelFontSize() {
          return le.xs;
        }
      }), D(y, R);
    },
    $$slots: { trigger: !0, content: !0 }
  });
  var L = m(w, 2), C = m(b(L), 2);
  Qe(C, {
    position: "right",
    trigger: (y) => {
      Ze(y, {});
    },
    content: (y) => {
      var R = du(), P = m(b(R), 2);
      const F = /* @__PURE__ */ x(() => St([0, 1], (ee) => Hr(1 - ee))), G = /* @__PURE__ */ x(() => le.sm * 16), O = /* @__PURE__ */ x(() => le.sm * 2), W = /* @__PURE__ */ x(() => le.sm * 2);
      bn(P, {
        get color() {
          return i(F);
        },
        get width() {
          return i(G);
        },
        height: 56,
        orientation: "horizontal",
        title: "Activation value",
        marginTop: 18,
        marginBottom: 24,
        get marginLeft() {
          return i(O);
        },
        get marginRight() {
          return i(W);
        },
        get titleFontSize() {
          return le.sm;
        },
        get tickLabelFontSize() {
          return le.xs;
        },
        tickValues: [0, 1],
        tickFormat: (ee) => ee === 0 ? "Min" : ee === 1 ? "Max" : ""
      }), D(y, R);
    },
    $$slots: { trigger: !0, content: !0 }
  });
  var I = m(L, 2);
  Ae(I, 17, () => Ir.value, Te, (A, S, y) => {
    var R = gu();
    const P = /* @__PURE__ */ x(() => y !== Ir.value.length - 1);
    var F = Se(R);
    let G;
    var O = b(F), W = b(O);
    W.__click = [vu, t, S];
    var ee = b(W), H = m(F, 2);
    let j;
    var z = b(H), Y = b(z), K = m(H, 2);
    let V;
    var ie = b(K);
    ua(ie, {
      get data() {
        return i(S).sequence_acts_histogram;
      },
      get width() {
        return i(l);
      },
      get height() {
        return i(a);
      },
      tooltipEnabled: u,
      get tooltipData() {
        return Ji;
      }
    });
    var ae = m(K, 2);
    let Z;
    var ge = b(ae);
    const me = /* @__PURE__ */ x(() => o(i(S))), ye = /* @__PURE__ */ x(() => i(l) + s);
    tl(ge, {
      get marginalEffects() {
        return i(S).marginal_effects;
      },
      get classes() {
        return i(me);
      },
      get width() {
        return i(ye);
      },
      get height() {
        return i(a);
      },
      maxColorDomain: 1,
      showColorLegend: !1,
      marginTop: 0,
      marginRight: 0,
      marginBottom: 0,
      marginLeft: s,
      showXAxis: !1,
      showYAxis: !0,
      tooltipEnabled: u
    });
    var Me = m(ae, 2);
    let Ye;
    var U = b(Me);
    const Q = /* @__PURE__ */ x(() => St([0, i(S).max_act], (B) => Hr(1 - B)));
    ca(U, {
      get colorScale() {
        return i(Q);
      },
      get sequence() {
        return i(S).sequence_intervals[0].sequences[0];
      },
      wrap: !1,
      tooltipEnabled: u
    }), te(
      (B, fe, be, xe, Ee, ue) => {
        G = ze(F, 1, "sae-table-cell sae-table-number-value svelte-6xvqq1", null, G, B), de(ee, i(S).feature_id), j = ze(H, 1, "sae-table-cell sae-table-number-value svelte-6xvqq1", null, j, fe), de(Y, be), V = ze(K, 1, "sae-table-cell svelte-6xvqq1", null, V, xe), Z = ze(ae, 1, "sae-table-cell svelte-6xvqq1", null, Z, Ee), Ye = ze(Me, 1, "sae-table-cell sae-table-example-sequence svelte-6xvqq1", null, Ye, ue);
      },
      [
        () => ({ "sae-table-border": i(P) }),
        () => ({ "sae-table-border": i(P) }),
        () => Jn(i(S).sequence_act_rate),
        () => ({ "sae-table-border": i(P) }),
        () => ({ "sae-table-border": i(P) }),
        () => ({ "sae-table-border": i(P) })
      ]
    ), D(A, R);
  });
  var X = m(d, 2), $ = b(X);
  su($, {}), te(() => g = Ce(d, "", g, {
    "--cell-padding-x": `${i(n) ?? ""}px`,
    "--cell-padding-y": `${i(r) ?? ""}px`
  })), D(e, f), we();
}
Ct(["click"]);
var _u = /* @__PURE__ */ ne("<option> </option>"), mu = /* @__PURE__ */ ne("<div><!></div> <div> </div> <div> </div> <div><!></div>", 1), xu = /* @__PURE__ */ ne('<div class="sae-sequence-container svelte-i85elo"><div class="sae-sequences-header svelte-i85elo"><div class="sae-sequences-controls svelte-i85elo"><span>Example Activations</span> <label class="svelte-i85elo"><span>Range:</span> <select class="svelte-i85elo"><option>Max activations</option><!></select></label> <label class="svelte-i85elo"><input type="checkbox"/> <span>Wrap text</span></label></div> <div class="sae-sequences-color-legend"><!></div></div> <div class="sae-sequences-table svelte-i85elo"><div class="sae-sequences-table-cell sae-sequences-table-header svelte-i85elo"></div> <div class="sae-sequences-table-cell sae-sequences-table-header svelte-i85elo">Pred.</div> <div class="sae-sequences-table-cell sae-sequences-table-header svelte-i85elo">True</div> <div class="sae-sequences-table-cell sae-sequences-table-header svelte-i85elo">Tokens</div> <!></div></div>');
function pu(e, t) {
  pe(t, !0);
  let n = /* @__PURE__ */ re(0), r = /* @__PURE__ */ x(() => ft.value.sequence_intervals[i(n)]), a = /* @__PURE__ */ re(!1);
  function l(w) {
    const q = w.sequence_index === -1 ? [] : [
      {
        key: "Instance index",
        value: `${w.sequence_index}`
      }
    ], L = Object.entries(w.extras).map(([C, I]) => ({ key: C, value: I }));
    return [...q, ...L];
  }
  var s = xu(), o = b(s), u = b(o), f = b(u);
  Ce(f, "", {}, { "font-weight": "var(--font-medium)" });
  var v = m(f, 2), c = m(b(v), 2), d = b(c);
  d.value = d.__value = 0;
  var g = m(d);
  Ae(g, 17, () => ta(ft.value.sequence_intervals.length - 1, 0, -1), Te, (w, q) => {
    var L = _u(), C = {}, I = b(L);
    te(() => {
      C !== (C = i(q)) && (L.value = (L.__value = i(q)) ?? ""), de(I, `Interval ${i(q) ?? ""}`);
    }), D(w, L);
  });
  var h = m(v, 2), _ = b(h), p = m(u, 2), E = b(p);
  bn(E, {
    width: 256,
    height: 56,
    get color() {
      return t.tokenColor;
    },
    orientation: "horizontal",
    title: "Activation value",
    marginTop: 18,
    marginBottom: 24,
    get titleFontSize() {
      return le.sm;
    },
    get tickLabelFontSize() {
      return le.xs;
    },
    tickFormat: (w) => w === 0 ? "> 0" : Et(w)
  });
  var k = m(o, 2), T = m(b(k), 8);
  Ae(T, 17, () => i(r).sequences, Te, (w, q, L) => {
    var C = mu();
    const I = /* @__PURE__ */ x(() => L !== i(r).sequences.length - 1), X = /* @__PURE__ */ x(() => l(i(q)));
    var $ = Se(C);
    let A;
    var S = b($);
    {
      var y = (z) => {
        Qe(z, {
          position: "left",
          trigger: (V) => {
            Ze(V, {});
          },
          content: (V) => {
            Mn(V, {
              get data() {
                return i(X);
              }
            });
          },
          $$slots: { trigger: !0, content: !0 }
        });
      };
      se(S, (z) => {
        i(X).length > 0 && z(y);
      });
    }
    var R = m($, 2);
    let P;
    var F = b(R), G = m(R, 2);
    let O;
    var W = b(G), ee = m(G, 2);
    let H;
    var j = b(ee);
    ca(j, {
      get colorScale() {
        return t.tokenColor;
      },
      get sequence() {
        return i(q);
      },
      get wrap() {
        return i(a);
      },
      hidePadding: !1
    }), te(
      (z, Y, K, V) => {
        A = ze($, 1, "sae-sequences-table-cell svelte-i85elo", null, A, z), P = ze(R, 1, "sae-sequences-table-cell svelte-i85elo", null, P, Y), de(F, qe.value.labels[i(q).pred_label]), O = ze(G, 1, "sae-sequences-table-cell svelte-i85elo", null, O, K), de(W, qe.value.labels[i(q).label]), H = ze(ee, 1, "sae-sequences-table-cell sae-sequences-table-tokens svelte-i85elo", null, H, V);
      },
      [
        () => ({
          "sae-sequences-table-border": i(I)
        }),
        () => ({
          "sae-sequences-table-border": i(I)
        }),
        () => ({
          "sae-sequences-table-border": i(I)
        }),
        () => ({
          "sae-sequences-table-border": i(I)
        })
      ]
    ), D(w, C);
  }), ks(c, () => i(n), (w) => J(n, w)), cn(_, () => i(a), (w) => J(a, w)), D(e, s), we();
}
function wu(e, t) {
  e.key === "Enter" && t();
}
var yu = /* @__PURE__ */ ne(`<div class="sae-info svelte-1b2v2yq">Enter some text and check to see if it causes the feature to
            activate. Special tokens are automatically added.</div>`), ku = /* @__PURE__ */ ne('<div class="sae-sequences-table svelte-1b2v2yq"><div class="sae-sequences-table-cell sae-sequences-table-header svelte-1b2v2yq">Pred.</div> <div class="sae-sequences-table-cell sae-sequences-table-header svelte-1b2v2yq">Prob.</div> <div class="sae-sequences-table-cell sae-sequences-table-header svelte-1b2v2yq">Tokens</div> <div> </div> <div> </div> <div><!></div></div>'), Mu = /* @__PURE__ */ ne('<div class="sae-feature-testing-container svelte-1b2v2yq"><div class="sae-controls svelte-1b2v2yq"><div class="sae-title svelte-1b2v2yq"><span class="svelte-1b2v2yq">Test Feature</span> <!></div> <label class="svelte-1b2v2yq"><input type="checkbox"/> <span>Hide padding</span></label> <label class="svelte-1b2v2yq"><input type="checkbox"/> <span>Wrap text</span></label></div> <div class="sae-input-row svelte-1b2v2yq"><input type="text" class="svelte-1b2v2yq"/> <button>Test</button></div> <!></div>');
function Tu(e, t) {
  pe(t, !0);
  let n = /* @__PURE__ */ re(!1), r = /* @__PURE__ */ re(!0), a = /* @__PURE__ */ x(() => t.featureId === Fn.value.feature_index ? Fn.value.sequence : "");
  function l() {
    Fn.value = {
      feature_index: t.featureId,
      sequence: i(a)
    };
  }
  var s = Mu(), o = b(s), u = b(o), f = m(b(u), 2);
  Qe(f, {
    position: "right",
    trigger: (q) => {
      Ze(q, {});
    },
    content: (q) => {
      var L = yu();
      D(q, L);
    },
    $$slots: { trigger: !0, content: !0 }
  });
  var v = m(u, 2), c = b(v), d = m(v, 2), g = b(d), h = m(o, 2), _ = b(h);
  _.__keydown = [wu, l];
  var p = m(_, 2);
  p.__click = l;
  var E = m(h, 2);
  {
    var k = (T) => {
      var w = ku(), q = m(b(w), 6);
      ze(q, 1, "sae-sequences-table-cell svelte-1b2v2yq", null, {}, { "sae-sequences-table-border": !0 });
      var L = b(q), C = m(q, 2);
      ze(C, 1, "sae-sequences-table-cell svelte-1b2v2yq", null, {}, { "sae-sequences-table-border": !0 });
      var I = b(C), X = m(C, 2);
      ze(X, 1, "sae-sequences-table-cell sae-sequences-table-tokens svelte-1b2v2yq", null, {}, { "sae-sequences-table-border": !0 });
      var $ = b(X);
      ca($, {
        get colorScale() {
          return t.tokenColor;
        },
        get sequence() {
          return Dt.value;
        },
        get wrap() {
          return i(n);
        },
        get hidePadding() {
          return i(r);
        }
      }), te(
        (A) => {
          de(L, qe.value.labels[Dt.value.pred_label]), de(I, A);
        },
        [
          () => hn(Dt.value.pred_probs[Dt.value.pred_label])
        ]
      ), D(T, w);
    };
    se(E, (T) => {
      Dt.value.feature_index === t.featureId && T(k);
    });
  }
  cn(c, () => i(r), (T) => J(r, T)), cn(g, () => i(n), (T) => J(n, T)), cr(_, () => i(a), (T) => J(a, T)), D(e, s), we();
}
Ct(["keydown", "click"]);
var Au = /* @__PURE__ */ ne('<div class="sae-info svelte-h6hjia"></div>'), qu = /* @__PURE__ */ ne('<div class="sae-info svelte-h6hjia"></div>'), Su = /* @__PURE__ */ ne('<div class="sae-inference-container svelte-h6hjia"><!></div>'), Eu = /* @__PURE__ */ ne('<div class="sae-container svelte-h6hjia"><div class="sae-controls svelte-h6hjia"><div class="sae-feature-input svelte-h6hjia"><label class="svelte-h6hjia"><span>Feature ID:</span> <input type="number" class="svelte-h6hjia"/></label> <button class="svelte-h6hjia">Go</button></div> <div><span>Activation Rate:</span> <span> </span></div></div> <div><div class="sae-effects-container svelte-h6hjia"><div class="sae-effects-controls svelte-h6hjia"><div class="sae-title svelte-h6hjia"><span class="svelte-h6hjia">Predicted Probabilities</span> <!></div> <label class="svelte-h6hjia"><input type="checkbox"/> <span></span></label></div> <div class="sae-effects-vis svelte-h6hjia"><!></div></div> <div class="sae-cm-container svelte-h6hjia"><div class="sae-cm-controls svelte-h6hjia"><div class="sae-title svelte-h6hjia"><span class="svelte-h6hjia">Confusion Matrix</span> <!></div> <label class="svelte-h6hjia"><input type="checkbox"/> <span></span></label></div> <div class="sae-cm-vis svelte-h6hjia"><!></div></div> <div class="sae-sequences-container svelte-h6hjia"><!></div> <!></div></div>');
function Lu(e, t) {
  pe(t, !0);
  const n = /* @__PURE__ */ x(() => Math.log10(Mt.value.n_total_features) + 1), r = /* @__PURE__ */ x(() => St().domain([0, ft.value.max_act]).interpolator((B) => Hr(1 - B)));
  let a = /* @__PURE__ */ x(() => fn.value);
  function l() {
    fn.value = i(a);
  }
  let s = /* @__PURE__ */ re(0), o = /* @__PURE__ */ re(0), u = /* @__PURE__ */ x(() => fa(i(o), i(s), 1.6));
  const f = 8, v = 88, c = 80, d = 80;
  let g = /* @__PURE__ */ re(0), h = /* @__PURE__ */ re(0);
  const _ = /* @__PURE__ */ x(() => Qi(i(g), i(h), 1, f, v, c, d));
  let p = /* @__PURE__ */ re(!1), E = /* @__PURE__ */ re(!1);
  var k = Eu(), T = b(k), w = b(T), q = b(w), L = b(q);
  Ce(L, "", {}, { "font-weight": "var(--font-medium)" });
  var C = m(L, 2);
  let I;
  var X = m(q, 2);
  X.__click = l;
  var $ = m(w, 2), A = b($);
  Ce(A, "", {}, { "font-weight": "var(--font-medium)" });
  var S = m(A, 2), y = b(S), R = m(T, 2), P = b(R), F = b(P), G = b(F), O = m(b(G), 2);
  Qe(O, {
    position: "right",
    trigger: (be) => {
      Ze(be, {});
    },
    content: (be) => {
      var xe = Au();
      xe.textContent = `Each cell in the heatmap shows the model's mean predicted
                probability for the given class on instances that cause the
                feature to activate in the given range. Checking "Compare to base probabilities"
                shows the difference relative to the model's mean predicted
                probabilities for the entire dataset.`, D(be, xe);
    },
    $$slots: { trigger: !0, content: !0 }
  });
  var W = m(G, 2), ee = b(W), H = m(ee, 2);
  H.textContent = "Compare to base probabilities";
  var j = m(F, 2), z = b(j);
  tl(z, {
    get marginalEffects() {
      return ft.value.marginal_effects;
    },
    get distribution() {
      return ft.value.sequence_acts_histogram;
    },
    get classes() {
      return qe.value.label_indices;
    },
    get compareToBaseProbs() {
      return i(p);
    },
    marginTop: 32,
    marginRight: 88,
    marginLeft: 80,
    marginBottom: 40,
    get width() {
      return i(u).width;
    },
    get height() {
      return i(u).height;
    },
    xAxisLabel: "Activation value",
    yAxisLabel: "Predicted label",
    showColorLegend: !0
  });
  var Y = m(P, 2), K = b(Y), V = b(K), ie = m(b(V), 2);
  Qe(ie, {
    position: "right",
    trigger: (be) => {
      Ze(be, {});
    },
    content: (be) => {
      var xe = qu();
      xe.textContent = `This confusion matrix is calculated from instances that cause
                this feature to activate. Checking "Compare to whole dataset" shows
                the difference relative to the confusion matrix for all
                instances.`, D(be, xe);
    },
    $$slots: { trigger: !0, content: !0 }
  });
  var ae = m(V, 2), Z = b(ae), ge = m(Z, 2);
  ge.textContent = "Compare to whole dataset";
  var me = m(K, 2), ye = b(me);
  el(ye, {
    get cm() {
      return ft.value.cm;
    },
    get other() {
      return Ot.value.cm;
    },
    get showDifference() {
      return i(E);
    },
    legend: "vertical",
    get width() {
      return i(_).width;
    },
    get height() {
      return i(_).height;
    },
    marginTop: f,
    marginRight: v,
    marginBottom: c,
    marginLeft: d
  });
  var Me = m(Y, 2), Ye = b(Me);
  pu(Ye, {
    get tokenColor() {
      return i(r);
    }
  });
  var U = m(Me, 2);
  {
    var Q = (B) => {
      var fe = Su(), be = b(fe);
      Tu(be, {
        get tokenColor() {
          return i(r);
        },
        get featureId() {
          return fn.value;
        }
      }), D(B, fe);
    };
    se(U, (B) => {
      Dr.value && B(Q);
    });
  }
  te(
    (B, fe) => {
      I = Ce(C, "", I, { width: `${i(n) + 1}em` }), de(y, `${B ?? ""} (${fe ?? ""} instances)`), ze(
        R,
        1,
        ps([
          "sae-main",
          Dr.value ? "sae-grid-inference" : "sae-grid-no-inference"
        ]),
        "svelte-h6hjia"
      );
    },
    [
      () => Jn(ft.value.sequence_act_rate),
      () => Ht(ft.value.cm.n_sequences)
    ]
  ), cr(C, () => i(a), (B) => J(a, B)), cn(ee, () => i(p), (B) => J(p, B)), Ue(j, "clientWidth", (B) => J(o, B)), Ue(j, "clientHeight", (B) => J(s, B)), cn(Z, () => i(E), (B) => J(E, B)), Ue(me, "clientWidth", (B) => J(g, B)), Ue(me, "clientHeight", (B) => J(h, B)), D(e, k), we();
}
Ct(["click"]);
var Nu = /* @__PURE__ */ ne('<div class="sae-widget-container svelte-zqdrxr"><div class="sae-tabs-container svelte-zqdrxr"><!></div> <div class="sae-tab-content svelte-zqdrxr"><!></div></div>');
function Fu(e, t) {
  pe(t, !0);
  let n = /* @__PURE__ */ re("overview");
  function r(g) {
    J(n, g, !0);
  }
  function a(g) {
    fn.value = g, J(n, "detail");
  }
  var l = Nu();
  let s;
  var o = b(l), u = b(o);
  Cs(u, {
    get selectedTab() {
      return i(n);
    },
    changeTab: r
  });
  var f = m(o, 2), v = b(f);
  {
    var c = (g) => {
      zf(g, {});
    }, d = (g, h) => {
      {
        var _ = (E) => {
          bu(E, { onClickFeature: a });
        }, p = (E) => {
          Lu(E, {});
        };
        se(
          g,
          (E) => {
            i(n) === "table" ? E(_) : E(p, !1);
          },
          h
        );
      }
    };
    se(v, (g) => {
      i(n) === "overview" ? g(c) : g(d, !1);
    });
  }
  te(() => s = Ce(l, "", s, {
    height: `${Di.value ?? ""}px`,
    "--text-xs": `${le.xs ?? ""}px`,
    "--text-sm": `${le.sm ?? ""}px`,
    "--text-base": `${le.base ?? ""}px`,
    "--text-lg": `${le.lg ?? ""}px`,
    "--text-xl": `${le.xl ?? ""}px`
  })), D(e, l), we();
}
const Cu = ({ model: e, el: t }) => {
  Rs(e), zs(t);
  let n = ds(Fu, { target: t });
  return () => gs(n);
}, Ru = { render: Cu };
export {
  Ru as default
};
